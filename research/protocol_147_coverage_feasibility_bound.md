# Protocol 147 — Coverage feasibility bound under abstention

Date: 2026-11-08. Status: analytic design audit only; no experiment executed.

## A necessary bound that changes the preregistration

Let D be the event that an interval is returned, and C the event that the returned interval contains a fixed population estimand. Count undefined or abstained outputs as noncoverage for the unconditional metric. Then

P(C and D) = P(D) P(C | D) <= P(D) = 1 - P(not D).

Consequently, **95% unconditional coverage is mathematically impossible whenever the undefined-output probability exceeds 5%**, regardless of how accurate the intervals are on defined outputs. This is an elementary probability identity, not a new theorem or scientific result. For a claimed nominal 1-alpha unconditional coverage, a necessary (not sufficient) condition is P(not D) <= alpha.

When the undefined probability is exactly q, a target unconditional coverage of 1-alpha requires conditional coverage at least (1-alpha)/(1-q), provided q < 1; if this quotient exceeds 1, the target is impossible. Equality of conditional coverage and nominal coverage does not imply unconditional nominal coverage.

## Exact design checks

For an iid Bernoulli acceptance mask with n observed lineages and a accepted, resampling n times with replacement gives conditional probability of an all-rejected resample q=((n-a)/n)^n. This is conditional on the observed mask. For independent family-level resampling, the chance that at least one family's denominator fails is 1 - product_j(1-q_j), restricted to the actually included families. It is **not** the probability that the outer experiment's interval is undefined: that depends on the estimator, number of bootstrap replicates, and interval policy. Never substitute one for the other.

For illustration, if the *outer* interval itself has undefined probability 0.10, its unconditional coverage cannot exceed 0.90. This hypothetical value is not an observed project result.

## Testable reporting contract

Record for each prespecified cell: N total outer datasets, N returned intervals, N containing target among returned intervals, N abstained; require N_returned + N_abstained = N. Compute return rate r=N_returned/N, selective coverage s=N_containing/N_returned when N_returned>0, unconditional coverage u=N_containing/N. Assert u=r*s within numerical tolerance and u<=r. When N_returned=0, selective coverage is undefined, not 100%.

Before any simulation, distinguish (1) undefined single-bootstrap replicate, (2) undefined aggregate interval, and (3) model abstention. Define a deterministic interval construction and minimum finite-replicate threshold; count all invalid outer outputs. Avoid using a Wilson interval over the *selected* outer cases as though it estimates unconditional coverage.

For uncertainty: compute binomial intervals for return rate and unconditional coverage across independent outer datasets. Conditional coverage is estimated only on returned cases and must be labeled selective. Where outer observations share random sources, account for clustering rather than treating them as iid.

## Falsification and paper implications

- Any unconditional 95% claim with a verified interval-level undefined rate above 5% is refuted without needing interval-content experiments.
- A high selective coverage rate cannot rescue low unconditional coverage; compare methods at matched return rates as well as fixed computational budgets.
- A bound on denominator failures alone does not prove an interval-level failure bound without a verified mapping from failed replicates to interval construction.
- A physics-specific claim still requires a frozen physical estimand, simulator or empirical measurement process, admissibility rule, estimator, independent ground truth, and NLP-to-physics evaluation.
- Novelty remains unestablished: probability identities, bootstrap, and selective inference are established prior art. The possible contribution must be evaluated against existing abstention/calibration/verification systems and held-out physical tasks.

## Execution and cost gate

No cloud job was launched. The existing GitHub Actions workflow imports pytest through tests but does not install it; do not alter or dispatch the workflow until the user's account-specific free allowance, billing exposure and spending controls are verified. Do not run experiments on the user's laptop. Maintain strict separation from all other repositories. November 22 is a conditional target, not a publication claim.
