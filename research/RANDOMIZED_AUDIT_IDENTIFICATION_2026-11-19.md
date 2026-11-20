# Randomized answer auditing: identification and design boundary (2026-11-19)

Status: theoretical design and preregistration supplement; **no experimental result and no novelty claim**.

## Problem
An AI verifier accepts some answers and abstains on others. Correctness adjudication may be missing for a subset of accepted answers. The earlier finite-sample bounds e/N <= R <= (e+u)/N are valid without assumptions but may be too wide to compare systems. Naively calculating error only among adjudicated answers is generally biased if auditing depends on confidence, domain, or apparent difficulty.

## Identifiable estimand under a randomized audit
Fix the evaluation set, generated answers, verifier outputs, and acceptance indicators **before** sampling audits. For each accepted item i, let y_i in {0,1} denote error, A_i in {0,1} its audit inclusion, and pi_i=P(A_i=1 | fixed evaluation frame) its known inclusion probability. Require pi_i>0 for every accepted item in the target estimand. Let N be the number of accepted items.

The Horvitz–Thompson estimator of accepted-answer error is

    R_hat_HT = (1/N) * sum_{i:accepted} A_i*y_i/pi_i.

Conditional on the frozen evaluation frame and fixed (though unobserved) correctness outcomes, E[R_hat_HT]=N^{-1} sum y_i. This is a design-based identity, **not** a model-generalization guarantee. The estimator can fall outside [0,1] in finite samples, and variance can be large when some pi_i are small. A clipped estimate sacrifices exact unbiasedness.

For independent Bernoulli audits, an unbiased design-based variance estimator is

    V_hat = (1/N^2) * sum_{i:accepted} A_i*(1-pi_i)*y_i^2/pi_i^2.

This formula is **not valid unchanged** for fixed-size sampling without replacement; that design requires joint inclusion probabilities and the corresponding covariance terms. Normal-approximation confidence intervals can be poor when few errors are audited. Prespecify design-appropriate exact or conservative intervals and report their assumptions.

## Paired comparison
For two verifiers, define the common target population and fixed acceptance-policy comparison first. A paired audit should preferentially adjudicate the same task/answer unit where both systems' error outcomes are well-defined, with known nonzero inclusion probabilities. When their accepted sets differ, do **not** silently estimate a paired difference on the intersection and describe it as a difference between each system's full accepted risk. Report separate denominators and the intersection estimand explicitly. Shared audits may reduce variance, but the covariance depends on the actual sampling design.

## Stratification
Stratify by NLP, mathematics, and physics, plus source and score band when useful. Choose nonzero inclusion probabilities within every preregistered stratum. Compute per-family estimates before any pooled result; declare aggregation weights independently of observed outcomes. Small strata may require full adjudication or conservative intervals. Never infer a target-domain reliability guarantee from an unlabeled target sample without explicit transport assumptions.

## Falsification and release checks
1. Publish the frozen item IDs, acceptance decisions, strata, audit probabilities, randomization seed, adjudication protocol, and provenance without disclosing protected answer keys.
2. Show balance diagnostics for the audit draw; verify every target unit has positive inclusion probability and that all audited outcomes have independent adjudication.
3. Compare complete-case error, worst-case missing-label bounds, and design-weighted error, with uncertainty intervals appropriate to the actual sampling design.
4. Report sensitivity to differential adjudication errors and nonresponse; a planned audit with missing adjudications is not automatically an ignorable randomized sample.
5. Evaluate within-family risks at matched family coverage and cost. Do not promote a pooled gain when a family reverses it.
6. Refuse claims of empirical improvement if intervals are too wide, labels leak into verifier selection, baseline budgets are mismatched, or held-out performance does not replicate.

## Prior-art and originality boundary
Horvitz–Thompson weighting and randomized survey auditing are established methods. Selective classification, conformal risk control, and conditional/shift-aware reliability have extensive prior art. This note is an adaptation of established sampling logic to the planned AI-verifier evaluation. Any original contribution must be separately demonstrated against close methods and supported by held-out evidence.

## Compute and publication gate
Only standard GitHub-hosted public-repository CI may be considered after confirming current eligibility and restrictions; never enable billable larger runners or paid services. Do not run model inference on the user's laptop. No model experiments were performed for this note. The November 22 checkpoint may produce a methods/preregistration release if empirical novelty remains unproven.
