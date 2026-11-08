# Protocol 126 — Quantile Monte Carlo precision audit

Date: 2026-11-07. Status: analytical audit only; no cloud execution or empirical claims.

## Audited implementation

At the repository state following Protocol 125, `research/safeguarded_admitted_bootstrap.py` suppresses intervals if fewer than 1,000 defined bootstrap draws are available. Its warning correctly states that this is not a guarantee of coverage. This note quantifies a separate unresolved issue: Monte Carlo uncertainty in the estimated percentile endpoints.

## Distribution-free diagnostic

Let `m` be the number of **independent, identically distributed defined bootstrap draws**, and let `F_m` be their empirical conditional CDF. The Dvoretzky–Kiefer–Wolfowitz inequality gives

`P(sup_x |F_m(x)-F(x)| > epsilon) <= 2 exp(-2 m epsilon^2)`.

Thus, with probability at least `1-alpha`, the conditional CDF rank error is at most

`epsilon = sqrt(log(2/alpha)/(2m))`.

At `alpha=.05` and `m=1000`, epsilon is approximately **0.04295**. This is larger than the target 2.5% tail probability, so the bound cannot tightly locate the 2.5% or 97.5% percentile endpoints. For a rank-error tolerance of 0.01 at 95% confidence, the sufficient DKW sample size is `ceil(log(40)/(2*.01^2)) = 18,445` defined draws. This is a conservative *sufficient* bound, not a requirement for every estimator, and is not a guarantee of interval coverage.

A second perspective: at m=1000, the expected number of samples below the true 2.5% quantile is 25, with binomial standard deviation `sqrt(1000*.025*.975) ≈ 4.94`. A nominal 1000-draw threshold therefore permits material Monte Carlo endpoint variation even when every draw is defined.

## Crucial qualifications

1. These statements concern the conditional distribution of defined bootstrap replicates, **not** the original sampling distribution or nominal 95% confidence interval coverage.
2. DKW requires independent identically distributed draws from a fixed conditional bootstrap distribution. Check whether the implementation uses independent replicate RNG streams or sequential draws with independence under the pseudorandom design. This is a mathematical idealization, not proof of cryptographic randomness.
3. Quantile *value* error additionally depends on density near each quantile; a small CDF rank error can correspond to a large endpoint shift in a flat or discrete distribution.
4. A large `m` does not repair selective acceptance, undefined original estimands, within/cross-lineage dependence, or conditional-on-defined-draw bias.
5. Do not replace the 1000 threshold with 18,445 without resource and scientific review. Higher resample counts can be costly, and the DKW bound may be too conservative for the intended descriptive analysis.

## Prespecified implementation and falsification plan

- Report `defined_replicates`, `requested_replicates`, `defined_fraction`, analytic undefined probability, interval eligibility and suppression reason together.
- Calculate and report the DKW rank-error diagnostic at prespecified alpha=.05; mark it as a *Monte Carlo CDF diagnostic*, not coverage.
- On a fixed admitted synthetic dataset, compare percentile endpoints across frozen independent seeds and m=1000, 2000, 10000 and, only if eligible free cloud resources permit, 20000. Measure between-seed endpoint spread; do not select favorable seeds.
- Add deterministic unit tests for m=0, 1, 1000, 18444 and 18445; invalid alpha and noninteger m; monotonicity of the bound.
- Perform an outer repeated-dataset experiment separately to estimate unconditional interval issuance, conditional coverage, and unconditional coverage, with binomial Monte Carlo errors.
- If the conditional interval is unstable, suppress it or report uncertainty as unresolved; do not assert 95% coverage.

## Novelty and publication implication

DKW is established probability theory. Applying it to a bootstrap Monte Carlo precision warning is **not** a novel theorem. The broader paper's contribution must be judged against selective prediction, clustered resampling, missingness/selection, and physics-grounded intervention benchmarks. This note supplies a falsifiable reporting criterion, not evidence of superior model reasoning.

## Execution and cost boundary

This document was prepared by reading repository code and analytical reasoning only. No model inference, cloud jobs, local training, laptop compute, or paid services were initiated. Account-specific GitHub Actions free eligibility and paid-overage safeguards remain unverified; do not dispatch CI until verified. Publication target 2026-11-22 remains conditional.
