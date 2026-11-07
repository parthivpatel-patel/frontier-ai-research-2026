# Protocol 115 — estimand identification and missingness stress test (2026-11-07)

Status: theoretical audit and executable-test design only. No measured effect, validated physics benchmark, or novelty claim. Follows Protocols 111–114.

## Units and target

Let i index independently sampled physical scenario lineages, j index prespecified interventions within lineage, and s ∈ {A,B} denote verifier systems. Let T_ij be independently adjudicated physical truth, R_ijs the system response, Z_ijs ∈ {0,1} the acceptance indicator, and U_ijs ∈ {0,1} an independently adjudicated unsafe-response indicator **defined only if Z_ijs=1**. The system-specific unsafe label is not physical truth. A lineage is the resampling unit; paraphrases and intervention variants are not independent replicates.

Define intention-to-evaluate error on every matched intervention, with abstentions scored using an explicitly prespecified utility or reported as a separate outcome. Define selective risk for system s at its frozen selection policy as E[U_ijs | Z_ijs=1] only when the acceptance denominator is positive. Report coverage E[Z_ijs] alongside risk. Comparing two systems at their *different realized coverage* is descriptive and does not isolate response quality.

## What a paired bootstrap does and does not identify

Resample lineage IDs within prespecified physics families, retaining all intervention variants and both systems in each selected lineage. Compute the paired statistic in every replicate. This preserves within-lineage covariance, but it cannot repair confounding from unequal system acceptance sets, incorrect adjudication, evidence leakage, or a nonrepresentative scenario sample. A percentile interval with many undefined replicates is not a reliable confidence statement; publish the undefined fraction and withhold confirmatory inference when preregistered feasibility criteria fail.

At a common target coverage c, thresholds must be chosen using calibration lineages only, with a frozen tie-breaking rule and calibration artifact digest. If exact matched coverage is infeasible, report that fact instead of selecting favorable evaluation cases. For a paired *accepted-case* comparison, define the common accepted subset Z_ijA Z_ijB=1; report its size and coverage separately. This estimand differs from each system's own selective risk and must never be relabeled as the latter.

## Identification threats and required negative controls

1. **Selection collider:** conditioning on acceptance can induce a difference even if systems have identical unconditional error. Run a synthetic counterexample where acceptance depends on item difficulty and verify that the report flags differing denominators.
2. **Intervention contamination:** paraphrases from the same physical lineage must not cross calibration, test, or model-selection partitions. Test two differently named variants with one lineage key.
3. **Truth versus response:** allow two systems to have different unsafe-response outcomes while preserving a single adjudicated physical truth; reject disagreement on the shared truth.
4. **Evidence dependence:** compare causal evidence replacement with shuffled, irrelevant, and proposition-preserving evidence controls on the same lineage. If changes are indistinguishable, the claimed evidence-reliance mechanism is falsified.
5. **Review bias:** reviewers must be blind to system identity and hypothesis where practicable. Store the rubric version, evidence digest, adjudicator assignment, disagreement resolution, and adjudication date. Metadata alone does not prove independence.
6. **Multiplicity:** declare one primary contrast and correction across secondary physics families and metrics before inspecting results.

## Proposed deterministic tests

- T1: permutation of rows changes neither canonical admitted records nor fixed-seed bootstrap output.
- T2: unequal matched intervention keys are rejected before estimator invocation.
- T3: a null unsafe label on abstention is permitted; a false unsafe label on abstention is rejected.
- T4: zero accepted denominator produces undefined risk, never zero.
- T5: differing coverage yields a diagnostic; common-accepted risk is not substituted for each-system selective risk.
- T6: lineage bootstrap always draws both systems and all variants together.
- T7: any missing adjudication provenance prevents confirmatory inference.
- T8: changed threshold/manifest digest prevents use of a prior inference artifact.
- T9: calibration/test lineage overlap blocks estimation.
- T10: shuffled-evidence negative control cannot be silently excluded from the preregistered primary contrast.

## Decision rule

No claim of a new physics-grounded verification capability is warranted until: independent ground truth is established; strong contemporaneous baselines are evaluated under identical evidence and budgets; intervention effects exceed a preregistered scientifically meaningful threshold with uncertainty and multiplicity handled; negative controls behave as predicted; and independent reviewers can reproduce the cloud artifacts. A synthetic passing test suite establishes implementation consistency only.

Next engineering action: inspect the current admission and bootstrap module interfaces, implement a minimal adapter that returns a typed admitted table and blocks estimator calls on validation failure, then run its synthetic tests in GitHub Actions **only after verifying the account's applicable free minutes and billing controls**. No laptop workload, model download, paid API, or new cloud run is authorized by this note.
