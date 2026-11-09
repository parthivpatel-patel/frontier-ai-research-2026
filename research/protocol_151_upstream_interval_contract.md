# Protocol 151 — Exact upstream interval construction and refined return contract

Date: 2026-11-08. Status: static production-source audit; no execution or empirical validation.

## Source inspected

Read the public default-branch implementations of `research/common_acceptance_bootstrap.py`, `research/preflight_gated_bootstrap.py`, and `research/safeguarded_admitted_bootstrap.py`. This narrows the uncertainty explicitly left open by Protocol 150.

The upstream bootstrap computes `point = contrast(original)`; draws `replicates` lineage-resampled contrasts; retains finite/defined contrasts in `draws`; and sets its percentile interval if and only if `point is not None and draws and fraction <= max_undefined_fraction`. The preflight wrapper calls this function with `max_undefined_fraction=1.0`. Thus, under normal successful execution and validated inputs, the upstream interval is present exactly when the original contrast is defined and at least one bootstrap replicate is defined. The two quantiles use linear interpolation over sorted defined draws. The safeguard then requires at least `min_defined_replicates` (default 1000), which is at least two.

## Refined deterministic contract

For fixed admitted data X and bootstrap draws D, define:
- A(X): scientific admission succeeds and the pipeline returns normally;
- G(X): analytic preflight says interval eligible;
- P(X): original `contrast(original)` is defined;
- K(X,D): number of defined bootstrap replicate contrasts;
- M: safeguard minimum defined replicate count, M >= 2.

For successful calls with the inspected implementation, the final reporting indicator is exactly

`R(X,D) = 1{G(X)} 1{P(X)} 1{K(X,D) >= M}`.

This is a refinement of Protocol 150's three-factor representation, not a new theorem. The former upstream factor U is no longer an independent unknown: given the wrapper's tolerance of 1.0, U is equivalent to P and K>=1. Since M>=2, K>=M implies K>=1. Admission errors and other exceptions are **not** returned intervals and must be counted separately in an end-to-end evaluation.

If conditional on X the replicate-validity indicators are independent and identically distributed with invalidity probability q(X), then for admitted, gate-eligible, point-defined X,

`Pr(R=0 | X) = Pr(K < M | X) = sum_{k=0}^{M-1} C(B,k)(1-q(X))^k q(X)^(B-k)`.

If G or P is false, reporting probability is zero. This reduction is conditional on the implementation, i.i.d. draws, and successful execution; it is not a coverage guarantee. The production RNG is seeded and sequential across families, but independent uniform calls support the conditional i.i.d. bootstrap-replicate model in the ideal pseudorandom model. Finite PRNG behavior and software correctness still require tests.

## Important edge case: zero original denominator

If any positive-weight family has zero jointly accepted interventions in the original data, `contrast(original)` returns None. Resampling cannot create jointly accepted observations absent from the original lineage population, so every bootstrap replicate is also undefined. Consequently P=false implies K=0 for this implementation. This can be tested as an invariant. Do not generalize it to other estimators or changed data pipelines.

## Source-specific falsification checks

1. With valid admitted data and G=true, P=true, K>=M, assert non-null ordered finite endpoints and `interval_reported=true`.
2. With G=false and P=true and K>=M, assert suppression despite defined draws.
3. With P=false, assert all replicates undefined and no interval.
4. With G=true, P=true and K<M, assert `insufficient_defined_bootstrap_draws`.
5. With M=2 and B=1, assert no interval even if the only draw is defined.
6. Inspect exception behavior for malformed data and distinguish pipeline failure from statistical abstention.
7. Use independent exact enumeration for small lineage populations and compare the production Monte Carlo distribution only after verifying zero-cost cloud eligibility.
8. Audit `analytic_preflight` and scientific admission for whether they ever allow G=true while P=false. If impossible, document the proven invariant and simplify further; do not assume it here.

## Scientific and resource limits

These are source-derived logical deductions, not executed tests or novel research findings. Conditional percentile intervals need independent calibration, outer-dataset uncertainty estimates, source-disjoint NLP/physics evaluation, and meaningful competitive baselines. The protocol does not demonstrate model gains. Existing bootstrap and selective-prediction literature remain necessary prior art. No laptop computation, cloud job, model inference, paid infrastructure, or new spending was initiated. The prior CI missing-pytest blocker and account-specific GitHub Actions billing/quota verification remain unresolved. The November 22 target is conditional on empirical evidence.
