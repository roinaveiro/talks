# Sources and design notes

Supporting the current [Quarto deck](secure-ml.qmd). Opening revised and sources checked on **16 September 2026**.

## Opening sources

The opening follows the pacing proposal, its two reasons, the Hugging Face / ExploitGym incident, AI-assisted AI development, agent coordination, and the Bayesian foundations of the lecture. Speaker notes distinguish incidents, forecasts, and illustrative scenarios.

| Source | Date | Supported use |
|---|---|---|
| [Washington Post / AP headline](https://www.washingtonpost.com/business/2026/09/12/anthropic-ai-dario-amodei/5cc3cc44-aec8-11f1-b498-8697f35a6743_story.html) | 12 September 2026 | Opening image: a typeset excerpt of the verified headline, generated for this deck. It is not a screenshot. |
| [Dario Amodei, pacing proposal](https://darioamodei.com/post/we-must-pace-the-frontier) | September 2026; no publication day on the page | A call for slower capability growth, motivated by AI-assisted AI development and the July incident. |
| [Hugging Face Hub documentation](https://huggingface.co/docs/hub/index) | Consulted 16 September 2026 | The platform's role in sharing models, datasets, and applications. |
| [Hugging Face incident disclosure](https://huggingface.co/blog/security-incident-july-2026) | 16 July 2026 | Data-processing compromise and unauthorized internal access. Attribution was incomplete then. |
| [OpenAI retrospective](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) | 26 August 2026 | ExploitGym assignment, reduced safeguards, boundary crossing, and the internal research model's involvement. |
| [METR / Redwood investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) | 26 August 2026 | Unauthorized communication, delegation, and efforts to manipulate evaluation. |
| [Papamarkou et al., Bayesian orchestration](https://arxiv.org/html/2605.00742v2) | v2, 6 May 2026 | Bayesian control over task outcomes; reliability, dependence, and decisions. A position paper, not a validated security guarantee. |

### Presentation choices

- Start with Amodei alone. Present the incident first and development acceleration second.
- Explain an agent, benchmark, flag, and scorer in ordinary language. The message board was improvised in Artifactory, a shared package service. Agents sought restricted CyberGym run records on Hugging Face as clues about the ExploitGym scorer; do not imply that Hugging Face hosted the scorer. Keep detailed exploit mechanics off the slides.
- Questions about multiple agents, uncertain evidence, and asking a human motivate the decision framework. The orchestration position paper receives one brief slide; passing selected tests does not establish safety.
- End the opening with the commitment to build Bayesian inference and decision theory from the basics, then analyze poisoning and evasion.
- Target 22 minutes for the opening and 180 for the complete session. The current slide numbers are in the [speaker guide](speaker-guide.md); the [teaching structure](talk-structure.md) records the current progression.

## Research papers

| Paper | Status and authors | Place in the talk |
|---|---|---|
| [Adversarial Machine Learning: Bayesian Perspectives](https://arxiv.org/abs/2003.03546) | JASA 2023. David Ríos Insua, Roi Naveiro, Víctor Gallego, Jason Poulos. | Conceptual foundation: account for uncertainty about an opponent's objectives and beliefs. |
| [Poisoning Bayesian Inference via Data Deletion and Replication](https://arxiv.org/abs/2503.04480) | AISTATS 2025. Matthieu Carreau, Roi Naveiro, William N. Caballero. | Main poisoning construction and Mexico example. |
| [Posterior Attraction with Exponential-Family Likelihoods and Their Conjugate Priors](https://doi.org/10.1214/26-BA1585) | Bayesian Analysis, accepted 2026. William N. Caballero, Roi Naveiro, Brian J. Lunday. | Optional conjugate example: perturb observation values. |
| [Posterior Attraction via Moment Matching](context/mmd/main.tex) | Unpublished local manuscript. Roi Naveiro, William N. Caballero, Juan Maroñas. | Targeted posterior functionals, spatial analysis, and radon decisions. |
| [Evasion Attacks Against Bayesian Predictive Models](https://proceedings.mlr.press/v286/arce25a.html) | UAI 2025. Pablo G. Arce, Roi Naveiro, David Ríos Insua. | Distributional and uncertainty attacks, including selective prediction. |
| [A unifying Bayesian framework for adversarial robustness](context/adv_bayes_tmlr/main.tex) | Unpublished local manuscript. Pablo G. Arce, Roi Naveiro, David Ríos Insua. | Adversarial channels; proactive and reactive evasion defenses. |
| [Advancing Bayesian Sequential Play Against Boundedly Rational Opponents](context/Filter_based_Approaches_for_Bayesian_Sequential_Play___Premium/main.tex) | Supplied local manuscript. Christopher Rafnson, William N. Caballero, Roi Naveiro, Wesley Marrero. | Closing section: EWA opponent learning, particle filtering, approximate planning, and one driving experiment. |

The UAI paper is **additional to the supplied TXT**, but is cited in the manuscripts and directly supports the requested evasion section. [Its full text](https://arxiv.org/html/2506.09640v1) was also reviewed.

The Bayesian Analysis publisher PDF could not be retrieved through the browser. Its title and accepted status were checked against a [coauthor's institutional publication list](https://www.afit.edu/bios/bio.cfm?a=publications&facID=248), and its relation to the other attacks is described in the local MMD manuscript. Keep it optional; check the full final text before building a detailed derivation from it. Local bibliography metadata for this paper is older than the accepted publication record.

The local manuscripts contain revision comments. Treat their results as work in progress and build slides from the current substantive text, not abandoned commented-out formulations.

## Case-study details to preserve

### Mexico microcredit

The [published experiment, Section 6.3](https://arxiv.org/html/2503.04480v1), uses 16,560 observations. Twenty deletion/replication operations, approximately 0.12%, move the posterior treatment-effect mean from −4.71 to +6.28; the attacked 95% credible interval is [0.02, 12.43].

- The study took place in **Sonora, Mexico**. Compartamos Banco expanded group lending in 2009; surveys in 2011–2012 covered 16,560 women in 238 retained geographic clusters. Credit access was randomized by community. The original outcomes included reported business revenue minus expenses over the preceding two weeks. See the [IPA overview](https://poverty-action.org/microcredit-women-mexico) and [original 2015 paper](https://doi.org/10.1257/app.20130537).
- The original profit regression used 16,005 nonmissing outcomes. The attack reanalysis fills missing profit with zero and multiplies profit by 0.1026493, retaining 16,560 records. Consequently, plotted effects are in **analysis profit units**, not untransformed Mexican pesos. See the [preprocessing notebook](https://github.com/Matthieu-Carreau/Poisoning_Bayesian_Inference/blob/main/notebooks/microcredit.ipynb).
- The revised opening plots the actual Student-t prior for beta_1: df 3, location 0, scale 1000. This is a stated prior, not fitted data. The [authors' implementation](https://github.com/Matthieu-Carreau/Poisoning_Bayesian_Inference/blob/main/src/studentT_prior_lin_reg.py) confirms the scale convention. The prior and empirical posterior plots use different horizontal ranges.
- Say **“twenty deletion/replication operations”** rather than automatically calling them twenty deletions.
- The attack is a research experiment on real data, not an allegation that the original study was manipulated.
- The lecture adds an explicit illustrative decision: expansion utility is effect minus cost, with cost **2** in profit-equivalent units; non-expansion utility is zero. Expected expansion utility changes from **−6.71 to +4.28**.
- That simple utility establishes a decision reversal, while the separate foundation exercise explains why uncertainty beyond a mean can matter.

The original [poisoning talk](../poisoning_bayes/poisoning_bayes.qmd) provides the storytelling and plots; the [Comillas talk](../aml_comillas/aml_comillas.qmd) adds the decision-theory bridge.

### Meuse spatial analysis

Source: [MMD manuscript](context/mmd/main.tex), subsection **Bayesian Spatial Regression**.

- 152 analyzed soil samples; standardized log-zinc response and spatial regression. Covariates include flooding, square-root river distance, elevation, and organic matter; a spatial field links nearby sites.
- The current manuscript reports a clean flooding-effect mean of **0.43**, with 95% interval **[0.17, 0.69]**, consistent with the currently supplied coefficient figure. A native-vector crop preserves the FFREQ panel; the full plot remains linked.
- The selected budget-20 Adam-R2 attack moves the mean to **0.03**, with 95% interval **[−0.26, 0.30]**. Twenty sites are approximately **13%**, materially different from the smaller fractions in the other examples.
- The displayed run is selected from the experiment; it should not be presented as an average or a universal guarantee.
- The result concerns an **association**. The explicit teaching rule restricts building when the flooding coefficient's 95% interval is entirely positive. It reverses after the attack, but this is an illustrative planning decision, not a documented permit or evidence of safety.
- Spatial dependence and covariates help explain why simple outlier removal is an incomplete account.
- The separate BA illustration is copied unchanged from `context/posterior_attraction_BA/Figures/spatial_lm/location_changes_with_response_EPA_b1=40_b3=1.0.png`. It changes coordinates, keeping covariates and measurements fixed, in a conjugate spatial model with fixed covariance hyperparameters. The sparse EPA budget permits 40 coordinate entries with a 1 km per-coordinate bound; it does not mean 40 deleted sites. EPA uses reverse KL, unlike the earlier forward-KL formulation.

### Minnesota radon

Source: [MMD manuscript](context/mmd/main.tex), subsection **Attacking Decisions**.

- **919 homes in 85 counties**. The target is a new basement home in Lake County.
- The illustrative cost model compares remediation cost **2000** with posterior predictive expected exposure cost $700\,\mathbb E[e^{\tilde y}]$.
- The original utility-gap figure implies clean expected cost **2179.9** and attacked cost **1988.6**, after six deletions outside Lake County. The slides use these values consistently. The draft prose instead reports approximately **2188** and **1988**; that difference remains unresolved.
- The corresponding expected utility gap changes from **+179.9 to −11.4**. The desired target margin of **−50 is not reached**, though the selected Bayes action changes.
- Lake County was chosen because its original action was near the threshold. This is not evidence that every county is equally vulnerable.
- Shared parameters transmit the effect across counties. The conditional expected exposure term contains $\exp(\alpha_{\rm Lake}+\sigma_y^2/2)$ for the basement target, so changing predictive variation can change the decision.
- The paper's **plug-in decomposition** is different from the posterior expected cost. The original figure gives 2156−142−52=1962; the prose gives approximately 2163−147−53=1963. These are explanatory components evaluated at posterior-mean parameters. Preserve the original annotations and do not equate the plug-in totals with the fully integrated values above.
- This is a modeled decision using illustrative costs, not medical guidance or an observed regulatory outcome.

### Radon: the stated second-moment assumption fails

A mathematical review of the current manuscript found a specific mismatch between the radon model and the sufficient assumptions used in its gradient theorem. The manuscript specifies $\sigma_y\sim\mathrm{HalfNormal}(1)$ and the utility-gap feature $g(\theta)=700\exp(\alpha_{\rm Lake}+\sigma_y^2/2)-2000$.

Hold the remaining parameters in a compact set of positive prior mass. As $\sigma_y\to\infty$, the Gaussian likelihood decays only polynomially, as $\sigma_y^{-\sum_i w_i}$, while $g^2$ grows as $\exp(\sigma_y^2)$ and the prior contributes $\exp(-\sigma_y^2/2)$. Thus the unnormalized second-moment tail behaves, up to bounded positive factors, as

$$
\sigma_y^{-\sum_i w_i}\exp(\sigma_y^2/2),
$$

whose integral diverges. Therefore the finite-second-moment assumptions stated for this feature and its linear kernel are not satisfied by this radon model. The corresponding gradient/convergence guarantees do not directly cover the numerical run. This argument alone neither invalidates its reported finite-sample mean estimates nor proves that the first posterior moment is infinite.

The slides retain the reported empirical example and label the qualification. The model, data, and manuscript have not been changed, and the experiment has not been rerun. Applying the theorem would require a separate mathematical justification or a revised model followed by new analysis.

### Image attacks and defenses

- The UAI evasion paper uses **MNIST and notMNIST letters** for its familiar/unfamiliar-image experiment. The new full-distribution examples use its original Figure 5a–b; the selective-accuracy result remains Figure 4d from the expectation-targeting experiment.
- The main evasion route gives the squared expectation-target objective and forward predictive-KL objective before their examples. The clean/targeted/entropy digit images are earlier Comillas illustrations, not newly run UAI experiments. The evasion section now leads directly into the defense motivation; adaptive evaluation appears with the defense experiments and in the technical appendix.
- The defense manuscript's selective-prediction experiment instead uses **MNIST and FashionMNIST**. Name the dataset on each figure.
- Distinguish predictive entropy, parameter uncertainty, calibration, and accuracy. None can be used as a synonym for another.
- Negative log-likelihood measures probabilistic prediction quality; low NLL alone does not establish calibration.
- Defense visualizations use the same clean inputs, but **attacks are optimized separately for each defense**. Comparisons must not imply identical attacked images.
- The main defense experiment sequence is now three slides. The digit-two example illustrates protection with an evaluation attack absent from the assumed one-step training channels. The curves focus on MIX and NN50 versus conventional adversarial training in accuracy and NLL; the latter is described as predictive probability quality, not an isolated calibration measure. The final plot shows selective accuracy at 50% coverage. The detailed model overview is omitted from the main route.

## Defense scope and mathematical qualifications

Source: [defense manuscript](context/adv_bayes_tmlr/main.tex), **Problem Formulation**, defense derivations, experiments, and conclusions.

1. **Scope:** inference-time covariate evasion in supervised models with clean training data. “Proactive” means preparing during training for subsequent evasion; it is not itself protection against poisoned training data.
2. **Unification:** a shared channel viewpoint yields two distinct probabilistic constructions, reactive and proactive, with generally different predictions.
3. **Conditioning matters:** the main reactive slide now displays Proposition 3.1's exact nested expectation. Its inner distribution infers the latent clean input conditional on the received input and parameters; its outer distribution also updates parameter beliefs using the received input. Ordinary training on clean data precedes these operational updates.
4. **Experimental implementation:** the main proactive equation displays the generalized Bayesian posterior induced by the channel-averaged loss, with learning rate one. The original proactive graphical model describes the label-independent generative construction. Keep its distinction from the implemented loss objective explicit; the appendix contains the derivation.
5. **Limits:** misspecified attack channels, approximate inference, and unseen adaptive attacks remain relevant. The reported reactive MNIST configuration has very large inference overhead.
6. **Decision protection:** the paper's evidence concerns predictive robustness and probabilistic performance. Robust downstream decision-making remains a proposed next step.
7. **Recovery of established methods:** deterministic worst-case attacks plus generalized-posterior MAP under a flat prior recover standard AT. Fixed parameters, a Gaussian channel and a flat prior over original inputs yield Gaussian smoothing; a deterministic base classifier gives the standard majority-vote rule. Point purification collapses the input posterior to a restored estimate. ALP/TRADES connections in the draft concern structural forms and are not presented as exact recoveries in the slides.
8. **Displayed MNIST comparison:** the table includes clean accuracy/NLL and PGD accuracy/NLL at epsilon two for BL, AT, MIX, NN50 and onPure. Values are copied from the manuscript tables. MIX and NN50 preserve clean accuracy and improve attacked performance over BL and this one-step AT comparator; BL retains the best clean NLL. Bold highlights best displayed means, not a significance test.

For poisoning, distinguish the KL direction $\mathrm{KL}(\pi_A\Vert\pi_w)$ from reverse KL. General MMD objectives need not be convex; optimization guarantees concern stated assumptions and the continuous problem, with additional issues introduced by integer rounding.

A decision-targeting condition formulated using **exact expected utility gaps** should not be described as automatically certified by a noisy Monte Carlo estimate. Numerical uncertainty must be accounted for before making a certification claim.

### Optional mathematical detour

The [covariance slide in the appendix](secure-ml-appendix.html#/poison-app-covariance) explains influence through:

$$
\frac{\partial}{\partial w_i}\mathbb E_{\pi_w}[h(\theta)]
=\operatorname{Cov}_{\pi_w}\!\left(h(\theta),\log p(y_i\mid x_i,\theta)\right).
$$

Interpretation: increasing an observation's weight moves a targeted expectation according to how its likelihood contribution covaries with that target. This connects posterior sampling, sensitivity, and decision utilities. Include regularity and integrability assumptions in notes; keep the main route accessible without the identity.

## Bayesian sequential play and the new ending

The closing section was rebuilt on 22 September 2026 and expanded on 23 September in response to the author's seven TODOs, using the supplied [sequential-play manuscript](context/Filter_based_Approaches_for_Bayesian_Sequential_Play___Premium/main.tex). Slides before `sequential-start`, including the Bayesian defenses, were preserved during the latest revision.

### Mathematical narrative

- **Scope (§3.1–3.3):** a finite-horizon, partially observed stochastic game. Both players choose simultaneously from fixed finite action menus; physical states need not be discrete. Our player observes the opponent's action and its own noisy state measurement after each stage. The objective is undiscounted cumulative expected utility under the defender's model.
- **Interaction diagram (Fig. 1a):** the complete original TikZ diagram is compiled to an SVG with text outlined. White and gray distinguish players, not observed and latent variables. Dashed links connect successive stages. The accompanying slides define the physical state, transition and observations, then state the policy objective and explicitly average over the opponent's action.
- **EWA (§3.2):** attractions and experience follow the manuscript's equations. The selected action receives full payoff reinforcement; foregone actions receive a fraction controlled by delta. Separate slides introduce payoff credit, attraction and experience updates, and the softmax action probabilities, in that order. Memory, experience decay, payoff sensitivity, utility parameters and private observations are uncertain. EWA describes the opponent; it is not the defender's value-learning algorithm.
- **Beliefs:** the augmented opponent vector explicitly contains phi, delta, rho, lambda, utility parameters beta, private-observation parameters eta, current attractions psi, and experience zeta. Bayes' rule updates beliefs over the preceding opponent state using the new observed action and sensor reading. The filter then advances the physical and behavioral state. Time indices on otherwise fixed parameters reflect the implemented artificial evolution, not an assumption that human preferences necessarily change each round.
- **Filter (Algorithm 1):** after our action and the observed opponent action, propagate the physical state, weight by the product of the action and observation likelihoods, resample, simulate the opponent's private observation, update EWA attractions/experience, and artificially evolve the remaining parameters. This is an approximate bootstrap filter with artificial parameter evolution, not exact inference for fixed parameters.
- **Planning (§3.4–3.5):** the deck first uses paired posterior samples to estimate immediate utility and define approximate myopic greedy choice (AMG). Separate slides then explain horizon simulation (H2S) and approximate dynamic programming (ADP). The latter learns continuation values by backward simulation; the driving implementation uses neural networks and mean-particle features. This compression introduces additional approximation error. The experiment's myopic clairvoyant (MC) benchmark knows action probabilities, not the next realized action or the entire optimal policy. MC-versus-ADP does not isolate the contribution of filtering. The teaching equation defines H as the number of planned stages; the experiment caption preserves the manuscript's reported H=2 setting without reinterpreting its indexing convention.

### One application: the highway merge (§4.3)

The substantive main text uses an eight-dimensional continuous physical state: two positions, heading, and speed for each of two cars. Each player has nine steering/acceleration combinations and decisions are spaced 0.1 seconds apart. Utilities combine road navigation, proximity and heading/comfort terms. The older one-dimensional ADS appendix is inside a `comment` environment and was not used.

The original `merge_demo_MC.png`, `merge_demo_H2S.png`, and `merge_demo_ADP.png` are copied unchanged into `assets/sequential-merge-mc.png`, `assets/sequential-merge-h2s.png`, and `assets/sequential-merge-adp.png`. The slide sequence preserves both the trajectory and distance panels, all axes, and the original legends. The MC episode fails to complete the merge; H2S merges late near the taper boundary; ADP begins moving across earlier and produces a smoother merge. These are representative simulated episodes, not deployment evidence or a controlled isolation of inference quality.

For discussion, the same application's wider study considers 54 value-network configurations, 25 evaluation episodes each, and trade-offs among distance from an ideal trajectory, aspirational episode rate, and collisions. Several strong merge configurations still collide. The paper explicitly discusses implausible behavior from some simulated EWA drivers and possible model misspecification. A zero-collision batch is not a safety certificate. These qualifications remain in the notes; the author's removal of the separate limitations slide is preserved.

The lane diagram is an original vector teaching schematic, not a reconstruction of measured trajectories. Source and asset checksums are in [sequential-play-provenance.json](assets/sequential-play-provenance.json) and [closing-sep23-provenance.json](assets/closing-sep23-provenance.json).

### Extension to AI agents

The ending connects the sequential framework to [Papamarkou et al., *Position: agentic AI orchestration should be Bayes-consistent*, v2](https://arxiv.org/html/2605.00742v2), reread on 22 September 2026. Its controller-level beliefs, utility-sensitive checking, and concerns about dependent evidence motivate the connection. Strategic opponent modeling in language interactions is our proposed extension; neither source establishes the resulting system as a validated security defense.

The shift is from physical variables and small control menus to text, memory, tools, and adaptive behavior. It is not accurately described as simply leaving discrete states: the car state is already continuous, while text itself is a discrete structured sequence. The final questions concern transfer of behavioral models to AI, decision-relevant compression of language histories, the value of checking when evidence is shared or manipulated, and opponents who adapt to our learning rule.

### Vacancies and final order

The scientific narrative ends with the AI-opponent questions. The following slide summarizes the author's supplied CUNEF tenure-track announcement: Assistant Professor positions in Quantitative Methods for the 2026–2027 job market, expected start September 2027, the five requested fields, qualifications, teaching languages, research environment, and CV/cover-letter contact. No application deadline is added. The official orange logo was extracted from the inline SVG on [CUNEF's homepage](https://www.cunef.edu/) on 23 September 2026, preserving its paths, dimensions and color. The bibliography then immediately precedes the unchanged thanks composition.

## Style references

### Restored design and gentle revision

The previous presentation design is restored, including the original fonts, colors, navigation, section labels, and highlighted conclusions. Wording is slightly tighter. Additional slides develop the doctors' story, pair general Bayesian formulas with the Mexico calculation, and introduce the spatial and radon context before the attacks. The two original defense graphical models are given their own explanations. The first and last slides retain the AIHUB composition.

### Narrative

Primary: [poisoning_bayes](../poisoning_bayes/poisoning_bayes.qmd) and its [short version](../poisoning_bayes_short/poisoning_bayes.qmd).

- A realistic problem and a surprising consequence appear before the formalism.
- Short conversational titles guide a sequence of reveals.
- A central example returns after the mathematics.
- Large clean/attacked comparisons carry the argument.
- Derivations and optimizer variants are available as detours.

Secondary: [aml_comillas](../aml_comillas/aml_comillas.qmd) already connects Bayesian foundations, decisions, poisoning, image attacks, and a probabilistic attack channel. [NFs](../NFs/NFs.qmd) provides a local precedent for manually constructed opening and closing slides.

### PowerPoint opening and closing

Source: [AIHUB summer-school template](AIHUB2026_EscuelaVerano_Template_v4.pptx), first and last of eight slides. Inspected the slide XML and the shared network artwork.

| Element | Template treatment |
|---|---|
| Aspect ratio | 16:9 |
| Background | Navy, **#004369** |
| Left stripe | Teal, **#1C7984**, approximately 0.8% of slide width |
| Main text | White, left aligned; original typeface Calibri |
| Divider | Thin white horizontal rule |
| Small contact markers | Muted red, **#982825** |
| Artwork | Transparent network silhouette at right, with white links and pink/red nodes |
| Opening | AIHUB CSIC label, event line, title, presenter/institution, date |
| Closing | Thank you, Questions?, email, website |

The artwork is embedded as **ppt/media/image1.png** in the PPTX. Reuse that exact asset when building the deck.

Only the first and last slides should use this composition. Middle slides should favor a light canvas, generous spacing, dark headings, consistent plot colors, and large figures. Avoid reproducing manuscript-sized tables or tiny labels.

### Reusable assets

| Use | Existing local asset |
|---|---|
| Doctor anecdote | [Doctor image](../poisoning_bayes/images/doc.jpg) |
| Clean Mexico posterior | [Posterior plot](../poisoning_bayes/images/posterior_treatment_effect.jpeg) |
| Attacked Mexico posterior | [Attacked plot](../poisoning_bayes/images/tainted_posterior_treatment_effect.jpeg) |
| Mexico distribution comparison | [Comparison](../poisoning_bayes/images/microcredit1.jpeg) |
| Predictive uncertainty illustration | [Predictive distribution](../aml_comillas/images/sin_ppd.webp) |
| Clean / attacked digit | [Clean](../aml_comillas/images/7_clean.png), [targeted](../aml_comillas/images/7_pgd.png), [entropy attack](../aml_comillas/images/7_ent.png) |
| Spatial sites | [Selected locations](context/mmd/figs/spatial_lm/spatial_mean_attacks_selected_attack_map.pdf) |
| Spatial posterior comparison | [Coefficient posteriors](context/mmd/figs/spatial_lm/spatial_mean_attacks_all_beta_posteriors.pdf) |
| Radon decision | [Utility-gap posterior](context/mmd/figs/radon_lake_utility_gap_posterior.pdf) |
| Radon uncertainty mechanism | [Cost decomposition](context/mmd/figs/radon_lake_cost_decomposition.pdf) |
| Baseline image attacks and predictions | [Images](context/adv_bayes_tmlr/images/training/MNIST_examples.png), [probabilities](context/adv_bayes_tmlr/images/training/MNIST_preds.png) |
| Protected image examples | [Images](context/adv_bayes_tmlr/images/training/MNIST_newlosses_examples.png), [probabilities](context/adv_bayes_tmlr/images/training/MNIST_newlosses_preds.png) |
| Defense performance | [PGD curves](context/adv_bayes_tmlr/images/filled/SEP_pgd.png), [selective accuracy](context/adv_bayes_tmlr/images/filled/SEP_sel_acc.png) |

Some older plots have small labels or broken axes; adapt their presentation carefully and retain the underlying numbers. In the implementation stage, copy the chosen assets into a local presentation asset directory so the finished deck is portable.
