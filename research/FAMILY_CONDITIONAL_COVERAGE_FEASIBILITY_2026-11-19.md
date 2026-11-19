# Family-conditional coverage feasibility and preregistered comparison gate

**Status (2026-11-19):** methodological derivation and prospective protocol, not empirical evidence or a novelty claim. This note extends the existing source-family aggregation-reversal audit.

## Why pooled coverage matching is insufficient

For family (f), let (n_f) be the number of evaluated candidate answers and (a_{mf}(t_m)) the number accepted by verifier (m) at threshold (t_m). Define (c_{mf}=a_{mf}/n_f). Pooled coverage is (C_m=\sum_f (n_f/N)c_{mf}). Equal pooled coverage imposes only one scalar constraint on the vector of family coverages. It does **not** imply (c_{Af}=c_{Bf}) for any family.

The published synthetic aggregation-reversal test provides a constructive example: with two families of 100 items each, verifier A accepts (90,10) and verifier B accepts (10,90). Both have 50% pooled coverage, but their family-specific coverage differs by 80 percentage points in both families. A pooled selective-risk comparison can therefore reverse a family-balanced comparison without any within-family improvement.

## Discrete thresholds and nonexistence of an exact match

With deterministic thresholding and a finite roster, attainable acceptance counts are discrete. If all scores in a family tie, a global threshold can accept either zero or all tied items; an exact target of 50% may be unattainable. Even if a method can attain a target pooled coverage, the same global threshold need not attain the target in every family. Post-hoc threshold tuning on the held-out test set is not a valid repair.

A family-specific randomized boundary rule could attain *expected* coverage, but it changes the deployment policy, adds randomness and requires preregistration; realized coverage remains random. Such a policy must not be silently substituted for a deterministic global threshold.

## Operational gate

1. Freeze candidate answers, source-family assignments, correctness labels, verification-cost measurement, thresholds and tie policy before opening held-out results.
2. Calibrate thresholds using calibration data only. Record both the target and attainable coverages; never force test-set equality by retrospective threshold adjustment.
3. On the full held-out roster, report for each verifier: total coverage, family coverage, family selective risk (undefined if no accepted answers), micro selective risk, prespecified macro risk, and complete verification cost including rejected cases.
4. Declare the pooled equal-coverage claim **ineligible** when coverage is not matched within the prespecified tolerance; even when pooled coverage matches, label it *pooled-only* unless family coverages also match.
5. For a family with zero accepted answers, report risk as undefined; do not impute zero or omit the family without an explicit sensitivity analysis.
6. Analyze paired acceptance disagreements and discordant accepted errors. Use source-family-aware resampling or uncertainty intervals; do not treat questions sharing a source/model family as independent by default.
7. Report budget-matching and coverage-matching as separate feasibility checks. If either fails, present descriptive comparisons rather than superiority at matched resources.
8. Keep deployment thresholds frozen. Equal-coverage retrospective curves are secondary diagnostics, not prospective deployment claims.

## Falsification criteria

- A purported cross-family improvement disappears under prespecified family-balanced weights.
- Family acceptance vectors differ beyond the prespecified tolerance despite matched pooled coverage.
- Target coverage cannot be attained under the frozen deterministic threshold/tie policy.
- Selective risk is undefined in a required family or confidence intervals fail to exclude no improvement.
- The proposed verifier exceeds the measured full-roster cost budget, or the budget audit cannot be reproduced.
- Improvements depend on test-set threshold selection, source-family leakage or altered candidate answers.

## Closest conceptual prior art and novelty boundary

This note does not claim to discover aggregation reversal, selective classification or calibration. Relevant established foundations include Geifman & El-Yaniv (2017), *Selective Classification for Deep Neural Networks*; Geifman & El-Yaniv (2019), *SelectiveNet*; and the broader literature on Simpson's paradox, distribution shift and group-conditional performance. A defensible contribution would require a genuinely new verified method or rigorous new evidence under source-family shifts, not merely this evaluation checklist.

## Reproducibility and resource constraint

The existing exact-arithmetic synthetic test `tests/test_source_family_aggregation_reversal.py` checks a pooled-versus-family reversal. A future no-charge standard GitHub-hosted runner may execute lightweight standard-library tests after verifying repository Actions eligibility and billing settings. This note neither triggers cloud jobs nor requires local inference, training, GPU resources or downloads. Real held-out NLP, mathematics and physics experiments remain unperformed.
