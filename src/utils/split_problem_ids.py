import json
import os

# ---- settings: edit these before running ----
NUM_PARTS = 8
SOURCE_JSON = "dataset/TraceBench/test/preprocessed/test_tasks_preprocessed_TOON_with_step.json"
OUTPUT_DIR = "dataset/TraceBench/test/parts"
EXPECTED_TOTAL = 9120
# ----------------------------------------------


def main():
    with open(SOURCE_JSON, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    problem_ids = [item["problem_id"] for item in tasks]

    if len(set(problem_ids)) != len(problem_ids):
        raise ValueError("Duplicate problem_ids found in source JSON. Check the file before splitting.")

    if len(problem_ids) != EXPECTED_TOTAL:
        raise ValueError(
            f"Expected {EXPECTED_TOTAL} problem_ids, found {len(problem_ids)}. "
            "Check SOURCE_JSON before proceeding."
        )

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # split into NUM_PARTS roughly equal chunks, preserving original order
    n = len(problem_ids)
    base_size = n // NUM_PARTS
    remainder = n % NUM_PARTS

    parts = []
    start = 0
    for i in range(NUM_PARTS):
        size = base_size + (1 if i < remainder else 0)
        parts.append(problem_ids[start:start + size])
        start += size

    # sanity check: parts must reconstruct the full set exactly, no loss, no overlap
    total_check = sum(len(p) for p in parts)
    assert total_check == EXPECTED_TOTAL, f"Split produced {total_check} ids, expected {EXPECTED_TOTAL}"
    rejoined = set()
    for p in parts:
        rejoined.update(p)
    assert rejoined == set(problem_ids), "Split ids do not match the original set exactly"

    for i, part in enumerate(parts, start=1):
        out_path = os.path.join(OUTPUT_DIR, f"part_{i}_ids.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(part, f, indent=2)
        print(f"Part {i}: {len(part)} ids -> {out_path}")

    print(f"Done. {NUM_PARTS} parts written, {total_check} ids total, verified against source.")


if __name__ == "__main__":
    main()