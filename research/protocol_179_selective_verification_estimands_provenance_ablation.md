# Protocol 179 — Selective-verification estimands and provenance ablation identifiability

Date: 2026-11-10. Status: prospective mathematical analysis, not an empirical result. Supplements Protocols 177–178.

## A problem with comparing abstaining verifiers

A provenance-aware checker can appear more accurate simply by declining difficult decisions. Comparing accuracy only among non-abstained examples changes the evaluated population and is not a fair test of physical grounding. Similarly, equal nominal coverage does not ensure the same *examples* were answered.

For source problem s, paired variant j, and method m, let Y_sj be the independently adjudicated label in {valid, invalid, underdetermined}, D_m,sj be its output in those labels or abstain, and A_m,sj = 1{D_m,sj != abstain}. Define C_m,sj = 1{D_m,sj = Y_sj}, with C=0 on abstention. The source-weighted **correct-verdict yield** is

  V_m = (1/S) sum_s (1/n_s) sum_j C_m,sj.

Coverage is Q_m = (1/S) sum_s (1/n_s) sum_j A_m,sj. Selective accuracy is V_m/Q_m only when Q_m > 0. Always publish all three; V alone rewards both accuracy and coverage, while conditional accuracy alone rewards abstention. If an explicit utility for abstention is chosen, predeclare it and report sensitivity rather than retrofitting a favorable penalty.

## A formal counterexample (constructed, not measured)

Consider four equally weighted items with truth labels fixed. Method P answers the two easy items correctly and abstains on two hard items: coverage 1/2, selective accuracy 1, correct-verdict yield 1/2. Method B answers all four and gets three correct: coverage 1, selective accuracy 3/4, yield 3/4. A claim that P is better based solely on 100% selective accuracy is false for total correct-verdict yield. Conversely, B's greater yield does not establish better calibrated risk at a fixed coverage level.

## Matched-coverage comparisons

Predeclare a coverage grid (for example 0.50, 0.75, 1.00), with feasible levels and tie handling fixed before reading test labels. Choose confidence thresholds using a separate source-disjoint development set. Evaluate all methods at each feasible coverage target on held-out sources. Report achieved rather than only requested coverage, per-family coverage, and uncertainty. Threshold selection or tuning on held-out test labels invalidates confirmatory interpretation.

Even with equal achieved Q, methods can select different examples. Include (a) an all-eligible yield comparison, (b) selective risk at matched coverage, and (c) a diagnostic comparison on the intersection of items both methods answer, explicitly labeling (c) a selected-subset comparison rather than a population effect.

## Identifying what provenance adds

Freeze the physical rule inventory, reasoning step, input context, numerical tolerances, model weights, prompt budget, and execution budget. Randomize only the provenance-link assignment in a *type- and scope-matched* pool. Compare: correct links; links removed with all rule text preserved; type/scope-matched permuted links; and irrelevant-placebo span links. Each ablation must preserve formatting and input length as closely as possible. Record failures of matching and reject unmatchable cases before viewing outcomes.

The paired contrast of correct-link versus shuffled-link decisions identifies a linkage-information effect **within the constructed intervention distribution**, not general physical understanding or out-of-distribution transfer. Link permutations may alter input naturalness; independently audit this artifact. If correct links provide additional task-relevant text unavailable to the baseline, the comparison is not isolated.

## Statistical and adjudication gates

Define one source problem as the independent sampling unit. Resample or randomize at source level; do not treat edited variants as independent. If there are too few independent sources, present exact paired differences and exploratory intervals rather than asymptotic significance. Stratify by physics family and label class; disclose family support and abstentions. Keep underdetermined as a third legitimate label. Independent blind adjudication and unresolved-case reporting are required before quantitative claims.

## Falsification criteria

The hypothesized contribution fails or is sharply limited if: correct links do not improve held-out source-weighted yield or matched-coverage risk; type/scope-matched link shuffles perform similarly; improvements are confined to items with additional information leaked through the link; irrelevant edits cause frequent false verdict flips; or independent adjudicators cannot consistently determine the labels. An inconclusive confidence interval is not evidence of success or failure.

## Execution and integrity status

This document is a mathematical and experimental specification only. No independent annotation, training, inference, or cloud experiment was run to establish these results. Existing CI regression success does not establish scientific validity. Before running even CPU-only cloud tests, verify the specific account's free GitHub Actions entitlement, remaining minutes/storage, billing behavior and spending controls; do not trigger paid jobs or require laptop computation. Record code revision, dataset hashes, labels, licenses, and AI assistance disclosures in the eventual manuscript. November 22 remains conditional.
