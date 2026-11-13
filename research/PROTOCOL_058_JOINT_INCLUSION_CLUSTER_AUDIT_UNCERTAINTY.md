# Protocol 058 — Joint inclusion and uncertainty under family-cluster auditing

Date: 2026-11-13. Status: theoretical design, not executed; no novelty or empirical claim.

## Scope

Protocols 057 and the finite-audit fixture distinguish Horvitz–Thompson (HT) totals from ratio estimates. This checkpoint closes a further gap: knowing each claim's marginal inclusion probability is enough for unbiased HT *totals*, but **not** enough to compute their design variance. Joint inclusion probabilities and a documented audit design are necessary. Claims sharing a theorem, source passage, prompt template, or physical regime may have correlated errors and correlated audit selection.

Let a finite target population contain N eligible claims, fixed binary truth labels y_i, audit indicators A_i, first-order inclusion probabilities pi_i=P(A_i=1)>0, and pairwise probabilities pi_ij=P(A_i=A_j=1). Let T=sum_i y_i and HT total T_hat=sum_i A_i*y_i/pi_i. Under a genuine known probability sampling design, E[T_hat]=T.

The design variance is

Var(T_hat)=sum_i sum_j (pi_ij-pi_i*pi_j)*y_i*y_j/(pi_i*pi_j),

where pi_ii=pi_i. This is a finite-population design identity, not an asymptotic approximation. An unbiased plug-in variance estimator of the displayed form additionally requires positive pi_ij for every term it estimates; if some pair is never sampled together, such a general unbiased estimator is unavailable without additional structure.

## Constructed two-claim counterexample

Take y_1=y_2=1 and pi_1=pi_2=1/2. Two designs share the **same marginal inclusion probabilities**:

- Independent Bernoulli audits: possible selected sets {}, {1}, {2}, {1,2}, each with probability 1/4. HT totals are 0, 2, 2, 4. E[T_hat]=2 and Var(T_hat)=2.
- Exactly-one audit: select {1} or {2}, each with probability 1/2. HT total is always 2. E[T_hat]=2 and Var(T_hat)=0.

Thus identical pi_i and identical unbiased expected totals do not imply identical uncertainty. The difference is pi_12=1/4 versus pi_12=0. These are synthetic, exact examples, not measured AI behavior.

A third design, cluster-all-or-none, selects both claims together with probability 1/2 and neither with probability 1/2. Its HT total is 4 or 0, so E[T_hat]=2 and Var(T_hat)=4. This models the audit-efficiency hazard when a whole related claim family is selected or omitted together.

## Consequences for the AI/ML/NLP/physics study

Define a claim family before seeing verifier outputs, and separate *target unit* (claim versus independent family) from *audit sampling unit*. For mathematical statements, related proof variants may be one family; for NLP, paraphrases and shared source documents may be one family; for physics, a family must also identify the model, units, parameter range, and boundary conditions. These definitions can change the estimand and must be preregistered.

A random audit of individual claims may understate uncertainty if the analysis incorrectly treats shared family errors as independent. Sampling entire families requires first- and second-order family inclusion probabilities or a justified cluster-aware inference procedure. If the design yields zero joint inclusion for some family pairs, explicitly disclose the limitation instead of reporting an unsupported design-unbiased variance estimate.

For stratified joint-positive verifier reliability, the HT numerator is sum_i A_i 1(V_i=11)y_i/pi_i and denominator is sum_i A_i 1(V_i=11)/pi_i. The ratio is generally biased in finite samples and undefined if the sampled denominator is zero. Variance of the numerator alone does not establish ratio confidence coverage. If the entire stratum size is known from the unlabeled sampling frame, consider the HT estimate of the truth total divided by that *fixed known stratum size* instead, with design-aware uncertainty; this remains unbiased for the finite-population stratum mean when the design and inclusion probabilities are valid.

## Falsification / reproducibility plan

1. Implement exact-fraction enumeration of the three two-claim designs and assert their common expectation 2 and distinct variances 2, 0, and 4.
2. Independently evaluate the pairwise variance identity and compare it with direct enumeration; include the diagonal terms.
3. Construct designs with zero joint inclusion, and ensure software refuses a generic unbiased plug-in variance estimator rather than dividing by zero.
4. Predefine audit budgets, claim-family partitions, shift regimes, and verifier dependence. Evaluate held-out family-level risk and coverage, with independent truth adjudication and appropriately documented audit inclusion probabilities.
5. Compare random claim audits, family-cluster audits, and stratified audits at equal *labeling cost*, not merely equal numbers of audited claims. Include naive independent-claim intervals as a deliberately misspecified negative control.
6. Reject the proposed approach if properly cluster-aware audit baselines match its performance, or if coverage fails under prespecified shifts.

## Prior art and novelty boundary

HT estimation, inclusion-probability variance, cluster sampling, and survey-design inference are classical results. This note is an internal methodological correction, **not** a novel theorem. The intended scientific contribution, if any, must be an experimentally supported AI scientific-claim verification system with a nontrivial advantage beyond design-aware auditing, calibrated selective prediction, and dependence-aware baselines. A verified bibliographic comparison and actual experiments are still required.

## Compute and disclosure gate

No execution is authorized until the public repository's GitHub Actions free-runner eligibility, remaining account quota, billing/card conditions, and possible artifact/storage charges are verified for this account. Do not use the user's laptop for computation; do not launch paid services or make inference calls. Mathematical examples in this protocol are constructed, not observations. Publication by 2026-11-22 is conditional on evidence and novelty.
