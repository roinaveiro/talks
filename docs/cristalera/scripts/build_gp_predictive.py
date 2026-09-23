#!/usr/bin/env python3
"""Exact GP teaching plot, with synthetic data and fixed hyperparameters.

Run with Python, NumPy, SciPy and Matplotlib. Outputs stay in assets/.
"""

import hashlib
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "cristalera-matplotlib"))
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.stats import norm


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SEED = 21
LENGTH_SCALE = 1.15
SIGNAL_SD = 1.2
NOISE_SD = 0.23


def kernel(a, b):
    return SIGNAL_SD**2 * np.exp(-0.5 * ((a[:, None] - b[None, :]) / LENGTH_SCALE)**2)


def main():
    rng = np.random.default_rng(SEED)
    x = np.array([-3.25, -2.9, -2.5, -2.1, -1.7, -1.2, -0.85, 1.35, 1.7, 2.1, 2.55, 3.05])
    y = np.sin(1.2 * x) + 0.25 * np.cos(2.1 * x) + rng.normal(0, NOISE_SD, len(x))
    grid = np.linspace(-5, 5, 501)
    covariance = kernel(x, x) + NOISE_SD**2 * np.eye(len(x))
    factor = cho_factor(covariance, lower=True)
    cross = kernel(grid, x)
    mean = cross @ cho_solve(factor, y)
    variance = SIGNAL_SD**2 - np.einsum("ij,ji->i", cross, cho_solve(factor, cross.T))
    assert np.all(variance > 0), "Latent variance must remain positive."
    latent_sd = np.sqrt(variance)
    predictive_sd = np.sqrt(variance + NOISE_SD**2)
    z = norm.ppf(0.975)

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 20,
        "axes.labelsize": 23, "xtick.labelsize": 19, "ytick.labelsize": 19,
        "text.color": "#253846", "axes.labelcolor": "#004369",
        "axes.edgecolor": "#B6C8CE", "xtick.color": "#617583", "ytick.color": "#617583",
        "axes.spines.top": False, "axes.spines.right": False,
        "svg.fonttype": "path", "svg.hashsalt": "secure-ml-gp-2026",
        "savefig.facecolor": "white",
    })
    fig, ax = plt.subplots(figsize=(13, 4.6))
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.18, top=0.77)
    outer = ax.fill_between(grid, mean-z*predictive_sd, mean+z*predictive_sd,
                            color="#DCE5E9", label="95% new observation")
    inner = ax.fill_between(grid, mean-z*latent_sd, mean+z*latent_sd,
                            color="#83C0C2", alpha=0.9, label="95% latent function")
    line, = ax.plot(grid, mean, color="#004369", linewidth=3, label="Posterior mean")
    dots = ax.scatter(x, y, color="#B3434E", edgecolor="white", linewidth=0.8,
                      s=63, zorder=4, label="Observed data")
    ax.set(xlim=(-5, 5), ylim=(-3.05, 3.05), xlabel="Input $x$", ylabel="Outcome")
    ax.set_xticks([-4, -2, 0, 2, 4])
    ax.set_yticks([-2, 0, 2])
    ax.grid(axis="y", color="#E8EFF1", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.legend([dots, line, inner, outer],
               ["Observed data", "Posterior mean", "95% latent function", "95% new observation"],
               loc="upper center", bbox_to_anchor=(0.54, 1.0), ncol=2, frameon=False,
               fontsize=19, columnspacing=2, handlelength=1.8)
    fig.text(0.98, 0.005, "Gaussian process · synthetic illustration", ha="right",
             fontsize=15, color="#617583")
    svg = ASSETS / "gp-posterior-predictive.svg"
    fig.savefig(svg, metadata={"Date": None, "Description":
        "Exact zero-mean GP with squared-exponential kernel, synthetic observations and fixed hyperparameters. "
        "Pointwise 95% intervals for the latent function and an independent noisy future observation."})
    # PNG preview is useful for inspecting the scientific figure without a browser.
    fig.savefig(Path(tempfile.gettempdir()) / "cristalera-gp-preview.png", dpi=150)
    plt.close(fig)
    provenance = {
        "asset": svg.name, "type": "synthetic teaching illustration",
        "generator": "scripts/build_gp_predictive.py", "seed": SEED,
        "prior_mean": 0, "kernel": "squared exponential",
        "length_scale": LENGTH_SCALE, "signal_sd": SIGNAL_SD, "observation_sd": NOISE_SD,
        "hyperparameters": "fixed, not fitted or integrated out",
        "x": x.tolist(), "y": y.tolist(),
        "data_mean_function": "sin(1.2*x) + 0.25*cos(2.1*x)",
        "intervals": "pointwise 95%, not simultaneous bands",
        "predictive_variance": "latent posterior variance + observation_sd**2",
        "sha256": hashlib.sha256(svg.read_bytes()).hexdigest(),
    }
    (ASSETS / "gp-posterior-predictive-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(f"Wrote {svg}")


if __name__ == "__main__":
    main()
