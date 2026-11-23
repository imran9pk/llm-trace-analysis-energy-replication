"""
directPrompting_2_combine_all_energy.py

Runs combine_parts.py's energy-combining step for each model x format
combo listed below. Edit MODELS/FORMATS in utils_config.py before
running: comment out a line (add a leading #) to skip it, e.g. if its
parts aren't all finished yet. Independent of directPrompting_1_combine_all_responses.py
-- reads the energy_*.jsonl part files directly, doesn't need responses
combined first.

Combined output lands in output_processed/ (see combine_parts.py).
Some runs (DeepSeek-R1) are kept in output/ as one file that is already
combined; when a model/format has no part files, that file is copied to
output_processed/ as it is.
Cross-platform: plain Python, run the same way on Windows or Linux.

Usage:
    python directPrompting_2_combine_all_energy.py
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
    """Copy an already combined energy file from output/ to output_processed/."""
    sources = glob.glob(os.path.join(OUTPUT_DIR, f"energy_{model}_{fmt}_with_step_*.jsonl"))
    sources = [s for s in sources if "_part_" not in os.path.basename(s)]
    if not sources:
        print(f"no part files and no combined file for {model} / {fmt}")
        return
    for source in sources:
        shutil.copy2(source, os.path.join(OUTPUT_PROCESSED_DIR, os.path.basename(source)))
        print(f"copied already combined file: {os.path.basename(source)}")


def main():
    for model in MODELS:
        for fmt in FORMATS:
            # energy filenames embed a per-part timestamp between format and part label
            energy_glob = os.path.join(
                OUTPUT_DIR,
                f"energy_{model}_{fmt}_with_step_*_part_*_ids.jsonl",
            )
            print(f"\n=== combining energy: {model} / {fmt} ===")
            if not glob.glob(energy_glob):
                copy_combined(model, fmt)
                continue
            subprocess.run(
                [sys.executable, COMBINE_PARTS_SCRIPT, "--energy-glob", energy_glob],
                check=True,
            )


if __name__ == "__main__":
    main()
