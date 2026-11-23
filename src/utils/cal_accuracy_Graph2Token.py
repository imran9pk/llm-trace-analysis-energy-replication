import argparse
import json
import re
import yaml
import os

from tqdm import tqdm


def get_format_answer(response):
    # step1
    pattern = r'<<<(.*?)>>>'
    matches = re.findall(pattern, response)
    if len(matches) == 0:
        return None
    answer = matches[0]
    if not answer:
        pattern = r'<<<>>>\s*(.*)'
        matches = re.findall(pattern, response)
        if len(matches) == 0:
            return None
        answer = matches[0]
    # step2
    try:
        return eval(answer) 
    except Exception:
        return answer


def get_eval_result(llm_response_list, gt_answer_list, problem_id_list):
    assert len(llm_response_list) == len(gt_answer_list) == len(problem_id_list)
    all_count = len(problem_id_list)
    correct_count = 0
    miss_count = 0

    for llm_response, gt_answer in zip(llm_response_list, gt_answer_list):
        if not llm_response:
            llm_answer = llm_response
        else:
            llm_answer = get_format_answer(llm_response)
        if type(llm_answer) != type(gt_answer):
            if isinstance(llm_answer, int) and isinstance(gt_answer, str):
                if str(llm_answer) == gt_answer:
                    correct_count += 1
                    continue
            if isinstance(llm_answer, str) and isinstance(gt_answer, list):
                format_answer = [item.strip() for item in llm_answer.split(',') if item.strip()]
                if set(format_answer) == set(gt_answer):
                    correct_count += 1
                    continue
            miss_count += 1
        else:
            if isinstance(llm_answer, list):
                try:
                    if set(llm_answer) == set(gt_answer):
                        correct_count += 1
                    else:
                        miss_count += 1
                except Exception:
                    miss_count += 1
            else:
                if isinstance(gt_answer, str) and isinstance(llm_answer, str):
                    if 'span' in llm_answer or 'Span' in llm_answer:
                        llm_answer = llm_answer.split()[-1].strip("'\"")
                if llm_answer == gt_answer:
                    correct_count += 1
                else:
                    miss_count += 1

    accuracy = correct_count/all_count
    result = {
        "accuracy": accuracy
    }

    return result


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Compute global/dimension/second-type-level accuracy from a combined LLMresponses file (see combine_parts.py)."
    )
    parser.add_argument("--input", required=True, help="Path to the combined LLMresponses_*.jsonl file")
    parser.add_argument("--output-dir", required=True, help="Directory to write the *_level_eval_results.json files into")
    args = parser.parse_args()

    RESULT_FILE = args.input
    OUTPUT_PATH = args.output_dir

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    with open(RESULT_FILE, 'r') as file:
        result = json.load(file)
    
    print('[START] Global-level Evaluation')
    llm_response_list, gt_answer_list, problem_id_list = list(), list(), list()
    for problem_id, response_info in tqdm(result.items(), desc='Global-level Evaluation'):
        llm_response_list.append(response_info['llm_response'])
        gt_answer_list.append(response_info['gt_answer'])
        problem_id_list.append(problem_id)
    eval_result = get_eval_result(llm_response_list, gt_answer_list, problem_id_list)
    final_results = {"global": eval_result}
    with open(os.path.join(OUTPUT_PATH, 'global_level_eval_results.json'), 'w') as file:
        json.dump(final_results, file, indent=4)
    print('[END] Global-level Evaluation')

    print('[START] Dimension-level Evaluation')
    result_summary = dict()
    for problem_id, response_info in result.items():
        task_name = response_info['task_id']
        task_level = task_name.split('_')[1]
        if task_level not in result_summary:
            result_summary[task_level] = {
                "llm_response_list": list(),
                "gt_answer_list": list(),
                "problem_id_list": list()
            }
        result_summary[task_level]["llm_response_list"].append(response_info['llm_response'])
        result_summary[task_level]["gt_answer_list"].append(response_info['gt_answer'])
        result_summary[task_level]["problem_id_list"].append(problem_id)
    final_results = dict()
    for task_level, task_results in tqdm(result_summary.items(), desc='Dimension-level Evaluation'):
        eval_result = get_eval_result(task_results["llm_response_list"], task_results["gt_answer_list"], task_results["problem_id_list"])
        final_results[task_level] = eval_result
    with open(os.path.join(OUTPUT_PATH, 'dimension_level_eval_results.json'), 'w') as file:
        json.dump(final_results, file, indent=4)
    print('[END] Dimension-level Evaluation')
    
    print('[START] Second-Type-level Evaluation')
    result_summary = dict()
    for problem_id, response_info in result.items():
        task_type = response_info['type_id'].split('_')[0]
        if task_type not in result_summary:
            result_summary[task_type] = {
                "llm_response_list": list(),
                "gt_answer_list": list(),
                "problem_id_list": list()
            }
        result_summary[task_type]["llm_response_list"].append(response_info['llm_response'])
        result_summary[task_type]["gt_answer_list"].append(response_info['gt_answer'])
        result_summary[task_type]["problem_id_list"].append(problem_id)
    final_results = dict()
    for task_type, task_results in tqdm(result_summary.items(), desc='Second-Type-level Evaluation'):
        eval_result = get_eval_result(task_results["llm_response_list"], task_results["gt_answer_list"], task_results["problem_id_list"])
        final_results[task_type] = eval_result
    with open(os.path.join(OUTPUT_PATH, 'second_type_level_eval_results.json'), 'w') as file:
        json.dump(final_results, file, indent=4)
    print('[END] Second-Type-level Evaluation')

    print('Done!')