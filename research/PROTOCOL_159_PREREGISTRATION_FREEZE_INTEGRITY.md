# Protocol 159 — Preregistration freeze integrity and executable decision gate

Date: 2026-11-18. Status: **design correction, not empirical evidence**.

## Identified reproducibility defect

Protocol 158 places `frozen_manifest_sha256` inside the same JSON document that is to be hashed. Requiring that field to equal the SHA-256 of the complete file creates a self-referential digest requirement; a routine hashing workflow cannot satisfy it. The freeze procedure must define precisely which bytes are hashed, without requiring a hash to contain itself.

**Correction:** keep the study manifest and freeze attestation in separate files. The study manifest contains no self-digest. The attestation contains the manifest's SHA-256 and Git commit ID. A later manifest modification invalidates the attestation. This correction does not retroactively freeze Protocol 158's blank template.

## Reproducible freeze procedure (cloud only)

1. Finalize `research/preregistration/study_manifest.json`, including the source-family definition, sampling frame, domain-specific hypotheses, source-disjoint splits, candidate policies, baselines, adjudication protocol, cost-matched verification budget, model and decoding versions, risk tolerance, multiplicity family, and exclusion rules. Do not include private keys, unreleased benchmark items, or sensitive labels.
2. Validate that no required fields are `null`, that `status` is `FROZEN`, that all candidate-policy and baseline identifiers are unique, and that each domain has an explicit target population and sample-size feasibility assessment. The frozen file must **not** contain `frozen_manifest_sha256`.
3. Serialize JSON with an explicit canonicalization rule (e.g., UTF-8, sorted object keys, compact separators, no NaN/Infinity), write the exact bytes, and calculate SHA-256 of those bytes using Python standard library in a **GitHub-hosted standard public-repository runner**, after checking current zero-cost eligibility.
4. Commit the manifest and separately commit `freeze_attestation.json` recording `manifest_path`, `sha256`, `git_commit`, `freeze_utc`, `canonicalization`, and `protocol_version`. A digest alone does not prove a pre-outcome freeze: a publicly timestamped immutable commit/run and audit trail are needed.
5. Prior to accessing held-out outcomes, independently verify that the attestation digest matches the committed manifest and that the freeze timestamp predates any confirmatory labels, model outputs used for selection, or policy tuning.
6. Any amendment after freeze requires a new version, documented reason, time, and a declaration whether the subsequent analysis is exploratory. Never overwrite the original attestation.

## Statistical decision specification

For domain `d`, let independent source-family observations be `D_{i,j}=L_{i,baseline}-L_{i,policy_j}`, where `D_{i,j}∈[-B,B]` and the domain-specific family sample size is `n_d`. For `K` precommitted policy–baseline–domain claims, a simultaneous one-sided lower bound is

`LB_{d,j} = mean_i(D_{i,j}) - B * sqrt(2 * log(K/delta) / n_d)`.

This follows from Hoeffding's inequality and a union bound, **not new mathematics**. `K` must include all confirmatory comparisons across all domains if familywise error is controlled globally; it cannot silently reset to the per-domain candidate count. Report `n_d`, `K`, `B`, `delta`, observed means, lower bounds, abstention rates, verification spend, and excluded sources. Reject a confirmatory improvement claim when `LB <= 0`, or any required independence, selection, provenance, licensing, or label-validity condition fails. A positive bound does not establish deployment robustness or novel AI mechanisms.

If loss is bounded in `[0,B]`, then the paired difference indeed lies in `[-B,B]`; if separate losses have different ranges, derive the correct paired range instead of reusing `B` blindly.

## Explicit feasibility and falsification gates

- **Source independence:** items derived from the same original source, solution, prompt template, or benchmark construction process cannot be counted as independent families without justification; audit cross-source leakage and pretraining exposure.
- **Cost matching:** compare abstaining policies to strong risk-control and verifier baselines with the same model calls/tokens or a separately reported normalized cost; superiority that disappears under matching falsifies the primary claim.
- **Cross-domain validity:** require positive domain-specific evidence in NLP, mathematics, and physics before making a cross-domain claim. Physics is physical-reasoning evaluation, not experimental discovery of physical laws.
- **Sampling feasibility:** if independent family counts are too small for nonvacuous bounds, downgrade to a clearly labeled pilot or methods paper rather than claiming certified improvement.
- **Prior-art collision:** distinguish classical simultaneous risk bounds, conformal risk control, selective prediction, and adaptive-data-analysis results from any new empirical contribution; conduct full-text theorem comparisons before a novelty claim.
- **Compute:** do not run inference until a free cloud provider's current quota, availability, billing/card requirements, and hard spend limits have been verified. Do not use the user's laptop for compute. No paid resources may be initiated.

## Evidence and publication status

Existing evidence: [GitHub Actions run 44212661794](https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/44212661794) reports 22 passing targeted deterministic tests, not a full-suite pass. This protocol introduces no new model results or regression passes. November 22 remains a conditional checkpoint. Disclose AI assistance according to the publication venue's rules.
