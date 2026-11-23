"""
utils_config.py

Shared settings for the post-processing scripts in this directory
(directPrompting_* and pot_*). Edit this ONE file to add/remove a model,
format or shot level: every script picks it up automatically. Comment out
a line (add a leading #) to skip that model/format/shot level for a run.
"""

# Comment out a model's line to skip it this run.
MODELS = [
    "Qwen3-8B",
    # "DeepSeek-R1-Distill-Llama-8B",  # not included in the paper
    "Llama-3.1-8B-Instruct",
    "Ministral-8B-Instruct-2410",
]

# Comment out a format's line to skip it this run.
# Order of the formats in the paper tables: JSON (baseline) first, then from the
# smallest to the largest token saving with respect to JSON (Table I of the paper).
FORMATS = [
    "JSON",
    "MARKDOWN",
    "TRON",
    "TOON",
    "CSV",
]

# PoT (task-level program generation): shot levels, as in the result
# filenames results_taskLevel_<model>_<shot>.json. Comment out to skip.
SHOTS = [
    "zeroshot",
    "oneshot",
    "twoshot",
    "threeshot",
    "fourshot",
    "fiveshot",
]

# PoT few-shot level reported in the paper (RQ3/RQ4), next to zero-shot.
# Chosen as the smallest number of examples after which accuracy, averaged
# across models, does not improve (see RQ3_shot_selection.csv, pot_2_statistics.py).
POT_FEWSHOT = "twoshot"
