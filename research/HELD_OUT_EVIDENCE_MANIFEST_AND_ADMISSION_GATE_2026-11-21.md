# Held-out evidence manifest and no-leakage admission gate (2026-11-21)

Status: preregistration / proposed protocol. **No model outcomes are reported here.** This document does not establish novelty, generalization, or empirical success.

## Purpose
Prevent the cross-domain temporal-verification study from treating timestamp decorations, duplicated evidence, or post-hoc threshold adjustment as genuine temporal reasoning. The proposed target is *incremental selective-risk improvement from temporally valid evidence* relative to strong non-temporal and shuffled-time controls at a frozen, source-domain-calibrated acceptance rule and matched inference budget.

## Required per-example manifest (version 1)
One row per immutable question/evidence bundle; retain a separate append-only annotation ledger.

- `example_id`: stable unique nonempty string; reject duplicate IDs across all splits.
- `domain`: one of `nlp`, `math`, `physics`; `task_family_id` and `source_family_id`: nonempty strings; group siblings and shared provenance together.
- `source_uri`, `source_revision_or_digest`, `license`, `retrieved_at_utc`: provenance. If access or reuse terms cannot be established, quarantine.
- `claim`, `evidence_text`, `question_as_of_utc`, `evidence_valid_from_utc`, `evidence_valid_until_utc` (nullable): distinguish claim time, evidence publication, and validity interval; unknown time is **missing**, not zero.
- `temporal_relevance_rationale`: explicit reason chronological ordering can change correctness; if none exists, classify as a non-temporal negative control, not a temporal test.
- `gold_label`, `label_protocol_version`, `adjudicator_ids`, `adjudication_status`: independent ground truth with disagreements retained; unresolved labels are excluded from confirmatory analysis with counts reported.
- `split`: development/calibration/held-out, assigned by family before running verifiers; `split_seed` and split-manifest digest.
- `verifier_version`, `prompt_digest`, `model_digest`, `input_tokens`, `output_tokens`, `wall_time_ms`, `estimated_cost_usd`, `run_environment`: exact execution trace and budget comparability. A reported $0 cost is not evidence that a provider permits the run without billing.
- `arm`: temporal, strong non-temporal, shuffled timestamps, or evidence-ablated. Arms must share the same eligible items, ground-truth labels and resource ceiling.
- `score`, `accepted`, `prediction`: store raw values before calculating metrics; reject nonfinite scores and non-Boolean decisions.

## Admission and freezing
1. Hash and publish the candidate manifest/schema, family-level split and label rubric **before** examining held-out arm outputs.
2. Check licensing, provenance, independence of adjudication, missingness, family overlap and genuine time dependence. Reject or quarantine ambiguous cases; record the number and reason.
3. Calibrate score mapping and threshold on designated development domains only. Save the threshold, tie policy, target coverage, metric implementation commit and digest. Do not tune on the target domain.
4. Execute each arm with matched items and prespecified CPU/time/token limits; if one arm fails, retain failure and missingness records rather than selectively dropping its hard cases.
5. Report held-out coverage and selective risk separately by domain and source family; compare paired outcomes only when coverage comparability is defensible. Include family-cluster uncertainty and leave-one-family-out sensitivity. Do not call a pooled mean evidence of success in all domains.
6. Preserve immutable raw outputs, workflow URL, runner image, exact dependency versions and reproducibility commands. Public GitHub Actions runners can execute bounded checks, but provider quota and no-billing eligibility must be verified at execution time.

## Falsification and interpretation
- **Temporal attribution fails** if shuffled timestamps match the temporal arm within the prespecified uncertainty/equivalence criterion, or if temporal ordering is irrelevant to the task.
- **Practical benefit fails** if a matched non-temporal baseline attains comparable or lower selective risk without a meaningful coverage penalty, or if gains vanish under family deletion.
- **Transfer fails** if improvement occurs only after recalibrating on held-out target-domain labels.
- **Confirmatory inference fails** if independent families are too few, labels are unresolved, arm costs are incomparable, timestamp validity is unverified, or data leakage is detected.
- A positive result would support a *bounded empirical contribution*, not a general theorem about AI reasoning, physics understanding, model safety or model welfare.

## Cross-domain interpretation
For NLP, timestamps can alter whether a fact was true as of the question date. For mathematics, a timeless theorem is **not** a temporal example: chronology must concern an explicitly dated proof state, evolving formal-library version or dated claim of discovery. For physics, distinguish changing observational estimates or instrument calibrations from invariant physical laws. Never add arbitrary dates merely to fill the domain matrix.

## Immediate execution decision
First collect a small licensed, independently adjudicated *manifest-only* pilot and validate its time-dependence and family splits with bounded GitHub Actions CPU jobs. Do not spend tokens on large-model inference until a verified no-card, no-billing cloud inference path exists. If that path cannot be confirmed by the Nov 22 checkpoint, publish a methods/preregistration artifact with explicit non-results instead of claiming discovery.

## Closest-work review still required
Compare against selective prediction / risk-coverage evaluation, calibration transfer, temporal fact verification, time-series verification and temporal reasoning benchmarks. Record exact paper versions, datasets, split practices, cost controls and whether their causal negative controls already test this claim. This file is not a completed systematic novelty audit.
