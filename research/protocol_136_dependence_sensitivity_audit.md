# Protocol 136 — Dependence sensitivity and denominator-failure bounds

Date: 2026-11-08. Status: mathematical specification, not empirical validation.

## Scope and finding

Protocol 135 computes the exact union probability of undefined denominators **only when family-level resampling streams are independent**. This assumption is stronger than the marginal statement that each family has n independent uniform lineage draws with replacement. Correlated seeds, shared sampled lineage indices, common upstream random streams, or a jointly resampled panel may invalidate the product formula even when each family's marginal undefined probability remains correct.

For each positive-weight family i, define U_i as the event that its resample contains no jointly accepted lineage. Under within-family independent draws, p_i = P(U_i) = ((n_i-a_i)/n_i)^{n_i}. Without any assumption about dependence **between** family events, elementary union bounds give

max_i p_i <= P(union_i U_i) <= min(1, sum_i p_i).

When families are independent, the sharper equality is P(union_i U_i) = 1 - product_i (1-p_i). The equality must not be used for shared-index resampling without proving independence. These are established probability identities, not novel theory.

## Exact dependence counterexample

Consider two families, each with two lineages and exactly one accepted lineage. Both have marginal p_i=1/4.

* Independent family resampling gives union probability 1-(3/4)^2 = 7/16.
* Perfectly coupled resampling with identical accepted flags and identical two sampled indices gives union probability 1/4.
* Both values satisfy the dependence-robust bounds [1/4,1/2].

Thus an independent-family analytic preflight may be numerically wrong for an implementation using common resample indices. The direction of error is not generally fixed.

## Required implementation audit

1. Trace the production sampler's unit of resampling: lineage, family, physics task, intervention, or global panel.
2. Establish whether each family's draw indices are independently generated conditional on the observed data, rather than merely seeded reproducibly.
3. Confirm that the preflight's jointly accepted flags are computed from the same admissibility rule as the actual resampler.
4. If families share indices or constraints, replace the independent product with a joint exact oracle for small fixtures, or report the dependence-robust interval above; do not label the independent formula exact.
5. For any correlated-sampling fixture, compare empirical proportions only after an eligible zero-cost cloud run and report finite-sample uncertainty.

## Falsification criteria

* A shared-index two-family fixture whose production undefined frequency converges toward 7/16 rather than 1/4 when the two families' acceptance patterns and draws are identical falsifies the claimed coupling contract.
* A preflight returning 7/16 for that coupled fixture falsifies its calibration as an exact probability under the shared-index contract.
* A preflight returning a point probability outside [max p_i, min(1,sum p_i)] falsifies even the marginal assumptions or the implementation.
* A change in family weights that are strictly positive should not change the event; crossing to zero weight may change it.
* An undefined denominator is not equivalent to a failed scientific intervention, and its probability does not establish confidence-interval coverage.

## Reproducible zero-cost experiment plan

Author a standard-library-only deterministic exact enumeration of two shared-index families, with one test for identical flags and another for complementary flags. Compare its exact rational probability with the independent-family oracle and the dependence bounds. Keep these tests as source until GitHub Actions account-level billing settings, public-repository runner eligibility, concurrency limits and any applicable quotas have been verified. Do not dispatch a job on an unverified runner. The user's laptop is not a compute target.

## Publication boundary

The mathematical dependence audit strengthens a validation protocol. It supplies no measured improvement in NLP, physical reasoning, safety, or model calibration. A frontier-lab-relevant contribution still requires competitive baseline comparisons, a recent prior-art review, preregistered physics-language tasks, independent evaluation, and negative controls. The November 22 target is conditional.
