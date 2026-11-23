#!/bin/bash
#SBATCH --job-name=PoTGen-DSK
#SBATCH --partition=gprod
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=16
#SBATCH --time=6-00:00:00
#SBATCH --output=logs/PoTGen_DSK_%j.out
#SBATCH --error=logs/PoTGen_DSK_%j.err

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

module load miniconda3/22.11.1-broadwell-intel_2021.9.0
source $(conda info --base)/etc/profile.d/conda.sh
conda activate "${CONDA_ENV:-traceEnv}"   # name or full path of the conda env

cd "${SLURM_SUBMIT_DIR:-$PWD}/src/PoT"
mkdir -p "${SLURM_SUBMIT_DIR:-$PWD}/logs"   # submit from the repository root

echo "================ JOB INFO ================"
echo "Job ID              : $SLURM_JOB_ID"
echo "Node                : $(hostname)"
echo "CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES:-not set}"
echo "SLURM_CPUS_PER_TASK : $SLURM_CPUS_PER_TASK"
echo

echo "================ NODE SHARING CHECK ================"
scontrol show node $(hostname -s) | egrep -i "NodeName|State|CPUAlloc|CPUTot|CfgTRES|AllocTRES|Gres"
echo

echo "================ JOBS ON THIS NODE ================"
squeue -w $(hostname -s) -o "%.18i %.10u %.20j %.8T %.10M %.4C %R"
echo

echo "================ GPU CHECK ================"
nvidia-smi -L
nvidia-smi
echo

echo "================ HOST / SOFTWARE ================"
grep PRETTY_NAME /etc/os-release; uname -r
lscpu | grep -E "Model name|^CPU\(s\):"
free -h | grep Mem
python -V
python -c "import torch, transformers, pynvml; print('torch', torch.__version__, '| cuda', torch.version.cuda, '| transformers', transformers.__version__)"
pip freeze > "pipfreeze_${SLURM_JOB_ID}.txt"

echo "================ GPU POWER SETTINGS ================"
nvidia-smi -q -d POWER | grep -E "Power Limit"

echo "================ START WORKLOAD ================"
for s in 0 1 2 3 4 5
do
    echo "Running script generation with ${s}-shot"
    srun python3 01_generate_scripts.py --shots $s
    echo "Cooldown before next shot-level's idle-power baseline..."
    sleep 60
done
echo "================ DONE ================"
