# Evidence admission and falsification protocol (2026-11-22)

**Status:** preregistered design refinement; not an executed study, benchmark result, or novelty claim. Supplements `HELD_OUT_TEMPORAL_VERIFICATION_PREREG_2026-11-22.md`.

## Critical identification distinction

Two different temporal targets must not be conflated:

1. **Evidence-availability validity:** a retrieved document was demonstrably accessible before a decision cutoff.
2. **Historical correctness:** the claim's truth at the cutoff, established using an independently adjudicated, time-indexed reference.

A pre-cutoff document can contain false information; a post-cutoff document can accurately describe an earlier state. Filtering by availability alone therefore does **not** establish correctness or prevent all forms of answer leakage (e.g. model pretraining after the cutoff). Results must be framed as retrieval-time evidence-control effects unless model knowledge cutoffs and other leakage channels are independently controlled.

## Machine-readable evidence ledger (one row per claim × document)

Required fields: `claim_id`, `source_group_id`, `domain` (NLP/math/physics), `claim_text`, `claim_reference_time_utc`, `decision_cutoff_utc`, `document_id`, `document_url`, `archive_url`, `archive_capture_utc`, `first_proven_available_utc`, `availability_proof_type`, `availability_proof_url`, `snapshot_sha256`, `source_publication_time_utc`, `source_publication_time_provenance`, `admission_status`, `exclusion_reason`, `adjudicated_truth` (0/1/unknown), `truth_reference_time_utc`, `truth_evidence_ids`, `adjudication_method`, `split_id`, `retrieval_query_hash`, `model_version`, `prompt_hash`, `policy_arm`, `prediction`, `accepted`.

A capture timestamp is only an **upper bound on the time by which captured content existed**, not proof it existed at the claimed publication time. Admission at cutoff requires a qualifying archive capture at or before cutoff, or another independently auditable contemporaneous record containing the relevant content. Record the difference between publication, capture, and availability times. A snapshot taken after cutoff cannot by itself establish pre-cutoff availability. For sources with corrections, hash and adjudicate the exact version.

## Locked adjudication sequence

1. Construct candidate claims and cutoffs without viewing model responses; preserve rejected candidates and sampling rules.
2. Freeze claim/source groups and split by group to avoid duplicate-document or near-duplicate leakage. Time-block split when testing future cutoffs.
3. Two independent adjudicators or a mechanically checkable external authority establish time-indexed truth; disagreements are logged and unresolved labels remain unknown, not guessed. If no independent adjudication is feasible, classify the case as unverified.
4. Authenticate evidence availability independently of the label and model output. Keep excluded and unarchived cases in the denominator of the **availability audit**, while clearly separating them from the admissible benchmark.
5. Freeze retrieval index, document snapshots, prompts, models, acceptance rule, and random seeds before opening held-out truth labels.
6. Run B0/B1/T/T+A on the same claim frame, log failures and costs, then publish per-domain coverage, accepted error, abstention, and paired sharp identification intervals.

## Predeclared falsification and negative controls

- **Timestamp shuffle:** shuffle availability timestamps within predeclared source strata. If T performs similarly and admits equally many demonstrably future documents, temporal filtering may not be functioning as intended.
- **Future-evidence trap:** seed identifiable post-cutoff documents. T must exclude all of them; any admitted trap is a protocol-integrity failure, regardless of accuracy.
- **Historical truth mismatch:** cases where current and historical truth differ test whether evaluation inadvertently uses present-day labels.
- **Retrieval coverage:** report cases with zero authenticated eligible documents separately. Dropping these cases silently biases coverage.
- **Source-family holdout:** hold out publishers/archives, not just individual passages, to test reliance on recurring source templates.
- **Model-memory confound:** closed-book B0 may already know post-cutoff facts. Report this explicitly; without independent control, no claim that T eliminates *all* hindsight leakage.

## Mathematical and statistical boundaries

For fixed accepted denominators and unconstrained binary missing labels, the paired sharp endpoints are sums of per-item extrema. This is an identification calculation, **not** a confidence interval and not evidence of a new theorem. If denominators are random across bootstrap resamples, some draws may have zero accepted items; record their frequency and define handling before inference. Simple endpoint bootstrapping is not automatically a uniformly valid confidence set for a partially identified parameter. Consult the partial-identification inference literature and justify the chosen confidence procedure before presenting population uncertainty. Do not label a percentile bootstrap of endpoint estimates as validated inference without coverage analysis.

## Novelty and publication gate

Closest-work review must include selective prediction/abstention, temporal QA and retrieval leakage, missing-label partial identification, and time-stamped evidence provenance. The candidate contribution is a *combination* of an evidence-admission audit and paired selective-verification evaluation, not an invented standalone temporal-reasoning or interval-optimization algorithm. Publish a methods/preregistration paper only with explicit limitations; do not claim empirical improvement, novel mathematics, or physics-general AI capability before independent evidence exists.

## Execution and cost boundary

No GPU or local workload is required for this protocol document. Any future execution must be restricted to confirmed free, standard public-repository cloud CI, bounded jobs, and non-billable public datasets. No card enrollment, paid API, larger runner, or laptop inference. Verify actual provider eligibility and repository settings immediately before launching each workload.
