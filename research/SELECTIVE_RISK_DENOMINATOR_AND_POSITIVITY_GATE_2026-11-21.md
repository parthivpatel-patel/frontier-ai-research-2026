# Selective-risk denominator stability and positivity gate (2026-11-21)

Status: theoretical audit and preregistration amendment proposal. No model results, new novelty claim, or cloud quota verification.

## Identification issue

For arm a, let A_ai be the acceptance indicator and E_ai the adjudicated error on item i. The pooled selective risk is R_a = (sum_i A_ai E_ai)/(sum_i A_ai), provided sum_i A_ai > 0. This is a ratio estimand, not the average of family risks. If family j has m_aj accepted items and family risk r_aj, then R_a = (sum_j m_aj r_aj)/(sum_j m_aj). An unweighted mean of r_aj answers a different question. Unequal acceptance counts can reverse the ordering of arms under pooled versus equal-family estimands (a Simpson-type composition effect). Report both, with the pooled contrast primary only if frozen before test inspection.

A matched *global* coverage target does not imply family-level positivity: an arm may accept zero items in a source family even when global coverage is nonzero. In such families r_aj is undefined, not zero. Filtering these families separately by arm creates post-selection asymmetry and can change the population being compared.

## Required diagnostic outputs

For each arm and family report total items n_j, accepted m_aj, errors among accepted k_aj, acceptance fraction m_aj/n_j, and whether r_aj is defined. Report arm-wise coverage, absolute coverage difference, pooled risk, equal-family risk on a common predefined evaluable-family subset, and the fraction of families with no acceptance under either arm. The common subset must be disclosed as a *secondary conditional population*, not substituted for the full population.

Report how many source families contribute at least one accepted item to each arm and the minimum, median and maximum accepted count per contributing family. Report effective concentration of accepted observations across families using H_a = sum_j (m_aj / sum_l m_al)^2 and effective family count 1/H_a, clearly labeled as a descriptive concentration statistic rather than a valid inferential sample size.

## Frozen analysis and failure rules

1. Lock the independent-family taxonomy and one primary coverage target on calibration data. Do not choose a target because it maximizes held-out acceptance overlap.
2. Compute the pooled primary risk difference on the untouched test set; if either denominator is zero, mark the primary contrast undefined and the confirmatory comparison failed, not favorable.
3. In each whole-family bootstrap replicate, recompute both denominators. Record the fraction of undefined replicates. Do not replace undefined risks with zero, omit them silently, or report a percentile interval without the undefined-draw rate and a defensible handling rule.
4. If family-specific coverage is highly unequal, include a predeclared leave-one-family-out sensitivity and the common-evaluable-family analysis. Treat a sign reversal as estimand sensitivity, not an invitation to choose a preferred result.
5. The family-level sign-flip procedure from the earlier note requires an explicit symmetry/exchangeability argument and an identical, predeclared family set. Pairing algorithm outputs is insufficient for exact randomization inference.
6. For a fixed budget, compare retrieval tokens, model calls, latency, and verifier acceptance rules across temporal and non-temporal arms. A temporal advantage that vanishes under timestamp shuffle, irrelevant chronology, or matched-cost controls does not support the proposed mechanism.

## Mathematics and physics scope

Use dated proof-state revisions or evolving experimental measurements only where evidence really changes. No timestamp on a static theorem or invariant physical law can by itself create a meaningful chronology intervention. Keep a separate domain-by-family table and never aggregate a favorable cross-domain headline while hiding a failing domain.

## Minimum executable unit tests for later cloud CI

- Two families with unequal accepted counts where pooled and equal-family risk rankings differ; assert both are reported with different labels.
- One family with zero accepted items in only one arm; assert its family risk is undefined and common-evaluable-family membership is symmetric.
- Zero global acceptance for either arm; assert primary risk comparison fails closed.
- Bootstrap resample with a zero denominator; assert undefined-draw count increments.
- Identical acceptance and errors across arms; assert zero pooled contrast and complete overlap.
- Invalid/duplicate source-family identifiers; assert manifest validation fails.

## Publication and resource gate

These are analytic requirements, not observed outcomes. No independent held-out model results are asserted. A positive claim requires the frozen manifest, independent labels, source-family audit, matched-cost baselines, negative controls, and uncertainty robust to denominator instability. If not available by November 22, publish a transparent methods/preregistration artifact only. No local laptop computation, paid cloud service, credit-card signup, or unverified free inference is authorized.
