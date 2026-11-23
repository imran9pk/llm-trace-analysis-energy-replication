#!/bin/bash
# Not meant to be sbatch'd directly -- use submit_all_sequential.sh /
# submit_all_parallel.sh, which set SUBMITTED_VIA_WRAPPER and pass the
# correct job-name + part-ids file.

#SBATCH --job-name=tracepart
#SBATCH --partition=gprod
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=6
#SBATCH --time=6-00:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

module load miniconda3/22.11.1-broadwell-intel_2021.9.0
source $(conda info --base)/etc/profile.d/conda.sh
conda activate "${CONDA_ENV:-traceEnv}"   # name or full path of the conda env

if [ -z "$SUBMITTED_VIA_WRAPPER" ]; then
    echo "ERROR: run_part.sh must be submitted via submit_all_sequential.sh or submit_all_parallel.sh, not sbatch'd directly."
    exit 1
fi

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

if [ -z "$1" ] || [ ! -f "$1" ]; then
    echo "ERROR: run_part.sh requires a valid part-ids file as \$1 (got: '$1'). Refusing to silently run the full dataset."
    exit 1
fi

source scripts/direct_prompting/diagnostics.sh
print_job_diagnostics

echo "================ START WORKLOAD ================"
python3 -u src/DirectPrompting/app_inference_with_measure.py "$1"
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "================ FAILED (exit $STATUS) ================"
    exit $STATUS
fi
echo "================ DONE ================"
