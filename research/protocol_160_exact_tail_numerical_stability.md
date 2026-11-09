# Protocol 160 — Numerical stability audit of exact paired discordance

Date: 2026-11-09. Status: source-inspected defect and proposed repair; not an executed regression.

## Concrete implementation risk

The Protocol 159 fixture oracle evaluates the two-sided exact McNemar binomial tail as

`min(1.0, 2.0 * sum(comb(D,k) for k in range(m+1)) / (2 ** D))`

where `D=n10+n01` and `m=min(n10,n01)`. This is mathematically correct for independent paired observations, but the integer-to-floating conversion implicit in Python's true division can overflow for sufficiently large D, even though the desired p-value lies in [0,1]. In particular, `D=2000, m=0` should yield `2**(1-2000)` (underflowing to 0 in binary64), not an exception. Balanced large D must return approximately 1, not overflow.

The previous five tests use D<=6 and cannot detect this failure mode. This is a source-level finding, not a verified runtime failure.

## Stable implementation contract

For D=0 return 1. For m=floor(D/2), the doubled lower tail is capped at 1. For all other cases compute the lower tail in log space:

`log_terms[k] = lgamma(D+1)-lgamma(k+1)-lgamma(D-k+1)-D*log(2)`, k=0..m.

Use log-sum-exp to calculate `log_tail` and return `min(1, exp(log(2)+log_tail))`. For very large D, an established special-function binomial CDF may be more efficient, but introducing third-party dependencies requires separate justification. Accuracy near p=1 and extreme tails must be checked against high-precision reference values.

## Proposed deterministic cloud regression cases

1. D=0 returns 1.
2. D=6,m=0 returns 0.03125.
3. D=2000,m=0 returns a finite number in [0,1], possibly 0 due to binary64 underflow.
4. D=2000,m=1000 returns 1.
5. Swap n10/n01 and confirm identical p.
6. Validate all n-cells sum to N and delta_yield matches the direct difference.
7. Verify clustered paraphrases are not passed to the independent-pairs significance routine as if independent.

## Scientific boundaries

Numerical stability does not address dependence, leakage, selection bias, or statistical novelty. Exact McNemar inference is established prior art. Until regression execution and real physics/NLP comparisons, no empirical improvement or novel theorem is claimed.

## Cost and execution

No model inference, training, download, or cloud job was run for this audit. Do not trigger CI until account-specific free quota, billing requirements, and spending safeguards are verified.