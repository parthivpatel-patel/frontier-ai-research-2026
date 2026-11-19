# Frozen matched-coverage evaluation: executable contract (2026-11-19)

Status: methodological specification, **not** empirical evidence or a novelty claim. Scope: independent frontier-AI verifier study only.

## Scientific question

On identical candidate answers in NLP, mathematics, and physics, does a proposed shared verification score reduce selective error relative to calibrated confidence-only and domain-specific verification, at a prespecified accepted-answer fraction and comparable per-item verification cost, when evaluated on unseen source families?

A positive finding would be a narrow empirical result about selective decision quality, **not** proof of a common physical mechanism, model consciousness, causal mediation, or distribution-free safety.

## Dataset and split invariants

Each observation has immutable question_id, source_family_id, domain, candidate_answer_id, candidate_answer_hash, reference provenance, blinded correctness label, and per-method verification cost. Every method sees the *same* candidate answer and ground-truth label. If methods generate their own answers, analyze separately; do not pool with this experiment.

Assign whole source families to train/calibration/held-out partitions before score inspection. Check for near-duplicate questions, template families, answer contamination, and cross-partition shared provenance. Document label uncertainty and adjudication; exclude disputed labels only under a rule fixed before outcome inspection.

## Exact acceptance-budget protocol

Pre-register coverage targets (illustrative: 0.50, 0.70, 0.90; final targets must be frozen before testing). For each method, calibrate score direction and threshold on calibration families only. Record deterministic tie-breaking based on a predeclared cryptographic hash of immutable question_id and a published seed. Never choose a held-out threshold to hit target coverage: achieved held-out coverage is an **outcome**. Consequently, comparisons at a common calibration target are not automatically comparisons at matched achieved held-out coverage.

A distinct descriptive fixed-k analysis may accept exactly k held-out candidates per method using held-out scores without labels; it achieves equal held-out coverage but is a **transductive ranking evaluation**, not a deployed fixed-threshold policy. Label this analysis explicitly, freeze k beforehand, and never use it as evidence of deployable coverage calibration.

For each method report n, accepted n, accepted errors, achieved coverage, selective error (undefined if accepted n=0), family-weighted coverage, and the full source-family distribution. Do not replace undefined selective risk with zero. Report risk differences only when both denominators are nonzero; report decision disagreement cells and errors separately. Do not call the both-accepted subset a matched-coverage effect.

## Verification cost and baseline parity

Account for tokens, model calls, tool calls, wall time, and monetary equivalent where determinable. A zero-dollar hosted runner does not make external APIs free. Exclude paid APIs, paid runners, and card-dependent services unless independently verified eligible and explicitly approved. Match verifier budgets by precommitted resource caps, not by post-hoc pruning. Include confidence-only, domain-specific verifier, and cost-matched random-abstention controls; report any infeasible parity honestly.

## Inference and multiplicity

Use paired question-level differences, with source-family resampling as the primary uncertainty unit. With too few independent held-out families, refrain from asymptotic significance claims and show per-family effects. Freeze one primary coverage target and one primary comparator; treat other domains, targets, and comparators as secondary and correct for multiplicity or describe as exploratory. Include cluster bootstrap implementation details and seeds in the eventual code package.

## Adversarial falsification

- NLP: plausible fluent claims contradicted or unsupported by source documents.
- Mathematics: correct numerical conclusion paired with invalid derivation; distinguish answer correctness from proof validity.
- Physics: dimensionally valid but physically false claims, including violated boundary conditions or conservation laws.
- Source shift: held-out families must differ in provenance, not merely random item partitions.
- Baseline parity: no advantage if matched cost/coverage removes the gain.
- Leakage: halt confirmatory claims if threshold, label, or source provenance crosses the held-out boundary.

## Stop/go before November 22

**Go for empirical paper** only with public, independently rerunnable held-out evidence, adequate independent families, validated cost accounting, and a documented closest-prior-art distinction. **Go for methods/pre-registration note only** if empirical evidence is missing; title and abstract must not imply measured improvements. **No go for novel-performance claim** if effects fail under source shift, controls, or multiplicity correction.

## Compute safety

Run only on verified free standard GitHub-hosted runners for a public repository, after checking repository Actions permissions, runner availability, and current pricing/limits. Do not activate paid larger runners, external inference endpoints, or local workloads. If eligibility cannot be verified, keep experiments unlaunched and publish reproducible plans only.

## Disclosure

Record model/tool assistance, licenses, dataset provenance, negative findings, and all deviations. No fabricated results, hidden selection, or unsupported priority claims.
