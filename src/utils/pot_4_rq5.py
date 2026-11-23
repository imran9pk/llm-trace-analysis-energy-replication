r"""
pot_4_rq5.py

RQ5 (effectiveness-efficiency trade-offs), from the CSVs of
directPrompting_5/6 (RQ1, RQ2) and pot_2_statistics.py (RQ3, RQ4).

Pareto dominance: option A dominates option B (same LLM) if A is at least as
accurate and consumes at most as much energy as B, and is better in at least
one of the two. Options that no other option dominates are Pareto-optimal.
Two analyses per LLM:
  formats      the five formats under direct prompting, by accuracy and mean
               GPU energy per instance (RQ1, RQ2);
  all options  the five formats and PoT with zero and POT_FEWSHOT examples,
               by accuracy and total energy to analyze the test set (RQ1-RQ4).

Writes:
  output_processed/analysis/RQ5_pareto.csv        every option, with both Pareto flags
  output_processed/figures/RQ5_formats.pdf        formats and PoT vs JSON, one column (panels stacked, one per LLM)
  output_processed/figures/RQ5_formats_figure.tex its figure environment (figure, \\columnwidth) with the caption
  output_processed/figures/RQ5_formats_wide.pdf   the same plot, full width (panels side by side)
  output_processed/figures/RQ5_formats_wide_figure.tex its figure environment (figure*, \\textwidth)
  output_processed/tables/RQ5_pareto_table.tex     number of LLMs for which each option is Pareto-optimal

Usage:
    python pot_4_rq5.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from paper_labels import FORMAT_LABELS, MODEL_LABELS  # noqa: E402
from utils_config import FORMATS, MODELS, POT_FEWSHOT  # noqa: E402

REPO_DIR = SCRIPT_DIR.parent.parent
ANALYSIS_DIR = REPO_DIR / "output_processed" / "analysis"
TABLE_DIR = REPO_DIR / "output_processed" / "tables"
FIG_DIR = REPO_DIR / "output_processed" / "figures"
BASELINE = "JSON"
NUMBER_WORDS = {"zeroshot": "zero", "oneshot": "one", "twoshot": "two", "threeshot": "three",
                "fourshot": "four", "fiveshot": "five"}
FEW = NUMBER_WORDS[POT_FEWSHOT]
NUMBER_TEXT = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
SHOT_DIGITS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}

# One colour per compact format (validated categorical palette, colour-blind safe);
# the format name is also printed next to each dot.
FORMAT_COLORS = {"MARKDOWN": "#2a78d6", "TRON": "#eb6834", "TOON": "#1baf7a", "CSV": "#eda100"}
# Label position (offset in points, alignment) where the default (right of the dot) would overlap.
LABEL_OFFSETS = {
    ("Qwen3-8B", "TOON"): (0, 6, "center"), ("Qwen3-8B", "TRON"): (4, -3, "left"),
    ("Qwen3-8B", "CSV"): (-4, -3, "right"), ("Qwen3-8B", "MARKDOWN"): (-4, 2, "right"),
    ("Llama-3.1-8B-Instruct", "MARKDOWN"): (4, 3, "left"), ("Llama-3.1-8B-Instruct", "TOON"): (-4, -3, "right"),
    ("Llama-3.1-8B-Instruct", "CSV"): (4, 2, "left"), ("Llama-3.1-8B-Instruct", "TRON"): (4, -3, "left"),
    ("Ministral-8B-Instruct-2410", "TRON"): (-4, 2, "right"), ("Ministral-8B-Instruct-2410", "CSV"): (4, 3, "left"),
    ("Ministral-8B-Instruct-2410", "TOON"): (4, -4, "left"), ("Ministral-8B-Instruct-2410", "MARKDOWN"): (0, 6, "center"),
    ("DeepSeek-R1-Distill-Llama-8B", "MARKDOWN"): (-4, 0, "right"), ("DeepSeek-R1-Distill-Llama-8B", "CSV"): (4, 0, "left"),
}
LABEL_OFFSETS_WIDE = {  # full-width layout: positions that differ from the one-column layout
    ("Qwen3-8B", "TOON"): (-4, -1, "right"), ("Qwen3-8B", "MARKDOWN"): (0, 6, "center"),
}


def pareto_optimal(accuracy: pd.Series, energy: pd.Series) -> list[bool]:
    """True for the options that no other option dominates (higher accuracy, lower energy)."""
    flags = []
    for i in accuracy.index:
        dominated = ((accuracy >= accuracy[i]) & (energy <= energy[i])
                     & ((accuracy > accuracy[i]) | (energy < energy[i]))).any()
        flags.append(not dominated)
    return flags


def load_options() -> pd.DataFrame:
    """One row per LLM and option: accuracy, mean energy per instance, total energy for the test set."""
    acc = pd.read_csv(ANALYSIS_DIR / "RQ1_accuracy.csv")
    acc = acc[acc.scope == "Overall"][["model", "format", "accuracy"]]
    energy = pd.read_csv(ANALYSIS_DIR / "RQ2_energy.csv")[["model", "format", "energy_mean_j", "energy_total_j"]]
    direct = acc.merge(energy, on=["model", "format"]).rename(columns={"format": "option"})
    pot_acc = pd.read_csv(ANALYSIS_DIR / "RQ3_pot_accuracy.csv").set_index("model")
    pot_en = pd.read_csv(ANALYSIS_DIR / "RQ4_pot_energy.csv").set_index("model")
    rows = []
    for model in MODELS:
        for key, option in [("zeroshot", "PoT zero-shot"), ("fewshot", f"PoT {FEW}-shot")]:
            rows.append({"model": model, "option": option,
                         "accuracy": pot_acc.loc[model, f"pot_{key}_accuracy"],
                         "energy_total_j": pot_en.loc[model, f"pot_{key}_gen_energy_j"]
                         + pot_en.loc[model, f"pot_{key}_exec_energy_j"]})
    options = pd.concat([direct, pd.DataFrame(rows)], ignore_index=True)
    return options[options.model.isin(MODELS)]


def pareto_table(options: pd.DataFrame) -> pd.DataFrame:
    options = options.copy()
    options["pareto_formats"] = pd.NA
    options["pareto_all_options"] = False
    for model, group in options.groupby("model"):
        options.loc[group.index, "pareto_all_options"] = pareto_optimal(group.accuracy, group.energy_total_j)
        fmts = group[group.option.isin(FORMATS)]
        options.loc[fmts.index, "pareto_formats"] = pareto_optimal(fmts.accuracy, fmts.energy_mean_j)
    return options


def formats_figure(options: pd.DataFrame, layout: str = "column") -> None:
    """Per LLM: change of accuracy (pp) and of mean energy per instance (%) of every option against JSON.

    The five formats (direct prompting) and PoT with zero and POT_FEWSHOT examples. PoT energy is the energy of
    generating the programs and executing them, divided by the number of test instances. PoT lies near -100%,
    so each panel has a narrow left segment around -100% and a broken x axis. Filled markers are Pareto-optimal
    among all options of the LLM (pareto_all_options).
    """
    plt.rcParams.update({"font.family": "serif", "font.serif": ["STIXGeneral"], "mathtext.fontset": "stix",
                         "font.size": 8, "axes.linewidth": 0.6, "axes.edgecolor": "0.3", "xtick.color": "0.3",
                         "ytick.color": "0.3", "xtick.labelsize": 7, "ytick.labelsize": 7})
    pot_style = {"PoT zero-shot": ("^", "#8e5fd1", "PoT 0-shot"),
                 f"PoT {FEW}-shot": ("s", "#4b2a91", f"PoT {SHOT_DIGITS[FEW]}-shot")}
    opts = options.copy()
    n_instances = (opts[(opts.option == BASELINE)].energy_total_j / opts[(opts.option == BASELINE)].energy_mean_j).round().iloc[0]
    opts["mean_j"] = opts.energy_total_j / n_instances
    base = opts[opts.option == BASELINE].set_index("model")
    opts["d_acc"] = [100 * (r.accuracy - base.loc[r.model, "accuracy"]) for r in opts.itertuples()]
    opts["d_energy"] = [100 * (r.mean_j / base.loc[r.model, "mean_j"] - 1) for r in opts.itertuples()]
    opts["optimal"] = opts.pareto_all_options.astype(bool)
    ylim = (-23, 10)
    n_models = len(MODELS)
    wide = layout == "wide"
    if wide:  # full width, one panel per LLM side by side
        fig = plt.figure(figsize=(7.16, 2.9))
        outer = fig.add_gridspec(1, n_models, wspace=0.16, left=0.06, right=0.985, top=0.91, bottom=0.14)
    else:  # one column, one row per LLM
        fig = plt.figure(figsize=(3.4, 1.6 * n_models + 0.45))
        outer = fig.add_gridspec(n_models, 1, hspace=0.42, left=0.15, right=0.97, top=0.955, bottom=0.075)
    offsets = {**LABEL_OFFSETS, **(LABEL_OFFSETS_WIDE if wide else {})}

    def label(ax, x, y, text, model, option, dark):
        dx, dy, ha = offsets.get((model, option), (4, 0, "left"))
        ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=6.3, ha=ha, va="center",
                    color="0.15" if dark else "0.45", annotation_clip=False)

    for i, model in enumerate(MODELS):
        group = opts[opts.model == model]
        inner = outer[i].subgridspec(1, 2, width_ratios=[1, 3.2] if wide else [1, 3.6], wspace=0.06 if wide else 0.05)
        axl = fig.add_subplot(inner[0])
        axr = fig.add_subplot(inner[1], sharey=axl)
        axl.patch.set_alpha(0)
        axr.patch.set_alpha(0)
        # shaded: more accurate than JSON and less energy
        axl.fill_between([-100.2, -98.8], 0, ylim[1], color="#2a78d6", alpha=0.07, lw=0)
        axr.fill_between([-20, 0], 0, ylim[1], color="#2a78d6", alpha=0.07, lw=0)
        for ax in (axl, axr):
            ax.axhline(0, color="0.6", lw=0.5, zorder=1)
        axr.axvline(0, color="0.6", lw=0.5, zorder=1)
        for r in group[group.option.isin(FORMAT_COLORS)].itertuples():
            color = FORMAT_COLORS[r.option]
            axr.scatter(r.d_energy, r.d_acc, s=26, facecolors=color if r.optimal else "white", edgecolors=color,
                        linewidths=1.1, zorder=3)
            label(axr, r.d_energy, r.d_acc, FORMAT_LABELS[r.option], model, r.option, r.optimal)
        json_optimal = bool(group[group.option == BASELINE].optimal.iloc[0])
        axr.scatter(0, 0, s=24, marker="D", facecolors="0.15" if json_optimal else "white", edgecolors="0.15",
                    linewidths=1.0, zorder=4)
        axr.annotate(FORMAT_LABELS[BASELINE], (0, 0), xytext=(4, 4), textcoords="offset points", fontsize=6.3, color="0.15")
        for r in group[group.option.isin(pot_style)].itertuples():
            marker, color, text = pot_style[r.option]
            axl.scatter(r.d_energy, r.d_acc, s=26, marker=marker, facecolors=color if r.optimal else "white",
                        edgecolors=color, linewidths=1.1, zorder=3)
            label(axl, r.d_energy, r.d_acc, text, model, r.option, r.optimal)
        axl.set_xlim(-100.2, -98.8)
        axl.set_xticks([-100])
        axr.set_xlim(-20, 20)
        axr.set_xticks([-20, -10, 0, 10, 20])
        axl.set_ylim(*ylim)
        for ax in (axl, axr):
            ax.spines["top"].set_visible(False)
        axl.spines["right"].set_visible(False)
        axr.spines["left"].set_visible(False)
        axr.spines["right"].set_visible(False)
        axr.tick_params(axis="y", left=False, labelleft=False)
        if wide and i:  # y tick labels only on the first panel
            axl.tick_params(axis="y", labelleft=False)
        if not wide and i < n_models - 1:  # x tick labels only on the bottom row
            axl.tick_params(axis="x", labelbottom=False)
            axr.tick_params(axis="x", labelbottom=False)
        d = 0.02  # break marks on the x axis
        kw = dict(color="0.3", clip_on=False, lw=0.6)
        axl.plot([1 - d * 3, 1 + d * 3], [-d * 1.5, d * 1.5], transform=axl.transAxes, **kw)
        axr.plot([-d, d], [-d * 1.5, d * 1.5], transform=axr.transAxes, **kw)
        title_ax = fig.add_subplot(outer[i], frameon=False)
        title_ax.set_xticks([])
        title_ax.set_yticks([])
        title_ax.set_title(MODEL_LABELS[model], fontsize=8 if wide else 7.5, pad=6 if wide else 3)
    if wide:
        fig.text(0.008, 0.53, "Accuracy vs. JSON (pp)", rotation=90, va="center", fontsize=8)
        fig.text(0.53, 0.02, "Mean energy per instance vs. JSON (%)", ha="center", fontsize=8)
    else:
        fig.text(0.015, 0.5, "Accuracy vs. JSON (pp)", rotation=90, va="center", fontsize=8)
        fig.text(0.56, 0.012, "Mean energy per instance vs. JSON (%)", ha="center", fontsize=8)
    name = "RQ5_formats_wide" if wide else "RQ5_formats"
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{name}.pdf")
    plt.close(fig)
    caption = ("Changes in accuracy (percentage points) and mean energy consumption per instance (percent) relative to "
               "JSON. The x axis is broken.")
    env, width = ("figure*", "\\textwidth") if wide else ("figure", "\\columnwidth")
    # Both files use the same label: include only one of them in the paper.
    (FIG_DIR / f"{name}_figure.tex").write_text(
        "\n".join([f"\\begin{{{env}}}[t]", "\\centering", f"\\includegraphics[width={width}]{{figures/{name}.pdf}}",
                   f"\\caption{{{caption}}}", "\\label{fig:rq5_formats}", f"\\end{{{env}}}"]) + "\n", encoding="utf-8")
    print(f"wrote {FIG_DIR / (name + '.pdf')} and {name}_figure.tex")


def pareto_count_table(options: pd.DataFrame) -> None:
    """Number of LLMs for which each option is Pareto-optimal, among the formats and among all options."""
    order = list(FORMATS) + ["PoT zero-shot", f"PoT {FEW}-shot"]
    labels = {**{f: FORMAT_LABELS[f] for f in FORMATS}, "PoT zero-shot": "Program generation zero-shot", f"PoT {FEW}-shot": f"Program generation {FEW}-shot"}
    n = options.model.nunique()
    lines = ["\\begin{table}[t]", "\\centering",
             f"\\caption{{Number of LLMs, out of {NUMBER_TEXT.get(n, n)}, for which each option is Pareto-optimal among the five "
             "formats and among all seven options.}",
             "\\label{tab:rq5_pareto}",
             "\\begin{tabularx}{\\columnwidth}{lXX}", "\\toprule",
             "Option & Among formats & Among all options \\\\", "\\midrule"]
    for opt in order:
        group = options[options.option == opt]
        among_formats = int((group.pareto_formats == True).sum()) if opt in FORMATS else None  # noqa: E712
        among_all = int(group.pareto_all_options.astype(bool).sum())
        if opt == "PoT zero-shot":
            lines.append("\\midrule")
        lines.append(f"{labels[opt]} & {'--' if among_formats is None else among_formats} & {among_all} \\\\")
    lines += ["\\bottomrule", "\\end{tabularx}", "\\end{table}"]
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    (TABLE_DIR / "RQ5_pareto_table.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {TABLE_DIR / 'RQ5_pareto_table.tex'}")


def main() -> None:
    needed = ["RQ1_accuracy.csv", "RQ2_energy.csv", "RQ3_pot_accuracy.csv", "RQ4_pot_energy.csv"]
    missing = [n for n in needed if not (ANALYSIS_DIR / n).exists()]
    if missing:
        print(f"skip: {', '.join(missing)} not found (run the RQ1-RQ4 steps first)")
        return
    options = pareto_table(load_options())
    options.to_csv(ANALYSIS_DIR / "RQ5_pareto.csv", index=False)
    formats_figure(options, "column")
    formats_figure(options, "wide")
    pareto_count_table(options)
    pd.set_option("display.width", 200)
    for model in MODELS:
        g = options[options.model == model]
        print(f"{MODEL_LABELS[model]:13s} formats: {', '.join(g[g.pareto_formats == True].option)}"
              f" | all options: {', '.join(g[g.pareto_all_options].option)}")


if __name__ == "__main__":
    main()
