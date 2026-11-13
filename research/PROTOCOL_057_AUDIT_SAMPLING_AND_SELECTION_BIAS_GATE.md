# Protocol 057 — Audit-sampling identification and selection-bias gate

Date: 2026-11-13. Status: analytical design; no experiments executed and no novelty claim.

## Why this gate is necessary

Protocol 056 proves that unlabeled verifier outputs do not identify truth-conditioned reliability. A labeled audit can help, but **a convenient or selectively chosen audit is not necessarily representative**. This protocol specifies the sampling conditions under which a joint-positive claim's truth probability is estimable, and the failure modes that must be reported.

Let Y denote independently audited truth, V=(V1,V2) the two verifier outputs, and A=1 indicate that a claim receives an audit. The target is theta=P(Y=1 | V=11) in a prespecified population of eligible claim families. The observed audited quantity is theta_A=P(Y=1 | V=11,A=1). These need not coincide.

## Exact nonidentification example

Suppose the joint-positive stratum has equal proportions of true and false claims. Audit every true claim but only one in four false claims. Then

P(Y=1 | V=11)=1/2,

but

P(Y=1 | V=11,A=1)=(1/2)/(1/2+1/8)=4/5.

Thus an apparently 80% reliable audited sample can correspond to 50% population reliability. The numerical example is constructed, not an empirical measurement.

## Identification conditions and estimators

**Random auditing within the stratum.** If A is independent of Y conditional on V=11 and the target population definition, then theta_A=theta. In practice the sampling protocol must establish this, not merely assume it. If families are sampled unequally, use design weights and family-aware uncertainty.

**Known unequal inclusion probabilities.** If each eligible claim i has a known positive audit inclusion probability pi_i, a design-based ratio estimate for the joint-positive stratum is

    theta_hat = [sum_i A_i 1(V_i=11) Y_i/pi_i] / [sum_i A_i 1(V_i=11)/pi_i].

This is a ratio of Horvitz–Thompson totals; it is not exactly unbiased in finite samples, and zero denominators are possible. It targets the specified finite population under the documented design. Audit selection depending on unobserved truth is not correctable merely by claiming propensity adjustment.

**Unknown selection mechanism.** Without credible selection assumptions, do not report a point-identified population reliability. A simple worst-case bound can be given if the audited fraction q=P(A=1|V=11) is known and the audited truth rate t=P(Y=1|V=11,A=1) is observed:

    q*t <= theta <= q*t + (1-q).

The bound follows by writing theta=q*t+(1-q)*P(Y=1|V=11,A=0) and allowing the unaudited truth rate to range from 0 to 1. It is a population identity, not a sampling confidence interval; uncertainty in q and t must be propagated separately. When q is tiny the bound is nearly vacuous.

## Claim-family and physics-specific safeguards

Define the sampling frame before inspecting verifier scores. Record eligibility, exclusions, source family, theorem or physical regime, version, label adjudicator, and audit probability. Avoid treating paraphrases of the same theorem or variants of the same physics equation as independent evidence. For physics, a statement can be true only under a declared model, units, initial/boundary conditions, and approximation regime. Label ambiguity is a separate outcome, not a forced binary ground truth.

If human auditors see verifier decisions, record that exposure and test for adjudication bias. Where feasible, use blinded adjudication and independent reference checks. If verification relies on the same shared retrieval evidence that produced the original outputs, report correlated evidence provenance.

## Falsification tests

1. Compare randomized within-stratum audits against convenience/uncertainty-selected audits using a *predeclared* finite synthetic population with known truth; never call this an LLM result.
2. Test a zero-audit stratum, missing inclusion probabilities, zero/near-zero propensities, and duplicate claim families.
3. Check that the worst-case interval contains both the constructed true population rate and all feasible completions of missing labels.
4. Evaluate interval width and risk-coverage at matched audit budgets, not merely observed audited accuracy.
5. Repeat the design under shifted theorem families, changed physics regimes, and verifier dependence; do not reuse calibration families in the held-out test.
6. Require confidence procedures that account for family clusters and the sampling design; the elementary bound above alone provides no frequentist coverage guarantee.

## Novelty and go/no-go

The selection-bias example, inverse-probability weighting, missing-outcome bounds, and stratified audit design are established statistical ideas. Relevant prior-art families include missing-data theory, survey sampling, verification bias in diagnostic testing, partial identification, and selective classification. A publishable claim requires a specific AI-verifier protocol and evidence of incremental value against strong audit-aware and duplicate-aware baselines. If a representative audit cannot be obtained, the manuscript must say so and limit conclusions to assumption-conditional or partially identified results.

## Zero-cost execution policy

This document requires no compute. Future code may use standard-library exact arithmetic on a **verified free cloud runner only**, after checking the repository's billing settings, account-specific included minutes, storage and artifact costs, and runner availability. Do not run workloads on the user's laptop or on a paid/trial/card-backed service. No inference, cloud job, or test execution is claimed here.
