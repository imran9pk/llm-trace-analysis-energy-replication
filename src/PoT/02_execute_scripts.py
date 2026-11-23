# %%
import os

# Limit library threading based on allocated SLURM CPUs
# SLURM-specific in the original runs; falls back to 1 thread outside SLURM
os.environ["OMP_NUM_THREADS"] = os.environ.get("SLURM_CPUS_PER_TASK", "1")
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import ast
import contextlib
import io
import json
import multiprocessing
import re
import time
import traceback
import yaml
import torch
from tqdm import tqdm
import argparse

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
# TraceLLM/ root -- BASE_DIR is TraceLLM/src/PoT/, two levels down from it.
TRACE_LLM_ROOT  = os.path.join(BASE_DIR, "..", "..")
RESULTS_DIR     = os.path.join(TRACE_LLM_ROOT, 'output', 'executed_scripts_results')
CONFIG_PATH     = os.path.join(TRACE_LLM_ROOT, 'configPoT.yaml')
TASK_INFO_PATH  = os.path.join(TRACE_LLM_ROOT, 'dataset', 'TraceBench', 'test', 'preprocessed', 'TaskInfo.json')

with open(CONFIG_PATH, 'r') as f:
    configs = yaml.safe_load(f)

SCRIPTS_DIR = None

with open(TASK_INFO_PATH, 'r') as f:
    TASK_INFO = json.load(f)

TIMEOUT_SECONDS  = 30
MAX_OUTPUT_LEN   = 1000


def parse_key_component(question: str, question_template: str) -> dict:
    """
    Extract key_component value(s) from a concrete question string using
    the question_template pattern from TaskInfo.json.

    Returns a dict with keys 'key_component', 'key_component_1',
    'key_component_2' as applicable. Empty dict if no key components.

    We do this via regex: replace {key_component} placeholders with
    named capture groups, then match against the concrete question.

    This is the only instance-specific information extracted without LLM.
    It is analogous to what their PoT LLM had to infer from the question text.
    """
    if not question_template:
        return {}

    placeholders = re.findall(r'\{(key_component(?:_\d)?)\}', question_template)
    if not placeholders:
        return {}

    # Build a regex from the template
    pattern = re.escape(question_template)
    for ph in placeholders:
        pattern = pattern.replace(re.escape('{' + ph + '}'), f'(?P<{ph}>.+?)')
    pattern += '$'

    match = re.search(pattern, question)
    if not match:
        return {}

    return match.groupdict()


def _execution_worker(script_source: str, call_code: str, queue: multiprocessing.Queue) -> None:
    """Worker process: exec script to define solution(), then exec call_code to invoke it."""
    output_buffer = io.StringIO()
    try:
        code_to_run = script_source + "\n" + call_code
        with contextlib.redirect_stdout(output_buffer):
            exec(code_to_run, {})
        queue.put(output_buffer.getvalue().strip())
    except Exception:
        queue.put(traceback.format_exc().strip())

def execute_script(task_id: str, trace1: list, trace2: list | None,
                   key_components: dict) -> tuple[str, float]:
    t_start = time.perf_counter()

    script_path = os.path.join(SCRIPTS_DIR, f'{task_id}.py')
    if not os.path.exists(script_path):
        return f"[ERROR] Script not found: {script_path}", time.perf_counter() - t_start

    # Build argument list for the call
    # Order: trace1, [trace2], [key_component(s)]
    call_args = ['trace1']

    if trace2 is not None:
        call_args.append('trace2')

    kc  = key_components.get('key_component')
    kc1 = key_components.get('key_component_1')
    kc2 = key_components.get('key_component_2')

    if not task_id.startswith("Task_4"):
        if kc is not None:
            call_args.append('key_component')
        elif kc1 is not None and kc2 is not None:
            call_args.append('key_component_1')
            call_args.append('key_component_2')

    # Build the call code string
    lines = []
    lines.append(f"trace1 = {repr(trace1)}")

    if trace2 is not None:
        lines.append(f"trace2 = {repr(trace2)}")

    # For Task_4_* tasks, key_component_1/key_component_2 refer only to
    # Input Trace 1 and Input Trace 2, so do not pass them to solution().
    if not task_id.startswith("Task_4"):
        if kc is not None:
            lines.append(f"key_component = {repr(kc)}")
        if kc1 is not None and kc2 is not None:
            lines.append(f"key_component_1 = {repr(kc1)}")
            lines.append(f"key_component_2 = {repr(kc2)}")

    lines.append(f"_answer = solution({', '.join(call_args)})")
    lines.append("print('<<<' + str(_answer) + '>>>')")

    call_code = '\n'.join(lines)

    with open(script_path, 'r') as f:
        script_source = f.read()

    queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=_execution_worker,
        args=(script_source, call_code, queue)
    )
    process.start()
    process.join(TIMEOUT_SECONDS)

    if process.is_alive():
        process.terminate()
        process.join()
        return f"[TIMEOUT] Execution timed out after {TIMEOUT_SECONDS} seconds.", time.perf_counter() - t_start

    try:
        result = queue.get_nowait()
    except Exception:
        result = "[ERROR] No output captured."

    time_total_s = time.perf_counter() - t_start
    return result[:MAX_OUTPUT_LEN] + ("...[truncated]" if len(result) > MAX_OUTPUT_LEN else ""), time_total_s


