"""
directPrompting_4_build_instance_table.py

Builds ONE long, instance-level table that every downstream RQ1/RQ2
analysis script (directPrompting_5_* onwards) reads. One row per (model, format,
problem_id): correctness under the unchanged TraceLLM evaluator
(cal_accuracy_Graph2Token.get_eval_result, applied to a single item),
whether an answer could be extracted, the extracted answer text, and
the matching energy record fields.

Why a separate table: accuracy per task granularity, the inspection of
answers (e.g. wrong-attribute answers) and the energy model all need the
per-instance join of responses and energy records.

Edit MODELS/FORMATS in utils_config.py. Combos missing either the
combined responses file or the combined energy file are skipped with a
message.

Writes output_processed/analysis/instance_level.csv.gz

Dependencies: pandas (plus tqdm, already required by
cal_accuracy_Graph2Token.py).

Usage:
    python directPrompting_4_build_instance_table.py
"""

from __future__ import annotations

import glob
import importlib.util
import json
import re
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from utils_config import FORMATS, MODELS  # noqa: E402

OUTPUT_PROCESSED_DIR = SCRIPT_DIR.parent.parent / "output_processed"
ANALYSIS_DIR = OUTPUT_PROCESSED_DIR / "analysis"
OUTPUT_FILE = ANALYSIS_DIR / "instance_level.csv.gz"

EXPECTED_INSTANCES = 9120

# Load the original evaluator without modifying it.
_spec = importlib.util.spec_from_file_location("cal_acc", SCRIPT_DIR / "cal_accuracy_Graph2Token.py")
cal_acc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cal_acc)  # type: ignore[union-attr]


def score_instance(llm_response: str | None, gt_answer) -> tuple[int, int]:
    """Return (correct, extracted) for one instance using the TraceLLM evaluator unchanged."""
    result = cal_acc.get_eval_result([llm_response], [gt_answer], ["_"])
    correct = int(round(result["accuracy"]))
    extracted = int(bool(llm_response) and cal_acc.get_format_answer(llm_response) is not None)
    return correct, extracted


def first_answer_text(llm_response: str | None) -> str:
    """Raw text of the first <<<...>>> block (for error diagnostics), truncated."""
    if not llm_response:
        return ""
    match = re.search(r"<<<(.*?)>>>", llm_response, flags=re.S)
    return match.group(1)[:200] if match else ""


def load_energy(model: str, fmt: str) -> dict[str, dict] | None:
    matches = glob.glob(str(OUTPUT_PROCESSED_DIR / f"energy_{model}_{fmt}_with_step_*.jsonl"))
    if not matches:
        return None
    records: dict[str, dict] = {}
    with open(matches[0], "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                records[rec["problem_id"]] = rec
    return records


def main() -> None:
    rows: list[dict] = []
    for model in MODELS:
        for fmt in FORMATS:
            responses_file = OUTPUT_PROCESSED_DIR / f"LLMresponses_{model}_woFineTuning_woCoT_{fmt}_with_step.jsonl"
            energy = load_energy(model, fmt)
            if not responses_file.exists() or energy is None:
                print(f"skip: {model}/{fmt} missing combined responses and/or energy file")
                continue
            with open(responses_file, "r", encoding="utf-8") as f:
                responses = json.load(f)

            missing_energy = set(responses) - set(energy)
            if missing_energy:
                print(f"WARNING: {model}/{fmt}: {len(missing_energy)} response(s) without an energy record")
            if len(responses) != EXPECTED_INSTANCES:
                print(f"WARNING: {model}/{fmt}: {len(responses)} responses, expected {EXPECTED_INSTANCES}")

            for pid, info in responses.items():
                correct, extracted = score_instance(info["llm_response"], info["gt_answer"])
                e = energy.get(pid, {})
                rows.append({
                    "model": model,
                    "format": fmt,
                    "problem_id": pid,
                    "task_id": info["task_id"],
                    "type_id": info["type_id"],
                    "granularity": int(info["task_id"].split("_")[1]),
                    "correct": correct,
                    "extracted": extracted,
                    "answer_text": first_answer_text(info["llm_response"]),
                    "gt_answer": str(info["gt_answer"])[:200],
                    "tokens_input": e.get("tokens_input"),
                    "tokens_output": e.get("tokens_output"),
                    "time_s": e.get("time_total_s"),
                    "energy_marginal_j": e.get("energy_marginal_j"),
                    "energy_total_j": e.get("energy_total_j"),
                    "idle_power_w": e.get("idle_power_w"),
                    "avg_power_w": e.get("avg_power_w"),
                })
            print(f"included: {model} / {fmt} ({len(responses)} instances)")

    if not rows:
        print("no model/format combo with both responses and energy found")
        return

    df = pd.DataFrame(rows)

    # Cross-check: instance-level accuracy must reproduce directPrompting_3_cal_accuracy_all.py's global accuracy exactly.
    for (model, fmt), acc in df.groupby(["model", "format"]).correct.mean().items():
        global_file = OUTPUT_PROCESSED_DIR / "accuracy" / f"{model}_{fmt}" / "global_level_eval_results.json"
        if global_file.exists():
            with open(global_file, "r", encoding="utf-8") as f:
                ref = json.load(f)["global"]["accuracy"]
            if abs(ref - acc) > 1e-9:
                raise ValueError(f"{model}/{fmt}: instance-level accuracy {acc:.6f} != 3_cal_accuracy_all {ref:.6f}")
    print("cross-check vs directPrompting_3_cal_accuracy_all.py: OK (where available)")

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, compression="gzip")
    print(f"\nSaved {len(df)} instance rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
