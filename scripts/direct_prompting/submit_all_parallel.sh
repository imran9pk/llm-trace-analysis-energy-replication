#!/bin/bash
# submit_all_parallel.sh
# TAG and NUM_PARTS come from config.yaml (job_model_name, input_data_format,
# job_parts)

# Always work from the repo root, regardless of which directory this script
# was launched from (e.g. run from inside scripts/, or via ./scripts/... from
# the repo root -- both work).
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1

JOB_MODEL_NAME=$(grep -m1 '^job_model_name:' config.yaml | sed 's/^job_model_name:[[:space:]]*//' | awk '{print $1}')
DATAFORMAT=$(grep -m1 '^input_data_format:' config.yaml | sed 's/^input_data_format:[[:space:]]*//' | awk '{print $1}')
NUM_PARTS=$(grep -m1 '^job_parts:' config.yaml | sed 's/^job_parts:[[:space:]]*//' | awk '{print $1}')
TAG="${JOB_MODEL_NAME}${DATAFORMAT}"

# fail fast, before submitting anything, if any part-ids file is missing
for i in $(seq 1 "$NUM_PARTS"); do
    f="dataset/TraceBench/test/parts/part_${i}_ids.json"
    [ -f "$f" ] || { echo "Missing $f -- aborting, nothing submitted."; exit 1; }
done

export SUBMITTED_VIA_WRAPPER=1
for i in $(seq 1 "$NUM_PARTS"); do
    JOB_ID=$(sbatch --parsable --job-name="${TAG}${i}" scripts/direct_prompting/run_part.sh dataset/TraceBench/test/parts/part_${i}_ids.json)
    echo "Submitted ${TAG}${i}: $JOB_ID"
done
