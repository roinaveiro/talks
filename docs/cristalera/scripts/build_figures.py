#!/usr/bin/env python3
"""Build the portable figure assets for the Secure Machine Learning lecture.

Run from any directory. Requires numpy, scipy, matplotlib, and pymupdf.
Raster source files are copied byte for byte. Scientific PDF figures retain
their complete first page and are converted to SVG paths, without redrawing.
Only the explicitly illustrative teaching figures are newly plotted.
"""

from __future__ import annotations

import hashlib
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "cristalera-matplotlib"))
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import fitz


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY = "#004369"
TEAL = "#1C7984"
RED = "#B3434E"
GOLD = "#B58A39"
MUTED = "#607482"
PALE = "#DCE5E9"

RASTER_SOURCES = {
    "doc.jpg": "../poisoning_bayes/images/doc.jpg",
    "microcredit-clean.jpeg": "../poisoning_bayes/images/posterior_treatment_effect.jpeg",
    "microcredit-attacked.jpeg": "../poisoning_bayes/images/tainted_posterior_treatment_effect.jpeg",
    "microcredit-comparison.jpeg": "../poisoning_bayes/images/microcredit1.jpeg",
    "digit-clean.png": "../aml_comillas/images/7_clean.png",
    "digit-pgd.png": "../aml_comillas/images/7_pgd.png",
    "digit-entropy.png": "../aml_comillas/images/7_ent.png",
    "pred-clean.png": "../aml_comillas/images/clean.png",
    "pred-pgd.png": "../aml_comillas/images/pgd.png",
    "pred-entropy.png": "../aml_comillas/images/ent.png",
    "uncertainty.webp": "../aml_comillas/images/sin_ppd.webp",
    "baseline-examples.png": "context/adv_bayes_tmlr/images/training/MNIST_examples.png",
    "baseline-preds.png": "context/adv_bayes_tmlr/images/training/MNIST_preds.png",
    "protected-examples.png": "context/adv_bayes_tmlr/images/training/MNIST_newlosses_examples.png",
    "protected-preds.png": "context/adv_bayes_tmlr/images/training/MNIST_newlosses_preds.png",
    "defense-pgd.png": "context/adv_bayes_tmlr/images/filled/SEP_pgd.png",
    "defense-pgd-plus.png": "context/adv_bayes_tmlr/images/filled/SEP_pgd_plus.png",
    "defense-selective.png": "context/adv_bayes_tmlr/images/filled/SEP_sel_acc.png",
}
PDF_SOURCES = {
    "spatial-map.svg": "context/mmd/figs/spatial_lm/spatial_mean_attacks_selected_attack_map.pdf",
    "spatial-posteriors.svg": "context/mmd/figs/spatial_lm/spatial_mean_attacks_all_beta_posteriors.pdf",
    "spatial-budget.svg": "context/mmd/figs/spatial_lm/spatial_mean_attacks_budget_vs_achieved_posterior_mean.pdf",
    "radon-gap.svg": "context/mmd/figs/radon_lake_utility_gap_posterior.pdf",
    "radon-counties.svg": "context/mmd/figs/radon_county_expected_health_cost.pdf",
    "radon-decomposition.svg": "context/mmd/figs/radon_lake_cost_decomposition.pdf",
    "radon-deletions.svg": "context/mmd/figs/radon_deleted_observations.pdf",
}
REMOTE_SOURCES = {
    "evasion-selective.png": "https://arxiv.org/html/2506.09640v1/img/mnist/10bnnvi/acc_reject.png",
    "evasion-entropy-density.png": "https://arxiv.org/html/2506.09640v1/img/mnist/10bnnvi/baseline.png",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_assets() -> dict:
    manifest = {}
    for target, relative in RASTER_SOURCES.items():
        source = ROOT / relative
        output = ASSETS / target
        shutil.copyfile(source, output)
        assert digest(source) == digest(output), target
        manifest[target] = {"source": relative, "method": "byte-for-byte copy", "sha256": digest(output)}
    for target, relative in PDF_SOURCES.items():
        with fitz.open(ROOT / relative) as document:
            assert len(document) == 1, f"Expected one complete figure page: {relative}"
            page = document[0]
            # Outlined PDF fonts ensure the complete scientific figure renders
            # correctly without installing the manuscript's fonts.
            (ASSETS / target).write_text(page.get_svg_image(text_as_path=True), encoding="utf-8")
            manifest[target] = {
                "source": relative,
                "method": "complete PDF page to SVG; text outlined; no crop or redrawing",
                "source_sha256": digest(ROOT / relative),
                "width_pt": page.rect.width,
                "height_pt": page.rect.height,
            }
    return manifest


def extract_template() -> dict:
    template = ROOT / "AIHUB2026_EscuelaVerano_Template_v4.pptx"
    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }
    with zipfile.ZipFile(template) as archive:
        artwork = archive.read("ppt/media/image1.png")
        (ASSETS / "template-network.png").write_bytes(artwork)
        layout = {"source": template.name, "width_emu": 9144000, "height_emu": 5143500, "slides": {}}
        for number in (1, 8):
            root = ET.fromstring(archive.read(f"ppt/slides/slide{number}.xml"))
            shapes = []
            for shape in root.findall(".//p:sp", ns) + root.findall(".//p:pic", ns):
                transform = shape.find("p:spPr/a:xfrm", ns)
                offset, extent = transform.find("a:off", ns), transform.find("a:ext", ns)
                text = " | ".join(t.text or "" for t in shape.findall(".//a:t", ns))
                box = [int(offset.get("x")), int(offset.get("y")), int(extent.get("cx")), int(extent.get("cy"))]
                fonts = [float(r.get("sz")) / 100 for r in shape.findall(".//a:rPr", ns) if r.get("sz")]
                shapes.append({
                    "text": text,
                    "kind": "picture" if shape.tag.endswith("pic") else "shape",
                    "box_emu": box,
                    "box_percent": [100 * x / d for x, d in zip(box, [9144000, 5143500, 9144000, 5143500])],
                    "font_sizes_pt": fonts,
                })
            layout["slides"][str(number)] = shapes
        (ASSETS / "template-layout.json").write_text(json.dumps(layout, indent=2) + "\n", encoding="utf-8")
    return {"source": f"{template.name}:ppt/media/image1.png", "method": "unchanged ZIP member extraction", "sha256": hashlib.sha256(artwork).hexdigest()}


