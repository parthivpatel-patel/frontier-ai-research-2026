# Protocol 167 — Coverage matching without test-set selection (2026-11-09)

**Status:** prospective analysis design. No experiments, code execution, cloud resources, or empirical results are claimed. This document extends Protocol 166; it does not establish novelty.

## Identifiability issue

Equal *nominal* calibration coverage does not imply equal *realized* held-out coverage. A verifier can appear to improve correct-and-answered yield merely by answering more examples. A test-set threshold chosen after inspecting test labels or test coverage would change the evaluation procedure after observing held-out data. This protocol separates a predeclared operating-point comparison from exploratory risk-coverage analysis.

Let source clusters be g=1,...,G, with observations j=1,...,n_g, physics family f(g), binary answer decision A_mgj and binary correctness C_mgj (correctness for unanswered items must not be imputed). Define U_mgj=A_mgj*C_mgj, with U=0 for abstentions. For each cluster define q_mg=mean_j A_mgj and y_mg=mean_j U_mgj. Equal-source-cluster coverage Q_m=mean_g q_mg and yield Y_m=mean_g y_mg. The paired primary effect against baseline b is Delta=mean_g(y_constraint,g-y_b,g). These estimands use the same held-out cluster set for both methods.

## Threshold freezing and ties

1. Partition by source problem before paraphrase generation. Keep all variants of a source problem within one split. Calibration and test source identifiers must be disjoint; publish salted or public stable IDs and split hashes.
2. Declare a target coverage q* and deterministic threshold selection algorithm before test evaluation. Estimate thresholds using calibration clusters only, with the same cluster-weighting rule used in the primary analysis.
3. Scores must have documented orientation, missing-value handling and a deterministic tie rule. Prefer a fixed ordering independent of correctness labels; if randomized ties are required, publish the seed and report seed sensitivity. Do not use test labels, test correctness or test-set target coverage to adjust thresholds.
4. Freeze model versions, candidate answers, verifier prompts, normalization, thresholds, and ties before opening test outcomes.
5. Report Q_m and Y_m on test separately for every method, plus achieved coverage gap |Q_constraint-Q_baseline|. Declare a practical coverage tolerance before testing. A tolerance breach means **no matched-coverage superiority claim** from the operating-point comparison, even if Delta is positive.
6. Report coverage and yield by physics family, source cluster count, paraphrase count, false rejection rate among correct candidate answers, and all abstentions. A method that abstains on every item must not be called accurate or superior.

## Sensitivity and inference

Report paired per-cluster differences d_g=y_constraint,g-y_baseline,g, their unweighted mean, equal-family mean, and leave-one-family-out estimates. Resample *whole source clusters*, not paraphrases, for descriptive bootstrap intervals; if family-level generalization is claimed, explain the number and sampling design of independent families and perform family-level sensitivity. Cluster bootstrap intervals are not a guarantee of valid inference for a small number of clusters, selection on a shared calibration set, or distribution shift. State assumptions and abstain from significance claims when they are not defensible.

Risk-coverage curves may be presented as secondary descriptive plots. Threshold sweeps over held-out scores must be labeled exploratory; selecting the best test threshold or cherry-picking a coverage point cannot support the preregistered primary hypothesis. Compare curves on the shared feasible coverage interval, state interpolation rules, and retain all baseline curves.

## Counterexamples and falsification checks

- **Different coverage:** constraint verifier answers 60% of held-out clusters, baseline 50%; higher unconditional yield does not establish better matched-coverage performance.
- **Paraphrase amplification:** one source problem has 20 variants and another has one; treating 21 rows as 21 independent sources changes the estimand and uncertainty.
- **All-abstain:** Q=0, Y=0; conditional accuracy is undefined, not 100%.
- **Tied scores:** thresholds with many equal scores can shift achieved coverage; fixed tie handling must be auditable.
- **Calibration shift:** equal calibration coverage but materially different test coverage is a result to report, not an excuse to retune on test.
- **Validity exceptions:** correct non-SI units, open-system conservation and approximation domains must not be falsely rejected by an overstrict constraint rule.

## Minimal artifact contract (future cloud execution only)

Store a versioned manifest containing source_id, family_id, paraphrase_id, split, ground_truth_provenance, candidate_answer_id, method_id, raw_score, threshold, tie_decision, answered, correctness_if_answered, and verifier_reason_code. Hash the manifest and code revision. Preserve predictions for *all* systems on *all* examples, including abstentions and invalid records, without filtering failures post hoc. Keep a separate calibration ledger and immutable test report.

## Decision gate

If held-out coverage matching fails, the primary conclusion is **inconclusive at matched coverage**, irrespective of the sign of Delta. If a credible baseline dominates or the constraint ablation adds no benefit, report a negative result. If the method duplicates prior work, remove the novelty claim. Do not present this evaluation protocol as a new statistical theorem.

## Compute and publication gate

No execution is authorized by this document. Use cloud-only execution only after verifying account-specific free quotas, billing/card requirements, runner availability and cost-prevention controls; otherwise do not dispatch. Do not use the user's laptop for computation. The November 22 manuscript date remains conditional on verified evidence, prior-art comparison and venue-compliant AI-assistance disclosure.
