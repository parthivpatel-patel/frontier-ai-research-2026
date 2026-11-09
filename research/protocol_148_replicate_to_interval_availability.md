# Protocol 148 — From replicate failure to interval availability

Date: 2026-11-08. Status: exact conditional probability derivation and preregistered verification design; no experiment executed.

## Problem and conditioning

Protocol 147 correctly distinguishes an invalid bootstrap replicate from an undefined outer confidence interval. This protocol supplies the missing bridge **only under explicitly testable assumptions**.

Fix an observed outer dataset X and a frozen bootstrap resampling contract. Let q(X) be the probability that one bootstrap replicate is invalid because at least one required denominator is zero. Suppose B bootstrap replicates are independently drawn conditional on X, each with identical invalidity probability q(X). Let K be the number of valid replicates. Then K | X ~ Binomial(B, 1-q(X)).

If a prespecified interval-construction policy returns an interval if and only if K >= m, for integer 1 <= m <= B, the conditional interval-abstention probability is

P(interval undefined | X) = P(K < m | X)
= sum_{k=0}^{m-1} binom(B,k) [1-q(X)]^k q(X)^(B-k).

Special cases: for m=1, the probability is q(X)^B; for m=B, it is 1-[1-q(X)]^B. Neither formula is valid if the interval may fail for other reasons, such as nonfinite estimates, invalid quantiles, estimator exceptions, or downstream model abstention.

If the interval policy requires a minimum finite *fraction* f, freeze m=ceil(f B) before running experiments. In particular, do not silently drop invalid replicates and report nominal coverage without recording the return rate.

## What is and is not identified

The formula is **conditional on the observed outer dataset** and the frozen sampling design. The unconditional interval-abstention rate across new datasets is E_X[P(K<m | X)], not the expression evaluated at E_X[q(X)]. Nonlinearity makes substitution generally wrong.

If bootstrap draws share a common random state, adaptive stopping, or other dependence, K need not be binomial. If family-level resampling is independent, q(X) may be computed from the verified independent-family oracle; if not, the correct joint resampling law is required. This derivation is elementary probability, not a novel result.

## Deterministic cloud test contract

1. Freeze representative observed acceptance masks, included-family weights, B, m, and seeds; independently enumerate small-case replicate outcomes to obtain exact rational q(X).
2. Compare the production preflight q(X) to the independent oracle. Include excluded zero-weight families and all-rejected masks.
3. For B <= 8, enumerate all valid/invalid replicate-status sequences and compare the exact fraction with the binomial tail formula. Use numerical stable binomial survival/CDF implementations for larger B; test q=0, q=1, m=1, and m=B.
4. Inspect the actual production interval builder: verify whether it returns iff K>=m. If not, record additional failure modes and do not present the binomial tail as the complete interval failure probability.
5. On independent outer datasets, report total datasets, returned intervals, covered intervals, and abstentions; report selective and unconditional coverage separately with uncertainty. Never treat repeated bootstrap replicates as independent outer datasets.
6. Freeze a physics estimand, measurement process, NLP extraction contract, and non-LLM baselines before any AI performance claims.

## Falsification gates

- Reject the conditional binomial model if production bootstrap draws are dependent or adaptive.
- Reject the claimed bridge if intervals can fail when K>=m or succeed when K<m.
- Reject any unconditional 95% coverage claim when measured outer interval abstention exceeds 5%, per Protocol 147.
- Reject novelty claims based solely on binomial tails, bootstrap, or selective-coverage identities; these are established prior art.
- Require independent physics/NLP results and a contemporary closest-prior-art comparison before submission.

## Execution boundary

No local workload, cloud run, inference, paid resource, or spending was initiated. CI remains blocked by missing pytest and account-specific free-tier/billing verification. Do not dispatch GitHub Actions until zero-cost eligibility and safeguards are confirmed. The November 22 manuscript target is conditional on empirical validation and a defensible novel contribution.
