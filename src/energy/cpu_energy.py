"""
cpu_energy.py

Measures CPU energy with Intel RAPL, read through `perf stat`.
Used to measure the energy of executing the generated programs.

RAPL keeps running energy counters, so there is no power sampling as for the
GPU: we read the counters when the measurement starts and when it stops.

Example:
    meter = PerfEnergyMeter()
    meter.start()
    run_the_code()
    busy = meter.stop()
    idle = measure_idle(meter, busy.duration_s)
    energy_of_the_code = busy.package_j - idle.package_j

perf needs permission to read the counters of the whole machine:
    sudo sysctl kernel.perf_event_paranoid=0
(machine-specific; adapt to your system)
"""

from __future__ import annotations

import os
import signal
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

PACKAGE_EVENT = "power/energy-pkg/"  # CPU packages, summed over the sockets
DRAM_EVENT = "power/energy-ram/"     # memory
PERF_START_DELAY_S = 0.5             # time perf needs to open the counters


@dataclass
class CpuEnergy:
    """Energy measured over one window."""
    package_j: float
    dram_j: Optional[float]  # None if the machine has no DRAM counter
    duration_s: float


def perf_events() -> list[str]:
    """RAPL events available in perf on this machine."""
    listing = subprocess.run(["perf", "list"], capture_output=True, text=True).stdout
    return [event for event in (PACKAGE_EVENT, DRAM_EVENT) if event in listing]


def read_perf_output(path: Path) -> tuple[Optional[float], Optional[float]]:
    """Package and DRAM energy (J) from a `perf stat -x ,` output file."""
    package, dram = None, None
    for line in path.read_text().splitlines():
        # line format: <value>,Joules,<event>,...
        fields = line.split(",")
        if line.startswith("#") or len(fields) < 3 or not fields[0]:
            continue
        if "energy-pkg" in fields[2]:
            package = float(fields[0])
        elif "energy-ram" in fields[2]:
            dram = float(fields[0])
    return package, dram


class PerfEnergyMeter:
    """Starts `perf stat` on the whole machine at start() and stops it at stop()."""

    def __init__(self) -> None:
        self.events = perf_events()
        if PACKAGE_EVENT not in self.events:
            raise RuntimeError(f"perf does not offer {PACKAGE_EVENT} on this machine")
        self.process: Optional[subprocess.Popen] = None
        self.output_file: Optional[Path] = None
        self.start_time = 0.0

    def start(self) -> None:
        self.output_file = Path(tempfile.mkstemp(suffix=".perf")[1])
        command = ["perf", "stat", "-a", "-x", ",", "-o", str(self.output_file)]
        for event in self.events:
            command += ["-e", event]
        self.process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        time.sleep(PERF_START_DELAY_S)
        if self.process.poll() is not None:
            error = self.process.stderr.read().decode()[-300:]
            raise RuntimeError(f"perf stopped right after starting: {error}")
        self.start_time = time.perf_counter()

    def stop(self) -> CpuEnergy:
        duration = time.perf_counter() - self.start_time
        # perf writes its totals when it receives Ctrl+C (SIGINT)
        self.process.send_signal(signal.SIGINT)
        self.process.wait(timeout=30)
        package, dram = read_perf_output(self.output_file)
        os.remove(self.output_file)
        if package is None:
            raise RuntimeError(f"perf reported no {PACKAGE_EVENT} value")
        return CpuEnergy(package_j=package, dram_j=dram, duration_s=duration)


def measure_idle(meter: PerfEnergyMeter, seconds: float) -> CpuEnergy:
    """Energy of the machine doing nothing for the given time.

    Use the same length as the measured window: perf's start and stop take the
    same time in both windows, so this overhead cancels out when subtracting.
    """
    meter.start()
    time.sleep(seconds)
    return meter.stop()
