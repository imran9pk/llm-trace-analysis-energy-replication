"""
03_measure_execution_energy.py

Measures the CPU energy of running the generated programs on the test set.
Run it on a dedicated Linux machine (dedicated measurement machine), from src/PoT:

    python 03_measure_execution_energy.py                    # all models
    python 03_measure_execution_energy.py --models Qwen3-8B  # one model

The output is shown in the terminal and also written to logs/exec_energy.log
(overwritten at every run). For a long run, start it inside `screen`.

Machine-specific settings (perf permissions, CPU governor) may need adapting to your system.

Procedure, for each model and shot level (zero-shot and the few-shot level of the paper):
  1. Load the 9,120 test instances and the 38 generated programs (not measured).
  2. Warm-up: run every program on every instance of its task once (not
     measured). This gives the time of one run of the test set, and drops any
     call that takes longer than the 30 s timeout of 02_execute_scripts.py.
  3. Repeat `repetitions` times:
       start the meter, run the test set `iterations` times in a loop, stop the meter;
       measure the idle machine for the same length of time;
       energy of one run of the test set = (measured - idle) / iterations.
`repetitions` and `iterations` are set in configPoT.yaml.

Why a loop: one run of the test set takes well under a second. RAPL updates
its counters about once per millisecond (Hahnel et al., 2012), and the programs
add only a few watts to the idle power of the machine. Looping makes the window
long enough for these errors to be negligible. A window must last at least
5 s, the minimum run length used by Solovyeva et al. (FORGE 2025).

The programs get the same inputs as in 02_execute_scripts.py, but they are
called directly in this process: 02_execute_scripts.py starts a new process
per instance, which is a safety measure and not part of the programs' cost.
Calls that raise an error are kept, because their energy is spent too.

Results are appended to output/execution_energy/execution_energy_<host>.csv.
If the run stops, start it again: finished repetitions are skipped.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import logging
import math
import os
import platform
import signal
import sys
import time
from pathlib import Path

import yaml

POT_DIR = Path(__file__).resolve().parent
ROOT = POT_DIR.parent.parent
sys.path.insert(0, str(ROOT / "src" / "utils"))
sys.path.insert(0, str(ROOT / "src" / "energy"))
from utils_config import MODELS, POT_FEWSHOT  # noqa: E402
from cpu_energy import PerfEnergyMeter, measure_idle  # noqa: E402

log = logging.getLogger("exec_energy")

SHOTS = ["zeroshot", POT_FEWSHOT]
CONFIG_FILE = ROOT / "configPoT.yaml"
TEST_INSTANCES_FILE = ROOT / "dataset" / "TraceBench" / "test" / "preprocessed" / "0.pt"
PROGRAMS_DIR = ROOT / "output" / "generated_scripts"
RESULTS_FILE = ROOT / "output" / "execution_energy" / f"execution_energy_{platform.node()}.csv"
LOG_FILE = ROOT / "logs" / "exec_energy.log"

TIMEOUT_S = 30        # same timeout per call as in 02_execute_scripts.py
MIN_WINDOW_S = 5.0    # shortest measurement window (Solovyeva et al., FORGE 2025)
COOLDOWN_S = 10.0     # pause before each measured window and each idle window
CPU_CORE = 2          # core the programs run on

RESULT_COLUMNS = [
    "model", "shot", "repetition", "iterations", "programs", "instances", "failed_calls",
    "timed_out_calls", "warmup_time_s", "window_ok", "duration_s", "package_j", "dram_j",
    "idle_package_j", "idle_dram_j", "idle_duration_s", "exec_package_j", "exec_dram_j",
    "exec_time_s", "timestamp",
]


# ---------------------------------------------------------------- settings and inputs

def read_settings() -> tuple[int, int]:
    """Number of repetitions and loop iterations, from configPoT.yaml."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return int(config["exec_energy_repetitions"]), int(config["exec_energy_iterations"])


