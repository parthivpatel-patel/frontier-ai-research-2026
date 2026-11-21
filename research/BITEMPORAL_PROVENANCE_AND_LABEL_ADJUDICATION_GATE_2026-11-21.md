# Bitemporal provenance and temporal-label adjudication gate (2026-11-21)

**Status:** prospective methods specification, not empirical evidence, a novelty claim, or a replacement for the frozen primary estimand. No compute or cloud account was used to develop this text.

## Why this additional gate is needed

The existing point-in-time leakage stress test distinguishes publication, validity, and archive timestamps, but a single timestamp for each is insufficient when a source is corrected or backfilled. A 2026 page describing a 2024 observation may be historically *about* 2024 without having been *available* in 2024. Conversely, a 2024 archive capture might prove that an older statement was available then even if the live page has since changed.

Adopt **bitemporal provenance**: (i) *valid time* of the fact being described, and (ii) *transaction/availability time* when the exact source version was demonstrably accessible. These are different axes. Record revisions rather than overwriting prior versions.

## Proposed immutable record schema

Each candidate evidence version should contain:
- `item_id`, `source_family_id`, `source_id`, `version_id`, `content_sha256`, `snapshot_uri`, `retrieved_at_utc`
- `published_at_utc` with precision and evidence for that date; `first_verified_available_at_utc` and `last_verified_available_at_utc` (or null), each with an archival proof reference
- `valid_from_utc`, `valid_until_utc` (nullable); `supersedes_version_id` and `correction_notice_uri` (nullable)
- `question_cutoff_utc`, `label_asof_utc`, `label_source_version_ids`, `adjudicator_ids`, `adjudication_status`, `domain`, `units` (for numerical measurements)
- `provenance_status` in {verified, ambiguous, rejected}; `exclusion_reason` when not verified.

Do not treat `retrieved_at_utc` as the historical availability date. Date-only or timezone-ambiguous metadata should not be silently rounded into an admissible timestamp.

## Conservative admission rule

For a question with cutoff t, evidence version v is confirmatorily admissible only if:
1. Its bytes are content-addressed and an immutable historical snapshot or equivalent verifiable version record exists.
2. There is affirmative evidence that **this exact version** was accessible at or before t; a publication date alone is insufficient.
3. The factual claim's valid-time interpretation is appropriate for the question, and any correction or revision after t is not imported into the earlier answer.
4. Source family and label adjudication provenance are recorded, and the evidence does not contain prohibited answer-key leakage.

An archive capture after t does **not** prove pre-t availability. An archive capture before or at t can establish availability no later than that capture (subject to source authenticity and access). An item whose earliest independently verified availability is after t is excluded from the historical confirmatory arm, even if it asserts an earlier publication date. Missing proof is **ambiguous**, not proof of future contamination. Report exclusion counts by reason and family.

## Label adjudication and physics/math edge cases

Define the answer target as `y_i(t)` and preserve separate fields for what was *true or measured at t*, what was *publicly knowable at t*, and what later revisions established. Never substitute a later corrected label for the historical knowability target without explicitly changing the estimand.

- NLP: retain archived text and dated factual-claim versions.
- Mathematics: test historical availability of a proof, conjecture status, or theorem-database release; do not imply that mathematical truth itself changes with time.
- Physics: test released measurement values, calibration vintages, or published experimental limits, including units and uncertainty; do not imply that physical laws change with publication date.

Two adjudicators should independently review ambiguous labels without seeing model-arm outcomes; disagreements and resolution rules are logged before evaluation. If independent adjudication is infeasible, mark the corresponding domain exploratory.

## Deterministic preflight tests (no model inference)

1. Version published before t but first archived after t: **ambiguous/excluded**, not admitted.
2. Version archived before t and corrected after t: admit only the archived earlier version, never corrected bytes.
3. Same URL with two different hashes: two versions, not one overwritten record.
4. A fact valid at t but not publicly released until later: exclude from historical knowability task.
5. Missing timezone or only month-level timestamp at a boundary: ambiguous unless the whole possible interval precedes t.
6. Evidence hash duplicated in training/evaluation labels or answer keys: flag for independent leakage review.
7. Question and evidence from the same source family: retain grouping for family-level inference.
8. Unverifiable physics units or revision provenance: exclude from confirmatory scoring.
9. Zero eligible evidence: report empty retrieval and preserve the item; do not silently drop the question.
10. A correction notice after t: preserve the earlier answer target and log a revision sensitivity analysis.

## Falsification and reporting

A claimed historical verification benefit fails its intended interpretation if it disappears when only demonstrably pre-cutoff evidence is admitted, if improvements arise only from post-cutoff revisions, or if source-family-level uncertainty is inconclusive. Compare coverage, selective risk, accepted-question overlap, paired common-acceptance loss, exclusion fractions, and independent family counts. Keep the existing frozen confirmatory estimand and multiplicity gate; this is a provenance validity preflight, not an opportunity to choose a favorable outcome.

## Closest prior-art categories to audit

Bitemporal databases, temporal knowledge graphs, dataset-versioning and data-lineage systems, time-aware retrieval benchmarks, selective classification, conformal risk control, and adaptive-holdout literature all contain established ideas. The bitemporal distinction itself is **not novel**. The proposed combined protocol must be compared against existing temporal QA and point-in-time retrieval evaluations before any originality claim. In particular, the existing project audit cites Geifman & El-Yaniv (2017) selective classification and the NeurIPS 2025 TimE benchmark; those contributions must not be repackaged as new.

## Execution and publication constraints

This specification can be reviewed and implemented as lightweight schema validation in free GitHub-hosted CI only after current quota and billing restrictions are verified. No GPU inference, local computation, dataset downloads, credit-card setup, or paid cloud activation is authorized. A November 22 release should be labeled methods/preregistration unless independent held-out experiments and the full novelty audit justify stronger claims. Disclose AI assistance in accordance with the target venue.
