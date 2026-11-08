# Protocol 146 — Estimand validity and selective-coverage audit

Date: 2026-11-08. Status: preregistration refinement, no experimental results.

## Problem found in Protocol 145

The proposed Bernoulli acceptance indicators are useful for testing bootstrap definedness, but **do not by themselves define a scientifically meaningful physics parameter or confidence interval**. A nominal 95% coverage statement requires a fixed estimand, a complete data-generating process (DGP), and a specified interval construction. A coverage number computed without those choices would be uninterpretable. This protocol is a design correction, not a new theorem or empirical finding.

## Two independent experiments

**A. Software correctness / definedness.** For each family j, define n_j, a_j and draw n_j indices uniformly with replacement. Let U_j denote no accepted lineage in the resample. Exact probability q_j=((n_j-a_j)/n_j)^n_j; with independently generated family draws P(union U_j)=1-product(1-q_j). This is conditional on the observed acceptance masks, not a frequentist confidence-interval guarantee. Compare analytic oracle to exhaustive enumeration for small cases. Include zero accepted, all accepted, zero-weight exclusion, and family-draw independence checks.

**B. Frequentist interval coverage.** Define a complete DGP independently of the observed data. One minimal diagnostic model: X_i iid Bernoulli(p), with p in {0.1, 0.5, 0.9}; target theta=p. Compare a precisely specified Wilson score interval to a precisely specified percentile bootstrap interval for p. The Wilson score interval is a *benchmark*, not a new method. For the bootstrap interval, specify B, percentile interpolation rule, random seed, whether resamples with all-zero accepted observations are undefined under the production estimator, and what is done when fewer than two finite bootstrap estimates exist. If the production estimator does not actually estimate Bernoulli p, this is a unit test of generic interval machinery only, **not** evidence of the production method's physical validity.

For the physics-specific evaluation, freeze a physical parameter (e.g. known spring constant in a specified noisy harmonic-oscillator simulator), observation model, accepted-lineage predicate, inference estimator, and bootstrap interval before running. Do not label synthetic Bernoulli diagnostics as physics performance.

## Failure and selection semantics

For each DGP cell, report N total, N_defined, N_covered_defined, and N_undefined. Unconditional coverage = N_covered_defined/N; conditional coverage = N_covered_defined/N_defined when denominator positive; definedness = N_defined/N. Report the three jointly, since selective coverage can look favorable while undefinedness increases. State explicitly whether the target claim is unconditional coverage or coverage after abstention. For a method with abstention, report selective risk and risk-coverage curves against matched-budget baselines; never silently discard abstentions.

At n=4 and p=0.1, all-zero datasets are common under the Bernoulli DGP. This is a designed stress case, not a reason to omit failures. Any proposed coverage guarantee must specify whether it includes such samples.

## Execution gate and falsification

1. Repair missing pytest in CI with reviewed, pinned dependencies and run full suite on a verified no-charge hosted runner. No CI execution until account-specific eligibility and spending controls are verified.
2. Record exact code SHA, runner version, dependency lock, seeds, runtime cap, results and logs.
3. Validate analytical definedness against enumeration before any coverage claims.
4. Compare intervals under identical data and compute budgets. Predeclare a tolerance and uncertainty calculation before interpreting nominal coverage.
5. Falsify a universal 95% unconditional-coverage claim with a statistically supported counterexample in any prespecified DGP cell. Do not claim a new guarantee from simulation.
6. Physics/NLP claims require held-out task sets, ground-truth provenance, strong direct-prompting/self-consistency/verification baselines, calibrated abstention, and explicit leakage controls.

## Novelty boundary

Bootstrap, Wilson intervals, selective prediction, and conformal methods are established prior art. A credible original contribution must arise from a validated natural-language-to-physics system and demonstrate distinct value over these baselines. This document makes no novelty or performance claim.

## Resource boundary

Zero spending; cloud compute only after explicit account-specific verification of free quota, billing/card requirements, runner eligibility, and remaining allowance. No laptop workloads. Publication target 2026-11-22 remains conditional.
