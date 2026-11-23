"""
directPrompting_1_combine_all_responses.py

Runs combine_parts.py's response-combining step for each model x format
combo listed below. Edit MODELS/FORMATS in utils_config.py before
running: comment out a line (add a leading #) to skip it, e.g. if its
parts aren't all finished yet.

Combined output lands in output_processed/ (see combine_parts.py).
Some runs (DeepSeek-R1) are kept in output/ as one file that is already
combined; when a model/format has no part files, that file is copied to
output_processed/ as it is.
Cross-platform: plain Python, run the same way on Windows or Linux.

Usage:
    python directPrompting_1_combine_all_responses.py
"""

import glob
import os
import shutil
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from utils_config import MODELS, FORMATS  # noqa: E402 -- see utils_config.py to edit the lists

COMBINE_PARTS_SCRIPT = os.path.join(SCRIPT_DIR, "combine_parts.py")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "output")
OUTPUT_PROCESSED_DIR = os.path.join(SCRIPT_DIR, "..", "..", "output_processed")


def copy_combined(model, fmt):
    """Copy an already combined responses file from output/ to output_processed/."""
    name = f"LLMresponses_{model}_woFineTuning_woCoT_{fmt}_with_step.jsonl"
    source = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(source):
        print(f"no part files and no combined file for {model} / {fmt}")
        return
    shutil.copy2(source, os.path.join(OUTPUT_PROCESSED_DIR, name))
    print(f"copied already combined file: {name}")


def main():
    for model in MODELS:
        for fmt in FORMATS:
            responses_glob = os.path.join(
                OUTPUT_DIR,
                f"LLMresponses_{model}_woFineTuning_woCoT_{fmt}_with_step_part_*_ids.jsonl",
            )
            print(f"\n=== combining responses: {model} / {fmt} ===")
            if not glob.glob(responses_glob):
                copy_combined(model, fmt)
                continue
            subprocess.run(
                [sys.executable, COMBINE_PARTS_SCRIPT, "--responses-glob", responses_glob],
                check=True,
            )


if __name__ == "__main__":
    main()
