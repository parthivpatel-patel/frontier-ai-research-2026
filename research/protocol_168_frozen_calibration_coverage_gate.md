# Protocol 168 — Frozen calibration and coverage gate executable contract (2026-11-09)

**Status:** prospective, unexecuted contract. Extends Protocol 167. No model results or novelty claims.

## Primary validity condition

Calibration chooses each method's score threshold using calibration observations only, grouped by source problem. The held-out evaluator must never optimize a threshold, tie break, score orientation, or tolerance using held-out outcomes. A test-set coverage mismatch cannot be repaired after inspecting the test set. Report the observed gap and mark the matched-coverage comparison **inconclusive**.

## Deterministic calibration specification

Inputs are a versioned collection of rows (source_id, family_id, variant_id, split, method_id, score, candidate_id), with a separate correctness ledger inaccessible to calibration. Scores are finite and higher means more likely to answer correctly; reject NaN, infinities, duplicate (source_id, variant_id, method_id), missing source/family IDs, cross-split source IDs, and missing method predictions. Each method must cover exactly the same calibration source/variant set.

Define coverage at threshold t as the unweighted mean over source IDs of the fraction of their variants with score >= t. For declared target q in [0,1], enumerate candidate thresholds from unique calibration scores plus an all-abstain sentinel. Choose the candidate minimizing absolute calibration coverage error, breaking ties first toward **lower** coverage and then toward **higher** threshold. The all-answer candidate must be representable. Do not infer a threshold from test data. A predeclared deterministic hash tie rule may be used only if the protocol specifies it before calibration; the simple >= threshold rule is preferred.

Persist for each method: threshold, achieved calibration coverage, target coverage, score orientation, tie rule, calibration manifest hash, code commit, and source IDs hash. Thresholds and method configurations must be frozen before test evaluation.

## Held-out reporting contract

Use a single held-out source set and all declared variants for all methods. Per method compute equal-source-cluster coverage Q and unconditional correct-answer yield Y, with abstentions contributing zero to Y; report conditional accuracy only if Q > 0. If correctness for an answered item is missing, reject the report rather than silently score it as wrong. Report pairwise coverage gaps, correct-answer yield differences, false rejection among known-correct candidate answers (when correctness is available for abstentions), and family-stratified summaries.

Primary decision:
- If missing predictions, leaked IDs, missing required correctness, or altered frozen configuration: **INVALID**.
- If either method has no answered items or absolute held-out coverage gap exceeds preregistered epsilon: **INCONCLUSIVE_AT_MATCHED_COVERAGE**.
- Otherwise: **ELIGIBLE_FOR_INFERENCE**, not “superior.” Inference still requires appropriate independent sampling units and predeclared uncertainty analysis.
- Even when eligible, a positive descriptive yield difference is not proof of superiority.

## Pre-execution regression cases

1. A source with twenty paraphrases and another with one contributes two equal-weight source units, not twenty-one independent observations.
2. Calibration target 0.5 with score ties may not achieve 0.5; report realized coverage rather than changing the threshold on test.
3. Disjoint calibration/test source IDs are mandatory, including variants with different text.
4. A method with calibration coverage 0.5 and test coverage 0.8 cannot be described as matched against a method with test coverage 0.5.
5. Reversing method order negates yield difference but leaves absolute coverage gap unchanged.
6. All-abstain conditional accuracy is undefined.
7. Missing correctness for an answered test item causes a hard failure.
8. Duplicate row keys and non-finite scores cause hard failures.
9. Changing candidate answers after calibration invalidates the frozen manifest.
10. If two thresholds have equally close coverage, the specified lower-coverage, higher-threshold tie rule is deterministic.

## Statistical and scientific limits

Threshold tuning on a shared calibration sample introduces dependence not removed by a test-only cluster bootstrap. Physics families may not represent an independent random sample. Paired tests require matched original source problems. Do not claim novelty from standard selective-prediction evaluation, exact paired tests, or cluster resampling. Compare against selective prediction, conformal risk control, process reward models, and physics-verification prior art before asserting any new contribution.

## Execution and integrity gate

No compute or spending is authorized by this protocol. Only dispatch cloud CI or model inference after verifying account-specific zero-cost quota, runner eligibility, billing/card requirements, and hard cost prevention. Never run workloads on the user's laptop. Publish complete failure cases, code revision, manifests, and any required AI-assistance disclosures. The November 22 target is conditional on real evidence.