def style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 22,
        "axes.labelsize": 23,
        "axes.titlesize": 26,
        "axes.titleweight": "bold",
        "xtick.labelsize": 22,
        "ytick.labelsize": 22,
        "legend.fontsize": 22,
        "text.color": NAVY,
        "axes.labelcolor": NAVY,
        "axes.edgecolor": PALE,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.titlepad": 18,
        "axes.labelpad": 12,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "svg.fonttype": "path",
        "svg.hashsalt": "secure-ml-cristalera-2026",
    })


def save(fig: plt.Figure, filename: str, description: str) -> None:
    fig.savefig(ASSETS / filename, bbox_inches="tight", pad_inches=0.22, metadata={"Date": None, "Description": description})
    plt.close(fig)


def footer(fig: plt.Figure, label: str = "Illustration", y: float = 0.005) -> None:
    fig.text(0.99, y, label, ha="right", va="bottom", color=MUTED, fontsize=22)


def bayes_sequence() -> dict:
    x = np.linspace(-20, 20, 1601)
    prior_mean, prior_sd, estimate, se = 0.0, 8.0, 3.0, 3.0
    posterior_var = 1 / (prior_sd ** -2 + se ** -2)
    posterior_mean = posterior_var * (prior_mean / prior_sd**2 + estimate / se**2)
    posterior_sd = np.sqrt(posterior_var)
    curves = [norm.pdf(x, prior_mean, prior_sd), norm.pdf(x, estimate, se), norm.pdf(x, posterior_mean, posterior_sd)]
    labels = ["Prior", "Likelihood (scaled)", "Posterior"]
    colors = [NAVY, GOLD, TEAL]
    titles = ["What seemed plausible before the data?", "Which values explain the data?", "Update, then keep the uncertainty"]
    names = ["bayes-prior.svg", "bayes-likelihood.svg", "bayes-posterior.svg"]
    for stage, name in enumerate(names):
        fig, ax = plt.subplots(figsize=(12.0, 5.8))
        fig.subplots_adjust(left=0.13, right=0.99, bottom=0.23, top=0.84)
        for index in range(stage + 1):
            color = colors[index] if index == stage else ["#A6BDC8", "#D9C29A", "#A5C9CD"][index]
            ax.plot(x, curves[index], lw=4 if index == stage else 2.5, color=color, label=labels[index], zorder=3)
            if index == stage:
                ax.fill_between(x, 0, curves[index], color=["#E6EDF0", "#F5F0E6", "#E8F1F2"][index], zorder=1)
        ax.axvline(0, color=PALE, lw=1.4, zorder=0)
        ax.set(xlim=(-20, 20), ylim=(0, 0.155), xticks=[-20, -10, 0, 10, 20], yticks=[0, 0.05, 0.1, 0.15])
        ax.set_xlabel(r"Treatment effect $\beta$")
        ax.set_ylabel("Density" if stage == 0 else "Density / support")
        ax.set_title(titles[stage], loc="left")
        ax.legend(loc="upper left", frameon=False, handlelength=1.7, borderaxespad=0.3)
        footer(fig)
        save(fig, name, "Illustration: normal prior N(0,8^2), likelihood proportional to N(3,3^2), and exact conjugate normal posterior. Common axes across the three figures. The likelihood is rescaled for visual comparison.")
    return {"prior_mean": prior_mean, "prior_sd": prior_sd, "likelihood_estimate": estimate, "likelihood_standard_error": se, "posterior_mean": float(posterior_mean), "posterior_sd": float(posterior_sd)}


