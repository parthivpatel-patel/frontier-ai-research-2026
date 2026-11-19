# Identifiability and shift counterexamples for cross-domain selective verification

Date: 2026-11-19. Status: theoretical design note; no model experiment, novelty claim, or performance result.

## Fixed-roster estimands

For held-out items i=1,...,n with fixed candidate answers and binary correctness labels Y_i (1 correct), let A_{mi}(t) in {0,1} indicate that verifier m accepts at threshold t, and C_{mi}>=0 denote the *entire* verification cost incurred on item i, regardless of acceptance. Define achieved coverage q_m(t)=n^{-1} sum_i A_{mi}(t) and selective error r_m(t)=[sum_i A_{mi}(t)(1-Y_i)]/[sum_i A_{mi}(t)] when the denominator is positive. Otherwise r_m(t) is undefined, not zero. Define full-roster mean cost c_m=n^{-1} sum_i C_{mi}. These are finite-sample descriptive quantities, not causal effects.

For two frozen methods evaluated on the identical roster, a comparison at the same *achieved* coverage q can be defined only if both have an admissible threshold or a prespecified tie-randomization scheme that attains q. If operational thresholds are calibrated before the held-out evaluation, unequal achieved coverage is itself a deployment outcome; do not silently retune thresholds on held-out labels or scores.

## A no-free-lunch shift construction

Consider two equally frequent item types, x=a and x=b. A score-based verifier assigns s(a)=1 and s(b)=0 and accepts only a, yielding 50% coverage. In population P, all a answers are correct and all b answers incorrect, so its selective error is 0. In population Q, reverse the correctness labels while preserving the feature distribution and scores. The same verifier still accepts 50%, but selective error is 1. A reversed-score baseline has the opposite ordering.

This construction shows that **without assumptions linking verification scores to correctness under shift**, a source-family-invariant selective-risk improvement cannot be guaranteed. It is not evidence that any actual verifier fails, nor a new impossibility theorem. The contribution, if any, must be empirical and conditional on a precisely stated shift class.

## Operational failure conditions

1. If held-out source-family labels determine a threshold, the deployment evaluation is contaminated.
2. If method A uses different candidate answers from method B, the contrast includes generation differences.
3. If one method pays for more external evidence or tool calls, a risk difference alone cannot isolate verifier quality.
4. If accepted counts are zero, selective risk is undefined; report coverage 0 and the complete cost.
5. If family-level improvements conflict, do not assert universal cross-domain transfer.
6. If the empirical effect is within uncertainty or vanishes against confidence-only and domain-specific baselines, report a negative or inconclusive result.

## A feasible zero-cost experiment, conditional on verified cloud eligibility

First validate pure-Python synthetic invariants in repository CI. Then freeze public, license-compatible small question/answer/label rosters, source-family splits and hashed evaluation artifacts. Compare (i) confidence-only rejection, (ii) a frozen general verifier, and (iii) domain-specialist checks on identical candidate answers. Report calibration-threshold and held-out ranking evaluations separately. Predeclare the primary coverage region, cost unit, 5% budget tolerance, tie policy and uncertainty method. Execute only after checking account-specific free quota, billing/card requirements, runner availability, and worst-case charge exposure. Do not run models on the user's laptop.

## Prior-art implications

Selective prediction and risk–coverage are established (Geifman & El-Yaniv, 2017; SelectiveNet, 2019); conformal calibration relies on explicit exchangeability or adjusted assumptions (Angelopoulos & Bates, 2023; Barber et al., 2023). Process supervision for math (Lightman et al., 2023), model confidence (Kadavath et al., 2022), and LLM judging (Zheng et al., 2023) provide essential baselines. Bibliographic versions, newer related papers, and licensing remain to be verified against primary texts. The counterexample above is elementary and must not be represented as original mathematics.

## Publication decision

The November 22 target is a checkpoint, not a license to overclaim. Without verified held-out evidence, matched budgets, and completed prior-art screening, publish only a methods/preregistration note with transparent AI-assistance disclosure where required.
