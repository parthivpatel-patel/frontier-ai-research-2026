# Protocol 177 — Paired intervention annotation and leakage-resistant pilot specification

Date: 2026-11-10. Status: prospective specification only. No new empirical result, annotation, or novelty assertion.

## Why this protocol exists

Protocol 176 identifies an identification problem: verdict changes under altered physics text are not evidence of correct physical reasoning without an independently adjudicated direction of change. This protocol converts that concern into an auditable dataset contract, explicit exclusion rules, and a baseline decision procedure. It does not assume that the proposed verifier will outperform existing methods.

## Unit and record schema (JSONL, UTF-8)

One record represents a **source problem and a single paired intervention**. Required fields:

- `source_id`: stable pseudonymous source-problem identifier, unique at the problem level.
- `pair_id`: unique intervention-pair identifier; multiple pairs may share a source.
- `physics_family`: preregistered taxonomy value, not inferred from the observed verifier result.
- `source_license`, `source_citation`, `source_revision`: provenance and redistribution gate.
- `original_text`, `edited_text`: immutable texts, with SHA-256 hashes for each.
- `fixed_step`: identical candidate reasoning step evaluated against both texts, with a hash.
- `intervention_type`: one of `truth_changing`, `equivalent_paraphrase`, `nonconstraint_placebo`.
- `edited_spans`: character offsets into original and edited text plus span roles (physical premise, scope qualifier, or nonconstraint).
- `constraint_inventory`: normalized constraints, units, scope, and traceable text-span references; never silently substitute an inferred constraint for a stated one.
- `annotator_a`, `annotator_b`: independently produced labels, rationale, relevant constraints, confidence, and adjudication timestamps. Do not expose verifier outputs during labeling.
- `adjudicated_y_original`, `adjudicated_y_edited`: each one of `valid`, `invalid`, `unresolved`; `adjudication_status` and `disagreement_reason`.
- `split`: `development`, `calibration`, or `held_out`, assigned at source level before evaluation.
- `manifest_version`, `record_sha256`: integrity fields; hashes must be recomputed from a documented canonical serialization.

For truth-changing edits, the adjudicated validity labels must differ. For equivalent paraphrases and nonconstraint placebos, they must agree. Otherwise quarantine the pair as a protocol violation, do not relabel it based on a verifier output.

## Annotation workflow

1. Prepare source problem, fixed step, and one minimal intervention; document any incidental changes in lexical complexity, units, or answer format.
2. Assign source-level split and immutable IDs before calibrating thresholds. All descendants of a source stay in one split, including paraphrases, near-duplicates, and generated counterfactuals.
3. Blind two independent adjudicators to model/verifier predictions, proposed method identity, and one another's labels. Both assess original and edited step validity and cite the controlling premise.
4. Resolve disagreement using a prespecified third adjudication procedure; retain all raw labels. An unresolved case stays unresolved, and its exclusion count is published.
5. Freeze the dataset manifest and its hash before held-out inference. Publish only material whose licensing and privacy rights allow redistribution; otherwise publish hashes, provenance and permitted derived metadata.

No independent human annotations have been collected or verified at the time of this protocol.

## Five matched comparison arms

A. Answer-only outcome checker; B. dimensional-consistency checker; C. physics-aware step judge; D. deterministic constraint checker with span provenance hidden; E. proposed text-span and scope-aware constraint checker. Freeze input visibility, tool access, calibration budget, abstention policy, and inference cost for each arm. Explicitly mark any arm infeasible instead of substituting an invented result. A separate randomized-linkage negative control permutes constraint-to-span associations **within the same split and physics family** using a recorded seed and a derangement when feasible; it must preserve the constraint inventory. Never permit a source or its edited descendants to cross splits.

## Outcomes and falsification

For each source, aggregate its pair scores before averaging across sources. Record: (i) original and edited verdict correctness, (ii) directionally correct transition when truth changes, (iii) false flips for truth-preserving edits, (iv) abstention and coverage, and (v) correct-answer yield with abstention counted as not correct. Show source counts and family counts, not only pair counts.

Compare E against the strongest feasible baseline at frozen matched coverage. Treat mismatched coverage as an estimand mismatch requiring explicit sensitivity analysis, not a win. Primary inference must resample or otherwise account for independent source clusters; do not assume paraphrases are independent. Report uncertainty, paired effect sizes, family sensitivity and multiplicity transparently. A positive result requires superiority beyond a **prospectively specified** minimum meaningful effect, adequate uncertainty evidence, and randomized-linkage degradation. No thresholds, sample sizes or power claims are set here without feasibility data.

Falsify or withhold the proposed mechanistic interpretation if randomized linkage matches E, placebo false flips increase, baseline superiority disappears under source-level aggregation, or adjudicators cannot reliably distinguish truth-changing edits. Even a successful external verifier does not prove the internal reasoning process of the language model is faithful.

## Execution and integrity gate

Before cloud execution, verify the account-specific zero-cost quota, billing controls, public-repository runner eligibility, and availability. Do not infer free capacity from a previous successful CI run. Never use laptop compute or paid model services. Record workflow SHA, dependency lock, manifest hash, runner metadata, test counts, and actual cost. No cloud job is authorized by this protocol alone.

Prior-art priority remains unresolved, particularly overlap with 2026 scientific process reward models and counterfactual physical-world evaluations. The manuscript should disclose AI assistance according to venue policy and distinguish authored hypotheses from measured findings. November 22 remains a conditional internal target.
