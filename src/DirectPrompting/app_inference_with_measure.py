# %%
import os

# Limit library threading based on allocated SLURM CPUs
# SLURM-specific in the original runs; falls back to 1 thread outside SLURM
os.environ["OMP_NUM_THREADS"] = os.environ.get("SLURM_CPUS_PER_TASK", "1")
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import gc
import yaml
import json
import time
import datetime
import sys
import torch
import importlib
import contextlib
from tqdm import tqdm
from dataclasses import asdict
from openai import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer
# Alternate tokenizer loader used for DeepSeek-R1-Distill-Llama-8B (see below).
from transformers.tokenization_utils_tokenizers import TokenizersBackend
from pynvml import nvmlInit, nvmlShutdown, nvmlDeviceGetHandleByIndex

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from energy.inference_energy import (
    measure_idle_power,
    PowerSampler,
    reset_gpu_state,
    EnergyRecord,
    resolve_nvml_index,
)


with open(f'./config.yaml', 'r') as f:
    configs = yaml.safe_load(f)
response_type = 'with_step' if configs['response_template_name']=='response_with_step_template' else 'without_step'

# optional part-ids filter for splitting a long run into pieces 
# Usage: python3 app_inference_with_measure.py dataset/TraceBench/test/parts/part_1_ids.json
# If no argument is given, the full dataset runs.
PART_IDS_FILE = sys.argv[1] if len(sys.argv) > 1 else None
PART_LABEL = os.path.splitext(os.path.basename(PART_IDS_FILE))[0] if PART_IDS_FILE else None

# drain residual CUDA activity between queries; Danish et al. inference script
COOLDOWN_BETWEEN_TASKS_S = configs['cooldown_between_tasks_s']  
MEASURE_ENERGY = configs['measure_energy']
print("Energy measurement enabled:", MEASURE_ENERGY)

def count_tokens_qwen(prompt, tokenizer):
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.encode(prompt, add_special_tokens=True)
    return len(tokens)

def split_from_mark(s, mark):
    index = s.find(mark)
    if index == -1:
        return s, ''  
    return s[:index], s[index:]

def import_template(template_type, template_name):    
    if template_type == 'instruction':
        module = importlib.import_module('DirectPrompting.Templates.InstructionTemplate')
    elif template_type == 'response':
        module = importlib.import_module('DirectPrompting.Templates.ResponseTemplate')
    elif template_type == 'codeprompt':
        module = importlib.import_module('DirectPrompting.Templates.CodePromptTemplate')
    return getattr(module, template_name)

def build_messages(system_prompt, user_instruction, llm_name):
    if 'deepseek' in llm_name.lower():
        # DeepSeek-R1-Distill's model card recommends against a system prompt;
        # fold it into the user turn instead. Same content, different packaging.
        return [{"role": "user", "content": system_prompt + '\n\n' + user_instruction}]
    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_instruction}]

def ask_llm(tokenizer, model, user_instruction, system_prompt):
    token_count = count_tokens_qwen(user_instruction+system_prompt, tokenizer)
    if token_count >= 129024:
        return None, token_count
    
    messages = build_messages(system_prompt, user_instruction, LLM_NAME)
    
    text = tokenizer.apply_chat_template(messages, **CHAT_TEMPLATE_KWARGS)
    model_input = tokenizer([text], return_tensors="pt").to(configs['device'])
    attention_mask = torch.ones(model_input.input_ids.shape, dtype=torch.long, device=configs['device'])
    generated_ids = model.generate(model_input.input_ids, max_new_tokens=configs['max_new_tokens'], attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id, do_sample=configs['do_sample'])
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_input.input_ids, generated_ids)]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response, token_count

def ask_llm_measured(tokenizer, model, user_instruction, system_prompt, handle, idle_power_w, problem_id):
    # measured generate() for full run; PowerSampler brackets generate(). Danish et al. (E-Energy 2026)
    token_count = count_tokens_qwen(user_instruction+system_prompt, tokenizer)
    if token_count >= 129024:
        return None, None, token_count

    messages = build_messages(system_prompt, user_instruction, LLM_NAME)

    text = tokenizer.apply_chat_template(messages, **CHAT_TEMPLATE_KWARGS)
    model_input = tokenizer([text], return_tensors="pt").to(configs['device'])
    attention_mask = torch.ones(model_input.input_ids.shape, dtype=torch.long, device=configs['device'])

    tokens_input = model_input.input_ids.shape[-1]
    sampler = PowerSampler(handle)

    torch.cuda.synchronize()
    print(f"  sync done, starting sampler", flush=True)
    sampler.start()
    print(f"  sampler started", flush=True)
    t_start = time.perf_counter()

    with torch.no_grad():
        output_ids = model.generate(model_input.input_ids, max_new_tokens=configs['max_new_tokens'], attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id, do_sample=configs['do_sample'])
    print(f"  generate done", flush=True)

    torch.cuda.synchronize()
    t_end = time.perf_counter()
    sampler.stop()

    tokens_output = max(output_ids.shape[-1] - tokens_input, 1)
    time_total_s      = t_end - t_start
    energy_total_j    = sampler.compute_energy_j()
    energy_marginal_j = max(0.0, energy_total_j - idle_power_w * time_total_s)

    record = EnergyRecord(
        problem_id=problem_id,
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

    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_input.input_ids, output_ids)]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return record, response, token_count

