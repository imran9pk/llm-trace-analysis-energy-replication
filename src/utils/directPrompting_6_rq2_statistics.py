"""
directPrompting_6_rq2_statistics.py

RQ2 (Efficiency of Trace Data Format): the numbers used in the paper,
from output_processed/analysis/instance_level.csv.gz (directPrompting_4_build_instance_table.py).
Energy = energy_marginal_j (GPU energy of the generate() call minus the
idle power of the job times the duration of the call). All instances are used.

How the numbers are computed, for one model and one format:
  mean   = sum over the 9,120 instances of the per-instance value / 9,120
           (value = marginal energy, input tokens or output tokens).
  change = mean of the format / mean of JSON (same model) - 1.
           Every format of a model covers the same 9,120 instances, so this
           is also the change of the total over the whole test set.

Writes (under output_processed/analysis/):
  RQ2_energy.csv
      Per model and format: instances, mean input tokens, mean output
      tokens, mean and total energy, and the change of each mean with
      respect to JSON for the same model (d_tokens_in, d_tokens_out, d_energy).
  RQ2_energy_per_token.csv
      Per model, a least squares fit of the energy of a call on its input and
      output tokens over all instances and formats: the energy per input token,
      the energy per output token, their ratio, the intercept and R^2.

Usage:
    python directPrompting_6_rq2_statistics.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from utils_config import FORMATS, MODELS  # noqa: E402

ANALYSIS_DIR = SCRIPT_DIR.parent.parent / "output_processed" / "analysis"
INPUT_FILE = ANALYSIS_DIR / "instance_level.csv.gz"
BASELINE = "JSON"
MEASURES = {"tokens_in": "tokens_input", "tokens_out": "tokens_output", "energy": "energy_marginal_j"}


def energy_per_token(df: pd.DataFrame) -> pd.DataFrame:
    """Per model: energy = intercept + a * input tokens + b * output tokens (ordinary least squares,
    all instances and formats pooled). b / a tells how much more a generated token costs than a read one."""
    rows = []
    for model in [m for m in MODELS if m in set(df.model)]:
        dm = df[df.model == model]
        X = np.c_[np.ones(len(dm)), dm.tokens_input.to_numpy(float), dm.tokens_output.to_numpy(float)]
        y = dm.energy_marginal_j.to_numpy(float)
        coef = np.linalg.lstsq(X, y, rcond=None)[0]
        r2 = 1 - ((y - X @ coef) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        rows.append({"model": model, "instances": len(dm), "intercept_j": coef[0],
                     "j_per_input_token": coef[1], "j_per_output_token": coef[2],
                     "output_to_input_ratio": coef[2] / coef[1], "r2": r2})
    return pd.DataFrame(rows)


def main() -> None:
    if not INPUT_FILE.exists():
        print(f"skip: {INPUT_FILE} not found (run directPrompting_4_build_instance_table.py first)")
        return
    df = pd.read_csv(INPUT_FILE)
    df = df[df.model.isin(MODELS) & df.format.isin(FORMATS)]

    rows = []
    for model in [m for m in MODELS if m in set(df.model)]:
        dm = df[df.model == model]
        means = dm.groupby("format")[list(MEASURES.values())].mean()
        for fmt in [f for f in FORMATS if f in means.index]:
            sub = dm[dm.format == fmt]
            row = {"model": model, "format": fmt, "instances": len(sub),
                   "tokens_in_mean": means.loc[fmt, "tokens_input"],
                   "tokens_out_mean": means.loc[fmt, "tokens_output"],
                   "energy_mean_j": means.loc[fmt, "energy_marginal_j"],
                   "energy_total_j": sub.energy_marginal_j.sum()}
            if fmt != BASELINE and BASELINE in means.index:
                # Same instances in every format -> change of the mean = change of the total.
                for key, col in MEASURES.items():
                    row[f"d_{key}"] = means.loc[fmt, col] / means.loc[BASELINE, col] - 1
            rows.append(row)
    energy = pd.DataFrame(rows)
    energy.to_csv(ANALYSIS_DIR / "RQ2_energy.csv", index=False)

    per_token = energy_per_token(df)
    per_token.to_csv(ANALYSIS_DIR / "RQ2_energy_per_token.csv", index=False)
    print(per_token.round(4).to_string(index=False))

    pd.set_option("display.width", 200)
    print(energy.round(3).to_string(index=False))
    print(f"\nSaved RQ2 numbers to {ANALYSIS_DIR}")


if __name__ == "__main__":
    main()
