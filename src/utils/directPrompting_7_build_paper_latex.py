r"""
directPrompting_7_build_paper_latex.py

Builds paste-ready LaTeX material for the Results section: tables go to
output_processed/tables/, figure environments go next to the figure PDFs
in output_processed/figures/. The script does NOT touch the paper
itself; to update the paper, copy these two folders into the paper
project as tables/ and figures/ (the paper uses \input{tables/...},
\input{figures/...} and \includegraphics{figures/...}).
Each artefact answers one question:

  RQ1_accuracy_table.tex     (Table)  Overall accuracy per model and format
                             (highest per model in bold).
  RQ1_granularity_table.tex  (Table)  The same, per task granularity.
  RQ1_example_listing.tex    (Figure, in figures/) One real Task 3.18 instance in JSON and CSV
                             with the model's answers (wrong-attribute example); its
                             problem_id is saved in analysis/RQ1_example_instance.csv.
  RQ2_energy_table.tex       (Table)  Mean energy per instance per model and format,
                             with the change vs. JSON (lowest per model in bold).
  RQ2_tokens_table.tex       (Table)  Mean input and output tokens, same layout.

In the paper:
    \input{tables/RQ1_accuracy_table}
    \input{figures/RQ1_example_listing}   etc.

Requires booktabs, multirow and listings (all already loaded in main.tex).

Usage:
    python directPrompting_7_build_paper_latex.py
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from paper_labels import FORMAT_LABELS, MODEL_LABELS, single_column_table  # noqa: E402
from utils_config import FORMATS, MODELS  # noqa: E402

REPO_DIR = SCRIPT_DIR.parent.parent
ANALYSIS_DIR = REPO_DIR / "output_processed" / "analysis"
FIG_DIR = REPO_DIR / "output_processed" / "figures"     # figure environments
TABLE_DIR = REPO_DIR / "output_processed" / "tables"    # table .tex files

def write(name: str, lines: list[str], folder: Path = TABLE_DIR) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    if folder == TABLE_DIR:  # result tables use the one-column layout of the paper
        lines = single_column_table(lines)
    (folder / f"{name}.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {folder / name}.tex")


def acc_block(acc: pd.DataFrame, scope: str, models: list[str]) -> list[str]:
    """Rows 'Format & acc & acc ...' for one scope; highest accuracy per model in bold."""
    sub = acc[acc.scope == scope].set_index(["model", "format"]).accuracy.round(3)
    fmts = [f for f in FORMATS if f in set(sub.index.get_level_values(1))]
    best = {m: sub[m].max() for m in models}
    rows = []
    for f in fmts:
        cells = []
        for m in models:
            v = sub.get((m, f))
            cells.append("" if v is None else (f"\\textbf{{{v:.3f}}}" if v == best[m] else f"{v:.3f}"))
        rows.append(f"{FORMAT_LABELS[f]} & " + " & ".join(cells) + " \\\\")
    return rows


def acc_change_block(acc: pd.DataFrame, scope: str, models: list[str]) -> list[str]:
    """Like acc_block, but each non-JSON cell also shows the change with respect to JSON in percentage
    points, in parentheses (same layout as the RQ2 tables). Highest accuracy per model in bold."""
    sub = acc[acc.scope == scope].set_index(["model", "format"]).accuracy
    fmts = [f for f in FORMATS if f in set(sub.index.get_level_values(1))]
    best = {m: sub[m].round(3).max() for m in models}
    rows = []
    for f in fmts:
        cells = []
        for m in models:
            v = sub.get((m, f))
            if v is None:
                cells.append("")
                continue
            num = f"{v:.3f}"
            if round(v, 3) == best[m]:
                num = f"\\textbf{{{num}}}"
            base = sub.get((m, "JSON"))
            if f != "JSON" and base is not None:
                d = round((v - base) * 100, 1)
                num += f" (${d:+.1f}$)"
            cells.append(num)
        rows.append(f"{FORMAT_LABELS[f]} & " + " & ".join(cells) + " \\\\")
    return rows


def rq1_accuracy_table(acc: pd.DataFrame) -> None:
    """Overall accuracy: one row per format, one column per model; highest value per model in bold."""
    models = [m for m in MODELS if m in set(acc.model)]
    lines = ["\\begin{table}[t]", "\\centering",
             "\\caption{Overall accuracy of trace data formats, with changes relative to JSON in percentage points.}",
             "\\label{tab:rq1_accuracy}",
             "\\begin{tabular}{l" + "c" * len(models) + "}", "\\toprule",
             "Format & " + " & ".join(MODEL_LABELS[m] for m in models) + " \\\\", "\\midrule",
             *acc_change_block(acc, "Overall", models),
             "\\bottomrule", "\\end{tabular}", "\\end{table}"]
    write("RQ1_accuracy_table", lines)


def rq1_granularity_table(acc: pd.DataFrame) -> None:
    """The RQ1 accuracy table repeated in one block per task granularity; highest value per model and block in bold."""
    models = [m for m in MODELS if m in set(acc.model)]
    lines = ["\\begin{table}[t]", "\\centering",
             "\\caption{Accuracy of trace data formats by task granularity, with changes relative to JSON in percentage points.}",
             "\\label{tab:rq1_granularity}",
             "\\begin{tabular}{l" + "c" * len(models) + "}", "\\toprule",
             "Format & " + " & ".join(MODEL_LABELS[m] for m in models) + " \\\\"]
    for scope, name in [("SN", "Single-node"), ("NP", "Node-pair"), ("ST", "Single-trace"), ("TP", "Trace-pair")]:
        sub = acc[acc.scope == scope]
        if sub.empty:
            continue
        lines += ["\\midrule",
                  f"\\multicolumn{{{len(models) + 1}}}{{l}}{{\\textit{{{name} ({sub.tasks.iloc[0]} tasks, "
                  f"{sub.instances.iloc[0]:,} instances)}}}} \\\\",
                  *acc_change_block(acc, scope, models)]
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    write("RQ1_granularity_table", lines)


# RQ1 example listing: a Task 3.18 instance ("which database is accessed most frequently") that the model
# answers correctly with JSON and with the value of the neighbouring db.system attribute with CSV and TOON.
EXAMPLE_TASK = "Task_3_18"
EXAMPLE_MODEL = "Llama-3.1-8B-Instruct"
EXAMPLE_FORMAT = "CSV"
DATASET_DIR = REPO_DIR / "dataset" / "TraceBench" / "test" / "preprocessed"
DB_SYSTEM = re.compile(r"mysql|redis|mongo|postgres", re.I)
KEEP = 4  # attributes shown at the start and at the end of each span; the middle ones are elided


def rq1_example_listing() -> None:
    """Selects the shortest qualifying instance deterministically and writes it as a two-column listing."""
    inst_file = ANALYSIS_DIR / "instance_level.csv.gz"
    files = {f: DATASET_DIR / f"test_tasks_preprocessed_{f}_with_step.json" for f in ("JSON", EXAMPLE_FORMAT)}
    if not inst_file.exists() or not all(p.exists() for p in files.values()):
        print("skip: example listing needs instance_level.csv.gz and the preprocessed JSON/CSV datasets")
        return
    d = pd.read_csv(inst_file)
    d = d[(d.task_id == EXAMPLE_TASK) & (d.model == EXAMPLE_MODEL)]
    ok = d[d.format == "JSON"].set_index("problem_id").correct == 1
    wrong = {f: d[d.format == f].set_index("problem_id") for f in (EXAMPLE_FORMAT, "TOON")}
    cand = [pid for pid in ok[ok].index
            if all(pid in w.index and w.loc[pid, "correct"] == 0 and DB_SYSTEM.search(str(w.loc[pid, "answer_text"]))
                   for w in wrong.values())]
    if not cand:
        print("skip: no qualifying example instance")
        return
    data = {}
    for f, path in files.items():
        with open(path, "r", encoding="utf-8") as fh:
            data[f] = {x["problem_id"]: x for x in json.load(fh) if x["problem_id"] in set(cand)}
    pid = min(cand, key=lambda p: (len(data[EXAMPLE_FORMAT][p]["input"]), p))
    gt = data["JSON"][pid]["answer"]
    ans = {f: d[(d.format == f) & (d.problem_id == pid)].answer_text.iloc[0] for f in ("JSON", EXAMPLE_FORMAT)}

    # JSON: the database span, first and last KEEP attributes
    spans = ast.literal_eval(data["JSON"][pid]["input"].split("Input Trace: ", 1)[1].strip())
    db_span = next(sp for sp in spans if "db.name" in sp)
    items = [f"'{k}': '{v}'" for k, v in db_span.items()]
    json_line = "{" + ", ".join(items[:KEEP]) + ", ..., " + ", ".join(items[-KEEP:]) + "}"
    # CSV: complete trace (header and every span), first and last KEEP columns
    rows = data[EXAMPLE_FORMAT][pid]["input"].split("Input Trace: ", 1)[1].strip().splitlines()
    cut = lambda r: ",".join(r.split(",")[:KEEP]) + ",...," + ",".join(r.split(",")[-KEEP:])
    csv_lines = [cut(r) for r in rows]

    model = MODEL_LABELS[EXAMPLE_MODEL]
    lines = ["\\begin{figure*}[t]", "\\centering",
             f"% problem_id: {pid} ({EXAMPLE_TASK}, ground truth {gt})",
             "\\begin{lstlisting}[basicstyle=\\ttfamily\\footnotesize, frame=single, breaklines=true, upquote=true]",
             "(a) JSON -- database span:", json_line,
             f"{model} answer: {ans['JSON']}   (correct)", "",
             f"(b) {FORMAT_LABELS[EXAMPLE_FORMAT]} -- complete trace (header and both spans):", *csv_lines,
             f"{model} answer: {ans[EXAMPLE_FORMAT]}   (incorrect)",
             "\\end{lstlisting}",
             f"\\caption{{RQ1: The same trace in JSON and {FORMAT_LABELS[EXAMPLE_FORMAT]} for Task 3.18, "
             f"``Which database is accessed most frequently in the Input Trace?'' (correct answer \\texttt{{ts}}), "
             f"with the answers of {model}. Part (a) shows the span that accesses the database, part (b) the "
             f"complete trace. Middle attributes are elided (\\texttt{{...}}).}}",
             "\\label{fig:rq1_example}", "\\end{figure*}"]
    write("RQ1_example_listing", lines, folder=FIG_DIR)
    # The same instance is the motivating example of the introduction (pot_2_statistics.py, pot_3_build_paper_latex.py).
    pd.DataFrame([{"problem_id": pid, "task_id": EXAMPLE_TASK}]).to_csv(ANALYSIS_DIR / "RQ1_example_instance.csv", index=False)


def mean_change_cell(mean: float, change: float | None) -> str:
    """'1,302 (-8.3\\%)'; JSON (change None) shows the mean only."""
    if change is None or pd.isna(change):
        return f"{mean:,.0f}"
    return f"{mean:,.0f} (${change * 100:+.1f}$\\%)"


def mean_change_rows(ov: pd.DataFrame, models: list[str], mean_col: str, change_col: str,
                     bold_lowest: bool) -> list[str]:
    """Rows 'Format & mean (change) & ...'; optionally the lowest mean per model in bold."""
    fmts = [f for f in FORMATS if f in set(ov.format)]
    lowest = {m: ov[ov.model == m][mean_col].round(0).min() for m in models}
    rows = []
    for f in fmts:
        cells = []
        for m in models:
            r = ov[(ov.model == m) & (ov.format == f)]
            if r.empty:
                cells.append("--")
                continue
            r = r.iloc[0]
            cell = mean_change_cell(r[mean_col], r.get(change_col))
            if bold_lowest and round(r[mean_col]) == lowest[m]:
                num, _, rest = cell.partition(" ")
                cell = f"\\textbf{{{num}}}" + (f" {rest}" if rest else "")
            cells.append(cell)
        rows.append(f"{FORMAT_LABELS[f]} & " + " & ".join(cells) + " \\\\")
    return rows


def rq2_energy_table(ov: pd.DataFrame) -> None:
    """Mean marginal GPU energy per instance: one row per format, one column per model; lowest per model in bold."""
    models = [m for m in MODELS if m in set(ov.model)]
    lines = ["\\begin{table*}[t]", "\\centering",
             "\\caption{Mean GPU energy consumption per instance (J) and percentage changes relative to JSON.}",
             "\\label{tab:rq2_energy}",
             "\\begin{tabular}{l" + "r" * len(models) + "}", "\\toprule",
             "Format & " + " & ".join(MODEL_LABELS[m] for m in models) + " \\\\", "\\midrule",
             *mean_change_rows(ov, models, "energy_mean_j", "d_energy", bold_lowest=True),
             "\\bottomrule", "\\end{tabular}", "\\end{table*}"]
    write("RQ2_energy_table", lines)


def rq2_tokens_table(ov: pd.DataFrame) -> None:
    """Mean input and output tokens per instance, one block each, same layout as the energy table;
    lowest per model in bold, separately for input and output."""
    models = [m for m in MODELS if m in set(ov.model)]
    ncol = len(models) + 1
    lines = ["\\begin{table*}[t]", "\\centering",
             "\\caption{Mean input and output tokens per instance for each trace data format, with changes relative to JSON in percentages.}",
             "\\label{tab:rq2_tokens}",
             "\\begin{tabular}{l" + "r" * len(models) + "}", "\\toprule",
             "Format & " + " & ".join(MODEL_LABELS[m] for m in models) + " \\\\"]
    for title, mean_col, change_col in [("Input tokens", "tokens_in_mean", "d_tokens_in"),
                                        ("Output tokens", "tokens_out_mean", "d_tokens_out")]:
        lines += ["\\midrule", f"\\multicolumn{{{ncol}}}{{l}}{{\\textit{{{title}}}}} \\\\",
                  *mean_change_rows(ov, models, mean_col, change_col, bold_lowest=True)]
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table*}"]
    write("RQ2_tokens_table", lines)


def main() -> None:
    need = ["RQ1_accuracy.csv", "RQ2_energy.csv"]
    if any(not (ANALYSIS_DIR / n).exists() for n in need):
        print("skip: run directPrompting_5_rq1_statistics.py and directPrompting_6_rq2_statistics.py first")
        return
    acc = pd.read_csv(ANALYSIS_DIR / "RQ1_accuracy.csv")
    rq1_accuracy_table(acc)
    rq1_granularity_table(acc)
    rq1_example_listing()
    ov = pd.read_csv(ANALYSIS_DIR / "RQ2_energy.csv")
    rq2_energy_table(ov)
    rq2_tokens_table(ov)


if __name__ == "__main__":
    main()