if __name__ == '__main__':
    start_time = time.time() 

    LLM_NAME = configs['llm_name']
    input_format = configs['input_data_format']
    BENCH_PATH = configs['trace_bench_dataset']
    # OUTPUT_FILE = configs['output_path'] + f"/LLMresponses_{LLM_NAME}_woFineTuning_woCoT_{input_format}_{response_type}.jsonl"
    # OUTPUT_ENERGY = configs['output_path'] + f"/energy_{LLM_NAME}_{input_format}_{response_type}_{int(start_time)}.jsonl"
    OUTPUT_FILE = configs['output_path'] + f"/LLMresponses_{LLM_NAME}_woFineTuning_woCoT_{input_format}_{response_type}{'_' + PART_LABEL if PART_LABEL else ''}.jsonl"
    OUTPUT_ENERGY = configs['output_path'] + f"/energy_{LLM_NAME}_{input_format}_{response_type}_{int(start_time)}{'_' + PART_LABEL if PART_LABEL else ''}.jsonl"
    CONVERTED_FORMAT_FILE = BENCH_PATH + f"/test/preprocessed/test_tasks_preprocessed_{input_format}_with_step.json"
    
    BATCHING_ENABLED = configs.get('batching_enabled', True)
    BATCH_SIZE = configs.get('batch_size', 1000)
    BATCH_DIR = OUTPUT_FILE.replace(".jsonl", f"_batches_{int(start_time)}")
    if BATCHING_ENABLED:
        os.makedirs(BATCH_DIR, exist_ok=True)
    batch_results = {}
    batch_id = 1

    # Starting the experiment for the given LLM and input format
    print(f"Starting for {LLM_NAME}, input format {input_format}, response type {response_type}")
    test_tasks = torch.load(BENCH_PATH+'/test/preprocessed/0.pt')
    
    # if input format is either from TOON, JSON, or MARKDOWN, CSV
    if(input_format in ['TOON', 'JSON', 'CSV', 'MARKDOWN', 'TRON']):
        print(f"Loading trace inputs for {input_format} from {CONVERTED_FORMAT_FILE}")

        with open(CONVERTED_FORMAT_FILE, "r", encoding="utf-8") as f:
            json_tasks = json.load(f)

        input_name = f"input_trace_{input_format}"

        # Overwrite only the input field, using pt file tasks for everything else
        for item in json_tasks:
            problem_id = item["problem_id"]
            if problem_id not in test_tasks:
                raise KeyError(f"problem_id {problem_id} from JSON not found in pt_tasks")
            test_tasks[problem_id][input_name] = item["input"]
        
    # keep only this part's problem_ids, if a part file was given 
    if PART_IDS_FILE:
        with open(PART_IDS_FILE, "r", encoding="utf-8") as pf:
            part_ids = set(json.load(pf))
        test_tasks = {pid: v for pid, v in test_tasks.items() if pid in part_ids}
        print(f"Running part {PART_LABEL}: {len(test_tasks)} tasks", flush=True)
    
    # test_tasks = dict(list(test_tasks.items())[:1])
    print(f"Total test tasks: {len(test_tasks)}", flush=True)

    # enable_thinking is Qwen-specific; detect from the model name 
    CHAT_TEMPLATE_KWARGS = {"tokenize": False, "add_generation_prompt": True}
    if 'qwen' in LLM_NAME.lower():
        CHAT_TEMPLATE_KWARGS['enable_thinking'] = False
    
    # Load LLM
    print(f"Loading {LLM_NAME}")
    model = AutoModelForCausalLM.from_pretrained(
            configs['llm_path'],
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        ).to(configs['device'])
    
    # DeepSeek-R1-Distill-Llama-8B needs a different tokenizer loader: AutoTokenizer
    # misroutes this checkpoint to a legacy tokenizer class that corrupts byte-level BPE
    # space handling (words lose their spaces during encoding, not just decoding).
    # Loading via TokenizersBackend directly avoids the misrouting.
    if 'deepseek' in LLM_NAME.lower():
        tokenizer = TokenizersBackend.from_pretrained(configs['llm_path'])
    else:
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=configs['llm_path'], use_fast=False)
    model.eval()

    print(f"Finish loading {LLM_NAME}!")
    print("Model device:", next(model.parameters()).device)

    # nvml init and idle baseline   
    if MEASURE_ENERGY:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(resolve_nvml_index())
        idle_power_w = measure_idle_power(handle)

    # response_results = dict()  # unused now -- responses are written incrementally to f_responses below
    energy_cm = open(OUTPUT_ENERGY, 'w') if MEASURE_ENERGY else contextlib.nullcontext()
    with energy_cm as f_energy, open(OUTPUT_FILE, 'w', encoding='utf-8') as f_responses:
        for problem_id, task_info in tqdm(test_tasks.items(), desc='LLM Response'):
            # step1
            # user instruction
            ## instruction
            instruction_name = list()
            instruction_name.append('instruction')
            instruction_name.append(configs['desc_method'])
            instruction_name.append(response_type)
            instruction_name = '_'.join(instruction_name)

            ## input
            input_name = f"input_trace_{input_format}"

            ## user instruction
            user_instruction_wo_qustion = split_from_mark(task_info[instruction_name], 'Question:')[0]
            user_instruction_qustion = split_from_mark(task_info[instruction_name], 'Question:')[1]
            input_traces = task_info[input_name]

            note_content = 'Note: The solution consists of the explicit reasoning path and the final answer. The final answer may be a number, a string, or a list, which can be empty (i.e., []). The final answer is presented within <<<>>>.'
            user_instruction = user_instruction_wo_qustion + '\n' + user_instruction_qustion + '\n' + input_traces + '\n' + note_content + '\n' + '\nAnswer:'
            # system prompt
            system_prompt_name = list()
            system_prompt_name.append('system_prompt')
            system_prompt_name.append(response_type)
            system_prompt_name = '_'.join(system_prompt_name)
            system_prompt = import_template(template_type='instruction', template_name=system_prompt_name)
            # response
            response_name = list()
            response_name.append('response')
            response_name.append(response_type)
            response_name = '_'.join(response_name)

            # step2
            print(f"Task {problem_id}", flush=True)
            if MEASURE_ENERGY:
                energy_record, response, token_count = ask_llm_measured(
                    tokenizer, model, user_instruction, system_prompt, handle, idle_power_w, problem_id
                )
                if energy_record is not None:
                    f_energy.write(json.dumps(asdict(energy_record)) + '\n')
                    f_energy.flush()
            else:
                response, token_count = ask_llm(tokenizer, model, user_instruction, system_prompt)

            # step3
            # write this response as one line immediately, instead of accumulating in memory
            record = dict()
            record['task_id'] = task_info['task_id']
            record['type_id'] = task_info['type_id']
            record['gt_response'] = task_info[response_name]
            record['gt_answer'] = task_info['answer']
            record['llm_response'] = response
            record['token_count'] = token_count
            f_responses.write(json.dumps({problem_id: record}, ensure_ascii=False) + '\n')
            f_responses.flush()

            # saving the batch results to a file
            if BATCHING_ENABLED:
                batch_results[problem_id] = record
                if len(batch_results) == BATCH_SIZE:
                    batch_file = os.path.join(BATCH_DIR, f"batch_{batch_id:05d}.json")
                    with open(batch_file, "w", encoding="utf-8") as file:
                        json.dump(batch_results, file, ensure_ascii=False, indent=4)

                    batch_results = {}
                    batch_id += 1
                
            if MEASURE_ENERGY:
                reset_gpu_state(model)
                print(f"  reset done", flush=True)
                time.sleep(COOLDOWN_BETWEEN_TASKS_S)

    if MEASURE_ENERGY:
        nvmlShutdown()

    total_time = time.time() - start_time
    total_time_str = str(datetime.timedelta(seconds=int(total_time)))
    print("-"*20)
    print("Testing time {}".format(total_time_str))
    print("-"*20)

    if BATCHING_ENABLED and batch_results:
        batch_file = os.path.join(BATCH_DIR, f"batch_{batch_id:05d}.json")
        with open(batch_file, "w", encoding="utf-8") as file:
            json.dump(batch_results, file, ensure_ascii=False, indent=4)

    # unused now -- responses already written incrementally to f_responses above
    # with open(OUTPUT_FILE, 'w') as file:
    #     json.dump(response_results, file, indent=4)

    print('Done!')