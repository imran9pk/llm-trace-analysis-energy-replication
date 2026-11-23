#!/bin/bash
# diagnostics.sh
# Shared job-diagnostics block for run_part.sh. Meant to be
# sourced (not executed standalone) after cd "$SLURM_SUBMIT_DIR", so relative
# paths (config.yaml, .git) resolve correctly. Usage:
#   source scripts/diagnostics.sh
#   print_job_diagnostics

print_job_diagnostics() {
    echo "================ JOB INFO ================"
    echo "Job ID              : $SLURM_JOB_ID"
    echo "Job name            : $SLURM_JOB_NAME"
    echo "Start time          : $(date)"
    echo "Node                : $(hostname)"
    echo "CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES:-not set}"
    echo "SLURM_CPUS_PER_TASK : $SLURM_CPUS_PER_TASK"
    echo

    echo "================ CODE VERSION ================"
    echo "Commit : $(git rev-parse HEAD 2>/dev/null || echo 'not a git repo / git unavailable')"
    echo "Dirty files:"
    git status --short 2>/dev/null
    echo

    echo "================ ACTIVE CONFIG (config.yaml, comments/blank/secret-looking lines stripped) ================"
    grep -v '^[[:space:]]*#' config.yaml | grep -v '^[[:space:]]*$' | grep -viE 'key|token|secret|password'
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

    echo "================ GPU CLOCKS ================"
    nvidia-smi -q -d CLOCK | grep -E "Clocks|SM|Memory|Graphics"
    echo

    echo "================ HOST / SOFTWARE ================"
    grep PRETTY_NAME /etc/os-release; uname -r
    lscpu | grep -E "Model name|^CPU\(s\):"
    free -h | grep Mem
    python -V
    python -c "import torch, transformers, pynvml; print('torch', torch.__version__, '| cuda', torch.version.cuda, '| transformers', transformers.__version__)"
    pip freeze > "pipfreeze_${SLURM_JOB_ID}.txt"
    echo

    echo "================ GPU POWER SETTINGS ================"
    nvidia-smi -q -d POWER | grep -E "Power Limit"
    echo
}
