# Secure Machine Learning — speaker guide

**120 main slides. 180-minute target**, including a ten-minute break and seven minutes of final discussion. The separate technical appendix has **11 slides**.

The previous visual design has been restored. Wording is only lightly condensed; extra slides give the stories and formulas room to develop. Explain the problem first, introduce one mathematical idea, and return to the example's consequence.

The thread is **evidence → beliefs → uncertainty → decisions → consequences**. A Bayes action is optimal for the stated beliefs and preferences. Security asks whether those beliefs properly represent how the evidence reached us.

## Running order

| Elapsed time | Slides | Section | Minutes | Transition |
|---|---:|---|---:|---|
| 00:00–00:22 | 1–18 | Motivation and coordination | 22 | Choosing what an agent should do is a decision under uncertainty. |
| 00:22–00:46 | 19–34 | Bayesian decision theory | 24 | We know how to decide; what if someone selects our evidence? |
| 00:46–01:34 | 35–68 | Poisoning, moments, and decisions | 48 | Change what the model learns from, then change what it sees. |
| 01:34–01:44 | 69 | Break | 10 | Hold the centered Evasion attacks divider. |
| 01:44–02:04:30 | 70–79 | Evasion | 20.5 | Parameter uncertainty does not model the attack process. |
| 02:04:30–02:31 | 80–93 | Adversarial channels and protection | 26.5 | Defended predictions can feed a decision rule. |
| 02:31–02:48 | 94–113 | Bayesian sequential play and the driving experiment | 17 | The opponent learns; we infer its behavior and plan ahead. |
| 02:48–02:53 | 114–119 | AI opponents, open questions, vacancies, and bibliography | 5 | What must change for language, memory, and strategic feedback? |
| 02:53–03:00 | 120 | Final discussion | 7 | Revisit the open questions or use the technical appendix. |

Times are rehearsal targets. The opening has 22 minutes and the foundations, including the AML roadmap, have 24. Poisoning has 48 minutes to accommodate the expanded Meuse and radon stories. Keep the brief coordination transition and general poisoning introduction short. Use this table for the overall schedule. The final 29 minutes contain 22 minutes of prepared material and seven minutes of discussion. Questions conclude the scientific narrative, followed by the vacancies announcement, bibliography, and closing template. Return to the questions slide during discussion if useful.

## How to pace the story

- **Opening:** distinguish Amodei's forecast about development speed from the documented intrusion. Define Hugging Face, an agent, a benchmark, and a flag before discussing the boundary crossing. Give the orchestration position paper one short slide.
- **Bayes:** use Mexico throughout. Introduce the ingredients, show the actual Student-t prior, then explain the observed data and likelihood. Write the general update and its specific regression form. Read the actual posterior before introducing utility.
- **Doctors:** tell the comparison, expectation, disappointment, and proposed adjustment as separate beats. The earlier talks document a suggestion; do not invent what happened afterward.
- **KL:** introduce weights, the target, and the gradient before revealing the Mexico attack. Give the numerical gradient example aloud.
- **Moments:** ask why an attacker should specify an entire posterior when only a mean or decision matters. Define MMD as a supremum over the RKHS unit ball, then show how a finite-feature kernel targets selected expectations. Keep this to two slides; leave gradient details in the appendix.
- **Meuse:** introduce the regulator, observations, spatial model and clean conclusion before the developer. Explain the illustrative restriction rule, then show the deletion map and attacked posterior together. Present the BA coordinate manipulation as a separate attack setting.
- **Radon:** explain the home, hierarchical model and utility before the attacker. Use the original deletion and utility-gap figures. Let the audience predict whether leaving Lake County untouched protects its decision. Distinguish the numerical result from the theorem's assumptions.
- **Images:** show the clean predictive probabilities, distinguish selected quantities from a full-distribution target, and formulate each optimization before its examples. Keep projected SGD brief. Introduce the review decision only after the prediction examples, then connect to an observation model for altered inputs.
- **Protection:** start with the goal of preserving predictions and decisions under manipulation. Investigate vulnerabilities, gather evidence about attacker behavior, and define an adversarial channel. Introduce test-time and training-time protection before their graphical models. Explain AT, randomized smoothing and point purification as limiting cases or approximations, then spend about five minutes on three results: the digit two remains recognizable under a different attack; MIX and NN50 improve accuracy and predictive probabilities relative to conventional adversarial training; and selective accuracy improves too. Use the original figures and keep method details for questions.
- **Sequential play:** begin with the frozen predictor, then add actions, utilities, feedback, and a simultaneously acting opponent. Use the original interaction diagram to define the variables, specify the dynamics, and state the expected-utility objective. Introduce EWA through payoff credit, then attractions, then action probabilities. Separate the opponent's learning from our Bayesian learning about it.
- **Filtering and planning:** define the unknown parameters and show their Bayesian update. Explain predict, weight, resample, and advance the opponent's learning in that order, including its hidden observation. The resulting paired posterior samples support a current-stage utility estimate, short-horizon simulation, or an ADP continuation value. EWA models the opponent's behavior; ADP supports our decisions.
- **Driving:** show the lane-closing schematic, then the original MC, H2S, and ADP episodes on successive slides. Read the top trajectories before the distance panels. The representative sequence goes from no completed merge to a late merge and then an earlier, smoother merge. Opponent information and planning belong together. Keep the wider experiment's qualifications in the notes for questions.
- **AI opponents:** move from physical variables and small control menus to text, memory, and tool calls. The car state is already continuous. Finish with behavioral-model transfer, useful belief representations, checking costs, and strategic manipulation of learning.

