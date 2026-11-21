# Selective-risk identification and coverage comparability (2026-11-21)

Status: theoretical analysis and preregistered reporting guidance, **not** empirical validation or a novelty claim.

## The estimand and a selection pitfall

For each held-out example i, let Y_i(a) be the binary error indicator under arm a and A_i(a) be its frozen-threshold acceptance indicator. At the target population, arm-specific selective risk is R_a = E[Y(a) A(a)] / E[A(a)] for positive coverage C_a = E[A(a)]. This conditions on **different accepted populations** if A(temporal) differs from A(baseline). Therefore R_temporal - R_baseline is a deployment-policy comparison, not the causal effect of timestamps on a fixed set of questions. Equal *aggregate* coverage does not imply identical accepted examples.

Example: On four items with identical per-item errors across two arms, suppose errors are [0,0,1,1]. Arm T accepts items 1 and 2; arm B accepts items 3 and 4. Both have coverage 50%, yet their selective risks are 0 and 1. An apparent 100-percentage-point improvement can arise entirely from acceptance-set composition. This is not a bug in the metric; it limits its interpretation.

## Mandatory complementary analyses

1. **Policy estimand (primary operational outcome):** compare R_T and R_B at each arm's preregistered frozen threshold, reporting C_T, C_B, accepted counts, numerator error counts, and the coverage noninferiority test. If coverage differs beyond the prespecified margin, mark the risk comparison non-confirmatory.
2. **Common-set diagnostic (not a replacement primary outcome):** compute error rates on the intersection of accepted examples, with intersection size and source-family breakdown. This asks whether predictions improve on questions both systems would answer, but may be underpowered or unrepresentative.
3. **Selection decomposition:** report accepted-only-T and accepted-only-B strata, their sizes and observed error rates, plus the overlap. Do not interpret differences between those disjoint strata as per-example causal effects.
4. **Paired prediction diagnostic:** on the full common held-out question set, compare per-item errors regardless of acceptance, when each arm produces a prediction. This estimates a distinct full-coverage prediction-quality outcome, not selective risk.
5. **Coverage–risk curve:** report descriptive curves using predeclared scores without selecting a post-hoc operating point from held-out labels. Curves are exploratory unless their construction and aggregation were frozen.
6. **Dependence and multiplicity:** use source-family clustered resampling with enough independent families, preserve domain-specific results, and adjust the prespecified confirmatory comparisons. A bootstrap cannot repair leakage or too few independent clusters.

## Temporal causal attribution

A randomized within-question assignment of timestamp condition (genuine vs shuffled), with identical evidence content and compute budget where feasible, provides a cleaner test of temporal sensitivity than observational differences between task collections. Shuffling must preserve surface formatting and avoid inadvertently altering answerability or licensing/provenance. Report manipulation validity checks and a placebo on timeless questions. A significant T-versus-shuffle difference alone is not proof of reliable temporal reasoning: verify directional correctness against independently adjudicated as-of labels.

## Hard stop conditions

Do not claim a temporal mechanism when gains disappear on common-accepted items and are fully consistent with changed acceptance composition; report this as policy-level selective-risk behavior only. Do not claim cross-domain generalization from pooled averages, from timeless math/physics items with decorative timestamps, from family-overlapping splits, or from recalibration on held-out labels. If no licensed independent labels or no genuinely free no-billing inference exists, label the November 22 output **methods/preregistration without empirical discovery**.

## Reproducibility outputs

For every domain and arm, publish immutable example IDs, family IDs, correctness labels, prediction errors, acceptance booleans, frozen thresholds, coverage, risk numerators/denominators, overlap and disjoint acceptance-stratum tables, paired full-coverage error table, workflow SHA, and adjudication protocol. Suppress personal or restricted data; publish digests and access instructions where redistribution is not licensed.

This note sharpens interpretation of the existing frozen-threshold and paired-disagreement code; it does not assert those implementations already produce all diagnostics above.