def import_execute_scripts():
    """Import 02_execute_scripts.py to reuse its input parsing."""
    # 02_execute_scripts.py reads this SLURM variable when it is imported
    os.environ.setdefault("SLURM_CPUS_PER_TASK", "1")
    spec = importlib.util.spec_from_file_location("execute_scripts", POT_DIR / "02_execute_scripts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_test_instances(execute_scripts) -> list[tuple[str, tuple]]:
    """Each test instance as (task_id, (trace1, trace2, key_components))."""
    import torch

    # 0.pt is a plain pickled dict; torch 2.6+ only loads it with weights_only=False
    data = torch.load(TEST_INSTANCES_FILE, map_location="cpu", weights_only=False)
    instances, parse_errors = [], 0
    for instance in data.values():
        task_id = instance["task_id"]
        try:
            trace1, trace2 = execute_scripts.parse_input_traces(instance["input_trace_raw_spans_desc"])
        except Exception:
            # 02_execute_scripts.py counts these as incorrect; there is nothing to run
            parse_errors += 1
            continue
        template = execute_scripts.TASK_INFO.get(task_id, {}).get("question_template", "")
        key_components = execute_scripts.parse_key_component(instance["question"], template)
        instances.append((task_id, (trace1, trace2, key_components)))
    log.info(f"loaded {len(instances)} test instances ({parse_errors} parse errors)")
    return instances


def load_programs(model: str, shot: str) -> dict:
    """The solution() function of each generated program, by task id."""
    programs = {}
    for script in sorted((PROGRAMS_DIR / f"generated_scripts_{model}_{shot}").glob("Task_*.py")):
        namespace: dict = {}
        try:
            exec(script.read_text(encoding="utf-8"), namespace)
        except Exception:
            # a program that does not even load fails on all its instances in 02 too
            continue
        if callable(namespace.get("solution")):
            programs[script.stem] = namespace["solution"]
    return programs


def solution_arguments(task_id: str, trace1, trace2, key_components: dict) -> list:
    """Arguments for solution(), in the same order as 02_execute_scripts.py."""
    arguments = [trace1]
    if trace2 is not None:
        arguments.append(trace2)
    # for Task_4_* tasks, 02_execute_scripts.py does not pass the key components
    if not task_id.startswith("Task_4"):
        if key_components.get("key_component") is not None:
            arguments.append(key_components["key_component"])
        elif key_components.get("key_component_1") is not None and key_components.get("key_component_2") is not None:
            arguments += [key_components["key_component_1"], key_components["key_component_2"]]
    return arguments


def build_calls(instances: list, programs: dict) -> list[tuple]:
    """One (solution, arguments) pair per test instance whose task has a program."""
    return [(programs[task_id], solution_arguments(task_id, *inputs))
            for task_id, inputs in instances if task_id in programs]


# ---------------------------------------------------------------- running the programs

class CallTimeout(Exception):
    pass


def raise_timeout(signum, frame):
    raise CallTimeout()


def warm_up(calls: list) -> tuple[list, int, int, float]:
    """Run the test set once, not measured.

    Returns the calls to measure (without those over the timeout), the number of
    calls that raised an error, the number that timed out, and the run time.
    """
    signal.signal(signal.SIGALRM, raise_timeout)
    kept, failed, timed_out = [], 0, 0
    start = time.perf_counter()
    for solution, arguments in calls:
        signal.setitimer(signal.ITIMER_REAL, TIMEOUT_S)
        try:
            solution(*arguments)
            kept.append((solution, arguments))
        except CallTimeout:
            timed_out += 1
        except KeyboardInterrupt:
            raise
        except BaseException:
            failed += 1
            kept.append((solution, arguments))
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
    return kept, failed, timed_out, time.perf_counter() - start


def run_test_set(calls: list) -> None:
    """Run every program once on every instance of its task."""
    for solution, arguments in calls:
        try:
            solution(*arguments)
        except KeyboardInterrupt:
            raise
        except BaseException:
            # errors were already counted during the warm-up
            pass


def measure_repetition(meter: PerfEnergyMeter, calls: list, iterations: int) -> dict:
    """One measured window with `iterations` runs of the test set, plus its idle window."""
    time.sleep(COOLDOWN_S)
    meter.start()
    for _ in range(iterations):
        run_test_set(calls)
    busy = meter.stop()

    time.sleep(COOLDOWN_S)
    idle = measure_idle(meter, busy.duration_s)

    exec_dram = None
    if busy.dram_j is not None and idle.dram_j is not None:
        exec_dram = (busy.dram_j - idle.dram_j) / iterations
    return {
        "window_ok": busy.duration_s >= MIN_WINDOW_S,
        "duration_s": round(busy.duration_s, 4),
        "package_j": busy.package_j,
        "dram_j": busy.dram_j,
        "idle_package_j": idle.package_j,
        "idle_dram_j": idle.dram_j,
        "idle_duration_s": round(idle.duration_s, 4),
        "exec_package_j": (busy.package_j - idle.package_j) / iterations,
        "exec_dram_j": exec_dram,
        "exec_time_s": busy.duration_s / iterations,
    }


# ---------------------------------------------------------------- results file

def finished_repetitions() -> set:
    """(model, shot, repetition) already in the results file."""
    if not RESULTS_FILE.exists():
        return set()
    with open(RESULTS_FILE, newline="") as f:
        return {(row["model"], row["shot"], int(row["repetition"])) for row in csv.DictReader(f)}


def open_results_file():
    """Open the results file for appending, with a header if it is new."""
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    is_new = not RESULTS_FILE.exists()
    f = open(RESULTS_FILE, "a", newline="")
    writer = csv.DictWriter(f, fieldnames=RESULT_COLUMNS)
    if is_new:
        writer.writeheader()
    return f, writer


# ---------------------------------------------------------------- one model and shot level

def measure_configuration(meter, writer, results, instances, model, shot, repetitions, iterations, done):
    """All repetitions for one model and shot level."""
    if all((model, shot, rep) in done for rep in range(1, repetitions + 1)):
        log.info(f"{model}/{shot}: already measured")
        return
    programs = load_programs(model, shot)
    if not programs:
        log.info(f"{model}/{shot}: no generated programs, skipped")
        return

    calls, failed, timed_out, warmup_s = warm_up(build_calls(instances, programs))
    log.info(f"{model}/{shot}: {len(programs)} programs, {len(calls)} calls, {failed} raise an error, "
          f"{timed_out} timed out; one run of the test set takes {warmup_s:.3f} s; "
          f"window of about {iterations * warmup_s:.0f} s")
    if iterations * warmup_s < MIN_WINDOW_S:
        needed = math.ceil(MIN_WINDOW_S / warmup_s)
        log.info(f"  skipped: the window would be shorter than {MIN_WINDOW_S:.0f} s; "
              f"set exec_energy_iterations to {needed} or more in configPoT.yaml")
        return

    for rep in range(1, repetitions + 1):
        if (model, shot, rep) in done:
            continue
        measured = measure_repetition(meter, calls, iterations)
        writer.writerow({
            "model": model, "shot": shot, "repetition": rep, "iterations": iterations,
            "programs": len(programs), "instances": len(calls), "failed_calls": failed,
            "timed_out_calls": timed_out, "warmup_time_s": round(warmup_s, 6),
            **measured, "timestamp": time.time(),
        })
        results.flush()
        warning = "" if measured["window_ok"] else "  (window too short, not used)"
        log.info(f"  repetition {rep}: {measured['package_j']:.1f} J in {measured['duration_s']:.1f} s, "
              f"idle {measured['idle_package_j']:.1f} J -> {measured['exec_package_j']:.2f} J "
              f"per run of the test set{warning}")


# ---------------------------------------------------------------- main

def setup_log() -> None:
    """Show messages in the terminal and write them to LOG_FILE."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, mode="w")])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=MODELS)
    args = parser.parse_args()

    setup_log()
    repetitions, iterations = read_settings()
    log.info(f"configPoT.yaml: {repetitions} repetitions, {iterations} iterations per window")
    os.sched_setaffinity(0, {CPU_CORE})

    meter = PerfEnergyMeter()
    instances = load_test_instances(import_execute_scripts())
    done = finished_repetitions()
    results, writer = open_results_file()
    with results:
        for model in args.models:
            for shot in SHOTS:
                measure_configuration(meter, writer, results, instances, model, shot,
                                      repetitions, iterations, done)
    log.info(f"done -> {RESULTS_FILE}")


if __name__ == "__main__":
    main()
