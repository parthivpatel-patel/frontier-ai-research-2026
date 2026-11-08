# Protocol 140 — Keyed lineage reference implementation

Date: 2026-11-08. Status: committed code and preregistered tests; **not cloud-executed**.

## Purpose

Protocol 139 showed that equal-length arrays do not establish valid shared-index alignment. This protocol provides a reference implementation that explicitly binds each Boolean acceptance flag to a stable lineage identifier. It rejects mismatched key sets rather than silently zipping arrays. It computes an exact union probability under the **specified** shared-key bootstrap design, not under an unverified production design.

## Assumptions and falsification

Each positive-weight family has the identical key set with at least two distinct keys. Exactly n keys are drawn independently and uniformly with replacement, and the resulting key sequence is reused by every family. Families with zero weight do not enter the union event. The family-specific undefined event occurs when no drawn key is accepted by that family. The inclusion-exclusion calculation is exact rational arithmetic.

The test suite requires 1/4 for aligned two-key acceptance, 1/2 for complementary acceptance, invariance to mapping insertion order, invariance to positive weight rescaling, exclusion of zero-weight families, and fail-closed behavior for mismatched keys and invalid types. These are *analytic expected results*, not test execution outcomes.

A production comparison is valid only after confirming whether sampling reuses actual lineage keys, positional indices, or independent family draws. If it uses another coupling, this reference oracle is not applicable. If keys represent different physical observations across families despite matching strings, the design remains invalid.

## Scientific and operational boundary

This is a software correctness and identifiability check, not a novel probability theorem or evidence of improved AI/ML/NLP/physics reasoning. Execute tests only on confirmed zero-cost cloud infrastructure, after checking account-specific billing and quota. Do not run training, inference, simulations, or large downloads on the user's laptop. Before a paper, independently audit prior work on paired/bootstrap resampling and selective prediction, validate the production contract, and perform real physics-language experiments with baselines and negative controls.