def predictive() -> None:
    rng = np.random.default_rng(14)
    observed_x = np.linspace(-1.0, 1.0, 9)
    noise_sd = 0.55
    observed_y = 0.3 + 0.65 * observed_x + rng.normal(0, noise_sd, size=observed_x.size)
    X = np.column_stack([np.ones_like(observed_x), observed_x])
    prior_cov = np.diag([4.0, 4.0])
    cov = np.linalg.inv(np.linalg.inv(prior_cov) + X.T @ X / noise_sd**2)
    mean = cov @ X.T @ observed_y / noise_sd**2
    grid = np.linspace(-3, 3, 301)
    Z = np.column_stack([np.ones_like(grid), grid])
    fmean = Z @ mean
    fsd = np.sqrt(np.einsum("ij,jk,ik->i", Z, cov, Z))
    ysd = np.sqrt(fsd**2 + noise_sd**2)
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.22, top=0.82)
    ax.fill_between(grid, fmean - 1.96 * ysd, fmean + 1.96 * ysd, color="#E6EDF0", label="New outcome: 95% interval")
    ax.fill_between(grid, fmean - 1.96 * fsd, fmean + 1.96 * fsd, color="#BAD3D6", label="Mean function: 95% interval")
    ax.plot(grid, fmean, color=TEAL, lw=3)
    ax.scatter(observed_x, observed_y, s=65, color=NAVY, edgecolors="white", zorder=4)
    ax.set(xlim=(-3, 3), ylim=(-5.3, 5.8), xticks=[-3, -1, 1, 3], yticks=[-4, -2, 0, 2, 4], xlabel="Input x", ylabel="Outcome y")
    ax.set_title("Uncertain function, noisy outcomes", loc="left")
    ax.legend(loc="upper left", frameon=False, handlelength=1.5)
    footer(fig, "Illustration · synthetic linear data")
    save(fig, "posterior-predictive.svg", "Illustration with synthetic data, random seed 14. Exact Gaussian linear regression with known observation SD=0.55 and N(0,4I) coefficient prior. Pointwise 95% posterior intervals for the mean and posterior predictive intervals for a new noisy observation.")


def same_mean() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.4), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.25, top=0.77, wspace=0.20)
    for ax, values, color, title, downside in zip(axes, [[0.5, 1.5], [-1, 3]], [TEAL, RED], ["Concentrated uncertainty", "Wider uncertainty"], ["P(effect < 0) = 0", "P(effect < 0) = 0.5"]):
        ax.axvline(1, ls="--", color=GOLD, lw=2, zorder=0)
        ax.vlines(values, 0, 0.5, color=color, lw=5)
        ax.scatter(values, [0.5, 0.5], s=160, color=color, zorder=3)
        ax.axvspan(-1.65, 0, color="#FCF7F7", zorder=0)
        ax.set(xlim=(-1.65, 3.65), ylim=(0, 0.64), xticks=[-1, 0, 1, 2, 3], yticks=[0, 0.5], xlabel="Treatment effect")
        ax.set_title(title, fontsize=23)
        ax.text(0.5, 0.9, downside, transform=ax.transAxes, ha="center", fontsize=22, color=color)
    axes[0].set_ylabel("Probability")
    fig.suptitle("Same expected effect: 1. Different downside risk.", fontsize=26, fontweight="bold", x=0.1, ha="left", y=0.98)
    footer(fig, "Illustration · two equally likely outcomes")
    save(fig, "same-mean-risk.svg", "Illustration: two discrete distributions with equal mean 1. Distribution A assigns probability 0.5 to each of 0.5 and 1.5; distribution B assigns probability 0.5 to each of -1 and 3. Their probabilities of a negative effect are 0 and 0.5, respectively. Dotted vertical lines mark mean 1.")