## Questions and calculations

| Slide | Prompt | Debrief |
|---|---|---|
| [Slide 14](secure-ml.html#/motivation-shared-evidence) | Many agents report findings. Whose evidence should count? | Model reliability and shared sources; agreement need not be independent evidence. Then ask whether another tool call or a human expert could improve the decision enough to justify its cost. |
| [Slide 27](secure-ml.html#/bayes-real-posterior) | What does a mean effect of −4.71 establish? | It summarizes this posterior. It neither makes every plausible effect negative nor chooses a policy without a utility. |
| [Slide 32](secure-ml.html#/bayes-microcredit-decision) | With expansion cost 2, what does the rule choose? | Expansion utility is −4.71−2=−6.71; no expansion gives 0. Choose no expansion under this illustrative model. |
| [Slide 46](secure-ml.html#/poison-gradient) | Current expected log likelihood −4; target −1. Which way does the weight move? | The derivative is −3. Gradient descent increases that row's weight if constraints allow it. |
| [Slide 49](secure-ml.html#/poison-mexico-attacked) | What happens after twenty operations? | The posterior mean moves to +6.28; expected expansion utility becomes +4.28. The illustrative action flips. |
| [Slide 50](secure-ml.html#/poison-target-summary) | Why replace a full posterior target with moments? | The attacker may care about an effect, probability, or utility gap without wanting a specific distribution for nuisance parameters. |
| [Slide 65](secure-ml.html#/poison-radon-restriction) | Can an attack outside Lake County affect its decision? | Shared hierarchical parameters carry information across counties. The selected attack deletes six non-Lake homes. |
| [Slide 67](secure-ml.html#/poison-radon-result) | What changes the action? | The reported estimated exposure cost crosses 2000: 2179.9→1988.6; mean utility gap +179.9→−11.4. The target −50 is missed, but the fitted action changes. |
| [Slide 78](secure-ml.html#/evasion-gate) | Does reviewing uncertain inputs ensure security? | The attacker can raise uncertainty for digits and lower it for unfamiliar inputs, changing which cases pass. |
| [Slide 82](secure-ml.html#/defense-attacker-beliefs) | Where should the channel come from? | Evidence about access, incentives, constraints, and observed attacks informs uncertain attacker goals and beliefs. Average over these to forecast behavior. |
| [Slide 86](secure-ml.html#/defense-reactive-joint) | Does reactive protection just choose one clean input? | Proposition 3.1 nests an expectation over clean inputs inside an expectation over parameters. Both distributions condition on the received input. |
| [Slide 101](secure-ml.html#/sequential-ewa-payoffs) | What changes when delta goes from zero to one? | The chosen action always receives its modeled payoff; unchosen actions change from receiving no payoff credit to receiving their full foregone payoff. |
| [Slide 106](secure-ml.html#/sequential-filter) | Why use both likelihood factors? | The observed action informs the behavioral model; the sensor reading informs the physical state. Both matter for forecasting the next interaction. |
| [Slide 111](secure-ml.html#/sequential-driving-myopic) | Why can a clairvoyant policy fail to merge? | MC knows current action probabilities but optimizes only the current stage. It is not a globally optimal oracle. |
| [Slide 117](secure-ml.html#/conclusions-questions) | Are behavioral-economics models useful for AI agents? | Treat this as a testable descriptive claim across prompts, memory, feedback and model changes. Then discuss representations, checking, and adversarial feedback. |

## Closing narrative

Slides 94–120 develop sequential play and close the talk. The source is *Advancing Bayesian Sequential Play Against Boundedly Rational Opponents* by Rafnson, Caballero, Naveiro and Marrero. Only the driving application is used.

The mathematics follows the current main text: two players with private noisy observations, EWA attractions, a belief state over the environment and opponent, bootstrap filtering with artificial parameter evolution, and approximate planning. The original MC, H2S, and ADP images show representative simulated trajectories. Notes retain the wider study's limitations without treating one smooth trajectory as a safety result. The future-work divider returns to the opening's AI agents, followed by four research questions. CUNEF vacancies come immediately after the questions; the bibliography immediately precedes the thanks slide.

The prepared ending takes 22 minutes. If time is tight, explain the EWA update verbally and omit the parameter-by-parameter reading; retain the posterior-to-decision connection, the trajectory comparison, and the final questions.

## Claims to keep precise

- **Mexico:** twenty deletion/replication operations, about 0.12% of the sample size. Cost 2 is a teaching assumption; the experiment does not allege manipulation of the original trial.
- **Meuse:** 20 of 152 sites is about 13%. The displayed MMD run changes an association and reverses the explicitly illustrative planning rule. The BA slide separately changes recorded coordinates in a conjugate spatial model. The current manuscript uses square-root river distance, elevation, and organic matter alongside flooding.
- **MMD:** Maximum Mean Discrepancy. The selected finite-feature kernel reduces squared MMD to squared differences of feature expectations. It need not identify an entire posterior.
- **Radon:** the costs are illustrative and the run is empirical. The current HalfNormal(1) residual-scale prior does not give the exponential utility gap a finite second posterior moment. The stated finite-second-moment gradient/convergence guarantees therefore do not directly apply. Finite Monte Carlo output does not resolve that issue.
- **Numerical uncertainty:** an estimated negative utility gap is not an exact decision certificate. Radon prose–figure discrepancies remain documented; the slides consistently quote the original figure annotations.
- **Defense scope:** clean-training covariate evasion. Reactive and proactive models differ. The main training equation now shows the generalized Bayesian objective used in the experiments; the preceding graphical model describes the label-independent generative construction.
- **Limiting cases:** standard AT requires a deterministic worst-case channel and MAP under a flat prior. Standard randomized smoothing also fixes the classifier and uses a Gaussian channel and flat latent-input prior. Point purification approximates the original-input posterior by one restoration. These connections do not give arbitrary channels a smoothing certificate.
- **Experimental comparison:** Focus the curves on MIX and NN50 versus AT. The plotted NLL assesses probability quality rather than isolating calibration. AT here uses one-step training attacks; the result is specific to this benchmark. The digit example illustrates one-step training versus iterative evaluation, not protection against every unseen attack.
- **Channel uncertainty:** MIX weights are specified experimental choices, not estimates of real attacker behavior.
- **Metrics:** predictive entropy, calibration, NLL, accuracy, and decision loss measure different things.
- **Image data:** UAI uses MNIST + notMNIST; defense selective prediction uses MNIST + FashionMNIST. Attacks are optimized separately for each defense.
- **Opponent learning:** EWA is a behavioral model supported by human repeated-game research, not a validated law of driving or AI behavior. Its counterfactual payoffs use the manuscript's stated utility model.
- **Filter:** the algorithm observes the opponent's action after each stage; artificial evolution of otherwise static parameters is an approximation and does not prevent all degeneracy.
- **Planning:** MC knows action probabilities, not realized future actions. ADP uses mean-particle features for the value approximation, losing some posterior information. Comparing MC and ADP does not isolate filtering quality.
- **Driving:** continuous eight-dimensional physical state, nine control combinations per player, and 0.1-second steps. The one-dimensional appendix draft is commented out. Avoid claiming human-driver validation or collision-free guarantees.
- **Agents:** task-level Bayesian orchestration motivates the ending, while strategic language-agent modeling is proposed work. Text is structured and discrete; the relevant change is representational and computational, rather than simply discrete versus continuous.

## Navigation and rehearsal

Open the main HTML. Use arrow keys or Space to advance, **S** for notes, **O/Esc** for overview, and the menu for sections. Use Quarto preview while editing; the [README](README.md) gives commands.

Check the projector view of a posterior, a graphical model, and the utility-gap equation. Reach the break at **01:34**, protection at **02:04:30**, and sequential play at **02:31**.

The appendix adds time unless it replaces part of the route. Use it for mathematical questions.

## If discussion runs long

Keep the motivation, doctor story, same-mean exercise, spatial context, radon decision, and graphical models. Save time by:

- Summarizing optimizer mechanics after the KL gradient.
- Keeping the MMD explanation to its two main slides and leaving the covariance derivation in the appendix.
- Summarizing the PGD curves before returning to the accept-or-review example.
- Explaining EWA's chosen-versus-foregone payoff rule verbally instead of reading every parameter.

Preserve the closing discussion; attendees should leave with a decision in their own field to reconsider.
