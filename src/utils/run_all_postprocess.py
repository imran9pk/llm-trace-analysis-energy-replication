"""
run_all_postprocess.py

Fail-safe orchestrator for the post-processing chains. Runs each script in
order; if a script exits non-zero, the run stops immediately, no later script
is started, and a FAILED summary shows which script broke. Reports SUCCESS
only if every script completed with exit code 0.

Two chains:
  directPrompting_1 .. directPrompting_7   direct prompting (RQ1, RQ2)
  pot_1 .. pot_4                           task-level program generation (RQ3, RQ4);
                                           uses outputs of the direct-prompting chain
                                           (JSON accuracy and energy) as the reference.

Edit MODELS/FORMATS/SHOTS in utils_config.py first to choose what is processed.
Cross-platform: plain Python, run the same way on Windows or Linux.

Usage:
    python run_all_postprocess.py          # both chains (direct prompting first)
    python run_all_postprocess.py dp       # direct prompting only
    python run_all_postprocess.py pot      # program generation only
"""

import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DIRECT_PROMPTING_STEPS = [
    "directPrompting_1_combine_all_responses.py",  # per-part responses -> output_processed/
    "directPrompting_2_combine_all_energy.py",     # per-part energy    -> output_processed/
    "directPrompting_3_cal_accuracy_all.py",       # TraceLLM evaluator, aggregate accuracies -> output_processed/accuracy/
    "directPrompting_4_build_instance_table.py",   # one row per (model, format, instance): correctness + energy
    "directPrompting_5_rq1_statistics.py",         # RQ1: accuracy overall and per granularity, wrong-attribute answers
    "directPrompting_6_rq2_statistics.py",         # RQ2: tokens and energy vs JSON, energy per input/output token
    "directPrompting_7_build_paper_latex.py",      # RQ1/RQ2 LaTeX -> output_processed/tables/ and figures/
]
POT_STEPS = [
    "pot_1_cal_accuracy_all.py",                   # TraceLLM evaluator per model x shot -> output_processed/accuracy_pot/
    "pot_2_statistics.py",                         # RQ3/RQ4: accuracy, shot-level check, generation energy
    "pot_3_build_paper_latex.py",                  # RQ3/RQ4 LaTeX tables -> output_processed/tables/
    "pot_4_rq5.py",                                # RQ5: Pareto analysis, formats figure, Pareto table
]
CHAINS = {"dp": DIRECT_PROMPTING_STEPS, "pot": POT_STEPS, "all": DIRECT_PROMPTING_STEPS + POT_STEPS}


def main():
    choice = sys.argv[1] if len(sys.argv) > 1 else "all"
    if choice not in CHAINS:
        print(f"unknown chain '{choice}'; use one of: {', '.join(CHAINS)}")
        sys.exit(2)
    steps = CHAINS[choice]
    start = time.time()
    for i, step in enumerate(steps, start=1):
        print(f"\n########## STEP {i}/{len(steps)}: {step} ##########", flush=True)
        result = subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, step)])
        if result.returncode != 0:
            print(
                f"\n================ FAILED ================\n"
                f"Step {i}/{len(steps)} ({step}) exited with code {result.returncode}.\n"
                f"Stopping here -- steps {i + 1}..{len(steps)} were NOT run.\n"
                f"Completed steps: {', '.join(steps[:i - 1]) if i > 1 else '(none)'}\n"
                f"Elapsed: {time.time() - start:.1f}s",
                flush=True,
            )
            sys.exit(1)
    print(
        f"\n================ SUCCESS ================\n"
        f"All {len(steps)} post-processing steps ({choice}) completed with no errors.\n"
        f"Elapsed: {time.time() - start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
