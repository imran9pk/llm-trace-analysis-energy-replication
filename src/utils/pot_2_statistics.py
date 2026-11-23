"""
pot_2_statistics.py

RQ3/RQ4 (task-level program generation, PoT) numbers, from:
  * output_processed/accuracy_pot/<model>_<shot>/   (pot_1_cal_accuracy_all.py)
  * output/executed_scripts_results/results_taskLevel_<model>_<shot>.json
  * output/generated_scripts/energy_generation_<model>_<shot>_<timestamp>.jsonl
    (latest timestamp is used if a shot level was generated more than once)
  * output_processed/analysis/RQ2_energy.csv         (direct prompting, JSON; directPrompting_6_rq2_statistics.py)
  * output_processed/accuracy/<model>_JSON/          (direct prompting, JSON; directPrompting_3_cal_accuracy_all.py)

Writes (under output_processed/analysis/):
  RQ3_shot_selection.csv  PoT accuracy per model and shot level, plus the mean
                          over the models that have all few-shot levels (1-5
                          examples); prints the smallest few-shot level after
                          which the mean does not improve (check for POT_FEWSHOT).
  RQ3_pot_accuracy.csv    per model: direct-prompting (JSON) accuracy, and PoT
                          accuracy and share of failed executions for zero-shot
                          and POT_FEWSHOT.
  RQ3_pot_tasks.csv       per model and strategy (direct JSON, PoT zero-shot,
                          PoT POT_FEWSHOT): number of tasks (of 38) with accuracy
                          >= 95% and <= 5%, and number of tasks on which PoT is
                          more accurate than direct prompting (JSON).
  RQ3_pot_errors.csv      per model and shot (zero-shot, POT_FEWSHOT): failed
                          instances by Python error type (e.g. KeyError).
  RQ4_pot_energy.csv      per model: direct-prompting (JSON) total energy for
                          9,120 calls vs PoT generation energy for 38 calls
                          (zero-shot, POT_FEWSHOT), total execution time, and the
                          CPU energy (exec_energy_j) and time (exec_run_time_s,
                          from the warm-up) of one run of the programs on all
                          instances, from src/PoT/03_measure_execution_energy.py
                          (mean over repetitions with window_ok; empty if not measured).

A PoT configuration is reported as missing (empty cells) when its files do not
exist, its execution results are incomplete, or no instance executed
successfully.

Usage:
    python pot_2_statistics.py
"""

from __future__ import annotations

import glob
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from utils_config import MODELS, POT_FEWSHOT, SHOTS  # noqa: E402

REPO_DIR = SCRIPT_DIR.parent.parent
RESULTS_DIR = REPO_DIR / "output" / "executed_scripts_results"
GEN_DIR = REPO_DIR / "output" / "generated_scripts"
EXEC_ENERGY_DIR = REPO_DIR / "output" / "execution_energy"   # 03_measure_execution_energy.py
PROCESSED_DIR = REPO_DIR / "output_processed"
ANALYSIS_DIR = PROCESSED_DIR / "analysis"
EXPECTED_INSTANCES = 9120
EXPECTED_TASKS = 38
FAIL_MARKERS = ("Traceback", "[ERROR]", "[TIMEOUT]", "[PARSE ERROR]")
TASK_HIGH, TASK_LOW = 0.95, 0.05
CSV_DATASET = REPO_DIR / "dataset" / "TraceBench" / "test" / "preprocessed" / "test_tasks_preprocessed_CSV_with_step.json"  # a task counts as solved / not solved above / below these accuracies

# Original TraceLLM evaluator, unchanged (same use as in directPrompting_4_build_instance_table.py).
_spec = importlib.util.spec_from_file_location("cal_acc", SCRIPT_DIR / "cal_accuracy_Graph2Token.py")
cal_acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cal_acc)  # type: ignore[union-attr]


def pot_execution(model: str, shot: str) -> dict | None:
    """Accuracy, failed-execution share and total execution time; None if missing/incomplete/invalid."""
    res_file = RESULTS_DIR / f"results_taskLevel_{model}_{shot}.json"
    acc_file = PROCESSED_DIR / "accuracy_pot" / f"{model}_{shot}" / "global_level_eval_results.json"
    if not res_file.exists() or not acc_file.exists():
        return None
    with open(res_file, "r", encoding="utf-8") as f:
        results = json.load(f)
    if len(results) < EXPECTED_INSTANCES:
        return None
    failed = sum(1 for r in results.values()
                 if any(k in (r.get("llm_response") or "") for k in ("Traceback", "[ERROR]", "[TIMEOUT]", "[PARSE ERROR]")))
    if failed == len(results):
        print(f"WARNING: {model}/{shot}: no instance executed successfully -- reported as missing")
        return None
    with open(acc_file, "r", encoding="utf-8") as f:
        accuracy = json.load(f)["global"]["accuracy"]
    exec_time = sum(float(r.get("time_total_s") or 0) for r in results.values())
    return {"accuracy": accuracy, "failed_share": failed / len(results), "exec_time_s": exec_time}


