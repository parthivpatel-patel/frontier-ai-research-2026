# Protocol 121 — Analytic preflight and uncertainty reporting contract

Date: 2026-11-07. Status: methodological specification, not an executed experiment.

## Scope and verified code dependency

Inspected `research/common_acceptance_bootstrap.py` and `research/denominator_failure_diagnostic.py` on the repository default branch. The bootstrap samples each positive-weight physics family's distinct lineages uniformly with replacement, exactly n draws for n observed lineages. A replicate is undefined if any positive-weight family contains zero jointly accepted interventions after resampling. The diagnostic calculates q_f=((n_f-k_f)/n_f)^n_f and q_any=1-product_f(1-q_f). These quantities condition on the observed acceptance pattern.

## New preflight decision contract

Before requesting cloud bootstrap execution, validate the paired heldout dataset using the admission gate and then calculate n_f, k_f, q_f, and q_any. A valid original contrast requires k_f >= 1 in every positive-weight family. If any k_f=0, mark the point and confidence interval undefined. Do not silently remove a family, replace an undefined contrast with zero, or renormalize remaining weights.

For B independent bootstrap replicates, conditional on the fixed observed dataset and the documented pseudorandom sampling mechanism, the undefined replicate count U has the Binomial(B,q_any) distribution. Therefore E[U]=B*q_any and Var(U)=B*q_any*(1-q_any). A preregistered implementation check can compare U/B with q_any using a conservative Hoeffding tolerance sqrt(log(2/alpha)/(2B)); at alpha=0.01 and B=2000, tolerance is approximately 0.0364. This is a stochastic implementation sanity check, **not** a confidence interval for scientific performance and **not** evidence of nominal bootstrap coverage. Because the pseudorandom generator is deterministic given a seed, repeated runs at the same seed are not independent replications.

If q_any exceeds the preregistered maximum undefined fraction, mark the percentile interval as ineligible *before* drawing replicates. This avoids seed-dependent eligibility decisions. Retain the empirical undefined count as an implementation diagnostic; report both analytic and empirical fractions. A small q_any does not validate percentile coverage or the scientific estimand.

## Audit of current behavior and required changes

The current bootstrap decides interval eligibility from the **observed** undefined fraction (`fraction <= max_undefined_fraction`). This means two seeds applied to identical observations can differ in whether they emit an interval, even though their exact conditional failure probability is identical. The current bootstrap also does not include q_any, n_f, or k_f in its output. These are reproducibility and reporting gaps; they are not proof of a coding defect in the point estimate.

Implement a shared, validated population representation to prevent the diagnostic and bootstrap from interpreting different system pairs. Require the exact two expected system IDs and explicit matched intervention keys; validate acceptance and unsafe-label semantics consistently. Report q_any, family diagnostics, seed, B, U, and a clearly labeled conditional interval. Preserve existing output fields where possible and add a versioned result schema. Test whether two different seeds can cause an eligibility flip under the current observed-fraction rule, then verify the analytic gate removes this flip. Do not fabricate a successful test run.

## Falsification matrix

1. Two families n=2,k=1: analytic q_any=0.4375; default 1% threshold must suppress the interval regardless of seed.
2. Every lineage jointly accepts: q_any=0; no undefined replicates should occur.
3. One active family k=0: original point and interval undefined.
4. A zero-weight family with k=0 must not change q_any for positive-weight families.
5. Multiple interventions in a lineage count as one lineage for n_f and k_f.
6. Identical lineage IDs in different families remain independent composite keys.
7. Invalid system IDs, missing counterpart, duplicate records, and contradictory labels must fail closed.
8. Row reordering must not change analytic diagnostics.
9. With B=2000, compare U/B with q_any under multiple fixed seeds and report discrepancies without reselecting seeds.
10. A deliberately biased acceptance mechanism must demonstrate that even q_any=0 does not establish valid inference about the full question population.

## Scientific interpretation and release gate

The common-acceptance paired difference answers a restricted question: among interventions accepted by both systems, what is the weighted difference in unsafe-response rates? It does not measure comparative performance over all interventions, and selection may invalidate transport to the full population. Report the four acceptance cells and coverage alongside this estimand. No confirmatory claims until independent adjudication, calibrated repeated-sampling coverage, heldout provenance, competitive baselines, and a source-verified novelty review are completed.

## Compute and publication safeguards

This protocol contains no experiment, model inference, local workload, or quota assertion. Run future deterministic tests and synthetic simulations only on independently verified no-charge cloud capacity; verify account-specific quota, billing and card requirements first. Do not claim novel mathematics: the binomial and Hoeffding facts are standard probability theory. Cite standard sources before publication and disclose AI assistance according to venue rules. The November 22, 2026 date is an internal target, not a promise of publishable results.
