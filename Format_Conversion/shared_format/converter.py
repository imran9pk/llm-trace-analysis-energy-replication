import ast
import csv
import io
import json
import os
import sys
from pathlib import Path

# --- paths, resolved from this script's own location so it doesn't depend on cwd ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "test_tasks_preprocessed_Graph2Text_raw_spans_desc_with_step.json")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# --- import toon_format and tron from the local sibling source dirs (not the
# installed PyPI toon_format package) so this script stays self-contained
# alongside toon-python/ and tron-python/ for the replicable package ---
sys.path.insert(0, os.path.join(SCRIPT_DIR, "..", "toon-python", "src"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "..", "tron-python", "src"))
from toon_format import encode, count_tokens
from tron import TRON


def normalize_spans(trace):
    all_keys = []
    seen = set()
    for span in trace:
        for key in span.keys():
            if key not in seen:
                all_keys.append(key)
                seen.add(key)
    return [{key: span.get(key, "") for key in all_keys} for span in trace]


def parse_trace_input(json_input):
    if "Input Trace 1:" in json_input:
        part1, part2 = json_input.split("\nInput Trace 2:", 1)
        trace1 = ast.literal_eval(part1.replace("Input Trace 1:", "", 1).strip())
        trace2 = ast.literal_eval(part2.strip())
        return trace1, trace2
    trace = ast.literal_eval(json_input.replace("Input Trace:", "", 1).strip())
    return trace, None


def encode_toon(spans):
    return encode(spans)


def encode_csv(spans):
    fieldnames = list(spans[0].keys()) if spans else []
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    writer.writeheader()
    writer.writerows(spans)
    return buf.getvalue().rstrip("\n")


def encode_markdown(spans):
    fieldnames = list(spans[0].keys()) if spans else []
    header = "| " + " | ".join(fieldnames) + " |"
    sep = "| " + " | ".join("---" for _ in fieldnames) + " |"
    rows = ["| " + " | ".join(str(span[k]).replace("|", "\\|") for k in fieldnames) + " |" for span in spans]
    return "\n".join([header, sep] + rows)


def encode_tron(spans):
    return TRON.stringify(spans)


def convert_with(json_input, enc):
    trace1, trace2 = parse_trace_input(json_input)
    if trace2 is not None:
        return (
            "Input Trace 1: " + enc(normalize_spans(trace1))
            + "\nInput Trace 2: " + enc(normalize_spans(trace2))
        )
    return "Input Trace: " + enc(normalize_spans(trace1))


FORMATS = {
    "TOON"     : encode_toon,
    "CSV"      : encode_csv,
    "MARKDOWN" : encode_markdown,
    "TRON"     : encode_tron,
}


def run_format(fmt_name, enc):
    fmt = fmt_name.lower()
    output_file  = OUTPUT_DIR + f"/test_tasks_preprocessed_{fmt_name}_with_step.json"
    summary_file = OUTPUT_DIR + f"/test_tasks_preprocessed_{fmt_name}_with_step_summary.json"

    records = json.loads(json.dumps(base_records))

    total_json_tokens_tiktoken = 0
    total_fmt_tokens_tiktoken  = 0
    total_json_chars           = 0
    total_fmt_chars            = 0

    counter = 0
    for record in records:
        counter += 1
        print(f"[{fmt_name}] Processing record {counter}/{len(records)}", end="\r")
        json_input = record["input"]
        fmt_input = convert_with(json_input, enc)

        json_tokens_tiktoken = count_tokens(json_input)
        fmt_tokens_tiktoken  = count_tokens(fmt_input)
        json_chars           = len(json_input)
        fmt_chars            = len(fmt_input)

        record["input"]      = fmt_input
        record["input_json"] = json_input

        record["json_tokens_tiktoken"]           = json_tokens_tiktoken
        record[f"{fmt}_tokens_tiktoken"]         = fmt_tokens_tiktoken
        record[f"token_saving_tiktoken"]         = json_tokens_tiktoken - fmt_tokens_tiktoken
        record[f"token_saving_percent_tiktoken"] = ((json_tokens_tiktoken - fmt_tokens_tiktoken) / json_tokens_tiktoken * 100) if json_tokens_tiktoken > 0 else 0

        record["json_chars"]          = json_chars
        record[f"{fmt}_chars"]        = fmt_chars
        record["char_saving"]         = json_chars - fmt_chars
        record["char_saving_percent"] = ((json_chars - fmt_chars) / json_chars * 100) if json_chars > 0 else 0

        total_json_tokens_tiktoken += json_tokens_tiktoken
        total_fmt_tokens_tiktoken  += fmt_tokens_tiktoken
        total_json_chars           += json_chars
        total_fmt_chars            += fmt_chars

    summary = {
        "format"                      : fmt_name,
        "num_records"                 : len(records),

        "total_json_tokens"           : total_json_tokens_tiktoken,
        f"total_{fmt}_tokens"         : total_fmt_tokens_tiktoken,
        "total_token_saving"          : total_json_tokens_tiktoken - total_fmt_tokens_tiktoken,
        "total_token_saving_percent"  : ((total_json_tokens_tiktoken - total_fmt_tokens_tiktoken) / total_json_tokens_tiktoken * 100) if total_json_tokens_tiktoken > 0 else 0,

        "total_raw_chars"             : total_json_chars,
        f"total_{fmt}_chars"          : total_fmt_chars,
        "total_char_saving"           : total_json_chars - total_fmt_chars,
        "total_char_saving_percent"   : ((total_json_chars - total_fmt_chars) / total_json_chars * 100) if total_json_chars > 0 else 0,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2))
    print(f"Records saved to : {output_file}")
    print(f"Summary saved to : {summary_file}")
    return summary


if __name__ == "__main__":
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        base_records = json.load(f)

    all_summaries = {}
    for fmt_name, enc in FORMATS.items():
        all_summaries[fmt_name] = run_format(fmt_name, enc)

    combined_file = OUTPUT_DIR + "/all_formats_summary.json"
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_summaries, f, indent=2, ensure_ascii=False)
    print(f"Combined summary saved to : {combined_file}")

    # Short summary for the paper (tiktoken is the reference tokenizer of the
    # format-comparison table).
    paper_summary = []
    for fmt_name, summary in all_summaries.items():
        fmt = fmt_name.lower()
        total_tokens_tiktoken = summary[f"total_{fmt}_tokens"]
        num_records = summary["num_records"]
        paper_summary.append({
            "format"                  : fmt_name,
            "total_tokens_tiktoken"   : total_tokens_tiktoken,
            "mean_tokens_tiktoken"    : (total_tokens_tiktoken / num_records) if num_records > 0 else 0,
            "saving_percent_tiktoken" : summary["total_token_saving_percent"],
        })

    paper_summary_file = OUTPUT_DIR + "/all_formats_summary_paper.json"
    with open(paper_summary_file, "w", encoding="utf-8") as f:
        json.dump(paper_summary, f, indent=2, ensure_ascii=False)
    print(f"Paper summary saved to : {paper_summary_file}")
