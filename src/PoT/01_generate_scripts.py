# %%
import os

# Limit library threading based on allocated SLURM CPUs
# SLURM-specific in the original runs; falls back to 1 thread outside SLURM
os.environ["OMP_NUM_THREADS"] = os.environ.get("SLURM_CPUS_PER_TASK", "1")
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import sys
import json
import yaml
import re
import time
import datetime
import torch
import argparse
import importlib
import contextlib
from dataclasses import asdict
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.tokenization_utils_tokenizers import TokenizersBackend  # DeepSeek tokenizer fix, see main()
from langchain_core.prompts import PromptTemplate
from pynvml import nvmlInit, nvmlShutdown, nvmlDeviceGetHandleByIndex

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))  # src/ -- for energy.inference_energy

from energy.inference_energy import (
    measure_idle_power,
    PowerSampler,
    reset_gpu_state,
    EnergyRecord,
    resolve_nvml_index,
)

# TraceLLM/ root -- BASE_DIR is TraceLLM/src/PoT/, two levels down from it.
TRACE_LLM_ROOT = os.path.join(BASE_DIR, "..", "..")

CONFIG_PATH = os.path.join(TRACE_LLM_ROOT, "configPoT.yaml")

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def import_template(module_name, template_name):
    module = importlib.import_module(module_name)
    return getattr(module, template_name)


def extract_code_block(text):
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def count_tokens(prompt, tokenizer):
    return len(tokenizer.encode(prompt, add_special_tokens=True))

def shot_name(n):
    names = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
    }
    return names.get(n, str(n))

_GRANULARITY_NOTE_MAP = {
    "Task_1": "task_level_note_single_trace_one_key",
    "Task_2": "task_level_note_single_trace_two_keys",
    "Task_3": "task_level_note_single_trace_no_key",
    "Task_4": "task_level_note_two_traces",
}

def select_note_name(task_id):
    prefix = "_".join(task_id.split("_")[:2])  # 'Task_1', 'Task_2', etc.
    note = _GRANULARITY_NOTE_MAP.get(prefix)
    if note is None:
        raise ValueError(f"Unrecognized task_id prefix '{prefix}' in task_id='{task_id}'")
    return note


def build_example_block(task_id, bench_path, input_name, example_count):
    task_pt_path = os.path.join(bench_path, "Tasks", f"{task_id}.pt")
    if not os.path.exists(task_pt_path):
        print(f"Warning: no example .pt found for {task_id}, skipping example block.")
        return ""

    if example_count == 0:
        return ""

    same_id_tasks = torch.load(task_pt_path, weights_only=False)
    instances = list(same_id_tasks.values())

    if example_count > len(instances):
        raise ValueError(
            f"script_example_count={example_count} exceeds available instances "
            f"({len(instances)}) for {task_id}."
        )

    example_template = import_template("templates.TaskLevelCodePromptNote", "code_example_template")
    example_prompt = PromptTemplate.from_template(template=example_template)

    example_block = ""
    for i in range(example_count):
        instance = instances[i]
        example_block += example_prompt.format(
            example_id=str(i + 1),
            question=instance["question"],
            input_traces=instance[input_name],
            answer=instance["answer"]
        )

    return example_block


def build_prompt(task_id, task_info, trace_format_desc, example_block):
    note_name = select_note_name(task_id)
    note = import_template("templates.TaskLevelCodePromptNote", note_name)
    common_requirements = import_template("templates.TaskLevelCodePromptNote", "common_task_level_requirements")

    prompt = f"""
## Task
Task Description: {task_info.get("task_description", "")}
Task Definition: {task_info.get("task_definition", "")}
Question Template: {task_info.get("question_template", "")}

## Trace Format
{trace_format_desc}

{example_block}
{note}
{common_requirements}
"""
    return prompt



def build_messages(system_prompt, user_instruction, llm_name):
    if 'deepseek' in llm_name.lower():
        # DeepSeek-R1-Distill's model card recommends against a system prompt;
        # fold it into the user turn instead. Same content, different packaging.
        return [{"role": "user", "content": system_prompt + '\n\n' + user_instruction}]
    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_instruction}]


