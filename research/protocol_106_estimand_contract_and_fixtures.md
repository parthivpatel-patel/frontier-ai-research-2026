# Protocol 106 — Executable estimand contract and adversarial fixtures

Date: 2026-11-06. Status: specification and hand-checkable fixtures only. **No model experiments or cloud test executions are claimed.**

## Objective
Turn Protocol 105's corrected familywise matched-coverage estimand into deterministic, testable requirements. This is an evaluation-methods contract, **not a novelty claim**. No additional datasets, model calls, or compute services are authorized.

## Definitions and separation of datasets
For each claim i: immutable lineage ID L_i, physics family F_i, binary unsafe truth Y_i in {0,1}, and verifier score S_vi with a documented orientation (larger = more confidence in safe acceptance). Calibration and test sets must be split by lineage and source family *before* selecting any thresholds. Thresholds are frozen from calibration only. At threshold t, A_vi(t)=1[S_vi >= t]. In each test family f:

- coverage C_vf = sum_i A_vi / n_f;
- accepted unsafe count U_vf = sum_i Y_i A_vi;
- conditional unsafe risk R_vf = U_vf / sum_i A_vi, **undefined when no claims are accepted**;
- pooled risk = sum_f U_vf / sum_f accepted_vf, also undefined if none accepted;
- standardized family risk = sum_f w_f R_vf for prespecified nonnegative weights summing to one, **undefined if any positive-weight family risk is undefined**.

Never replace an undefined cell with zero, never silently omit a family, and never claim a risk guarantee based on point estimates. Preserve integer numerator and denominator for every reported ratio.

## Coverage-matching contract
1. Prespecify coverage targets, tolerance epsilon, family weights, score tie policy, and threshold search procedure before seeing test labels.
2. Select each method/family threshold from calibration scores only; if acceptance counts are discrete, report achieved calibration coverage and the distance from target.
3. Mark a comparison **not coverage-identifiable** when either method misses the declared calibration tolerance in any positively weighted family. Do not use held-out test scores to tune thresholds.
4. On test data report achieved coverage per method and family, whether or not calibration coverage matched. Large test coverage divergence is a finding, not an invitation to recalibrate.
5. Randomized tie-breaking, if used, must have frozen seed and logged decisions. Default deterministic rule: sort by descending score then stable claim ID, and select the calibration acceptance count nearest the target (ties choose smaller count). This is a top-k policy rather than a scalar score threshold when scores tie; label it explicitly. Deployment on new data requires a defined tie rule that does not use test-set ranks.

## Hand-checkable fixture A: pooling reversal
Two families, mechanics and circuits, with 100 claims each and 10 unsafe labels in each. Each method accepts only claims whose outcomes are specified below; accepted safe/unsafe counts must be feasible within the family totals.

| Family | Verifier | Accepted safe | Accepted unsafe | Accepted total | Conditional risk |
| --- | --- | ---: | ---: | ---: | ---: |
| Mechanics | A | 9 | 1 | 10 | 1/10 |
| Mechanics | B | 72 | 8 | 80 | 1/10 |
| Circuits | A | 72 | 8 | 80 | 1/10 |
| Circuits | B | 9 | 1 | 10 | 1/10 |

This is a **negative control**: despite different familywise coverage, both pooled risks are 9/90 = 0.1 and standardized risks at equal weights are 0.1. A purported Simpson reversal here would indicate a fixture or estimator bug. The 200-claim fixture from Protocols 095–097 is separate and must not be substituted without checking its own actual counts.

## Hand-checkable fixture B: undefined cells
Mechanics: A accepts zero claims; B accepts 2 safe and 1 unsafe. Circuits: both accept 2 safe claims. With w_mechanics = w_circuits = 1/2, standardized A risk is **undefined**, not 0; standardized B risk is (1/3 + 0)/2 = 1/6. Pooled A risk is 0/2 = 0; pooled B risk is 1/5. These are different estimands.

## Hand-checkable fixture C: unequal mixture
Mechanics: A accepts 1 unsafe of 10; B accepts 2 unsafe of 10. Circuits: A accepts 3 unsafe of 10; B accepts 4 unsafe of 10. With w_mechanics = 0.75, w_circuits = 0.25, standardized A risk = 0.75(0.1)+0.25(0.3)=0.15; standardized B = 0.75(0.2)+0.25(0.4)=0.25. Both methods have equal acceptance counts per family. These are synthetic arithmetic fixtures, not measurements.

## Required adversarial unit tests before analysis
- Reject boolean, string, NaN, infinity, negative or >1 weights; require weight sum one within declared numeric tolerance.
- Reject duplicate claim IDs, missing family labels, nonbinary unsafe truth, and mismatched lineage joins.
- Preserve undefined risk with zero accepted; ensure no 0/0 conversion.
- Distinguish pooled risk from standardized risk in unequal-coverage fixtures.
- Reject threshold selection or coverage matching that reads test outcomes.
- Reject post hoc family reweighting; log calibration-vs-test coverage shifts.
- Cluster resampling by independent lineage, not claim; report number of clusters and abstain from precision claims with too few.
- Audit score direction, ties, threshold equality, stable ID order and deterministic replay.
- Test both methods on identical frozen adjudicated claims, including explicit unresolved-label exclusions documented before evaluation.

## Falsification and novelty guardrail
If evidence ablation does not materially change verifier decisions, source-family holdout removes any apparent advantage, independent physics reviewers disagree, or deterministic dimensional checks match the proposed system, the paper must report the null/negative result and narrow its claim. Closest prior art from Protocol 105 remains a collision risk; no claim of first-of-kind groupwise selective risk is permitted.

## Zero-cost execution gate
Implement tests using Python standard library in GitHub Actions only after verifying public-repository standard-runner eligibility, account permissions, billing restrictions and current available quota. Do not use larger runners, paid APIs, laptop compute, or self-hosted machines. Until those checks pass, these fixtures remain unexecuted specifications.

## Publication integrity
Separate synthetic arithmetic examples from actual scientific verification results. Archive raw predictions, source provenance, independent adjudication, evaluation code, configuration and exact model versions. Disclose AI assistance as required by venue policy. The 2026-11-22 manuscript target remains conditional.
