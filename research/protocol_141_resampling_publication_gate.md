# Protocol 141 — Resampling-contract decision gate and publication audit

Date: 2026-11-08. Status: methodological audit only; no cloud tests or model experiments claimed.

## Immediate decision

Do **not** select the Protocol 135 independent-family oracle or the Protocol 140 shared-key oracle from matching marginal lineage counts. The probability of an undefined bootstrap denominator is a *joint* event and requires a documented coupling of the family's resample draws. Both oracles are conditional reference implementations, not evidence about production behavior.

## Production trace: evidence required

1. Locate the actual production function that generates bootstrap indices, including all callers and the point where random state is initialized.
2. Record whether the sampling unit is a row, an intervention, a lineage, a family, or a physical case. Preserve stable identifiers through filtering and sorting.
3. Record whether the index vector is generated once per replicate for all families, once per family, or in another nested loop. A shared RNG seed does **not** establish identical index vectors.
4. Determine whether families have identical *semantic* observation units, not merely matching key strings or counts. For unmatched keys, a shared-key reference is inapplicable without an explicit matching policy.
5. Verify how zero-weight families, missing acceptance values, duplicate keys, rejected systems, and resamples with undefined denominators are handled.
6. Compare observed production events against exact reference probabilities on tiny deterministic fixtures, with independent random seeds and explicit assertions about the generated index sequences. A Monte Carlo agreement alone cannot establish the sampling contract.
7. Record the exact commit SHA, Python version, deterministic fixtures, random seeds, and cloud CI URL for every executed result.

## A falsifiable coupling example

Consider two families with two aligned keys. Both accept only key A. Two draws with replacement are made.

* If the same two key draws are reused for both families, the probability that at least one family receives no accepted draw is 1/4.
* If each family draws its own independent two-key sequence, the union probability is 1 - (3/4)^2 = 7/16.
* If the second family accepts only key B and the draws are shared, the union probability is 1/2.

All three statements are analytic consequences of the specified sampling designs; none are measured AI results. This example shows that family-specific acceptance rates alone do not identify the joint probability.

## Closest prior-art families to examine before claiming novelty

* Classical nonparametric bootstrap and its dependence assumptions: Efron (1979), *Bootstrap Methods: Another Look at the Jackknife*, Annals of Statistics, DOI: 10.1214/aos/1176344552.
* Clustered/dependent resampling: Cameron, Gelbach and Miller (2008), *Bootstrap-Based Improvements for Inference with Clustered Errors*, Review of Economics and Statistics, DOI: 10.1162/rest.90.3.414.
* Conformal prediction and distribution-free coverage: Vovk, Gammerman and Shafer (2005), *Algorithmic Learning in a Random World*; Angelopoulos and Bates (2023), *Conformal Prediction: A Gentle Introduction*, Foundations and Trends in Machine Learning.
* Selective prediction and abstention: Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, NeurIPS.
* Scientific reasoning evaluation: inspect established physics question answering and scientific-language benchmark papers and their train/test leakage analyses before selecting any benchmark.

These are **candidate closest-prior-art categories**, not an exhaustive, current literature search. Verify bibliographic details and search 2025–2026 work before publication. In particular, exact inclusion-exclusion, paired resampling, and finite-bootstrap undefined-event probabilities should be treated as established mathematics unless a genuinely new theorem or application is demonstrated.

## Experimental and falsification gates

* **Correctness gate:** production sampler contract must match a specified oracle, or a new oracle must be derived for the actual coupling. Any mismatch blocks the estimator claim.
* **Calibration gate:** repeated independent physics-case samples must estimate coverage, conditional coverage by family, abstention rate, and effective sample size with uncertainty intervals. Predefine a coverage tolerance and reject the claim if the lower confidence bound fails.
* **Baseline gate:** compare to simple no-abstention, majority/consensus, confidence threshold, and established selective-prediction or conformal baselines where their assumptions apply. Equalize data and inference budgets.
* **Scientific gate:** use physics problems with externally checkable answers, unit/dimensional consistency, and out-of-distribution perturbations. Include negative controls and leakage checks. Do not infer improved physics reasoning from bootstrap correctness.
* **Novelty gate:** search and document directly overlapping work, distinguish an original problem formulation from a new estimator, and state negative results. If the only contribution is an implementation of established bootstrap identities, frame it as a reproducibility or engineering note, not a novel research paper.

## Zero-cost cloud and integrity constraints

No model training, inference, simulations, large downloads, or compute-heavy tasks on the user's laptop. No cloud execution until the actual account's free quota, billing/card requirements, usage ceilings, and workflow availability are verified. Public GitHub visibility does not prove GitHub Actions minutes remain. Keep all work separate from other repositories. Log AI assistance and any disclosure requirements of the eventual publication venue. November 22, 2026 is an internal target, not a promise of publishable evidence.
