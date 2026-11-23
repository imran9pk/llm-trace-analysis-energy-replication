"""
paper_labels.py

Model and format names as printed in every paper table (directPrompting_7_build_paper_latex.py and pot_3_build_paper_latex.py),
so that all tables use the same names.
"""

MODEL_LABELS = {
    "Qwen3-8B": "Qwen3-8B",
    "DeepSeek-R1-Distill-Llama-8B": "DeepSeek-R1",
    "Llama-3.1-8B-Instruct": "Llama-3.1",
    "Ministral-8B-Instruct-2410": "Ministral-8B",
}

FORMAT_LABELS = {
    "JSON": "JSON",
    "MARKDOWN": "Markdown",
    "TOON": "TOON",
    "CSV": "CSV",
    "TRON": "TRON",
}


# Short model names for the column headers of the one-column tables.
TABLE_MODEL_LABELS = {
    "Qwen3-8B": "Qwen",
    "DeepSeek-R1-Distill-Llama-8B": "DeepSeek",
    "Llama-3.1-8B-Instruct": "Llama",
    "Ministral-8B-Instruct-2410": "Ministral",
}


def single_column_table(lines: list[str]) -> list[str]:
    """Turn a generated table into the one-column layout used in the paper.

    table* -> table, tabular -> tabularx at \\columnwidth (first column l, the
    others X), and the model names in the header row -> TABLE_MODEL_LABELS.
    Cell contents are not changed.
    """
    out = []
    for line in lines:
        if line.startswith("\\begin{table*}") or line.startswith("\\end{table*}"):
            line = line.replace("table*", "table")
        elif line.startswith("\\begin{tabular}{"):
            spec = line[len("\\begin{tabular}{"):].rstrip("}")
            line = "\\begin{tabularx}{\\columnwidth}{l" + "X" * (len(spec) - 1) + "}"
        elif line.startswith("\\end{tabular}"):
            line = "\\end{tabularx}"
        elif "&" in line and any(f"& {lab}" in line for lab in MODEL_LABELS.values()):
            for model, lab in MODEL_LABELS.items():
                line = line.replace(f"& {lab} ", f"& {TABLE_MODEL_LABELS[model]} ")
        out.append(line)
    return out
