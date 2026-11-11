# Protocol 187 — Closest-prior-art triage and estimand boundary

Date: 2026-11-11 UTC. Status: literature triage based on accessible abstracts and repository Protocols 183/186; **not a full-text systematic review, novelty finding, or experiment**.

## Verified primary records and overlap

| Work | Primary record | Established scope from abstract | Overlap and boundary |
|---|---|---|---|
| Turpin et al. (2023), *Language Models Don't Always Say What They Think* | https://arxiv.org/abs/2305.04388 | Prompt bias interventions can alter predictions without being disclosed in chain-of-thought explanations. | Strong precedent for intervention-based reasoning faithfulness; cannot claim input perturbation itself is novel. Our proposed intervention targets source-to-derivation provenance assignments rather than answer cues. |
| Lightman et al. (2023), *Let's Verify Step by Step* | https://arxiv.org/abs/2305.20050 | Process versus outcome supervision for mathematical solution verification; releases step-level labels. | Strong precedent for step-level verification. Our proposed study measures fixed-model sensitivity to evidence mappings and does not train a process reward model. |
| Gao et al. (2023), *Enabling Large Language Models to Generate Text with Citations* (ALCE) | https://arxiv.org/abs/2305.14627 | Benchmark and metrics for answer correctness and citation quality. | Direct precedent for citation attribution evaluation; source-link validity and citations cannot be claimed new as general concepts. |
| Chen et al. (2025), *Reasoning Models Don't Always Say What They Think* | https://arxiv.org/abs/2505.05410 | Tests whether reasoning-model chain-of-thought acknowledges injected hints. | Closely relevant modern intervention-based faithfulness evaluation. An observed accuracy difference would not by itself establish new mechanistic insight. |

This table reflects abstracts, not verified full-text/code differences. No claim of exhaustive coverage is warranted.

## Candidate research question (not a novelty claim)

For a fixed physics-verification item with independently established source-to-step admissibility, does an intervention that preserves evidence inventory, link-type/scope, source degrees, target multiset, and problem text but corrupts at least one semantically necessary provenance edge change a frozen model's independently graded correctness relative to the correct graph?

**Primary estimand:** paired average correctness difference among pre-registered eligible *templates*, not among arbitrarily numerous paraphrases. Report paired uncertainty and template-level clustering. A secondary endpoint may test explicit attribution judgments, clearly separate from final-answer accuracy.

**Identification warning:** a changed graph can alter attention, positional features, and pragmatic plausibility. A causal effect of the *assigned graph* is identifiable under randomized assignment; a causal effect uniquely attributable to *truth of provenance* is not identified without both-valid, order-only, and other matched controls. Do not equate this with internal reasoning faithfulness.

## Pre-registered falsifiers and stop rules

1. If independent annotators cannot establish that correct edges are valid and at least one shuffled edge invalid, the item is not eligible for the primary contrast.
2. If the correct and shuffled arms differ in non-provenance text or registered evidence inventory, the item fails the structural gate.
3. If a both-valid swap or order-only placebo yields a comparable effect, report presentation sensitivity and withhold a provenance-specific interpretation.
4. If effects vanish under a held-out physics family or are dominated by one template, restrict generalization accordingly.
5. If the paired interval includes zero, or observed results oppose the preregistered direction, publish null/adverse findings without changing the primary endpoint.
6. If no independently verified $0 cloud runner and no independently adjudicated pilot are available, release only a methodological note, not an empirical paper.

## Immediate implementation audit

The current Protocol 183 validator verifies source/target *membership* and graph-multiset invariants. It does **not** verify a source-to-target semantic admissibility matrix or independently anchored assignment. The invariant's allowed IDs are model-visible and may inadvertently cue intended mappings; a blinded identifier-aliasing control should be preregistered. A source/target multiset check does not establish semantic invalidity.

## Next audit tasks

- Read full texts and publicly available code for all four records; record intervention units, data, endpoints, controls, and exact differentiating claims with page references.
- Expand search to evidence-graph perturbation, counterfactual citation attribution, entailment verification, physics reasoning benchmarks, and retrieval corruption.
- Build independently labeled physics items before running any model; keep raw adjudication and exclusion records separate from model-visible artifacts.
- Verify runner eligibility, quotas, overage controls, and billing/card requirements immediately before any hosted execution. No compute is authorized by this note.

No model tests, inference, training, cloud jobs, or local laptop workloads were run for this audit. No results are asserted.
