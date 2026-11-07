# Protocol 111 — Paired lineage bootstrap: executable contract and failure gates

Date: 2026-11-06. Status: design specification only; no bootstrap execution or empirical findings. Extends Protocol 109 without modifying its preregistered primary estimand.

## Fixed inputs
Each held-out record must include `lineage_id`, `physics_family`, `intervention_id`, `system_id`, `adjudicated_unsafe` (boolean), `acceptance_score`, and a frozen calibration threshold identifier. Record the physical assumptions, provenance, adjudicator disagreement state, and split manifest hash. A lineage cannot cross development, calibration, and held-out splits. Reject missing IDs, nonfinite scores, nonboolean adjudications, duplicate system/intervention/lineage keys, and unadjudicated labels in the primary test. Intervention outcomes must not be silently pooled as independent scenarios.

## Estimand and sampling unit
For each system and family, use held-out accepted unsafe claims divided by all held-out accepted claims; undefined when none are accepted. The primary family-standardized contrast is sum of fixed family weights times (risk of proposed verifier minus risk of comparator). Calculate it only when both systems have nonzero accepted counts in every positive-weight family and calibration achieved preregistered feasible matched familywise coverage. Report the full held-out family coverage vectors regardless of whether the contrast is defined.

For each replicate, sample *distinct lineage IDs* with replacement **within each physics family**, using the same sampled lineage multiset for every system and intervention. Keep every row associated with each sampled lineage, and multiply its contributions by the lineage's sampled multiplicity. Do not deduplicate repeated draws; do not draw individual prompts. A lineage assigned to multiple physics families is an invalid manifest unless a prespecified single-family mapping is recorded. Never retune thresholds in a replicate.

## Determinism and uncertainty
Freeze the seed, pseudorandom generator implementation/version, sorted lineage ordering, 2,000 or more replicates, fixed weights, and percentile CI level (95% provisional). The point estimate comes from original held-out data, not the bootstrap mean. Compute replicate contrasts only when all required family risks exist. Report undefined replicate count and fraction **before** any interval. Predeclare an undefined-replicate admissibility threshold (provisional maximum 1%; requires sensitivity analysis at 0%, 1%, 5%). If exceeded, suppress the headline CI rather than selectively dropping failures. Percentile CIs are descriptive uncertainty summaries, not distribution-free risk guarantees; inspect small-cluster and boundary behavior separately.

## Hand-checkable regression fixtures
1. **Identical systems:** same scores and truth across systems; every defined replicate contrast must be exactly zero.
2. **Correlated copies:** duplicate paraphrases within a lineage; lineage count must not increase, and sampled multiplicities must apply jointly to all copies.
3. **Two-family weighting:** family A risk contrast +1 and family B contrast -1; equal family weights yield zero regardless of family sample-size imbalance, provided all denominators are positive.
4. **Zero acceptance:** any positive-weight family with zero accepted observations makes primary contrast undefined; report counts rather than a fabricated zero.
5. **Paired direction:** when systems have discordant accepted unsafe claims within a lineage, the bootstrap must resample their joint outcomes, never independent system indices.
6. **Determinism:** identical manifest, seed, and version yield identical replicate counts and quantiles.
7. **Coverage infeasibility:** an infeasible calibration family prevents a primary matched-coverage claim even if held-out aggregate coverage happens to match.
8. **Split contamination:** any shared lineage across calibration and held-out data fails closed.

## Interpretation and falsification
Predefine a minimum scientifically meaningful improvement and report confidence intervals, effect sizes, family coverage, and acceptance counts. A CI crossing zero does not establish superiority. An apparent gain that disappears against a simple dimensional-analysis baseline, under truth-changing physical interventions, or after lineage grouping defeats the primary contribution. Compare evidence removal and contradictory evidence to full evidence within the same lineage; compare truth-preserving paraphrases separately from truth-changing interventions. Avoid claiming causal evidence dependence unless interventions and adjudication justify that interpretation.

## Next implementation sequence
Implement a pure standard-library Python module with immutable validated inputs, explicit undefined results, deterministic family-stratified lineage resampling, and fixture tests. Run on an eligible GitHub-hosted standard runner only after checking repository-specific permissions, current public-repository pricing and billing configuration; do not trigger any potentially billable runner. Capture commit SHA, runner type, test count, log URL, and exit status. Then freeze a provenance-rich pilot manifest and conduct independent blind physics adjudication. Do not claim model results before running them.

## Novelty boundary and research integrity
This is an inference implementation specification, **not** a new bootstrap method. Cluster bootstrap, paired comparisons, selective prediction, and group-conditional risk control are established areas of prior art. The potential contribution remains a carefully falsified empirical investigation of physical-evidence dependence in scientific verification, if a genuine gap survives a full-text prior-art audit. Preserve zero expenditure, no laptop compute, no cross-project reuse, and venue-appropriate AI-assistance disclosure.
