# Hosted source-partition regression evidence — 2026-11-23

## Verified execution

- Repository: `parthivpatel-patel/frontier-ai-research-2026` (public).
- Workflow: `Archival identification reference checks`.
- Run: https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/45161439267
- Run ID: `45161439267`; job ID: `137647579837`; job: `exact-small-frame`.
- Trigger: push; tested commit: `3af1efb140f87888ff92c2b6ff548e03868a7184`.
- GitHub API reported completed/success; job and its exact-arithmetic/metamorphic step both reported success.
- Downloaded hosted job log explicitly reports `65 passed in 0.52s` for the ten listed pytest modules, including `research/test_paired_archival_source_cluster_oracle.py`.
- Runner checkout log confirms the same commit SHA. The 65 figure is the aggregate suite count, **not** a claim of 65 source-cluster-specific tests.
- This is evidence of executable regression behavior only; it is not an empirical AI benchmark, a proof of the general theorem, or a validation of novelty.

## Scientific release gates still open

1. Independently reconstruct the small-frame oracle with an algorithmically distinct implementation and compare every admissible label assignment, not just interval endpoints.
2. Check source-provenance partition choices are frozen before viewing held-out labels and policy outcomes; predeclare partition sensitivity.
3. Compare against unrestricted missing-label bounds, record-budget relaxation, and established group-robust/partial-identification formulations.
4. Build independently adjudicated, leakage-audited held-out NLP, mathematics and physics tasks. Logical consistency alone cannot certify physical truth.
5. Verify citations against original sources; no novel-theorem, improved-accuracy, or coverage claims until supported by independent evidence.

## Operational limits

The hosted test used GitHub Actions, not the user's laptop. This note authorizes no new compute purchases, GPUs, larger runners, model downloads, or billable services. Confirm zero-cost eligibility and quotas before launching additional cloud experiments.
