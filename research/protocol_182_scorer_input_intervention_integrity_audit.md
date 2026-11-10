# Protocol 182 — Scorer input hardening and provenance-condition identifiability audit

Date: 2026-11-10. Status: audit findings and implementation requirements; **not** executed experimental evidence.

## Audited implementation

Reviewed `research/protocol_181_reference_scorer.py` and its companion adversarial tests at the repository default branch. The two previously reported regressions (pairwise `prompt_hash` mismatch and cross-edit `physics_family` inconsistency) are implemented as rejection checks. Their tests have not been independently executed in this session.

## Newly identified gaps

1. **Malformed identifier handling.** The scorer checks only for `None` or empty string in pair keys. A JSON array or object used as a key component raises a native `TypeError` rather than the documented `InvalidPilot`. Even scalar booleans or numbers can be accepted as identifiers. Required remedy: validate every key as a nonempty string with a documented canonicalization policy, and reject ambiguous identifiers before dictionary insertion.
2. **Unvalidated numeric budgets.** Pair equality alone permits negative, zero, boolean, or nonfinite budgets (the latter possible when permissive JSON parsing accepts NaN). Required remedy: require finite, positive, correctly typed budget values and document units.
3. **Weak metadata validation.** The fields `rule_inventory_hash`, `prompt_hash`, `model_or_verifier_version`, `physics_family`, `edit_stratum`, and `assignment_seed` are required to exist but are not all checked for valid types or nonempty values. Required remedy: explicit schema validation before aggregation.
4. **Source and manifest ambiguity.** A source can appear in multiple manifests and is averaged under the same `source_id`. This may be legitimate only if a predeclared design specifies how repeated runs are weighted. Required remedy: enforce a single manifest for primary analysis or specify source/run hierarchical aggregation in advance.
5. **Paired prompt-hash interpretation.** A correct-link prompt and shuffled-link prompt necessarily differ in provenance content if hashes cover the entire serialized prompt. Equality of full prompt hashes would reject legitimate interventions; equality of hashes that exclude the intervention may be appropriate. Required remedy: define `prompt_hash` as a canonical *invariant prompt skeleton* hash, store a separate full-input hash, and validate that the only allowed difference is the assigned provenance intervention.
6. **Condition-label leakage.** A stored `provenance_condition` field is not proof that the verifier was blinded to assignment. Required remedy: preserve sanitized model input, condition-independent prompt template, immutable assignment manifest, and checks that condition names and expected labels were not present in the input.

## Adversarial acceptance tests to implement

- Reject array/object/boolean/number source IDs, edits, steps and manifest identifiers as `InvalidPilot`.
- Reject negative, zero, boolean and nonfinite budgets; reject empty model versions and hashes.
- Test an intervention-aware prompt skeleton hash: identical invariant template, distinct full-input hashes, exactly one provenance-link change.
- Reject undeclared cross-manifest pooling; retain valid multi-run data only under a prespecified hierarchical estimator.
- Validate deterministic score on invented fixtures with source imbalance, abstention, and opposing signs. Never present fixture output as model performance.

## Scientific decision gate

**Do not run or publish a confirmatory evaluation** until schema, intervention integrity, label independence, source grouping, and blinding checks are implemented and pass on an independently verified zero-charge cloud runner. A passing software test would establish only software behavior, not physical understanding or novelty.

## Resource and disclosure constraints

No compute provisioning or model inference is authorized by this note. The user's laptop remains browser-only. GitHub Actions minutes, billing state, and account-specific entitlements must be checked before running any workflow. No paid fallback, card enrollment, or automatic billing. Independently adjudicated pilot data and full-text prior-art review remain prerequisites to a defensible public manuscript. November 22 is conditional.