def pot_instances(model: str, shot: str) -> pd.DataFrame | None:
    """One row per instance: task, correct (TraceLLM evaluator) and error type ('' if the program ran)."""
    if pot_execution(model, shot) is None:
        return None
    with open(RESULTS_DIR / f"results_taskLevel_{model}_{shot}.json", "r", encoding="utf-8") as f:
        results = json.load(f)
    rows = []
    for pid, r in results.items():
        resp = r.get("llm_response") or ""
        error = ""
        if "[TIMEOUT]" in resp:
            error = "Timeout"
        elif any(k in resp for k in FAIL_MARKERS):
            # Python ends a traceback with "<ErrorType>: <message>" (e.g. "KeyError: '-1'", "StopIteration").
            last = resp.strip().splitlines()[-1] if resp.strip() else ""
            match = re.match(r"([A-Z]\w*)(?::|$)", last)
            error = match.group(1) if match else "Other"
        correct = int(round(cal_acc.get_eval_result([resp], [r["gt_answer"]], ["_"])["accuracy"]))
        rows.append({"problem_id": pid, "task_id": r["task_id"], "correct": correct, "error": error})
    return pd.DataFrame(rows)


def task_counts(task_acc: pd.Series) -> dict:
    return {"tasks": len(task_acc), "tasks_acc_ge_95": int((task_acc >= TASK_HIGH).sum()),
            "tasks_acc_le_5": int((task_acc <= TASK_LOW).sum())}


def pot_generation(model: str, shot: str) -> dict | None:
    """Total marginal energy, tokens and time of the 38 generation calls; None if missing/incomplete."""
    files = sorted(glob.glob(str(GEN_DIR / f"energy_generation_{model}_{shot}_*.jsonl")))
    if not files:
        return None
    records = [json.loads(line) for line in open(files[-1], encoding="utf-8") if line.strip()]
    if len(records) < EXPECTED_TASKS:
        return None
    return {"gen_energy_j": sum(r["energy_marginal_j"] for r in records),
            "gen_tokens_out": sum(r["tokens_output"] for r in records),
            "gen_time_s": sum(r["time_total_s"] for r in records)}


