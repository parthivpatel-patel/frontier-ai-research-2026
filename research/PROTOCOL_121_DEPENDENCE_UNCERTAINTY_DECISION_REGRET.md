# Protocol 121 — Dependence-estimation uncertainty and decision-regret gate (2026-11-16)

Status: analytical design; no executed tests, measured accuracies, or novelty claim.

## Why a held-out gain may be illusory
Protocol 120 calls for estimating conditional 2×2 joint-verifier tables. In sparse data, four-cell tables fitted separately for T=0 and T=1 can be unstable, especially for rare concordant mistakes. An apparent gain in synthetic decision value may be a consequence of parameter selection or leakage rather than genuine out-of-sample improvement. Report calibration sample sizes by truth state, source cluster, and domain, not only the overall N.

## Finite-sample mathematical audit
For a fixed truth state t, let n_t be the number of independently sampled, adjudicated examples and let X_i be the indicator that both verifiers output positive. Then q_t=P(A=+,B=+|T=t) is estimated by the sample mean. Under IID Bernoulli sampling, Hoeffding gives

P(|qhat_t-q_t| >= epsilon) <= 2 exp(-2 n_t epsilon^2).

Thus a two-sided 95% bound with epsilon=0.05 requires n_t >= ceil(log(40)/(2*0.05^2)) = 738 *per truth state*. This is a conservative distribution-free sufficient bound for a single cell, **not** a guarantee under correlated source clusters, nonrandom labeling, distribution shift, or adaptive selection. To cover all eight conditional cells simultaneously by a union bound, the same epsilon at familywise alpha=0.05 requires n_t >= ceil(log(320)/(2*0.05^2)) = 1754 per truth state. These counts are design calculations, not observed dataset sizes or a claim that this sample is attainable at $0.

For a prior pi and observed ++, the posterior is pi*q_1/[pi*q_1+(1-pi)*q_0]. Even a small absolute error in q_0 can cause a large posterior error if the denominator is small. Do not present plug-in posteriors as calibrated confidence without interval propagation and out-of-sample checking. When the denominator is zero, the observation has zero model probability and the posterior is undefined, not 0 or 1.

## Preregistered evaluation gates
1. Fix label adjudication rules and truth-state stratification before verifier output inspection. Record provenance, uncertainty, abstentions and shared model/prompt lineage.
2. Reserve source-cluster-disjoint train, calibration and test sets. If insufficient independent clusters exist, explicitly downgrade to exploratory evidence.
3. Compare (a) independence plug-in, (b) saturated joint-likelihood plug-in, (c) regularized joint model with predeclared smoothing and (d) a marginal-only/first-verifier baseline. Fit all on the same calibration split.
4. Use held-out log loss and Brier score as primary probabilistic metrics. State an epsilon probability floor for log loss in advance; report clipping sensitivity. Assess decision risk for a preregistered grid of asymmetric losses and verification costs, with no tuning on test labels.
5. Calculate paired claim-level differences, then uncertainty intervals using independent source clusters as resampling units. Where clusters are few, report the limitation instead of pretending IID claim-level bootstrap is valid.
6. Perform stress tests for prevalence shift, missing/abstaining verifier outputs, common-source errors, duplicate verifiers, rare joint cells, and deliberately misspecified dependence. A duplicated verifier must not be credited as independent evidence.
7. Falsification: if the joint model fails to improve both preregistered proper scoring rules and cost-adjusted decision risk under the specified uncertainty criterion, do not claim a practical advantage. If only one improves, label the result mixed; report all domains and negative controls.

## Novelty and prior-art boundary
This is standard concentration inequality, probabilistic calibration and decision-theoretic methodology. Closest established areas include conditional-dependence models for diagnostic tests, ensemble calibration, selective classification, Bayesian value of information, and dependent evidence aggregation. A defensible paper needs a narrowly specified original contribution and independent baselines, not a renamed application of Bayes' rule. Compare against relevant correlated-diagnostic-test and classifier-calibration literature before any novelty assertion.

## $0 reproducibility gate
No laptop execution, model inference or large downloads. Candidate GitHub-hosted CI is not authorized by this document: verify current account-specific included Actions minutes, billing/card requirements, spending limits, repository settings and workflow eligibility before dispatching. Keep synthetic arithmetic checks separate from any model-based benchmark. Archive exact commands, hashes, versions, logs and exit codes after verified free execution.

## November 22 decision
If executable regressions and independently adjudicated held-out evidence remain unavailable, publish only a clearly labeled methods/protocol document, or defer the empirical paper. Never report this design as measured scientific progress.
