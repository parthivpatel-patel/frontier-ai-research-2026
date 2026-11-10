# Protocol 184 — External preregistration anchor and provenance permutation audit

Status: design specification only; no executed experiment, no validated novelty claim. 2026-11-10.

## Finding from source inspection

The Protocol 183 validator checks `assignment[item_key] == ["correct","matched_shuffle"]`, which only lists two arm names. It neither encodes which target was randomly assigned nor verifies that the assignment was fixed before outcomes. A modified assignment dictionary can therefore remain internally consistent. The existing expected-failure test recreates the same dictionary and asks the validator to reject it; this is an intentionally impossible expectation without an independent anchor, not evidence of a runtime defect by itself.

A second gap is that matching multisets of (source,type,scope) while changing targets does not guarantee a *permutation* of original target assignments. For example, correct targets [A,B] and shuffled targets [B,B] pass the current structural checks when both targets are allowed, despite destroying the original target multiset. This could change graph degree and difficulty, confounding any causal interpretation.

## Required preregistration contract

Before model inference, freeze an external, independently retrievable manifest containing: protocol version; study identifier; all item IDs and source IDs; eligibility/exclusion rules; both candidate link sets; the target multiset per matched stratum; deterministic assignment procedure and its seed-commitment policy; model/prompt and decoding specifications; primary outcome; source-level weighting; missingness/abstention handling; planned uncertainty and multiplicity methods; stopping rule. Publish a content digest and timestamp in a GitHub commit or archived release **before** outcomes are collected, and preserve the commit identifier independently of the scored artifact. A SHA-256 field stored solely inside a mutable audit document is not an independent preregistration anchor. GitHub history is useful provenance but not equivalent to a trusted third-party timestamp or cryptographic signature.

At evaluation, provide the expected manifest digest via a separately supplied, pinned CLI argument or trusted configuration, compare the canonical manifest bytes to it, and verify each observed item and intervention against the pinned manifest. Never allow the audit JSON to nominate its own expected digest. If the external digest is missing, fail closed for preregistration claims while allowing an explicitly labeled exploratory structural-only report.

## Intervention design

Within each prespecified (link type, scope, target universe) stratum, require the shuffled condition to preserve source multiset, target multiset, link count, and target in/out degree when relevant. Require at least one changed source-to-target mapping. Reject duplicate links and any self-links, unless an explicit registered protocol permits them. When a valid derangement is impossible, mark the item ineligible *before* outcomes, not after seeing results. Ensure provenance shuffling cannot introduce invalid physics facts that are themselves answers.

This is a design decision: preserving target degrees may be too restrictive for some graph structures. Report the number of eligible and ineligible cases and compare against an alternative placebo that preserves only link counts. Do not silently substitute a weaker control.

## Minimal adversarial acceptance matrix

1. Externally pinned manifest matches the exact preregistered bytes: accept preregistration check.
2. Manifest edited and rehashed within the audit document, external pin unchanged: reject.
3. Missing external pin: report exploratory-only, never preregistered.
4. Duplicate or missing item after preregistration: reject or report prespecified attrition without silent deletion.
5. Correct [A,B], shuffled [B,B]: reject target-multiset mismatch.
6. Correct [A,B], shuffled [B,A] with compatible constraints: accept structural permutation.
7. No valid derangement: record pre-outcome ineligibility.
8. Identical arms: reject.
9. Random seed or assignment regenerated after labels are observed: reject when detectable; disclose that procedural controls cannot prove absence of all human tampering.
10. Model-visible text contains explicit or implicit answers: syntactic checks plus independent human semantic audit; no claim of automatic semantic detection.

## Inference and falsification

A permutation of provenance links is not automatically a randomized experiment. Valid causal randomization inference requires a documented randomized assignment mechanism, exchangeability conditions, and attention to source-level interference. Primary estimand: source-weighted difference in adjudicated verification yield between correct and shuffled provenance, with abstention treated as incorrect. Predefine a null of no benefit and a minimum practically meaningful improvement; report confidence intervals, uncertainty clustered at source level, negative controls, and sensitivity to target-degree constraints. A null, reversal, or improvement that disappears under matched difficulty is a falsifying outcome for the claimed intervention benefit.

## Scientific and operational gates

Do not call a synthetic passing fixture a physics result. Do not claim novelty until closest literature on provenance attribution, citation faithfulness, evidence graph interventions, counterfactual evaluation, and physics-reasoning verification is reviewed with dates and concrete methodological differences. Only run tests or model inference on independently verified $0 cloud resources with account-specific quota and billing eligibility checked; no local laptop workloads or paid API use. Publication target November 22 is conditional on preregistration, independent labels, credible baselines, and replicated evidence.
