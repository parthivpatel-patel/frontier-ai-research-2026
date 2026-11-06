# Protocol 109 — Lineage-aware inference and decision gate

Date: 2026-11-06. Status: preregistered design, **not executed**. Independent frontier-AI research; no relationship to the user's other projects.

## Claim boundary
The candidate contribution is an **empirical test of physical-evidence dependence in selective language-model scientific verification**, not a new general theory of abstention, conformal prediction, or physics reasoning. A reduction in unsafe acceptance is insufficient if coverage differs, labels are unreliable, or linguistic artifacts explain the result. No experimental superiority or novelty is established.

## Unit, labels, and split
The independent sampling unit is a *scenario lineage*: all paraphrases, versions, interventions, source-family aliases and derived prompts from a common physical scenario are grouped. Freeze this grouping **before** model evaluation. All members of one lineage belong to exactly one of development, calibration, or held-out test. Physics families are declared before sampling; ambiguous cases are excluded from the primary analysis and reported separately. Independently adjudicate the physical truth under explicitly recorded assumptions. Adjudicators must not see model outputs or experimental condition. Disagreements receive an unresolved label until reconciled; do not count them as safe.

## Primary estimand
For system m, family f and a threshold t selected only from calibration, let A_mi(t) indicate acceptance and U_mi indicate an independently adjudicated unsafe accepted claim. Define family coverage C_mf = sum(A)/N_f and conditional unsafe-acceptance risk R_mf = sum(A*U)/sum(A), undefined when denominator is zero. For fixed preregistered weights w_f summing to one, standardized risk R_m = sum(w_f R_mf) only if every positive-weight family has accepted claims. Do not silently replace undefined risk with zero. Compare the proposed verifier to each baseline using Delta = R_proposed - R_baseline at **feasible matched familywise coverage**. Report coverage vector, accepted counts, and infeasible families even if the primary Delta cannot be estimated. A pooled statistic is secondary and must not substitute for standardized risk.

## Threshold and tie rules
Choose all thresholds using calibration only, separately for each system and family. Specify target coverage and tolerance before examining test outcomes. Apply frozen thresholds to test without adjustment. Accept tied scores together; do not break ties using truth labels. If calibration cannot attain target coverage within tolerance, mark comparison infeasible rather than optimizing on test. Record achieved test coverage and deviations; calibration matching does not guarantee test matching.

## Uncertainty
Use a paired, stratified cluster bootstrap: within each family resample *scenario-lineage IDs* with replacement, keeping all paired systems, paraphrases and interventions of each sampled lineage together. Recompute family risks and Delta using frozen thresholds; never recalibrate in bootstrap replicates. Predeclare a fixed pseudorandom seed, number of replicates (at least 2,000 for final inference), weights and CI method. Report the fraction of undefined replicates. If undefined replicates are appreciable, report that the interval is not reliably estimable rather than discarding them without disclosure. Cluster-robust uncertainty is not a guarantee against biased adjudication, selective dataset construction, or distribution shift. Include raw per-family numerator/denominator tables.

## Adversarial evidence-dependence test
For the same lineage, compare (a) full physical evidence, (b) evidence removed, (c) physically contradictory evidence, (d) surface paraphrase preserving physical truth, and (e) an explicitly controlled physical-assumption intervention that changes the correct label. Hold prompt budget, task wording template, and evaluation rules as comparable as possible. Avoid treating generated counterfactuals as ground truth: independently adjudicate each intervention. A credible physical-evidence dependence claim requires sensitivity to truth-changing interventions and relative invariance to meaning-preserving paraphrases, beyond matched baselines.

## Baselines and falsification
Compare language-only, retrieval/evidence-aware, deterministic units/dimensional checks, and any feasible established verifier. Audit closest prior work on selective prediction, group-conditional risk, scientific QA and evidence attribution before choosing a novelty claim. Falsify or narrow the claim if: (1) leakage is detected; (2) independent adjudication fails; (3) apparent gains vanish under matched familywise coverage; (4) a simple dimensional checker or retrieval baseline matches performance; (5) the method reacts to paraphrases more than physical interventions; (6) results depend on post-hoc exclusions; or (7) a prior method already implements the proposed mechanism and outcome.

## Implementation gates (not yet completed)
1. Execute all existing Python tests on a **verified zero-charge** GitHub-hosted standard public-repository runner; verify repository Actions permissions, billing restrictions and current runner eligibility first. Do not launch paid/larger runners or require a payment card.
2. Add a small pure-Python paired cluster-bootstrap module with hand-checkable tests for identical systems (Delta zero), correlated lineage copies, zero accepted counts, family-weighting and deterministic seed.
3. Freeze a benchmark manifest with provenance and blinded adjudication; run pilot before claiming results.
4. Document full prior-art citations with publication dates and precise differences; produce an explicit collision table.
5. Only then decide whether a public paper is justified. November 22, 2026 is a conditional internal target, not a promised publication date.

## Integrity and cost
No empirical results are asserted here. No model inference, simulations, cloud jobs, or laptop computation are required by this document. Keep actual spending at $0; verify free-tier conditions immediately before each cloud experiment. Disclose AI assistance in accordance with the eventual venue's policy.
