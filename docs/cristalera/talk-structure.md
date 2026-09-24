# Secure Machine Learning — narrative and teaching plan

**122 slides, a 180-minute target, in English.** The separate appendix contains 11 optional slides. The [speaker guide](speaker-guide.md) gives timings and discussion answers.

## The story

A system can achieve a good score while taking an unwanted action. Agent coordination makes this a question about interactions, evidence, and control. Ultimately someone must decide what to do under uncertainty. Bayesian decision theory provides a principled rule—conditional on its beliefs and preferences—but the evidence forming those beliefs can be manipulated.

We build that rule from scratch, show what can fail, and introduce probabilistic models of attacks. The closing section puts both players into a sequential decision loop, models human learning with EWA, and uses particle filtering and planning in a simulated lane merge. It then returns to AI agents, where language, memory, tools, and strategic feedback create new modeling questions.

## Sequence

| Stage | Story or example | What the audience should understand |
|---|---|---|
| 1. Motivation | Amodei's call, Hugging Face, and ExploitGym | Separate the assigned task from the intrusion; distinguish events from forecasts. |
| 2. Coordination | Agents, tools, shared findings, and uncertain evidence | Interactions can amplify failure; agreement can duplicate evidence. |
| 3. Decisions | Use a change, run a test, or ask a person | Predictions need consequences and costs before they determine an action. |
| 4. Bayesian framework | One brief mention of the orchestration position paper | Updated beliefs and expected utility give conditional optimality. |
| 5. Foundations | Mexico microcredit | Introduce the ingredients, then explain prior, data, model/likelihood, posterior, prediction, and utility. Pair general formulas with the specific case. |
| 6. What might fail? | Someone selects the evidence; AML roadmap | Distinguish poisoning, evasion, and defenses, and examine each probabilistically. |
| 7. Doctors | Treatments, expectations, disappointing results, proposed adjustment | Follow the Comillas story before the formal attack. |
| 8. KL poisoning | Training-data manipulation, threat model, weighted posterior, gradient, feasible edits | Explain integer-search hardness, intractable normalizers, and the convex relaxation. Posterior samples guide projected SGD, followed by rounding and refitting. |
| 9. Mexico again | Twenty deletion/replication operations | See the empirical posterior change and its illustrative expansion consequence. |
| 10. Moments and MMD | A desired mean or probability | Define the RKHS supremum, then use a finite-feature kernel to compare selected expectations. Explain sampling-based optimization without a main-slide derivation. |
| 11. Spatial analysis | Zinc and flooding along the Meuse | Follow regulator → data → spatial model → clean restriction → developer → deletion map and tainted posterior. Finish with the separate BA coordinate attack. |
| 12. Utility gaps | Minnesota radon; a Lake County home | Explain the hierarchical model and utility, then the clean action, outside-Lake deletions and reversal. Use the original deletion and utility-gap figures to show the reversal. |
| 13. Evasion | MNIST and an accept-or-review rule | Distinguish selected predictive quantities from full-distribution targets. Present each optimization before its examples, then reconnect uncertainty to review decisions and the need for an observation model. |
| 14. Protection | Attack evidence, channels, reactive/proactive models | Connect vulnerability analysis to probabilistic attacker models and integrate them at test time or training time. Recover AT and randomized smoothing in stated limits; explain point purification as an approximation. |
| 15. Protected MNIST | Digit two, accuracy/NLL curves, and selective accuracy | Three messages: protection under a different attack, better accuracy and probability quality than conventional adversarial training, and a more accurate set of accepted predictions. |
| 16. Robust decisions | Expected utility using defended predictions | A foundation needs tested models and explicit losses. |
| 17. Sequential decisions | Original interaction diagram, dynamics, and policy objective | Model latent state transitions and noisy observations; average over the opponent when maximizing cumulative expected utility. |
| 18. Behavioral learning | Experience Weighted Attraction | Build payoff credit, attraction updates, and action probabilities in that order. Separate the opponent's learning from our uncertainty about it. |
| 19. Inference and planning | Explicit Bayesian update and particle filtering | Use paired posterior samples for current-stage utility, horizon simulation, and an ADP continuation value. |
| 20. Driving experiment | One highway merge, original MC, H2S, and ADP trajectories | Knowing action probabilities does not replace planning; descriptive validity and safety still require testing. |
| 21. AI opponents | Language, memory, tools, and strategic evidence | Ask whether behavioral models transfer, what a belief state should retain, and when further checking is useful. |

## Design and pace

The earlier design is restored: fonts, colors, section labels, and highlighted conclusions. Wording is slightly tighter. Extra slides separate story beats and mathematical steps; they are not a reason to speak faster.

Each part starts with a situation and a decision. Original figures and earlier-talk images carry the empirical results. The first and last slides retain the supplied PowerPoint composition. Full explanations, qualifications, and timing remain in notes.

## Scientific boundaries

The microcredit policy, Meuse planning rule and radon costs are illustrative. Meuse shows a changed conditional association; the teaching rule translates it into a planning decision. Attacks are research experiments on real data, not allegations about the original studies. The defenses paper unifies proactive and reactive evasion defenses with clean training data.

Bayesian optimality is conditional on the probability model, actions, and utility. The radon run does not meet the manuscript's stated finite-second-moment assumptions; keep the numerical illustration separate from those guarantees. Details are in [source notes](sources-and-design-notes.md).

The driving results are simulations, with EWA opponents and approximate inference and planning. Their extension to language agents is proposed work, not an implemented defense. The final substantive slide poses open research questions. The CUNEF vacancies announcement follows, then the bibliography and thanks slide.
