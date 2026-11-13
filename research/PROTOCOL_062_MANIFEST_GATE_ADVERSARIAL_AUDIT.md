# Protocol 062 — Manifest gate adversarial audit and estimand integrity

Status: DESIGN REVIEW ONLY — 2026-11-13. No experiments, cloud execution, or novelty claim.

## Scope and verified observation

This review examines `research/manifests/evaluation_manifest_v0_1_DRAFT.json` and `research/fixtures/test_evaluation_manifest_gate.py` as retrieved from the public repository on 2026-11-13. The existing gate appropriately blocks the current draft. However, passing its checks is **not sufficient** to establish experimental readiness or reproducibility.

## Specific gaps and adversarial controls

1. **Hash-shaped strings are not provenance verification.** The gate accepts any lowercase 64-hex-character string. It does not open referenced artifacts, recompute SHA-256, or prove that calibration and test family IDs are disjoint. Negative control: provide plausible-looking hashes for nonexistent artifacts; a complete gate must reject them.
2. **Declared disjointness is not independently checked.** `family_disjoint_verified: true` is accepted without loading family assignments. Negative control: duplicate one provenance-family identifier across calibration and test while setting the flag true; reject.
3. **Freeze metadata are not mutually bound.** A syntactically valid 40-hex commit and timestamp do not prove that the frozen manifest matches the referenced commit. Negative control: alter one experimental setting after freeze without changing the alleged commit; reject.
4. **The audit budget may be zero.** The current integer condition permits `audit_budget: 0`, although estimating false acceptance from newly audited labels may be impossible without a separately justified complete-label source. Require a positive budget or a formally documented alternative identifiability argument.
5. **Coverage and tolerance are not jointly validated.** Each is checked separately to lie in (0,1), but the gate does not define whether tolerance is absolute or relative, nor enforce feasible intervals. Specify the exact coverage acceptance rule before looking at test outcomes.
6. **Statistical methods can be placeholders.** Nonempty strings for family-cluster uncertainty, missing-label policy, and multiplicity control are not a machine-checkable statistical plan. Require enumerated method identifiers, versions, parameters, and an explicit rejection criterion.
7. **Boolean authorization is not an account-level billing attestation.** `cloud_execution_authorized: true` is insufficient without dated, attributable evidence of the repository's Actions settings, runner class, account billing limits, and storage exposure. Do not run jobs based on a manifest flag alone.
8. **The primary endpoint can be undefined.** `false_acceptance_among_released_at_fixed_coverage` needs a prespecified rule for zero released claims, unresolved truth labels, family weights, and the distinction between population and audited-sample estimands.

## Proposed acceptance contract

Before any held-out evaluation, create immutable content-addressed artifacts for population, source corpus, family mapping, splits, baseline, model/prompt versions, sampling design, and analysis code. Recompute all hashes; verify family disjointness from records, not flags; enforce independent calibration; bind the freeze to a specific Git commit and manifest digest. Specify sampling inclusion and joint-inclusion probabilities, identifiability conditions, uncertainty intervals, zero-release policy, coverage tolerance, audit budget, and multiple-testing correction. The publication gate must separately evaluate scientific novelty, empirical falsification, and disclosure.

## Predeclared falsification

Reject an apparent improvement if it disappears under matched audit budget and matched release coverage, if a family-disjoint held-out test fails, if uncertainty intervals under-cover under the prespecified sampling design, or if the result depends on post-hoc threshold selection. Do not describe this gate hardening as a new theorem.

## Literature connections (prior art, not novelty)

- Horvitz and Thompson (1952), generalization of sampling without replacement: inverse-probability estimation.
- Aronow and Samii (2013), conservative variance estimation for sampling designs with zero pairwise inclusion probabilities.
- Geifman and El-Yaniv (2017), selective classification for deep neural networks.
- Angelopoulos and Bates (2023), conformal prediction tutorial: distributional and coverage assumptions.

These are comparison anchors; a systematic, current literature search and closest-method reproduction remain outstanding.

## Resource boundary

No code execution was undertaken for this review. No local training/inference, no cloud jobs, no API charges. GitHub-hosted runner use remains blocked until account-specific $0 eligibility and billing/card/storage safeguards are verified. The November 22 target is conditional, not a deadline that overrides scientific integrity.
