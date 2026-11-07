# Protocol 112 — paired estimand integrity audit (2026-11-07)

Status: methodological audit, not empirical evidence. Protocol 111 code and nine authored tests were inspected at commit `092c15c8d711eda77fe0c758268e9430b076cf28`. No new cloud execution is claimed here.

## Blocking issue: outcome consistency across systems

`Observation.unsafe` is currently stored separately for each `system_id`. For a fixed (lineage_id, intervention_id), a reference scientific truth label should be invariant across systems when both systems are judging the **same proposition**. The existing fixture `test_paired_lineage_direction` assigns opposite unsafe labels to new and baseline for the same intervention. Such rows may be legitimate only if `unsafe` refers to system-specific output correctness, **not** a shared prompt truth label. This semantic ambiguity must be resolved and documented before inference.

**Decision gate:** define `unsafe` as an adjudicated property of each system's *accepted response*, with adjudication evidence and blinded independent reviewers; do not impose cross-system equality under this definition. If instead it is a prompt-level truth label, enforce equality across systems and replace contradictory fixtures. The protocol must not silently mix these interpretations.

## Blocking issue: paired observation completeness

The current validator prevents duplicate (lineage, intervention, system) keys but does not require both systems to appear for each intervention. Consequently, unmatched interventions can contribute to a nominally paired lineage bootstrap, making estimands sensitive to differing case mixes. Before claiming a paired comparison, enforce matching of (lineage_id, intervention_id) keys for both systems or explicitly define a missingness-adjusted estimand with a prespecified missingness model. Missingness must be counted and reported; do not silently drop cases.

## Statistical scope

The bootstrap currently resamples lineages within families and computes a difference of accepted-response unsafe fractions. Its CI is a descriptive percentile interval, conditional on the observed accepted subsets and frozen thresholds. It does not provide finite-sample coverage or selective-risk guarantees. Zero accepted denominators suppress the CI, correctly. Investigate whether highly variable acceptance rates and rare unsafe events cause the percentile CI to under-cover, using cloud-executed synthetic coverage simulations only after $0 runner eligibility is verified.

## Pre-registered falsification gates

1. On fully matched held-out lineages, compare physical-evidence-complete, evidence-removed, evidence-contradictory and physically intervened variants, with paraphrases clustered within lineage.
2. Require independent adjudication of physical truth and system-response safety, blinded to system name; record provenance and disagreement.
3. Report acceptance/coverage and unsafe risk together, with frozen calibration thresholds; abstention alone cannot be scored as improved reasoning.
4. Include text-only shortcut baselines, evidence-shuffled controls, and an uninformative abstain-all baseline. A claimed evidence-grounding effect fails if evidence removal or contradiction does not materially change decisions in the expected direction at matched coverage.
5. Predefine the primary contrast, minimum meaningful effect, uncertainty method, and multiplicity correction before competitive model results are viewed.
6. Stop novelty claims if closest prior work already establishes the same empirical effect or if results fail under lineage-held-out testing.

## Required engineering follow-up

Add a strict matched-intervention validator and tests for missing counterparts, unmatched extra interventions, and duplicate adjudication provenance. Resolve the `unsafe` semantic contract first. Add split-manifest leakage checks, immutable calibration artifact hashes, and provenance checks before any empirical paper tables. No GPU, local laptop workload, paid inference, or external dataset download is authorized by this protocol.

## Novelty boundary

Clustered bootstrap, selective prediction, abstention, and evidence perturbation are established techniques, not standalone novelty. The potentially publishable contribution would have to be a new, rigorously validated empirical finding or benchmark about physical-evidence reliance under controlled linguistic variation, with independent truth labels and robust comparisons. That claim is currently unestablished.