def ask_llm(tokenizer, model, prompt, system_prompt, configs):
    token_count = count_tokens(prompt + system_prompt, tokenizer)

    messages = build_messages(system_prompt, prompt, configs['llm_name'])

    # enable_thinking is Qwen-specific; detect from the model name
    chat_template_kwargs = {"tokenize": False, "add_generation_prompt": True}
    if 'qwen' in configs['llm_name'].lower():
        chat_template_kwargs['enable_thinking'] = False

    text = tokenizer.apply_chat_template(messages, **chat_template_kwargs)

    # truncate (don't skip/crash) if the prompt exceeds the model's context window;
    # left-side truncation keeps the trailing question/instruction intact and drops
    # the earliest few-shot examples first.
    max_new_tokens = configs["max_new_tokens"]
    model_max_length = tokenizer.model_max_length
    if not model_max_length or model_max_length > 10**6:
        model_max_length = 129024  # fallback ceiling also used in app_inference_with_measure.py
    max_input_len = max(1, model_max_length - max_new_tokens)
    if token_count > max_input_len:
        print(f"[WARN] prompt has {token_count} tokens, exceeds max input length {max_input_len} -- truncating")

    model_input = tokenizer(
        [text],
        return_tensors="pt",
        truncation=True,
        max_length=max_input_len
    ).to(configs["device"])

    attention_mask = torch.ones(
        model_input.input_ids.shape,
        dtype=torch.long,
        device=configs["device"]
    )

    generated_ids = model.generate(
        model_input.input_ids,
        max_new_tokens=configs["max_new_tokens"],
        attention_mask=attention_mask,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=configs['do_sample']
    )

    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(model_input.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response, token_count


def ask_llm_measured(tokenizer, model, prompt, system_prompt, configs, handle, idle_power_w, task_id):
    # measured generate() for script generation; PowerSampler brackets generate(). Danish et al. (E-Energy 2026)
    token_count = count_tokens(prompt + system_prompt, tokenizer)

    messages = build_messages(system_prompt, prompt, configs['llm_name'])

    # enable_thinking is Qwen-specific; detect from the model name
    chat_template_kwargs = {"tokenize": False, "add_generation_prompt": True}
    if 'qwen' in configs['llm_name'].lower():
        chat_template_kwargs['enable_thinking'] = False

    text = tokenizer.apply_chat_template(messages, **chat_template_kwargs)

    # truncate (don't skip/crash) if the prompt exceeds the model's context window;
    # left-side truncation keeps the trailing question/instruction intact and drops
    # the earliest few-shot examples first.
    max_new_tokens = configs["max_new_tokens"]
    model_max_length = tokenizer.model_max_length
    if not model_max_length or model_max_length > 10**6:
        model_max_length = 129024  # fallback ceiling also used in app_inference_with_measure.py
    max_input_len = max(1, model_max_length - max_new_tokens)
    if token_count > max_input_len:
        print(f"[WARN] prompt has {token_count} tokens, exceeds max input length {max_input_len} -- truncating")

    model_input = tokenizer(
        [text],
        return_tensors="pt",
        truncation=True,
        max_length=max_input_len
    ).to(configs["device"])

    attention_mask = torch.ones(
        model_input.input_ids.shape,
        dtype=torch.long,
        device=configs["device"]
    )

    tokens_input = model_input.input_ids.shape[-1]
    sampler = PowerSampler(handle)

    torch.cuda.synchronize()
    sampler.start()
    t_start = time.perf_counter()

    with torch.no_grad():
        output_ids = model.generate(
            model_input.input_ids,
            max_new_tokens=configs["max_new_tokens"],
            attention_mask=attention_mask,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=configs['do_sample']
        )

    torch.cuda.synchronize()
    t_end = time.perf_counter()
    sampler.stop()

    tokens_output = max(output_ids.shape[-1] - tokens_input, 1)
    time_total_s      = t_end - t_start
    energy_total_j    = sampler.compute_energy_j()
    energy_marginal_j = max(0.0, energy_total_j - idle_power_w * time_total_s)

    record = EnergyRecord(
        problem_id=task_id,
        repeat_idx=0,
        tokens_input=tokens_input,
        tokens_output=tokens_output,
        time_total_s=round(time_total_s, 6),
        latency_per_token_s=round(time_total_s / tokens_output, 6),
        energy_total_j=round(energy_total_j, 6),
        energy_marginal_j=round(energy_marginal_j, 6),
        avg_power_w=round(energy_total_j / time_total_s, 4) if time_total_s > 0 else 0.0,
        idle_power_w=round(idle_power_w, 4),
        energy_per_token_j=round(energy_marginal_j / tokens_output, 6),
    )

    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(model_input.input_ids, output_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return record, response, token_count


def save_script(task_id, task_info, code, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    header = f'''"""
Auto-generated task-level solver.

Task ID: {task_id}
Task Type: {task_info.get("task_type", "")}
Task Description: {task_info.get("task_description", "")}
Question Template: {task_info.get("question_template", "")}
"""
'''

    path = os.path.join(output_dir, f"{task_id}.py")

    with open(path, "w") as f:
        f.write(header)
        f.write("\n")
        f.write(code)
        f.write("\n")

    return path


def main():
    print("Starting script generation...")
    start_time = time.time()

    configs = load_yaml(CONFIG_PATH)

    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, required=True)
    args = parser.parse_args()

    example_count = args.shots
    label = f"{shot_name(example_count)}shot"

    MEASURE_ENERGY = configs.get('measure_energy', False)
    COOLDOWN_BETWEEN_TASKS_S = configs.get('cooldown_between_tasks_s', 2.0)
    print("Energy measurement enabled:", MEASURE_ENERGY)

    shared_output_dir = os.path.join(TRACE_LLM_ROOT, "output", "generated_scripts")

    generated_scripts_dir = f"generated_scripts_{configs['llm_name']}_{label}"
    generation_log_path = f"generation_log_{configs['llm_name']}_{label}.json"
    generation_energy_path = f"energy_generation_{configs['llm_name']}_{label}_{int(start_time)}.jsonl"

    task_info_path = os.path.join(BASE_DIR, configs["task_info_path"])
    trace_format_path = os.path.join(BASE_DIR, configs["trace_format_desc_path"])
    bench_path = os.path.join(BASE_DIR, configs["trace_bench_dataset"])

    generated_scripts_dir = os.path.join(shared_output_dir, generated_scripts_dir)
    generation_log_path = os.path.join(shared_output_dir, generation_log_path)
    generation_energy_path = os.path.join(shared_output_dir, generation_energy_path)

    task_info_all = load_json(task_info_path)
    trace_format_all = load_json(trace_format_path)

    # phantom-task filter: TaskInfo.json has 39 entries but the benchmark defines only 38
    test_instances_path = os.path.join(BASE_DIR, configs["test_instances_path"])
    test_instances = torch.load(test_instances_path, map_location='cpu')
    real_task_ids = set(inst["task_id"] for inst in test_instances.values())
    skipped_task_ids = [tid for tid in task_info_all if tid not in real_task_ids]
    if skipped_task_ids:
        print(f"Skipping TaskInfo entries with no real test instances: {skipped_task_ids}")
    task_info_all = {tid: v for tid, v in task_info_all.items() if tid in real_task_ids}
    trace_format_desc = trace_format_all[configs["trace_format_key"]]

    # input_name mirrors the key construction in app_with_cot.py:
    # 'input_trace_{desc_method}', e.g. 'input_trace_raw_spans_desc'
    input_name = f"input_trace_{configs['desc_method']}"

    system_prompt = import_template(
        "templates.InstructionTemplate",
        "system_prompt_with_code"
    )

    print(f"Loading model: {configs['llm_name']}")

    model = AutoModelForCausalLM.from_pretrained(
        configs["llm_path"],
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    ).to(configs["device"])

    # tokenizer = AutoTokenizer.from_pretrained(
    #     configs["llm_path"],
    #     use_fast=False
    # )
    # AutoTokenizer mis-decodes DeepSeek-R1-Distill (raw Ġ/Ċ markers); same fix as direct prompting.
    if 'deepseek' in configs["llm_name"].lower():
        tokenizer = TokenizersBackend.from_pretrained(configs["llm_path"])
    else:
        tokenizer = AutoTokenizer.from_pretrained(
            configs["llm_path"],
            use_fast=False
        )

    model.eval()
    tokenizer.truncation_side = 'left'

    print("Model loaded.")

    # nvml init and idle baseline
    if MEASURE_ENERGY:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(resolve_nvml_index())
        idle_power_w = measure_idle_power(handle)

    generation_log = {}
    first_task = True

    os.makedirs(os.path.dirname(generation_energy_path), exist_ok=True)
    energy_cm = open(generation_energy_path, 'w') if MEASURE_ENERGY else contextlib.nullcontext()
    with energy_cm as f_energy:
        for task_id, task_info in tqdm(task_info_all.items(), desc="Generate task scripts"):
            # Build few-shot example block from per-task .pt file.
            example_block = build_example_block(task_id, bench_path, input_name, example_count)

            prompt = build_prompt(task_id, task_info, trace_format_desc, example_block)

            if first_task:
                print("SYSTEM PROMPT:")
                print(system_prompt)
                print("=" * 60)
                print(f"TASK: {task_id}")
                print("=" * 60)
                print(prompt)
                # break

            if MEASURE_ENERGY:
                energy_record, response, token_count = ask_llm_measured(
                    tokenizer, model, prompt, system_prompt, configs, handle, idle_power_w, task_id
                )
                if energy_record is not None:
                    f_energy.write(json.dumps(asdict(energy_record)) + '\n')
                    f_energy.flush()
            else:
                response, token_count = ask_llm(
                    tokenizer=tokenizer,
                    model=model,
                    prompt=prompt,
                    system_prompt=system_prompt,
                    configs=configs
                )

            code = extract_code_block(response)
            success = "def solution" in code

            script_path = save_script(task_id, task_info, code, generated_scripts_dir)

            generation_log[task_id] = {
                "task_type": task_info.get("task_type", ""),
                "question_template": task_info.get("question_template", ""),
                "token_count": token_count,
                "script_path": script_path,
                "success": success,
                "raw_response": response,
                "prompt": prompt if first_task else None
            }
            first_task = False

            if MEASURE_ENERGY:
                reset_gpu_state(model)
                print(f"  reset done", flush=True)
                time.sleep(COOLDOWN_BETWEEN_TASKS_S)

    if MEASURE_ENERGY:
        nvmlShutdown()

    os.makedirs(os.path.dirname(generation_log_path), exist_ok=True)

    with open(generation_log_path, "w") as f:
        json.dump(generation_log, f, indent=4)

    total_time = str(datetime.timedelta(seconds=int(time.time() - start_time)))

    print("-" * 20)
    print(f"Generation time: {total_time}")
    print(f"Generated scripts directory: {generated_scripts_dir}")
    print(f"Generation log: {generation_log_path}")
    if MEASURE_ENERGY:
        print(f"Generation energy log: {generation_energy_path}")
    print("Done.")


if __name__ == "__main__":
    main()
