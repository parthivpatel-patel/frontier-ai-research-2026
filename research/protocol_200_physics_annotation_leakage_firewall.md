# Protocol 200 — Physics provenance annotation and leakage firewall

Date: 2026-11-11. Status: preregistration design only. No examples adjudicated, model runs executed, or novelty established.

## Purpose and scientific boundary

Before evaluating language models, construct a small, independently adjudicated set of physics claims with explicitly typed evidence dependencies. A graph-theoretically feasible edge swap is **not** evidence that a swapped source is physically invalid. Graph feasibility and semantic correctness require separate certificates. This protocol prevents automatic labels from being laundered into physics ground truth.

## Unit of analysis and source provenance

The unit is a physics *claim–evidence bundle* rather than an isolated sentence. Each bundle contains (a) a precisely scoped claim, including assumptions, units and regime; (b) source passages or derivation steps with stable identifiers and location markers; (c) a typed support graph; (d) a claim-specific validity judgment; and (e) a documented counterfactual edit.

Record source title, authors, publication year, persistent URL/DOI where available, page/section/equation, retrieval date, license or quotation constraints, and whether the source is primary or secondary. Keep quoted passages short; store reference locations and original annotations, not redistributed copyrighted documents. No model-generated physics assertion may be treated as a reference label.

## Minimal record schema (one immutable JSONL object per variant)

- `problem_id`, `claim_id`, `variant_id`, `pair_id`, `split_id`, `schema_version`
- `claim_text`, `assumptions`, `units`, `physical_regime`, `reference_answer`
- `source_ids`, `source_locations`, `evidence_nodes`, `claim_support_edges`
- `edit_type` in {original, corruption, sham, valid_reassignment}
- `edit_operations`, `graph_certificate_path`, `graph_checker_version`
- `semantic_label` in {supports, does_not_support, ambiguous, disputed}
- `annotator_ids_pseudonymous`, `annotation_rationale_refs`, `adjudication_status`
- `surface_template_id`, `identifier_permutation_id`, `prompt_order_seed`
- `source_license_notes`, `data_version`, `content_digest`

A record cannot enter the primary evaluation set with semantic_label=ambiguous/disputed or unresolved adjudication. Such records remain in a published exclusions ledger with reasons; do not delete them silently.

## Two independent adjudication passes

**Pass 1: physical validity.** Two independent reviewers, blinded to intended edit arm and model outputs, separately judge whether the *specific evidence actually entails the scoped claim under its assumptions*. They must cite a derivation or primary source and document dimensional consistency, limiting cases, sign conventions and physical regime. Record categorical agreement and the full confusion matrix; a single agreement percentage is insufficient. Disagreements go to a third independent adjudicator, with original votes preserved. If independent qualified reviewers cannot be obtained at zero cost, label the corpus *unadjudicated* and do not publish ground-truth accuracy claims.

**Pass 2: intervention integrity.** A separate check confirms that only intended provenance relationships changed. For sham variants, semantic support must be invariant. For valid reassignments, physical support must remain valid even when graph edges differ. For corruptions, at least one indispensable evidence dependency must be invalidated while the surface claim and answer remain unchanged. Graph certificate acceptance alone never supplies this label.

## Leakage and falsification controls

Freeze a problem-level split **before** model evaluation; all variants, paraphrases and evidence fragments of the same physical claim stay in the same split. Search for duplicate claims and near-duplicate source passages across splits. Counterbalance labels, identifiers, edge order, source length and answer positions; record all random seeds. Keep the correct judgment and arm names out of the model-facing prompt and filenames. A surface-only classifier or identifier heuristic that separates arms invalidates a provenance-specific interpretation until repaired.

The primary evaluation contrasts the *natural-response acceptance frequency* in original versus corrupted variants, with sham and valid-reassignment controls and the full paired response categories. Abstentions/refusals are observed outcomes, not imputed forced answers; transport errors are operational failures. Report all attempted pairs, exclusions, raw outputs and uncertainty at the problem-cluster level. Never infer internal causal reasoning from response differences alone.

## Explicit stop rules

1. Stop ground-truth claims if independent physics reviewers cannot substantiate the labels.
2. Stop empirical interpretation if a sham or identifier-only contrast is comparable to the corruption contrast at the preregistered resolution.
3. Stop graph-dependent claims if any bounded exhaustive oracle counterexample invalidates the certificate checker.
4. Stop novelty claims if full-text closest prior art already supplies the same intervention, estimand and controls.
5. Stop all execution if free-cloud account eligibility, quota, billing exposure, or model access is not verified; do not ask the user's laptop to run the workload.

## Execution and publication gates

First validate the annotation schema and mathematical certificate tests on an independently verified zero-cost cloud runner. Then obtain genuinely independent physics adjudication, finish the 2024–2026 full-text literature collision audit, preregister sample size and decision thresholds, and only then run a bounded pilot using confirmed free model access. Record the exact cloud account/quota verification date and the immutable code/data versions. No provider's generic advertised free tier proves this account has zero billing exposure.

**Current evidence:** This document specifies a reproducible process only. There are no completed annotations, adjudicator agreements, cloud regression results, or model results. The November 22, 2026 target is conditional; if gates remain unmet, release a transparent methods/feasibility manuscript rather than fabricate empirical findings.
