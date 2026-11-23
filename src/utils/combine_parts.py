"""
combine part-split inference outputs.

Usage:
    python combine_parts.py --responses-glob "<glob pattern>" [--dry-run]
    python combine_parts.py --energy-glob "<glob pattern>" [--dry-run]
    python combine_parts.py --responses-glob "..." --energy-glob "..." [--dry-run]

Example (matches the part_1..part_6 files):
    python combine_parts.py \\
        --responses-glob "../../output/LLMresponses_Qwen3-8B_woFineTuning_woCoT_JSON_with_step_part_*_ids.jsonl" \\
        --energy-glob "../../output/energy_Qwen3-8B_JSON_with_step_*_part_*_ids.jsonl"

Output is written to an output_processed/ directory, a sibling of wherever
the source files live (e.g. output/ -> ../output_processed/), using the
source basename with the "_part_N_ids" suffix stripped.
"""

import argparse
import glob
import json
import os
import re

PART_SUFFIX_RE = re.compile(r"_part_[^_]+_ids(?=\.[^.]+$)")

# Full TraceBench test set size (see split_problem_ids.py's EXPECTED_TOTAL) —
# used for the post-combine unique-task-count sanity check.
EXPECTED_TOTAL_TASKS = 9120


def _default_parts_dir() -> str:
    # combine_parts.py lives at TraceLLM/src/utils/ -> three levels up is TraceLLM/
    trace_llm_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(trace_llm_dir, "dataset", "TraceBench", "test", "parts")


def _check_part_count(part_files: list, parts_dir: str, label: str) -> None:
    if not os.path.isdir(parts_dir):
        print(f"[{label}] part-count check: skipped (parts dir not found: {parts_dir})")
        return
    expected_part_files = glob.glob(os.path.join(parts_dir, "part_*_ids.json"))
    expected_count = len(expected_part_files)
    actual_count = len(part_files)
    if actual_count == expected_count:
        print(f"[{label}] part-count check: OK ({actual_count}/{expected_count} parts present, per {parts_dir})")
    else:
        print(
            f"[{label}] part-count check: COMBINING A SUBSET -- {actual_count} part file(s) matched "
            f"vs {expected_count} part-id file(s) in {parts_dir} "
            f"({expected_count - actual_count} part(s) missing; expected if this run is still in progress)"
        )


def _check_unique_task_count(unique_problem_ids: int, label: str) -> None:
    if unique_problem_ids == EXPECTED_TOTAL_TASKS:
        print(f"[{label}] task-count check: OK ({unique_problem_ids}/{EXPECTED_TOTAL_TASKS} unique problem_ids)")
    else:
        print(
            f"[{label}] task-count check: INCOMPLETE -- {unique_problem_ids} unique problem_id(s) combined, "
            f"expected {EXPECTED_TOTAL_TASKS} ({EXPECTED_TOTAL_TASKS - unique_problem_ids} missing)"
        )


def _combined_output_path(one_source_file: str) -> str:
    src_dir = os.path.dirname(one_source_file)
    combined_dir = os.path.join(os.path.dirname(src_dir), "output_processed")
    base = os.path.basename(one_source_file)
    base = PART_SUFFIX_RE.sub("", base)
    return os.path.join(combined_dir, base)


def combine_responses(glob_pattern: str, dry_run: bool, parts_dir: str) -> None:
    part_files = sorted(glob.glob(glob_pattern))
    if not part_files:
        print(f"[responses] no files matched pattern: {glob_pattern}")
        return

    _check_part_count(part_files, parts_dir, label="responses")

    merged = {}
    duplicates = []
    for part_file in part_files:
        with open(part_file, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            part_data = json.loads(content)  # old format: one big dict per file
        except json.JSONDecodeError:
            part_data = {}  # new format: one JSON object per line
            for line in content.splitlines():
                line = line.strip()
                if line:
                    part_data.update(json.loads(line))
        for problem_id, record in part_data.items():
            if problem_id in merged:
                duplicates.append((problem_id, part_file))
                continue
            merged[problem_id] = record

    if duplicates:
        raise ValueError(
            f"[responses] duplicate problem_id(s) found across part files "
            f"(overlapping part-id files?): {duplicates}"
        )

    _check_unique_task_count(len(merged), label="responses")

    out_path = _combined_output_path(part_files[0])
    print(
        f"[responses] {len(part_files)} part file(s), "
        f"{len(merged)} total record(s) -> {out_path}"
    )
    if dry_run:
        return

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4)


def combine_energy(glob_pattern: str, dry_run: bool, parts_dir: str) -> None:
    part_files = sorted(glob.glob(glob_pattern))
    if not part_files:
        print(f"[energy] no files matched pattern: {glob_pattern}")
        return

    _check_part_count(part_files, parts_dir, label="energy")

    merged_lines = []
    seen_keys = set()
    duplicates = []
    for part_file in part_files:
        with open(part_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                key = (record.get("problem_id"), record.get("repeat_idx"))
                if key in seen_keys:
                    duplicates.append((key, part_file))
                    continue
                seen_keys.add(key)
                merged_lines.append(line)

    if duplicates:
        raise ValueError(
            f"[energy] duplicate (problem_id, repeat_idx) found across part "
            f"files (overlapping part-id files?): {duplicates}"
        )

    _check_unique_task_count(len(set(k[0] for k in seen_keys)), label="energy")

    out_path = _combined_output_path(part_files[0])
    print(
        f"[energy] {len(part_files)} part file(s), "
        f"{len(merged_lines)} total record(s) -> {out_path}"
    )
    if dry_run:
        return

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for line in merged_lines:
            f.write(line + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Combine part-split LLMresponses/energy output files "
        "produced by separate app_inference_with_measure.py part runs."
    )
    parser.add_argument(
        "--responses-glob",
        default=None,
        help="Glob pattern matching LLMresponses_..._part_*_ids.jsonl files to combine",
    )
    parser.add_argument(
        "--energy-glob",
        default=None,
        help="Glob pattern matching energy_..._part_*_ids.jsonl files to combine",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print what would be combined; do not write output files",
    )
    parser.add_argument(
        "--parts-dir",
        default=None,
        help="Directory containing part_*_ids.json (for the part-count sanity check); "
        f"defaults to {_default_parts_dir()}",
    )
    args = parser.parse_args()

    if not args.responses_glob and not args.energy_glob:
        parser.error("at least one of --responses-glob / --energy-glob is required")

    parts_dir = args.parts_dir or _default_parts_dir()

    if args.responses_glob:
        combine_responses(args.responses_glob, args.dry_run, parts_dir)
    if args.energy_glob:
        combine_energy(args.energy_glob, args.dry_run, parts_dir)


if __name__ == "__main__":
    main()
