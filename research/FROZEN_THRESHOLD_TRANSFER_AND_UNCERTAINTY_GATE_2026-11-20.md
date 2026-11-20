# Frozen-threshold transfer and uncertainty gate (2026-11-20)

## Status
This is a **prospective analysis protocol**, not a result, a new theorem, or a claim of first discovery. It extends the paired selective-risk note without changing its definitions. No model evaluation was run to produce it.

## Primary target and held-out procedure
Let domains d be NLP, mathematics and physics; let families g group related questions or shared generation sources. A frozen answer has adjudicated correctness Y_i in {0,1}. For each policy p, its scalar score s_pi and acceptance A_pi(t)=1[s_pi >= t] are recorded with immutable item and family IDs. A verifier may abstain; do not code abstention as answer correctness.

For each of the three leave-one-domain-out trials, fit all feature transforms, calibration maps, and acceptance thresholds **only on the other two domains**, with source families disjoint from the held-out domain. Apply the frozen policy unchanged to the third domain. Do not retune to force identical held-out coverage: that would leak held-out score-distribution information. Report realized coverage, accepted-answer error, false rejection of correct answers, and cost. Equal-coverage *oracle* comparisons using held-out thresholds may be shown only as clearly labeled descriptive sensitivity analyses, not deployable transfer evidence.

## Primary estimand and feasibility
Choose a predeclared target acceptance coverage c0 (e.g. 0.50) on development data. Threshold selection minimizes development selective error subject to development coverage >= c0 and the specified resource cap; specify deterministic tie-breaking before evaluation. On held-out data, report the realized (possibly unequal) coverage and risk for temporal T and conventional B. Because selective risk can be trivially reduced by rejecting more, a superiority claim requires BOTH (i) held-out coverage for T not below B by more than a predeclared tolerance delta_C, and (ii) lower held-out selective risk, with family-cluster uncertainty. Predeclare delta_C numerically before running models; until then this is an incomplete preregistration, not a confirmatory test.

A paired equal-coverage estimand is valid for *fixed* policies with equal observed acceptance counts, but should not be conflated with the frozen-threshold cross-domain estimand. If a policy accepts zero items, risk is undefined and the trial fails the usefulness gate.

## Inference
Resample independent **source families**, not individual paraphrases. Within a resampled family, retain every item and both policy outcomes; recompute each statistic and coverage in each replicate. Report the number of independent families and percentile/bootstrap uncertainty with the seed and replication count fixed in advance. If there are too few independent families for credible resampling, mark inference exploratory and provide family-level differences; do not manufacture narrow confidence intervals. Treat the three domain trials as three tests; do not interpret one favorable domain as universal transfer. Any aggregate across domains must use frozen domain weights, not weights chosen after seeing outcomes.

## Negative controls and falsification
Compare T against confidence-only C, shuffled temporal S (shuffle within eligible development-defined strata without crossing source-family or time boundaries), and strong conventional-feature B. Temporal evidence is not distinctive if T cannot outperform S and B on the primary held-out criteria. Leakage audits must check answer keys, future timestamps, source family overlap, and verifier exposure to ground-truth labels. Report label disagreements and missing adjudications rather than deleting them without a declared rule. Fail the mechanistic claim if temporal features remain equally predictive after time-order destruction, or if a stronger non-temporal baseline explains the difference.

## Resource and zero-dollar boundary
Log token counts, model calls, latency, and, when measurable, CPU time/memory separately; do not call matched tokens matched energy or FLOPs. No model API call, GPU rental, paid runner, or laptop workload is authorized by this protocol. Standard GitHub public-repository CI is a candidate only after verifying actual workflow runner class, public-repo eligibility, current billing settings and applicable limits. Quotas and availability are not inferred from documentation alone.

## November 22 publication gate
A public protocol may be published as methods/preregistration with full disclosure of AI assistance where required. Do not claim empirical cross-domain transfer, a new physics result, or a novel statistical guarantee until independent held-out evidence and full-text prior-art audit support the precise claim. Record any deviations from this protocol with timestamps before examining held-out results.
