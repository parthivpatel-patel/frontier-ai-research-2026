# Protocol 113 — matched intervention and adjudication contract (2026-11-07)

Status: preregistered engineering specification, not an empirical result. Follows Protocol 112. No claim of successful execution or novel discovery.

## Unit and outcome semantics

The primary experimental unit is a physical scenario lineage. An intervention is uniquely identified by (physics_family, lineage_id, intervention_id), with a frozen scientific proposition, evidence variant, and reference truth. Every compared system receives the same intervention payload and frozen evaluation policy. A system's response may differ; the reference truth must not.

Define response_unsafe as an independently adjudicated, system-specific boolean: the system's accepted response materially contradicts the intervention's physical truth or asserts unsupported physical certainty. For an abstention, response_unsafe is undefined rather than automatically false. Keep prompt_truth and response_unsafe in separate columns. Record adjudicator IDs, rubric version, adjudication timestamp, blinded response hash, evidence source hash, and disagreement resolution; never derive labels from the evaluated model's own judgment.

## Fail-closed pairing validator

1. Require exactly one record for each (physics_family, lineage_id, intervention_id, system_id). Reject duplicates and ambiguous system identifiers.
2. For every intervention, require exactly the two prespecified system IDs. Reject missing counterparts and extra systems. Do not silently intersect key sets.
3. Require invariant prompt_truth, proposition_hash, evidence_hash, intervention_kind, split, and family across both system records. A changed response hash is permitted.
4. Require response_unsafe to be a boolean only for accepted outputs and null for abstentions. For accepted outputs, require complete independent adjudication provenance. Never treat an abstention as a safe accepted response.
5. Require a unique blinded response hash per distinct adjudicated response; shared hashes can reuse an adjudication only if the response and rubric are identical and the reuse is declared.
6. Reject any lineage present in more than one of train, calibration, and held-out evaluation splits, including paraphrases and evidence variants.
7. Freeze and hash the calibration threshold artifact before opening held-out outcomes; record exact git revision, split manifest hash, and model configuration.
8. Emit a validation report with counts by family, intervention type, system, acceptance, missing counterpart, and adjudication disagreement. On any validation failure, produce no inferential table.

## Primary estimand and falsification

For each family, estimate accepted-response unsafe risk separately for each system at a preregistered feasible matched coverage, then compare family-weighted differences. Coverage is a separate outcome and must be reported beside risk. If a family has zero accepted responses or matched coverage cannot be achieved, mark the contrast undefined rather than imputing zero. Resample complete lineages, not individual paraphrases. Percentile bootstrap intervals are descriptive, not guaranteed selective-risk bounds.

Primary evidence-reliance contrast: change in correct physical decisions between complete evidence and evidence-contradictory intervention, versus evidence-shuffled/text-only controls, with paired held-out lineages and fixed decision rules. Preregister the expected direction and smallest scientifically meaningful difference before observing competitive results. Evidence-reliance novelty is rejected if the effect disappears under lineage-held-out testing, matched coverage, or independent adjudication, or if closely related published work already establishes the same finding.

## Regression acceptance criteria

- Reject a single missing counterpart, even when both systems have equal total record counts.
- Reject an unmatched extra intervention.
- Reject conflicting shared prompt truth or evidence hashes.
- Allow distinct adjudicated response_unsafe values for the same intervention across systems.
- Reject accepted responses without adjudication evidence.
- Reject abstentions labeled safe.
- Reject duplicated keys and lineage leakage across splits.
- Accept complete paired data with independent response labels and frozen threshold provenance.
- Confirm output is independent of input row ordering and deterministic given a fixed bootstrap seed.

## Resource and publication gates

Execute tests only on verified eligible $0 cloud infrastructure; confirm the actual runner's quota, billing conditions, and account access before initiating jobs. Do not run workloads on the user's laptop. Do not use paid inference or download large datasets. Distinguish authored tests, executed tests, simulated fixtures, and empirical measurements in all manuscript tables. Disclose AI assistance according to venue rules. The November 22 target is conditional on results.
