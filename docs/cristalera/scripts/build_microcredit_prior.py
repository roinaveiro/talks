#!/usr/bin/env python3
"""Plot the actual treatment-effect prior in the microcredit attack study.

Run from any directory with numpy, scipy, and matplotlib installed. This plots
the stated Student-t distribution, not a fitted empirical density or synthetic
normal approximation. It does not change any other figure assets.
"""

from pathlib import Path
import hashlib
import json
import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "cristalera-matplotlib"))
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUTPUT = ASSETS / "microcredit-study-prior.svg"
PARAMETERS = {"df": 3, "loc": 0, "scale": 1000}
LIMITS = [-5000, 5000]


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 22,
        "axes.labelsize": 24,
        "axes.titlesize": 29,
        "xtick.labelsize": 22,
        "ytick.labelsize": 21,
        "text.color": "#004369",
        "axes.labelcolor": "#004369",
        "axes.edgecolor": "#DCE5E9",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": "#607482",
        "ytick.color": "#607482",
        "axes.labelpad": 13,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "svg.fonttype": "path",
        "svg.hashsalt": "secure-ml-microcredit-study-prior-2026",
    })
    distribution = t(**PARAMETERS)
    x = np.linspace(*LIMITS, 3001)
    density = distribution.pdf(x)
    fig, ax = plt.subplots(figsize=(12, 6.8))
    fig.subplots_adjust(left=0.14, right=0.98, bottom=0.22, top=0.76)
    ax.fill_between(x, density, color="#004369", alpha=0.10)
    ax.plot(x, density, color="#004369", linewidth=3.7)
    ax.axvline(0, color="#607482", linestyle="--", linewidth=1.3, alpha=0.6)
    ax.set_xlim(*LIMITS)
    ax.set_ylim(0, 0.000405)
    ax.set_xticks([-5000, -2500, 0, 2500, 5000])
    ax.set_yticks([0, 0.0002, 0.0004])
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
    ax.set_xlabel(r"$\beta_1$: effect on profit (analysis units)")
    ax.set_ylabel("Prior density")
    fig.text(0.14, 0.92, r"$\beta_1 \sim t_3(0,\,1000)$", fontsize=31)
    fig.text(0.14, 0.84, "Location 0  |  Scale 1000", fontsize=23, color="#607482")
    fig.savefig(OUTPUT, bbox_inches="tight", pad_inches=0.15, metadata={
        "Date": None,
        "Title": "Microcredit treatment-effect prior",
        "Description": "Actual beta_1 prior from Carreau, Naveiro and Caballero (2025), Section 6.3: Student-t with 3 degrees of freedom, location 0, scale 1000. The horizontal axis uses the analysis profit units; plotted window -5000 to 5000. The distribution has unbounded support.",
    })
    plt.close(fig)
    provenance = {
        "asset": OUTPUT.name,
        "paper": "Poisoning Bayesian Inference via Data Deletion and Replication",
        "paper_source": "https://arxiv.org/html/2503.04480v1#S6.SS3",
        "paper_section": "6.3 Case Study: Mexico Microcredit",
        "code_source": "https://github.com/Matthieu-Carreau/Poisoning_Bayesian_Inference/blob/main/src/studentT_prior_lin_reg.py",
        "data_preprocessing_source": "https://github.com/Matthieu-Carreau/Poisoning_Bayesian_Inference/blob/main/notebooks/microcredit.ipynb",
        "distribution": "Student-t",
        "parameter": "beta_1",
        "parameters": PARAMETERS,
        "parameter_convention": "df is degrees of freedom; loc is location; scale is the multiplicative Student-t scale, not a standard deviation or variance.",
        "method": "Evaluate the stated prior density using scipy.stats.t.pdf. No empirical data were fitted or approximated.",
        "axis_units": "Profit units used in the attack analysis. The notebook multiplies the Q10_9_toprof field by 0.1026493 after imputing missing outcomes with zero.",
        "plot_window": LIMITS,
        "probability_in_plot_window": float(distribution.cdf(LIMITS[1]) - distribution.cdf(LIMITS[0])),
        "support": "All real numbers; the displayed window does not truncate or renormalize the prior.",
        "script": "scripts/build_microcredit_prior.py",
        "source_verified": "2026-09-16",
        "asset_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    }
    (ASSETS / "microcredit-study-prior-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(f"Created {OUTPUT.name}: Student-t(df=3, loc=0, scale=1000)")


if __name__ == "__main__":
    main()
