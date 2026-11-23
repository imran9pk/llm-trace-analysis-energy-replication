r"""
pot_3_build_paper_latex.py

Paste-ready LaTeX tables for RQ3/RQ4 (task-level program generation), from
the CSVs of pot_2_statistics.py. Written to output_processed/tables/
(copy into the paper project's tables/ folder, like the RQ1/RQ2 tables).

  RQ3_pot_accuracy_table.tex  Accuracy of direct prompting (JSON) vs PoT with
                              zero and POT_FEWSHOT examples, with failed executions.
  RQ4_pot_energy_table.tex    GPU energy of direct prompting (9,120 calls) vs
                              PoT generation (38 calls), and execution time.

Models whose PoT run is missing or incomplete are shown with "--".

Usage:
    python pot_3_build_paper_latex.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from paper_labels import MODEL_LABELS, single_column_table  # noqa: E402
from utils_config import MODELS, POT_FEWSHOT  # noqa: E402

REPO_DIR = SCRIPT_DIR.parent.parent
ANALYSIS_DIR = REPO_DIR / "output_processed" / "analysis"
TABLE_DIR = REPO_DIR / "output_processed" / "tables"
FIG_DIR = REPO_DIR / "output_processed" / "figures"
DATASET_DIR = REPO_DIR / "dataset" / "TraceBench" / "test" / "preprocessed"
GEN_DIR = REPO_DIR / "output" / "generated_scripts"
SHOT_WORDS = {"zeroshot": 0, "oneshot": 1, "twoshot": 2, "threeshot": 3, "fourshot": 4, "fiveshot": 5}
N_SHOT = SHOT_WORDS[POT_FEWSHOT]
NUMBER_WORDS = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}  # numbers in running text


def cell(value, fmt: str) -> str:
    return "--" if pd.isna(value) else format(value, fmt)


def write(name: str, lines: list[str], folder: Path = TABLE_DIR) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    if folder == TABLE_DIR:  # result tables use the one-column layout of the paper
        lines = single_column_table(lines)
    (folder / f"{name}.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {folder / name}.tex")


def rq3_table(acc: pd.DataFrame) -> None:
    """Rows: strategies, laid out as in the RQ4 table (direct prompting, then one block per PoT variant with
    its accuracy and share of failed instances); columns: LLMs.
    Bold: highest accuracy per model (over the three strategies) and lowest failed share per model (PoT)."""
    few = NUMBER_WORDS[N_SHOT]
    rows = {m: acc[acc.model == m].iloc[0] for m in MODELS}
    acc_cols = ["direct_json_accuracy", "pot_zeroshot_accuracy", "pot_fewshot_accuracy"]
    fail_cols = ["pot_zeroshot_failed_share", "pot_fewshot_failed_share"]
    best = {m: max(round(rows[m][c], 3) for c in acc_cols if not pd.isna(rows[m][c])) for m in MODELS}
    fewest = {m: min(round(100 * rows[m][c], 1) for c in fail_cols if not pd.isna(rows[m][c])) for m in MODELS}
    def accuracy(m, c):
        """Accuracy to three decimals (bold if best); for program generation, the change with respect to
        direct prompting in percentage points, computed from the unrounded accuracies."""
        v = rows[m][c]
        if pd.isna(v):
            return "--"
        num = f"{v:.3f}"
        if round(v, 3) == best[m]:
            num = f"\\textbf{{{num}}}"
        if c != "direct_json_accuracy" and not pd.isna(rows[m]["direct_json_accuracy"]):
            num += f" (${(v - rows[m]['direct_json_accuracy']) * 100:+.1f}$)"
        return num
    failed = lambda m, c: ("--" if pd.isna(rows[m][c]) else f"\\textbf{{{100 * rows[m][c]:.1f}\\%}}"
                           if round(100 * rows[m][c], 1) == fewest[m] else f"{100 * rows[m][c]:.1f}\\%")
    ncol = len(MODELS) + 1
    lines = ["\\begin{table*}[t]", "\\centering",
             f"\\caption{{Accuracy of direct prompting with JSON and of task-level program generation, with changes relative "
             f"to direct prompting in percentage points computed from unrounded accuracies. Failed instances "
             f"(errors and timeouts) count as incorrect.}}",
             "\\label{tab:rq3_pot_accuracy}",
             "\\begin{tabular}{l" + "r" * len(MODELS) + "}", "\\toprule",
             " & " + " & ".join(MODEL_LABELS[m] for m in MODELS) + " \\\\", "\\midrule",
             "Direct prompting & " + " & ".join(accuracy(m, "direct_json_accuracy") for m in MODELS) + " \\\\"]
    for key, label in [("zeroshot", "Program generation zero-shot"), ("fewshot", f"Program generation {few}-shot")]:
        lines += ["\\midrule", f"\\multicolumn{{{ncol}}}{{l}}{{\\textit{{{label}}}}} \\\\",
                  "\\quad Accuracy & " + " & ".join(accuracy(m, f"pot_{key}_accuracy") for m in MODELS) + " \\\\",
                  "\\quad Failed instances & " + " & ".join(failed(m, f"pot_{key}_failed_share") for m in MODELS) + " \\\\"]
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table*}"]
    write("RQ3_pot_accuracy_table", lines)


def rq4_table(en: pd.DataFrame) -> None:
    """Rows: strategies, as in the RQ3 table; columns: LLMs. Energy (J) to answer the test set once:
    direct prompting = GPU energy of all calls; PoT = GPU energy of generating the programs plus
    CPU energy of executing them once on the test set. Bold: lowest total per model."""
    few = NUMBER_WORDS[N_SHOT]
    rows = {m: en[en.model == m].iloc[0] for m in MODELS}
    total = lambda gen, ex: gen + ex if not (pd.isna(gen) or pd.isna(ex)) else float("nan")
    totals = {m: {"direct": rows[m].direct_json_energy_j,
                  "zeroshot": total(rows[m].pot_zeroshot_gen_energy_j, rows[m].get("pot_zeroshot_exec_energy_j")),
                  "fewshot": total(rows[m].pot_fewshot_gen_energy_j, rows[m].get("pot_fewshot_exec_energy_j"))}
              for m in MODELS}
    lowest = {m: min(round(v) for v in totals[m].values() if not pd.isna(v)) for m in MODELS}
    joules = lambda v: "--" if pd.isna(v) else f"{v:,.0f}"
    bold_total = lambda m, key: ("--" if pd.isna(totals[m][key]) else
                                 f"\\textbf{{{totals[m][key]:,.0f}}}" if round(totals[m][key]) == lowest[m]
                                 else joules(totals[m][key]))
    missing = any(pd.isna(v) for m in MODELS for v in totals[m].values())
    ncol = len(MODELS) + 1
    lines = ["\\begin{table*}[t]", "\\centering",
             f"\\caption{{Energy (J) to analyze the 9,120 test instances with direct prompting and with task-level "
             f"program generation. For program generation, the total is the GPU energy of the 38 generation calls "
             f"plus the CPU energy of executing the programs."
             + (" --: run not yet complete." if missing else "") + "}",
             "\\label{tab:rq4_pot_energy}",
             "\\begin{tabular}{l" + "r" * len(MODELS) + "}", "\\toprule",
             " & " + " & ".join(MODEL_LABELS[m] for m in MODELS) + " \\\\", "\\midrule",
             "Direct prompting & " + " & ".join(bold_total(m, "direct") for m in MODELS) + " \\\\"]
    for key, label in [("zeroshot", "Program generation zero-shot"), ("fewshot", f"Program generation {few}-shot")]:
        lines += ["\\midrule", f"\\multicolumn{{{ncol}}}{{l}}{{\\textit{{{label}}}}} \\\\",
                  "\\quad Generation (GPU) & " + " & ".join(joules(rows[m][f"pot_{key}_gen_energy_j"]) for m in MODELS) + " \\\\",
                  "\\quad Execution (CPU) & " + " & ".join(cell(rows[m].get(f"pot_{key}_exec_energy_j"), ",.2f") for m in MODELS) + " \\\\",
                  "\\quad Total & " + " & ".join(bold_total(m, key) for m in MODELS) + " \\\\"]
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table*}"]
    write("RQ4_pot_energy_table", lines)


def main() -> None:
    acc_f, en_f = ANALYSIS_DIR / "RQ3_pot_accuracy.csv", ANALYSIS_DIR / "RQ4_pot_energy.csv"
    if not acc_f.exists() or not en_f.exists():
        print("skip: run pot_2_statistics.py first")
        return
    rq3_table(pd.read_csv(acc_f))
    rq4_table(pd.read_csv(en_f))


if __name__ == "__main__":
    main()