def parse_input_traces(input_field: str) -> tuple[list, list | None]:
    """
    Parse the 'input' field of a test instance into trace1 (and trace2).
    The input field is a string like:
      "Input Trace: [{...}, {...}]"
    or for trace-pair tasks:
      "Input Trace 1: [...] Input Trace 2: [...]"
    """
    if "Input Trace 1: " in input_field and "Input Trace 2: " in input_field:
        start1 = input_field.find("Input Trace 1: ") + len("Input Trace 1: ")
        start2 = input_field.find("Input Trace 2: ")
        trace1_str = input_field[start1:start2].strip()
        trace2_str = input_field[start2 + len("Input Trace 2: "):].strip()
        trace1 = ast.literal_eval(trace1_str)
        trace2 = ast.literal_eval(trace2_str)
        return trace1, trace2
    elif "Input Trace: " in input_field:
        trace_str = input_field.split("Input Trace: ", 1)[1].strip()
        trace1 = ast.literal_eval(trace_str)
        return trace1, None
    else:
        raise ValueError(f"Unrecognized input format: {input_field[:100]}")

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


def main():
    print(f"Starting script execution for {configs['llm_name']}...")
    global SCRIPTS_DIR

    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, required=True)
    args = parser.parse_args()

    label = f"{shot_name(args.shots)}shot"

    SCRIPTS_DIR = os.path.join(TRACE_LLM_ROOT, 'output', 'generated_scripts', f"generated_scripts_{configs['llm_name']}_{label}")

    test_instances_path = os.path.join(BASE_DIR, configs['test_instances_path'])
    output_path = os.path.join(
        RESULTS_DIR,
        f"results_taskLevel_{configs['llm_name']}_{label}.json"
    )

    os.makedirs(RESULTS_DIR, exist_ok=True)

    test_instances = torch.load(test_instances_path, map_location='cpu')
    # test_instances = dict(list(test_instances.items())[:100])

    results = {}
    stats = {
        'total': 0,
        'script_missing': 0,
        'parse_error': 0,
        'execution_error': 0,
        'timeout': 0,
        'success': 0
    }

    for problem_id, instance in tqdm(test_instances.items(), desc='Executing scripts'):
        stats['total'] += 1

        task_id = instance['task_id']
        type_id = instance['type_id']

        # 0.pt uses this field for raw span input
        input_field = instance['input_trace_raw_spans_desc']
        

        try:
            trace1, trace2 = parse_input_traces(input_field)
        except Exception as e:
            llm_response = f"[PARSE ERROR] {str(e)}"
            stats['parse_error'] += 1

            results[problem_id] = {
                'task_id': task_id,
                'type_id': type_id,
                'gt_response': instance.get('response_without_step', ''),
                'gt_answer': instance.get('answer', ''),
                'llm_response': llm_response,
                'token_count': 0,
                'time_total_s': 0.0
            }
            continue

        # 0.pt already has the concrete question separately
        question_template = TASK_INFO.get(task_id, {}).get('question_template', '')
        question = instance['question']
        key_components = parse_key_component(question, question_template)

        if not task_id.startswith("Task_3") and not task_id.startswith("Task_4"):
            if not key_components:
                print(f"[WARN] No key components parsed for {problem_id} {task_id}")
                print(f"       Question: {question}")
                print(f"       Template: {question_template}")

        llm_response, time_total_s = execute_script(
            task_id=task_id,
            trace1=trace1,
            trace2=trace2,
            key_components=key_components
        )

        if '[ERROR] Script not found' in llm_response:
            stats['script_missing'] += 1
        elif '[TIMEOUT]' in llm_response:
            stats['timeout'] += 1
        elif '[ERROR]' in llm_response or 'Traceback' in llm_response:
            stats['execution_error'] += 1
        else:
            stats['success'] += 1

        results[problem_id] = {
            'task_id': task_id,
            'type_id': type_id,
            'gt_response': instance.get('response_without_step', ''),
            'gt_answer': instance.get('answer', ''),
            'llm_response': llm_response,
            'token_count': 0,
            'time_total_s': round(time_total_s, 6)
        }

        if stats['total'] % 500 == 0:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=4)

            print(
                f"[CHECKPOINT] {stats['total']} processed "
                f"(success={stats['success']}, "
                f"errors={stats['execution_error']}, "
                f"timeouts={stats['timeout']})",
                flush=True
            )

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"\n{'─' * 50}")
    print(f"Results saved to: {output_path}")
    print(f"{'─' * 50}")
    print(f"Summary for PoT Scripts Execution - {configs['llm_name']}_{label}:")
    print(f"Total instances : {stats['total']}")
    print(f"Success         : {stats['success']}")
    print(f"Execution errors: {stats['execution_error']}")
    print(f"Timeouts        : {stats['timeout']}")
    print(f"Parse errors    : {stats['parse_error']}")
    print(f"Script missing  : {stats['script_missing']}")
    print(f"{'─' * 50}")
    print(f"Run cal_accuracy_Graph2Token.py on {output_path} for accuracy.")


if __name__ == '__main__':
    main()