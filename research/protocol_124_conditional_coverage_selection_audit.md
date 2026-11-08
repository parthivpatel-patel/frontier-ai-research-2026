# Protocol 124 — Conditional bootstrap coverage and selection audit

Status: preregistered analysis plan; **not executed**. Date: 2026-11-07. Scope: independent frontier AI research only.

## Audited implementation
Reviewed `research/common_acceptance_bootstrap.py`, `research/analytic_preflight.py`, `research/preflight_gated_bootstrap.py`, and `research/admitted_preflight_bootstrap.py` at commit `89b34c204e52f23ec471c8976fa2e4ea1b19107f`.

The point estimand is a normalized weighted sum of within-family unsafe-label differences **conditional on both systems accepting the same intervention**. It is not the unconditional safety effect of deployment and cannot compare systems' safety on interventions outside common acceptance. Conditioning on a post-response acceptance variable may select a systematically different set of problems. This is descriptive matched-support inference, not causal identification.

## Newly identified reporting hazard
The preflight eligibility gate is deterministic given the observed sample, but the reported percentile endpoints still depend on the random seed and on the number of *defined* bootstrap draws. Passing the analytic gate does not guarantee a specified effective Monte Carlo sample size: `replicates=1` can return a degenerate interval with two equal endpoints if the single draw is defined. Such an interval must not be interpreted as calibrated 95% uncertainty. The exact conditional undefined probability bounds the frequency of undefined draws under the resampling design; it does **not** bound statistical coverage error or guarantee precision of the estimated 2.5% and 97.5% quantiles.

A second hazard is that `max_undefined_fraction=1.0` in the underlying bootstrap suppresses its old Monte Carlo eligibility rule but conditions percentile endpoints on *defined* draws. The distribution of retained draws is the bootstrap distribution conditional on all active families having a nonzero joint-acceptance denominator. It is not the unconditional distribution of the original estimator, which is partly undefined.

## Frozen falsification matrix (before any cloud run)
1. **Complete acceptance, null contrast:** independent lineages, both systems accept, equal unsafe probabilities. Estimate type-I rejection and interval coverage for the true zero contrast.
2. **Complete acceptance, nonzero contrast:** controlled paired Bernoulli outcomes with a known population contrast; measure bias, coverage, and interval width.
3. **Rare common acceptance:** vary joint acceptance probability across 0, .01, .05, .2, 1; compare empirical undefined-draw frequency with exact preflight probability.
4. **Family heterogeneity:** vary family-specific acceptance and error rates, including opposite-sign contrasts, holding prespecified weights fixed.
5. **Lineage dependence:** induce within-lineage correlations and cross-lineage correlations separately. The latter violates the resampling independence assumption and must be reported as a failure mode.
6. **Informative selection:** make acceptance depend on latent difficulty associated with unsafe responses. Report common-support contrast alongside unconditional unsafe-per-intervention risk with abstentions separately identified; never equate the estimands.
7. **Seed and replicate sensitivity:** fixed admitted dataset, prespecified seeds, and replicate counts 1, 20, 200, 2000, 10000. Eligibility should be seed-invariant; CI endpoints and effective defined counts need not be. Flag intervals based on too few defined draws as unreliable.
8. **Undefined original denominator:** no joint acceptance in at least one positive-weight family. Report undefined point and interval; never impute zero.
9. **Adjudication leakage:** intentionally duplicated or non-heldout interventions must fail admission.
10. **Physics-family shift:** train/calibration families disjoint from heldout families; quantify any out-of-family generalization separately from in-family results.

## Design and metrics
Use a fixed, disclosed synthetic data-generating process with a known population target. Generate independent *datasets* in an outer loop and bootstrap each dataset in an inner loop. Record unconditional coverage (with undefined intervals counted as noncoverage), coverage conditional on interval issuance, issuance probability, effective defined bootstrap draws, absolute bias, mean interval width, false-sign rate, and empirical versus analytic denominator-failure probability. Report Monte Carlo standard errors for estimated rates, including the number of outer datasets. Do not call conditional coverage nominal coverage. Never choose seeds, thresholds, or scenarios after inspecting favorable outcomes.

The analytical preflight threshold (currently .01) is a reporting convention, not a theorem. Treat it as a sensitivity parameter and justify it before confirmatory experiments. The percentile method requires independent evaluation against at least a cluster-aware alternative and a conservative no-interval baseline.

## Feasibility and resource controls
Implement small deterministic unit fixtures first. Run only on GitHub-hosted cloud CI **after** checking repository Actions permissions, actual available free quota, billing configuration, and that execution cannot consume paid overage. Do not assume public repository status guarantees free unlimited execution. No laptop training, inference, downloads, or simulation. Do not enable paid cloud services or submit GPU jobs. Any uncertainty about account-specific billing means **do not dispatch**.

## Publication and novelty gate
Closest-prior-art comparison must include selective classification/risk-coverage, abstention-aware evaluation, paired clustered bootstrap, missing-data/selection bias, causal intervention benchmarks, and physics-grounded reasoning evaluations. A new implementation of a standard conditional bootstrap is not itself evidence of novelty. Before a public manuscript: verify dated primary sources; run reproducible independent physics tests with adjudication provenance and competitive baselines; disclose AI assistance consistent with venue rules; publish negative findings and limitations. Target 2026-11-22 is conditional, not a submission promise.

## Session provenance
This file records a code-based audit and a future experiment specification only. **No CI tests, simulations, model inference, quota verification, or empirical experiments were run in this session. No numerical research results are claimed.**
