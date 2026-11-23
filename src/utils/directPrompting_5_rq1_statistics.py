"""
directPrompting_5_rq1_statistics.py

RQ1 (Effectiveness of Trace Data Format): the numbers used in the paper,
from output_processed/analysis/instance_level.csv.gz (directPrompting_4_build_instance_table.py).

Writes (under output_processed/analysis/):
  RQ1_accuracy.csv
      Accuracy per model, format and scope (Overall and each task
      granularity: SN single-node, NP node-pair, ST single-trace,
      TP trace-pair), with the number of tasks and instances per scope.
  RQ1_wrong_attribute_task_3_18.csv
      Task 3.18 ("which database is accessed most frequently"): per model
      and format, the number of answers that report a database system
      (mysql, redis, ...; the db.system attribute) instead of the database
      name (the db.name attribute).
  RQ1_trace_pair_tasks.csv
      Accuracy (%) per trace-pair task (4.1 to 4.10) and format, pooled over
      the LLMs, with the mean over the tasks in the last row.
  TTV_output_limit.csv
      Threats to validity: per model and format, the number of outputs that
      reached the output limit (max_new_tokens in config.yaml), and how many
      of these contain no extracted final answer and are therefore counted
      as incorrect, with their share of all instances in percent.

Usage:
    python directPrompting_5_rq1_statistics.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from utils_config import FORMATS, MODELS  # noqa: E402

ANALYSIS_DIR = SCRIPT_DIR.parent.parent / "output_processed" / "analysis"
INPUT_FILE = ANALYSIS_DIR / "instance_level.csv.gz"

GRANULARITY = {1: "SN", 2: "NP", 3: "ST", 4: "TP"}
DB_SYSTEM = re.compile(r"mysql|redis|mongo|postgres", re.I)
OUTPUT_LIMIT = 2000  # max_new_tokens of the direct-prompting runs (config.yaml)


def trace_pair_tasks(df: pd.DataFrame) -> pd.DataFrame:
    """Accuracy (%) per trace-pair task and format, pooled over the LLMs, plus the mean over the tasks."""
    tp = df[df.granularity == 4]
    acc = tp.pivot_table(index="task_id", columns="format", values="correct", aggfunc="mean") * 100
    acc = acc.reindex(columns=FORMATS)
    acc = acc.loc[sorted(acc.index, key=lambda t: int(t.split("_")[-1]))]
    acc.loc["Mean over tasks"] = acc.mean()
    return acc.round(1).reset_index()


def output_limit(df: pd.DataFrame) -> pd.DataFrame:
    """Outputs that reached the output limit, and those among them without an extracted final answer."""
    t = df.copy()
    t["reached_limit"] = t.tokens_output >= OUTPUT_LIMIT
    t["reached_limit_no_answer"] = t.reached_limit & (t.extracted == 0)
    out = t.groupby(["model", "format"], sort=False).agg(
        instances=("correct", "size"), reached_limit=("reached_limit", "sum"),
        reached_limit_no_answer=("reached_limit_no_answer", "sum")).reset_index()
    out["share_no_answer_pct"] = (out.reached_limit_no_answer / out.instances * 100).round(2)
    return out


def main() -> None:
    if not INPUT_FILE.exists():
        print(f"skip: {INPUT_FILE} not found (run directPrompting_4_build_instance_table.py first)")
        return
    df = pd.read_csv(INPUT_FILE)
    df = df[df.model.isin(MODELS) & df.format.isin(FORMATS)]

    rows = []
    for scope, sub in [("Overall", df)] + [(name, df[df.granularity == g]) for g, name in GRANULARITY.items()]:
        for (model, fmt), grp in sub.groupby(["model", "format"]):
            rows.append({"model": model, "format": fmt, "scope": scope,
                         "tasks": grp.task_id.nunique(), "instances": len(grp), "accuracy": grp.correct.mean()})
    acc = pd.DataFrame(rows)
    acc.to_csv(ANALYSIS_DIR / "RQ1_accuracy.csv", index=False)

    t = df[df.task_id == "Task_3_18"].copy()
    t["wrong_attribute"] = (t.answer_text.fillna("").str.contains(DB_SYSTEM)
                            & ~t.gt_answer.fillna("").str.contains(DB_SYSTEM))
    wa = t.groupby(["model", "format"]).agg(instances=("correct", "size"), accuracy=("correct", "mean"),
                                            wrong_attribute_answers=("wrong_attribute", "sum")).reset_index()
    wa.to_csv(ANALYSIS_DIR / "RQ1_wrong_attribute_task_3_18.csv", index=False)

    tpt = trace_pair_tasks(df)
    tpt.to_csv(ANALYSIS_DIR / "RQ1_trace_pair_tasks.csv", index=False)

    lim = output_limit(df)
    lim.to_csv(ANALYSIS_DIR / "TTV_output_limit.csv", index=False)

    pd.set_option("display.width", 200)
    print(acc[acc.scope == "Overall"].pivot(index="format", columns="model", values="accuracy").round(3))
    print(wa.pivot(index="format", columns="model", values="wrong_attribute_answers"))
    print(tpt.to_string(index=False))
    print(lim.pivot(index="format", columns="model", values="share_no_answer_pct"))
    print(f"\nSaved RQ1 numbers to {ANALYSIS_DIR}")


if __name__ == "__main__":
    main()
