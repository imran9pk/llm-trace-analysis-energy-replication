"""
inference_energy.py

GPU energy measurement primitives for LLM inference experiments.

PowerSampler and reset_gpu_state follow Danish et al. (E-Energy 2026).
measure_idle_power follows Danish et al. §A.4.2.
"""

import os
import gc
import time
import threading
from dataclasses import dataclass
from typing import Optional

import torch
from pynvml import nvmlDeviceGetPowerUsage, NVMLError


SAMPLE_INTERVAL_S = 0.1  # 10 Hz — Danish et al., Alizadeh et al., Solovyeva
IDLE_DURATION_S   = 10.0


# ---------------------------------------------------------------------------
# Idle baseline — Danish et al. §A.4.2
# ---------------------------------------------------------------------------

def measure_idle_power(handle) -> float:
    """Sample GPU power for IDLE_DURATION_S seconds at rest; return mean watts."""
    readings = []
    t_end = time.perf_counter() + IDLE_DURATION_S
    while time.perf_counter() < t_end:
        try:
            readings.append(nvmlDeviceGetPowerUsage(handle) / 1000.0)
        except NVMLError:
            pass
        time.sleep(SAMPLE_INTERVAL_S)
    mean_w = sum(readings) / len(readings) if readings else 0.0
    print(f"[energy] idle baseline = {mean_w:.2f} W  ({len(readings)} samples)")
    return mean_w


# ---------------------------------------------------------------------------
# PowerSampler — Danish et al. (E-Energy 2026)
# ---------------------------------------------------------------------------

class PowerSampler:
    """
    Daemon thread sampling nvmlDeviceGetPowerUsage at 10 Hz.
    start() / stop() bracket the generate() call.
    compute_energy_j() uses trapezoidal integration. Danish et al. §A.4.2.
    """

    def __init__(self, handle):
        self._handle  = handle
        self._running = False
        self._samples: list[tuple[float, float]] = []  # (time.perf_counter, watts)
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        self._samples = []
        self._running = True
        self._thread  = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()

    def _loop(self) -> None:
        while self._running:
            try:
                w = nvmlDeviceGetPowerUsage(self._handle) / 1000.0
                self._samples.append((time.perf_counter(), w))
            except NVMLError:
                pass
            time.sleep(SAMPLE_INTERVAL_S)

    def compute_energy_j(self) -> float:
        """Trapezoidal integration over collected (perf_counter, watts) samples."""
        if len(self._samples) < 2:
            return 0.0
        total = 0.0
        for i in range(len(self._samples) - 1):
            t1, p1 = self._samples[i]
            t2, p2 = self._samples[i + 1]
            total += (p1 + p2) / 2.0 * (t2 - t1)
        return total

    @property
    def samples(self) -> list[tuple[float, float]]:
        return self._samples


def resolve_nvml_index() -> int:
    """Map the first CUDA_VISIBLE_DEVICES entry to the NVML physical index."""
    cvd = os.environ.get("CUDA_VISIBLE_DEVICES", "")
    first = cvd.split(",")[0].strip()
    return int(first) if first.isdigit() else 0

# ---------------------------------------------------------------------------
# GPU state reset — Danish et al. inference script
# ---------------------------------------------------------------------------

def reset_gpu_state(model: torch.nn.Module) -> None:
    """Clear CUDA caches and collect garbage before each inference run."""
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    gc.collect()
    if hasattr(model, "past_key_values"):
        model.past_key_values = None
    torch.cuda.synchronize()


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

@dataclass
class EnergyRecord:
    """
    Record capturing total inference energy and time from a single generate() call.
    Danish et al. (E-Energy 2026).
    """
    problem_id:          str
    repeat_idx:          int
    tokens_input:        int
    tokens_output:       int
    # time
    time_total_s:        float
    latency_per_token_s: float
    # energy — total window (Danish et al.)
    energy_total_j:      float
    energy_marginal_j:   float
    avg_power_w:         float
    idle_power_w:        float
    # normalised
    energy_per_token_j:  float