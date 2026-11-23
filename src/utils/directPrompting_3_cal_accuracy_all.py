"""
directPrompting_3_cal_accuracy_all.py

Runs cal_accuracy_Graph2Token.py against each model x format combo's
combined responses file (see directPrompting_1_combine_all_responses.py, must be run
first for a combo to be usable here). Edit MODELS/FORMATS in
utils_config.py before running: comment out a line to skip it. Combos
with no combined responses file yet are skipped automatically with a
message, so it's safe to leave every model/format uncommented as
results land incrementally.

Writes global/dimension/second_type_level_eval_results.json under
output_processed/accuracy/<model>_<format>/.
Cross-platform: plain Python, run the same way on Windows or Linux.

Usage:
    python directPrompting_3_cal_accuracy_all.py
"""

import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from utils_config import MODELS, FORMATS  # noqa: E402 -- see utils_config.py to edit the lists

CAL_ACCURACY_SCRIPT = os.path.join(SCRIPT_DIR, "cal_accuracy_Graph2Token.py")
OUTPUT_PROCESSED_DIR = os.path.join(SCRIPT_DIR, "..", "..", "output_processed")


def main():
    for model in MODELS:
        for fmt in FORMATS:
            input_file = os.path.join(
                OUTPUT_PROCESSED_DIR,
                f"LLMresponses_{model}_woFineTuning_woCoT_{fmt}_with_step.jsonl",
            )
            if not os.path.exists(input_file):
                print(f"skip: {model}/{fmt} not combined yet")
                continue
            output_dir = os.path.join(OUTPUT_PROCESSED_DIR, "accuracy", f"{model}_{fmt}")
            print(f"\n=== accuracy eval: {model} / {fmt} ===")
            subprocess.run(
                [sys.executable, CAL_ACCURACY_SCRIPT, "--input", input_file, "--output-dir", output_dir],
                check=True,
            )


if __name__ == "__main__":
    main()
