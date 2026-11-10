# Protocol 183 — Provenance intervention integrity: canonical serialization and blinded replay

Date: 2026-11-10. Status: implementation specification, not an executed experiment.

## Why the current scorer is insufficient

The current Protocol 181 scorer requires paired `prompt_hash` equality. That is appropriate **only if** the hash is of an invariant prompt skeleton. It cannot simultaneously be a hash of the full verifier input, because correctly linked and shuffled-link inputs should differ. The current scorer also accepts a condition label without checking what the verifier actually received. Consequently a perfectly valid descriptive score could be computed from pairs whose intervention was not correctly delivered.

This protocol is a pre-registered *software integrity gate*, not evidence of improved reasoning.

## Versioned record contract

For every paired observation preserve: `source_id`, `edit_id`, `candidate_step_id`, `run_manifest_hash`, `physics_family`, `edit_stratum`, `label_edited`, `label_adjudication_status`, `verifier_output`, `eligible`, `rule_inventory_hash`, `model_or_verifier_version`, `token_budget`, `compute_budget`, `assignment_seed`, `provenance_condition`.

Add the following required fields in a future scorer version (do **not** silently reinterpret existing `prompt_hash`):

- `schema_version = "183.1"`
- `invariant_prompt_sha256`: digest of a canonical serialized representation containing all non-intervention model-visible content, including the problem, candidate step, constraint text, rule inventory, numerical tolerance, instruction template and any non-provenance metadata.
- `full_input_sha256`: digest of the *exact bytes* sent to the verifier, not of a reconstructed response or of a postprocessed string.
- `intervention_payload_sha256`: digest of canonical serialized provenance-link data alone.
- `blinded_input_artifact_sha256`: digest of a separately retained, immutable model-visible input artifact; this must equal `full_input_sha256` if the artifact is the exact transmitted byte stream.
- `assignment_manifest_sha256`: digest of an immutable mapping of item keys to randomized condition, generated before verifier responses.
- `provenance_link_type`, `provenance_link_scope`, `provenance_link_target_ids`: typed fields checked against the source constraint graph, not free-text labels.

Canonical JSON for structured manifests: UTF-8, sorted object keys, compact separators, no NaN/Infinity, no duplicate keys, Unicode normalization policy fixed in the manifest, arrays preserved in specified semantic order. Hashes must be lowercase 64-character SHA-256 hex digests. The full-input digest is always calculated from the actual transmitted bytes, which may be non-JSON.

## Pair acceptance invariants

1. Exactly one `correct` and one `matched_shuffle` record per source/edit/step/run; same independently adjudicated edited-step truth label, invariant prompt digest, rule inventory, verifier version, budgets and seed.
2. Full-input and intervention-payload digests **must differ** between conditions when the intervention is defined to change provenance links. Equal digests indicate a failed manipulation and are rejected, not counted as a null effect.
3. A parser must reconstruct model-visible inputs and demonstrate that removing only the provenance-link payload yields byte-identical or canonically equivalent invariant content. Hash equality alone does not establish this; store and diff the underlying artifacts.
4. The shuffled payload must preserve link type, scope and permitted target universe; prohibit self-links, impossible target IDs, and edits to rule text, problem text, numeric tolerances, answer labels or instructions.
5. Reject any model-visible occurrence of the randomized condition labels, adjudicated truth labels, gold-answer fields or answer-key references. A denylist is necessary but insufficient: use structured field allowlisting plus human review of a sampled blinded replay.
6. Independently verify assignment from the immutable manifest. The scorer must not trust the row's `provenance_condition` alone.
7. Reject absent, malformed, duplicated or inconsistent hashes, mixed schema versions, and unregistered attrition. Do not infer scientific causality from this gate passing.

## Minimal adversarial acceptance fixtures (invented, not observations)

| Fixture | Expected |
| --- | --- |
| Same skeleton; distinct correct/shuffled link payloads; distinct full inputs; matched type/scope | Accept only after artifact diff and assignment verification |
| Same full-input digest for both conditions | Reject: intervention not delivered |
| Same full input except changed numerical tolerance | Reject: non-provenance manipulation |
| Condition string or gold verdict appears in model-visible text | Reject: leakage |
| Shuffled target outside admissible graph or different link type | Reject: invalid shuffle |
| Different invariant skeletons with equal budgets | Reject: confounded pair |
| Correct hashes but no retained transmitted input artifacts | Reject: unverifiable manipulation |
| Valid paired rows but different assignment manifests | Reject: assignment inconsistency |

## Falsification and reporting

Primary claim to test later: correct provenance linkage improves **source-weighted correct-verdict yield** over type/scope-matched shuffled links at matched budgets. Predefine the minimum practically relevant effect, source-cluster uncertainty, coverage/abstention handling and multiplicity correction before observing model results. A null or negative effect, benefit confined to leaked or invalid intervention pairs, or a reversal under source-level grouping fails the claim. Positive effects on a narrow distribution do not establish general physical reasoning or scientific novelty.

Report the number of attempted, rejected and accepted pairs by reason; publish the deterministic validator and non-sensitive artifacts. Never silently drop invalid pairs after inspecting outputs. Any human adjudication must be blinded to condition and independently documented.

## Execution and publication gate

The existing scorer and tests remain unexecuted here. This document does not claim code changes, successful tests, independent labels, cloud eligibility, model comparisons, or novelty. Before running tests or inference, verify the selected free cloud service's account-specific eligibility, quotas, billing state and card requirements. No paid fallback or laptop computation. Continue full-text prior-art review, particularly provenance-aware verification, counterfactual consistency, formal/physics constraint checking and selective prediction. November 22 is conditional on actual evidence.
