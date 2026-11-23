"""
pot_1_cal_accuracy_all.py

PoT (task-level program generation) counterpart of directPrompting_3_cal_accuracy_all.py:
runs the unchanged TraceLLM evaluator (cal_accuracy_Graph2Token.py)
against each model x shot-level PoT execution result produced by
src/PoT/02_execute_scripts*.py.

Input  : output/executed_scripts_results/results_taskLevel_<model>_<shot>.json
         (same structure as a combined direct-prompting responses file:
         problem_id -> task_id, type_id, gt_answer, llm_response, ...)
Output : output_processed/accuracy_pot/<model>_<shot>/
         global/dimension/second_type_level_eval_results.json
         plus output_processed/accuracy_pot/PoT_accuracy_summary.csv
         (one row per evaluated model x shot: accuracy and execution outcome counts).

Edit MODELS in utils_config.py and SHOTS in utils_config.py to choose
what is processed. A combo is SKIPPED (with a message) when:
  * its result file does not exist yet, or
  * the result file is incomplete (fewer than 9,120 instances -- e.g. a
    run still in progress that has written a checkpoint), because an
    accuracy over a partial test set is not comparable.
A WARNING is printed when every instance failed to execute (usually a
generation problem, not a model result).

Cross-platform: plain Python, run the same way on Windows or Linux.

Usage:
    python pot_1_cal_accuracy_all.py
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from utils_config import MODELS, SHOTS  # noqa: E402 -- see utils_config.py to edit the lists

REPO_DIR = SCRIPT_DIR.parent.parent
RESULTS_DIR = REPO_DIR / "output" / "executed_scripts_results"
OUTPUT_DIR = REPO_DIR / "output_processed" / "accuracy_pot"
CAL_ACCURACY_SCRIPT = SCRIPT_DIR / "cal_accuracy_Graph2Token.py"
EXPECTED_INSTANCES = 9120


def outcome(llm_response: str) -> str:
    """Classify one execution result, with the same rules as 02_execute_scripts*.py's summary."""
    if "[ERROR] Script not found" in llm_response:
        return "script_missing"
    if "[TIMEOUT]" in llm_response:
        return "timeout"
    if "[PARSE ERROR]" in llm_response:
        return "parse_error"
    if "[ERROR]" in llm_response or "Traceback" in llm_response:
        return "execution_error"
    return "success"


def main() -> None:
    summary: list[dict] = []
    for model in MODELS:
        for shot in SHOTS:
            input_file = RESULTS_DIR / f"results_taskLevel_{model}_{shot}.json"
            if not input_file.exists():
                print(f"skip: {model}/{shot} no PoT result file yet")
                continue
            with open(input_file, "r", encoding="utf-8") as f:
                results = json.load(f)
            if len(results) < EXPECTED_INSTANCES:
                print(f"skip: {model}/{shot} incomplete ({len(results)}/{EXPECTED_INSTANCES} instances)")
                continue

            counts = {k: 0 for k in ["success", "execution_error", "timeout", "parse_error", "script_missing"]}
            for record in results.values():
                counts[outcome(record.get("llm_response") or "")] += 1
            if counts["success"] == 0:
                print(f"WARNING: {model}/{shot}: no instance executed successfully -- check the generated scripts")

            output_dir = OUTPUT_DIR / f"{model}_{shot}"
            print(f"\n=== PoT accuracy eval: {model} / {shot} ===")
            subprocess.run(
                [sys.executable, str(CAL_ACCURACY_SCRIPT), "--input", str(input_file), "--output-dir", str(output_dir)],
                check=True,
            )
            with open(output_dir / "global_level_eval_results.json", "r", encoding="utf-8") as f:
                accuracy = json.load(f)["global"]["accuracy"]
            summary.append({"model": model, "shot": shot, "instances": len(results), "accuracy": f"{accuracy:.4f}", **counts})

    if not summary:
        print("no complete PoT result file found for any model/shot combo")
        return
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_file = OUTPUT_DIR / "PoT_accuracy_summary.csv"
    with open(summary_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)
    print(f"\nSaved PoT accuracy summary ({len(summary)} row(s)) to {summary_file}")


if __name__ == "__main__":
    main()