def main() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    # Shot selection check
    rows = []
    for shot in SHOTS:
        row = {"shot": shot}
        for model in MODELS:
            ex = pot_execution(model, shot)
            row[model] = ex["accuracy"] if ex else None
        rows.append(row)
    sel = pd.DataFrame(rows).set_index("shot")
    fewshot = [sh for sh in SHOTS if sh != "zeroshot"]
    # Models with results for every few-shot level (the zero-shot run is not needed for the choice).
    complete = [m for m in MODELS if sel.loc[fewshot, m].notna().all()]
    sel["mean_complete_models"] = sel[complete].mean(axis=1, skipna=False) if complete else None
    sel.to_csv(ANALYSIS_DIR / "RQ3_shot_selection.csv")
    if complete:
        means = sel.loc[fewshot, "mean_complete_models"].tolist()
        chosen = next((fewshot[i] for i in range(len(means) - 1) if means[i + 1] <= means[i]), fewshot[-1])
        print(f"shot selection (mean over {len(complete)} complete model(s): {', '.join(complete)}): "
              f"smallest level after which the mean does not improve = {chosen}; POT_FEWSHOT = {POT_FEWSHOT}"
              + ("" if chosen == POT_FEWSHOT else "  <-- DIFFERENT, check utils_config.POT_FEWSHOT"))

    # Direct-prompting (JSON) reference
    rq2 = PROCESSED_DIR / "analysis" / "RQ2_energy.csv"
    direct_energy = {}
    if rq2.exists():
        d = pd.read_csv(rq2)
        d = d[d.format == "JSON"]
        direct_energy = dict(zip(d.model, d.energy_total_j))

    # CPU energy of executing the programs: mean over repetitions (all measurement files).
    exec_files = sorted(EXEC_ENERGY_DIR.glob("execution_energy_*.csv"))
    exec_runs = pd.concat([pd.read_csv(f) for f in exec_files]) if exec_files else None
    if exec_runs is not None and "window_ok" in exec_runs:
        exec_runs = exec_runs[exec_runs.window_ok.astype(str) == "True"]     # windows >= 5 s only
    exec_energy = (exec_runs.groupby(["model", "shot"]).exec_package_j.mean()
                   if exec_runs is not None else pd.Series(dtype=float))
    exec_run_time = (exec_runs.groupby(["model", "shot"]).exec_time_s.mean()   # one run of the test set, in the window
                     if exec_runs is not None else pd.Series(dtype=float))

    acc_rows, energy_rows = [], []
    for model in MODELS:
        acc_file = PROCESSED_DIR / "accuracy" / f"{model}_JSON" / "global_level_eval_results.json"
        direct_acc = json.load(open(acc_file, encoding="utf-8"))["global"]["accuracy"] if acc_file.exists() else None
        acc_row = {"model": model, "direct_json_accuracy": direct_acc}
        energy_row = {"model": model, "direct_json_energy_j": direct_energy.get(model)}
        # Zero-shot and the few-shot level used in the paper.
        for label, shot in [("zeroshot", "zeroshot"), ("fewshot", POT_FEWSHOT)]:
            ex = pot_execution(model, shot)
            gen = pot_generation(model, shot)
            acc_row[f"pot_{label}_accuracy"] = ex["accuracy"] if ex else None
            acc_row[f"pot_{label}_failed_share"] = ex["failed_share"] if ex else None
            energy_row[f"pot_{label}_gen_energy_j"] = gen["gen_energy_j"] if gen else None
            energy_row[f"pot_{label}_gen_tokens_out"] = gen["gen_tokens_out"] if gen else None
            energy_row[f"pot_{label}_exec_time_s"] = ex["exec_time_s"] if ex else None
            energy_row[f"pot_{label}_exec_energy_j"] = exec_energy.get((model, shot))
            energy_row[f"pot_{label}_exec_run_time_s"] = exec_run_time.get((model, shot))
        acc_rows.append(acc_row)
        energy_rows.append(energy_row)
    # RQ3: how accuracy is spread over the 38 tasks, and why programs fail.
    inst_file = ANALYSIS_DIR / "instance_level.csv.gz"
    direct_inst = pd.read_csv(inst_file, usecols=["model", "format", "task_id", "correct"]) if inst_file.exists() else None
    task_rows, error_rows = [], []
    for model in MODELS:
        direct_task = None
        if direct_inst is not None:
            dm = direct_inst[(direct_inst.model == model) & (direct_inst.format == "JSON")]
            if len(dm):
                direct_task = dm.groupby("task_id").correct.mean()
                task_rows.append({"model": model, "strategy": "direct_json", **task_counts(direct_task)})
        for label, shot in [("pot_zeroshot", "zeroshot"), ("pot_fewshot", POT_FEWSHOT)]:
            pi = pot_instances(model, shot)
            if pi is None:
                continue
            pot_task = pi.groupby("task_id").correct.mean()
            row = {"model": model, "strategy": label, **task_counts(pot_task)}
            if direct_task is not None:
                row["tasks_pot_above_direct"] = int((pot_task > direct_task.reindex(pot_task.index)).sum())
            task_rows.append(row)
            for err, n in Counter(pi.error[pi.error != ""]).most_common():
                error_rows.append({"model": model, "shot": shot, "error": err, "instances": n})
    pd.DataFrame(task_rows).to_csv(ANALYSIS_DIR / "RQ3_pot_tasks.csv", index=False)
    pd.DataFrame(error_rows, columns=["model", "shot", "error", "instances"]).to_csv(
        ANALYSIS_DIR / "RQ3_pot_errors.csv", index=False)

    acc = pd.DataFrame(acc_rows)
    energy = pd.DataFrame(energy_rows)
    acc.to_csv(ANALYSIS_DIR / "RQ3_pot_accuracy.csv", index=False)
    energy.to_csv(ANALYSIS_DIR / "RQ4_pot_energy.csv", index=False)
    pd.set_option("display.width", 220)
    print(sel.round(3).to_string())
    print(acc.round(3).to_string(index=False))
    print(pd.DataFrame(task_rows).to_string(index=False))
    print(energy.round(1).to_string(index=False))
    print(f"\nSaved RQ3/RQ4 PoT statistics to {ANALYSIS_DIR}")


if __name__ == "__main__":
    main()
