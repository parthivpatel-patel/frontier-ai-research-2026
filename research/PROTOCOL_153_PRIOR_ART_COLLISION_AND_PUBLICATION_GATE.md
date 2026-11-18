# Protocol 153 — Prior-art collision matrix and publication decision gate (2026-11-17)

## Status
Research audit and falsifiable experimental design; **not** a novelty claim, full-text systematic review, or empirical finding. This document is deliberately limited to sources with stable bibliographic identifiers and clearly marks unverified theorem-level comparisons.

## Claim-by-claim collision matrix

| Proposed component | Closest established work | Collision / required distinction |
|---|---|---|
| Bounded risk from independent labeled clusters | Hoeffding (1963), *Probability Inequalities for Sums of Bounded Random Variables*, JASA, DOI 10.1080/01621459.1963.10500830 | Standard concentration. Source clusters are the sampling units; cannot claim a new theorem from changing unit names. |
| Simultaneous certificates for a selected fixed policy | Union bound; multiple testing; Angelopoulos et al. (2024), *Conformal Risk Control*, ICLR, arXiv:2208.02814 | Standard selection correction; compare precise risk targets, exchangeability, and calibration assumptions. |
| Selection after examining evaluation outcomes | Dwork et al. (2015), *The Reusable Holdout: Preserving Validity in Adaptive Data Analysis*, Science, DOI 10.1126/science.aaa9375 | Adaptivity is extensively studied; a precommitted finite class is not a novel adaptive-holdout solution. |
| Abstention / selective prediction | Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, NeurIPS, arXiv:1705.08500 | Compare coverage-risk curves at matched inference and annotation budgets, not accuracy alone. |
| Verifier agreement without ground-truth identification | Dawid and Skene (1979), *Maximum Likelihood Estimation of Observer Error-Rates Using the EM Algorithm*, JRSS C, DOI 10.2307/2346806; Manski (2003), *Partial Identification of Probability Distributions* | Latent-label identification needs assumptions; observational agreement alone does not identify true loss. |
| Anytime evidence / sequential stopping | Howard et al. (2021), *Time-uniform, Nonparametric, Nonasymptotic Confidence Sequences*, Annals of Statistics, DOI 10.1214/20-AOS1991 | Fixed-sample Hoeffding bounds cannot be reused under arbitrary optional stopping. |
| Multi-verifier reasoning systems | Cobbe et al. (2021), *Training Verifiers to Solve Math Word Problems*, arXiv:2110.14168; Lightman et al. (2023), *Let's Verify Step by Step*, arXiv:2305.20050 | Compare with outcome/process verification and majority vote under matched budgets; do not imply verification itself is new. |

Bibliographic identifiers are starting points for source retrieval, **not a claim that the exact theorem statements have been checked in full text**. Confirm titles, versions, assumptions, and relevant theorems before final manuscript citations.

## Narrow candidate research question

Can a source-cluster-calibrated abstaining verifier policy reduce *independently labeled, source-weighted decision loss* under a fixed verification budget, across NLP, mathematics and physics, compared with cost-matched single-verifier, vote, and selective-prediction baselines, when evaluation sources are sampled independently and policies are frozen in advance?

This is a testable **empirical** question. It is not established to be novel. An alternative useful contribution is a carefully documented negative result showing that apparent gains disappear under source-disjoint sampling.

## Preregistered falsification and reporting

1. Freeze source IDs, splits, losses, budget, model versions, candidate policies and aggregation rules before evaluation labels are inspected.
2. Use at least one truly independent held-out source collection per domain; report number of source clusters, not just prompts.
3. Primary estimand: source-weighted expected loss with abstention cost specified beforehand. Secondary: coverage-risk curve and cost-normalized error.
4. Bootstrap at the source level for exploratory uncertainty; use a valid prespecified source-level confidence procedure for confirmatory claims. Do not assume clustered bootstrap solves selection bias.
5. Include single-verifier, fixed majority vote, best development-set verifier, and selective abstention baselines under equal inference calls.
6. Report source sampling bias, label disagreement, duplicate contamination, model/data leakage, and sensitivity to abstention cost.
7. **Falsify the claimed benefit** if held-out confidence intervals fail to exclude zero improvement, if a cost-matched baseline matches it, or if the sign reverses under source-disjoint evaluation.
8. Do not extrapolate small open-model findings to proprietary frontier systems or to AI welfare/consciousness.

## Resource and evidence gates

No laptop computation. No training, inference, downloads or paid cloud use authorized. Existing standard GitHub public-repository runner is suitable only for small deterministic regression work subject to confirmed public-runner terms; external free cloud inference needs separate verification of quotas, card/billing requirements, licenses, and availability. A CI green check proves implementation tests, not statistical coverage or research novelty.

## Publication decision as of 2026-11-17

**NO-GO for novelty claims and an empirical paper** until theorem-level collision checks, independent cloud execution logs, and source-disjoint model results exist. A transparent methods/pre-registration note is possible if accurately labeled, but the Nov 22 target is a checkpoint rather than an unconditional deadline.