def microcredit_decision() -> None:
    fig, ax = plt.subplots(figsize=(12.0, 5.6))
    fig.subplots_adjust(left=0.21, right=0.96, bottom=0.25, top=0.74)
    values = [-6.71, 4.28]
    ys = [1, 0]
    ax.barh(ys, values, height=0.45, color=[TEAL, RED])
    ax.axvline(0, color=NAVY, linewidth=2)
    for y, value in zip(ys, values):
        ax.text(value + (-0.3 if value < 0 else 0.3), y, f"{value:+.2f}", ha="right" if value < 0 else "left", va="center", fontsize=26, fontweight="bold")
    ax.set(xlim=(-9, 6.5), ylim=(-0.7, 1.7), yticks=ys, yticklabels=["Clean data", "Attacked data"], xticks=[-8, -4, 0, 4], xlabel="Expected utility of expansion")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=12)
    fig.suptitle("Expand only when expected utility is positive", x=0.21, ha="left", y=0.99, fontsize=24, fontweight="bold")
    fig.text(0.21, 0.85, "No expansion: utility 0", fontsize=22, color=MUTED)
    footer(fig, "Illustrative utility · published posterior means")
    save(fig, "microcredit-decision.svg", "Illustrative decision model applied to published microcredit posterior means -4.71 and +6.28. Expansion utility equals treatment effect minus illustrative cost 2, hence expected utilities -6.71 and +4.28. No expansion has utility zero. This is not an observed policy decision.")


def radon_decision() -> None:
    fig, ax = plt.subplots(figsize=(12.0, 5.5))
    fig.subplots_adjust(left=0.23, right=0.97, bottom=0.26, top=0.77)
    ax.axvline(2000, color=GOLD, lw=3, ls="--", zorder=0)
    ax.hlines([1, 0], 1750, [2188, 1988], color=["#B6D2D5", "#E8C9CD"], lw=3)
    ax.scatter([2188, 1988], [1, 0], s=230, color=[TEAL, RED], zorder=3)
    ax.text(2188, 1.17, "2188", ha="center", va="bottom", fontsize=27, color=TEAL, fontweight="bold")
    ax.text(1988, -0.18, "1988", ha="center", va="top", fontsize=27, color=RED, fontweight="bold")
    ax.text(2000, 1.60, "Remediation cost: 2000", ha="center", color=GOLD, fontsize=23)
    ax.set(xlim=(1740, 2330), ylim=(-0.62, 1.92), xticks=[1800, 2000, 2200], yticks=[1, 0], yticklabels=["Clean data", "Six deletions"], xlabel="Posterior predictive expected exposure cost")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=12)
    ax.set_title("Lake County crosses the decision threshold", loc="left", fontsize=24)
    footer(fig, "Illustrative costs · rounded manuscript values")
    save(fig, "radon-decision.svg", "A new chart of the manuscript's rounded posterior predictive expected exposure costs: 2188 before and 1988 after six deletions outside Lake County. The illustrative remediation threshold is 2000. Source figure radon_lake_utility_gap_posterior.pdf has slightly different run annotations (179.9 and -11.4 utility gaps); this chart deliberately uses the manuscript narrative values and is not a reconstruction of that posterior curve.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download-remote", action="store_true", help="Download the two unchanged UAI paper figure images using curl.")
    args = parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    manifest = source_assets()
    manifest["template-network.png"] = extract_template()
    for name, url in REMOTE_SOURCES.items():
        if args.download_remote:
            subprocess.run(["curl", "-L", "--fail", url, "-o", str(ASSETS / name)], check=True)
        if (ASSETS / name).exists():
            manifest[name] = {"source": url, "method": "unchanged download of published figure", "sha256": digest(ASSETS / name)}
        else:
            print(f"Optional published asset missing: {name}. Run with --download-remote to retrieve it.")
    style()
    parameters = bayes_sequence()
    predictive()
    same_mean()
    microcredit_decision()
    radon_decision()
    for name in ["bayes-prior.svg", "bayes-likelihood.svg", "bayes-posterior.svg", "posterior-predictive.svg", "same-mean-risk.svg", "microcredit-decision.svg", "radon-decision.svg"]:
        manifest[name] = {"source": "scripts/build_figures.py", "method": "new scientific teaching plot; explicitly labeled illustrative", "sha256": digest(ASSETS / name)}
    (ASSETS / "asset-manifest.json").write_text(json.dumps({"assets": manifest, "normal_normal_illustration": parameters}, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(manifest)} visual assets in {ASSETS}")


if __name__ == "__main__":
    main()
