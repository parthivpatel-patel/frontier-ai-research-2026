# Protocol 185 — Source-universe and provenance semantics audit

Date: 2026-11-10. Status: design audit only; no experimental results.

## Verified implementation gap

Inspection of `research/protocol_183_integrity_validator.py` shows that each link's `target` is checked against `invariant.allowed_target_ids`, but its `source` is checked only for being a nonempty string and for differing from the target. The paired-arm signature comparison ensures source strings match *between arms*, not that they refer to a registered physics derivation step. Therefore a fabricated source such as `invented_step_999` can pass the structural gate if included identically in both arms and if the other conditions are satisfied. This is a concrete provenance-validity gap, not evidence of model failure.

## Required contract before a scientific pilot

1. Require a nonempty, unique `allowed_source_ids` universe from the invariant, with typed nonempty identifiers and explicit source-to-step bindings. Reject any edge referencing an unregistered source.
2. Validate unique, nonempty `allowed_target_ids`; reject duplicate identifiers, nonstring entries, and source/target namespace collisions unless explicitly permitted and typed.
3. Require every registered source's semantic identity to be independently checked against the actual derivation or statement in the problem, not inferred from its identifier. Verify target constraints and permissible link semantics through blinded human adjudication.
4. Distinguish syntactically valid permutations from semantically incorrect provenance. A target swap may accidentally remain valid when both constraints apply to both steps; the intervention must be independently labeled and ambiguous pairs excluded by a prespecified rule.
5. Preserve the source and target universes across arms, as well as link type, scope, source degree, and target multiset within strata. Store the full assignment and exclusion rules in an independently anchored preregistration before outcomes.
6. Add adversarial fixtures: fabricated source; duplicate source IDs; duplicate target IDs; nonstring identifiers; semantically valid swap; ambiguous link semantics; missing registered step; and changed step text with identical identifiers.

## Primary falsification criteria

- If blinded adjudicators cannot reliably distinguish correct from shuffled provenance on the preregistered sample, the manipulation fails and no causal intervention effect may be claimed.
- If treatment arms differ in task text, computational budget, visible answer cues, or target/source degree, reject the comparison.
- If estimated improvement disappears under independent semantic validity checks, negative controls, or a matched-budget baseline, report the null/fragile result.
- If close prior work already establishes the same construct and intervention, narrow the novelty claim rather than declaring originality.

## Evidence and execution constraints

This audit was based on source inspection, not a completed test run. The present validator returns `structural_gate_only`; this should not be described as semantic provenance verification or independently anchored preregistration. Run unit tests and pilots only on confirmed zero-charge cloud resources after checking current account eligibility, quotas, card/billing requirements, and cancellation safeguards. No local laptop compute, model training, or inference is authorized. Publication target November 22 remains conditional on independently reproduced findings and a full-text literature comparison.
