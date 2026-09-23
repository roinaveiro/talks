# Figure assets and provenance

These files support the Secure Machine Learning lecture. They are copied into
the presentation directory so the deck does not depend on neighboring talks.

## Optional figure regeneration

The included assets are ready to use with `quarto render`. Run the script below
only when you want to regenerate figures from their original sources.

Requirements: Python, NumPy, SciPy, Matplotlib, and PyMuPDF (`pymupdf`).

```bash
python scripts/build_figures.py
```

The first build requires the original neighboring talks and local manuscripts.
Those sources are unnecessary for rendering or viewing the presentation. The two
published UAI images are already included; to download them again:

```bash
python scripts/build_figures.py --download-remote
```

`asset-manifest.json` records individual source paths, transformations, checksums,
and parameters for the normal–normal illustration. `template-layout.json`
records exact first/last PowerPoint shape positions in EMU and percentages.

## Unchanged raster sources

Raster images are copied byte for byte; they have not been recolored, cropped,
retouched, or upscaled. Checksums are verified during the build.

| Assets | Original source |
|---|---|
| `doc.jpg` | `../poisoning_bayes/images/doc.jpg` |
| `microcredit-clean.jpeg` | `../poisoning_bayes/images/posterior_treatment_effect.jpeg` |
| `microcredit-attacked.jpeg` | `../poisoning_bayes/images/tainted_posterior_treatment_effect.jpeg` |
| `microcredit-comparison.jpeg` | `../poisoning_bayes/images/microcredit1.jpeg` |
| `digit-clean.png`, `digit-pgd.png`, `digit-entropy.png` | `../aml_comillas/images/7_clean.png`, `7_pgd.png`, `7_ent.png` |
| `pred-clean.png`, `pred-pgd.png`, `pred-entropy.png` | `../aml_comillas/images/clean.png`, `pgd.png`, `ent.png` |
| `uncertainty.webp` | `../aml_comillas/images/sin_ppd.webp` |
| `baseline-examples.png`, `baseline-preds.png` | `context/adv_bayes_tmlr/images/training/MNIST_examples.png`, `MNIST_preds.png` |
| `protected-examples.png`, `protected-preds.png` | `context/adv_bayes_tmlr/images/training/MNIST_newlosses_examples.png`, `MNIST_newlosses_preds.png` |
| `defense-pgd.png`, `defense-pgd-plus.png`, `defense-selective.png` | `context/adv_bayes_tmlr/images/filled/SEP_pgd.png`, `SEP_pgd_plus.png`, `SEP_sel_acc.png` |
| `template-network.png` | Exact `ppt/media/image1.png` ZIP member of `AIHUB2026_EscuelaVerano_Template_v4.pptx` |

Published UAI paper images, downloaded unchanged:

- [`evasion-selective.png`](https://arxiv.org/html/2506.09640v1/img/mnist/10bnnvi/acc_reject.png): selective prediction plot, Figure 4d.
- [`evasion-entropy-density.png`](https://arxiv.org/html/2506.09640v1/img/mnist/10bnnvi/baseline.png): predictive-entropy distributions.

Both belong to *Evasion Attacks Against Bayesian Predictive Models*, Arce,
Naveiro and Ríos Insua, UAI 2025. Its unfamiliar-image experiment uses notMNIST;
the later defense manuscript uses FashionMNIST in its selective-prediction
experiment. Keep this distinction in captions. Attacks against different
defenses are optimized separately, even when their original clean images match.

## Scientific PDFs converted to SVG

The complete page is preserved, including axes, legends, titles, and annotations.
PyMuPDF converts text to vector outlines so the scientific fonts remain portable.
These figures have not been redrawn or reinterpreted. All are from the unpublished
local *Posterior Attraction via Moment Matching* manuscript.

| Asset | Source under `context/mmd/figs/` |
|---|---|
| `spatial-map.svg` | `spatial_lm/spatial_mean_attacks_selected_attack_map.pdf` |
| `spatial-posteriors.svg` | `spatial_lm/spatial_mean_attacks_all_beta_posteriors.pdf` |
| `spatial-budget.svg` | `spatial_lm/spatial_mean_attacks_budget_vs_achieved_posterior_mean.pdf` |
| `radon-gap.svg` | `radon_lake_utility_gap_posterior.pdf` |
| `radon-counties.svg` | `radon_county_expected_health_cost.pdf` |
| `radon-decomposition.svg` | `radon_lake_cost_decomposition.pdf` |
| `radon-deletions.svg` | `radon_deleted_observations.pdf` |

### Bayesian orchestration: original paper panel

`orchestration-paper.svg` is Figure 1(a) from page 6 of
[Papamarkou et al., v2](https://arxiv.org/pdf/2605.00742v2).
The panel was extracted from the original PDF as vectors, with text converted to
outlines. Its labels and data are unchanged. The exact crop and checksums are in
`orchestration-paper-provenance.json`. This supplied asset is independent of the
optional local-figure regeneration script.

The Comillas illustration `uncertainty.webp` remains available with its original interval label. The current Bayesian prediction slide uses `gp-posterior-predictive.svg` to distinguish uncertainty about a latent function from variation in a new observation. The older linear-regression illustration `posterior-predictive.svg` remains available.

### Radon annotations differ from the manuscript narrative

The available utility-gap PDF labels its clean mean **179.9** and attacked mean
**−11.4**, corresponding to expected exposure costs **2179.9** and **1988.6**
when the remediation cost is 2000. The manuscript narrative instead reports
approximately **2188** and **1988**. The decomposition PDF labels **2156**,
**−142**, **−52**, and **1962**; those values also differ from the narrative's
approximate location/variation reductions of 147 and 53.

The main deck now uses the original radon figures and quotes their annotations consistently. The older teaching chart `radon-decision.svg` is retained as an unused asset and uses the rounded manuscript values. The source discrepancy remains unresolved. The plug-in decomposition is a different quantity from the posterior integrated expected cost in either case.

### Spatial source figures

The currently supplied spatial posterior figure has a clean flooding-effect curve consistent with the manuscript's mean 0.43. The earlier note about a curve near 0.7 does not describe the current file. `spatial-flooding-panel.svg` extracts the original FFREQ panel, including its axes and curves; the slide supplies the shared gray/blue legend. The complete original figure remains in `spatial-posteriors.svg`. The target is zero, with 20/152 deletions.

## New teaching figures

These are scientific plots generated by `scripts/build_figures.py`, not empirical
reconstructions of published posterior curves. All labels are at least 22 pt in
the original figure. The navy/teal/red/gold palette is consistent with the deck.

| Asset | Exact content and limits |
|---|---|
| `bayes-prior.svg` | Illustrative normal prior: mean 0, standard deviation 8. |
| `bayes-likelihood.svg` | Adds a normal likelihood with estimate 3, standard error 3, rescaled to integrate to one for plotting. |
| `bayes-posterior.svg` | Exact normal conjugate update: mean 192/73 ≈ 2.6301; standard deviation √(576/73) ≈ 2.8090. All three plots use the same grid −20 to 20 and the same axes. |
| `posterior-predictive.svg` | Synthetic Gaussian linear regression (seed 14), N(0,4I) coefficient prior, known observation SD 0.55, nine synthetic observations. Shows pointwise 95% intervals for the mean function and a new noisy observation. |
| `same-mean-risk.svg` | Two exact discrete distributions: equal masses at 0.5 and 1.5 versus equal masses at −1 and 3. Both have mean 1; probabilities of a negative effect are 0 and 0.5. No smooth fitted distributions are implied. |
| `microcredit-decision.svg` | Illustrative expansion utility = effect − 2; no-expansion utility = 0. Applied to published posterior means −4.71 and +6.28, expected expansion utilities become −6.71 and +4.28. This is a teaching decision model, not a historical policy decision. |
| `radon-decision.svg` | Manuscript's rounded expected exposure costs, 2188 and 1988, against illustrative remediation cost 2000. This chart displays a modeled decision threshold, not a newly fitted posterior or medical advice. |

The synthetic Bayesian illustrations are explicitly labeled “Illustration.”
The microcredit and radon charts label their illustrative utility/cost models.
The research examples remain separate from these invented teaching models.

## Original defense graphical models

`defense-reactive-dag-original.svg` and `defense-proactive-dag-original.svg` are unchanged vector panels from Figures 1 and 2 of `context/adv_bayes_tmlr/main.pdf`, pages 4 and 7. The extractions preserve every node, arrow, label, and observed-node shading. Text is converted to outlines for portability.

Exact page crops, source-PDF and TeX checksums, and asset checksums are in `defense-dags-original-provenance.json`. These figures are supplied assets; the optional teaching-figure regeneration script does not recreate them.

## PowerPoint layout

The template is 9,144,000 × 5,143,500 EMU, equivalent to 720 × 405 points (16:9).
The first and last slides share navy `#004369`, a teal `#1C7984` stripe occupying
0.8% of the slide width, and the unmodified network image at:

- Left 62.1998%, top 6.4001%, width 32.6999%, height 87.1998%.

Contact dots are `#982825`. Main template text is white, using Calibri; the
closing question uses `#CCCCCC`. The exact shape rectangles and font sizes for
both slides are in `template-layout.json`. At a 1280 × 720 slide size, a font
size in template points scales by 1280/720 ≈ 1.7778.

## Opening TODO revision: source assets

- `huggingface-logo.svg`: unchanged official brand asset; source and checksum in `huggingface-logo-provenance.json`.
- `orchestration-paper-title.png`: title and full author list, directly cropped from page 1 of Papamarkou et al., v2. Crop coordinates and checksums in `orchestration-title-provenance.json`.
- `orchestration-paper-title-short.png`: title and first three complete author rows, used on the slide to leave room for the explanation. Direct PDF crop documented in `orchestration-title-short-provenance.json`.
- `microcredit-study-prior.svg`: the actual marginal prior specified in the attack analysis, Student-t(df=3, location=0, scale=1000), with beta_1 and analysis profit units on the axis. Regenerate with `python scripts/build_microcredit_prior.py` (NumPy, SciPy, Matplotlib). Its provenance JSON links the paper, authors' code, and preprocessing notebook. This plots a stated prior; it does not fit empirical observations.

The opening now uses that Student-t prior and the original empirical posterior. The older normal prior/likelihood/posterior teaching figures remain available but are no longer used in the opening.

## September 21 slide additions

- `bayes2.png`: speaker-supplied illustration of Bayes wearing a red carnation, with Madrid landmarks. Used unchanged on the Bayesian update slide.
- `intrusion-anticlimax.png`: fictional cartoon generated with the built-in image-generation tool. Two exhausted robot burglars realize they already hold the flag. It illustrates the anticlimax, not the real incident. The complete prompt is in `intrusion-anticlimax-prompt.txt`.
- `sonora-hermosillo.jpg`: *Panarama de Hermosillo, Sonora al atardecer*, México en Fotos, A.C., 3 January 2022. [Wikimedia Commons source](https://commons.wikimedia.org/wiki/File:Panarama_de_Hermosillo,_Sonora_al_atardecer.jpg), [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/). The supplied 1280-pixel derivative is unchanged, without cropping or retouching. This is a geographical illustration, not a photograph of trial participants or a documented trial site.
- `gp-posterior-predictive.svg`: exact Gaussian-process conditioning on 12 synthetic observations, with a zero-mean squared-exponential prior and fixed hyperparameters. Teal shows pointwise 95% latent-function intervals; the wider gray band adds noise variance for a future observation. Regenerate using `scripts/build_gp_predictive.py`. Parameters, observations and checksum are in `gp-posterior-predictive-provenance.json`.

## Updated poisoning stories

- `data-poisoning-villain.png`: fictional editorial cartoon generated with the built-in image-generation tool. It illustrates deletion and replication of records; no experiment is depicted. The complete prompt is saved in `data-poisoning-villain-prompt.txt`.
- `spatial-flooding-panel.svg`: vector extraction from the original MMD coefficient PDF, with no redrawn scientific content.
- `spatial-ba-location-changes.png`: unchanged copy of the requested BA supplementary coordinate-manipulation figure.
- `poisoning-original-figures-provenance.json`: source paths, transformations, exact panel crop and checksums for the refreshed MMD figures and BA image.

## Evasion distribution targets

`evasion-distribution-rise.png` and `evasion-distribution-lower.png` are unchanged published panels from [Arce et al., UAI 2025, Figure 5](https://arxiv.org/html/2506.09640v1#S5.F5). They show predictive-entropy densities after full-distribution attacks on MNIST digits and notMNIST letters. They differ from the expectation-targeting experiment behind the existing Figure 4d selective-accuracy plot. Source URLs and checksums are in `evasion-distribution-provenance.json`.

## Bayesian sequential play and the closing section

- `sequential-merge-mc.png`, `sequential-merge-h2s.png`, and `sequential-merge-adp.png` are byte-for-byte copies of `merge_demo_MC.png`, `merge_demo_H2S.png`, and `merge_demo_ADP.png` under `context/Filter_based_Approaches_for_Bayesian_Sequential_Play___Premium/Figures/MergeGame/`. They retain both panels, axes, legends and annotations. No empirical trajectories have been redrawn.
- `sequential-merge-schematic.svg` is an editable teaching illustration of the closing lane and two cars. It contains no measured trajectory or performance result.
- `sequential-interaction-original.svg` preserves the manuscript's complete original Fig. 1(a), compiled from its TikZ source and converted to SVG with text outlined. `sequential-interaction-original.tex` keeps the editable standalone source.
- `cunef-logo.svg` is the official orange logo extracted from CUNEF's homepage, with its original paths, dimensions and color preserved. Only the CSS class was removed and an SVG namespace added for standalone use.
- `sequential-play-provenance.json` and `closing-sep23-provenance.json` record source paths, transformations and checksums. These supplied assets do not require the optional figure-regeneration script.

The plots compare representative simulated episodes. They do not validate human behavior or establish collision-free operation. The manuscript's broader experiment and model limitations are explained in the speaker notes and source notes.
