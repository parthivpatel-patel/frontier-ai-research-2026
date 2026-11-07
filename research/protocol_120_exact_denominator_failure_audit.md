# Protocol 120 — Exact bootstrap denominator failure audit

Date: 2026-11-07. Status: analytic diagnostic specification; no experiments or cloud tests executed.

## Question

When does the family-stratified lineage bootstrap in `research/common_acceptance_bootstrap.py` fail to produce a defined common-acceptance contrast? The existing estimator drops bootstrap draws with an empty joint-acceptance denominator in any positive-weight family. Protocol 119 correctly warns that the remaining percentile interval is conditional on defined draws.

## Exact finite-sample probability

For positive-weight family f, let n_f be the number of distinct sampled lineages, and let k_f be the number of lineages containing at least one intervention jointly accepted by systems A and B. The implementation draws n_f lineages independently with replacement, uniformly from these n_f lineages. Therefore the exact probability that a resampled family has no joint-acceptance denominator is

q_f = ((n_f - k_f) / n_f) ** n_f.

This follows because all n_f draws must select from the n_f-k_f lineages with zero joint acceptance. The formula holds for any number of interventions per lineage; a lineage with at least one joint acceptance contributes a positive denominator whenever selected. For k_f = 0, q_f = 1 and the original estimand is undefined. For k_f = n_f, q_f = 0.

Because families are resampled independently, the probability that at least one positive-weight family has an undefined denominator is

q_any = 1 - product_f (1 - q_f).

These probabilities are **conditional on the observed lineage-level acceptance pattern**, not the population probability of abstention or a proof of confidence-interval coverage. Families with zero preregistered weight are excluded from this calculation consistently with the implemented estimand.

## Concrete counterexample

For one family with n=2 and k=1, q_f=(1/2)^2=0.25. With two such positive-weight families, q_any=1-(0.75)^2=0.4375. Thus nearly 44% of bootstrap draws are expected to be undefined under the observed acceptance pattern, despite a defined original contrast. An arbitrary tolerance of 1% cannot turn the remaining percentile interval into an unconditional 95% confidence guarantee.

For n=10, k=1, q_f=0.9^10≈0.348678. Adding more lineages that never jointly accept does not necessarily make denominator failure rare.

## Implementation requirements

1. Report n_f, k_f and q_f for every positive-weight family, alongside q_any, observed undefined fraction and bootstrap seed.
2. Verify that the observed undefined fraction converges toward q_any with increasing synthetic replicate counts; this is a *test of implementation*, not an AI performance result.
3. If the original denominator is zero in any positive-weight family, return an undefined point estimate and no interval; never drop or silently reweight that family.
4. Distinguish finite Monte Carlo variation from systematic deviation: for B independent replicates, the undefined count has binomial distribution Binomial(B,q_any), conditional on the observed dataset and PRNG sampling assumptions. This diagnostic does not establish coverage.
5. Keep all prespecified weights and thresholds frozen; report joint-acceptance prevalence and the four acceptance cells.
6. Do not claim the interval is calibrated even if q_any is small. Separate Monte Carlo denominator validity from repeated-sampling coverage of the scientific estimand.
7. Test edge cases k=0, k=n, multiple families, zero-weight families, lineage-ID collisions across families, and within-lineage multiple interventions.
8. Use only eligible verified free cloud execution for computational checks; never run training, inference or simulations on the user's laptop.

## Falsification and publication consequence

If empirical undefined fractions consistently contradict the analytic q_any beyond expected Monte Carlo variation, investigate the resampling implementation before using any interval. If synthetic repeated-sampling coverage misses the prespecified nominal target materially, withdraw confirmatory coverage claims regardless of denominator validity. Even a correct analytic q_any does not establish physical reasoning, intervention validity, adjudicator independence or scientific novelty.

## Related implementation

- `research/common_acceptance_bootstrap.py` (family-stratified resampling)
- `research/admitted_common_acceptance_bootstrap.py` (admission bridge)
- `research/protocol_119_selection_bootstrap_novelty_audit.md` (selection and coverage concerns)

No compute or account-specific cloud quota was verified in this document. No new test execution or empirical findings are claimed.
