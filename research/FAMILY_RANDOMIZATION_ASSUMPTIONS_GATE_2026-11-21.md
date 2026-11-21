# Exact family-level randomization inference: applicability gate (2026-11-21)

Status: proposed analysis protocol; **no experimental results**. This note is not evidence of novelty.

## Problem

Paired question-level permutation tests can be anti-conservative when questions share source documents, generators, or evaluation templates. A family is the unit of dependence. The number of questions is not the effective number of independent replicates.

## Frozen quantities

Before inspecting confirmatory outcomes, record the dataset manifest SHA256, independent family definition, chronological split, predictions, accept/reject decisions, inference code commit, coverage grid, cost accounting, and one primary contrast. Let family j contain n_j questions. For each arm a, define its selective risk R_a = sum_i A_ai E_ai / sum_i A_ai, where A is acceptance and E is a binary adjudicated error. Empty accepted sets are undefined, not zero-risk. Matched coverage must be determined on calibration data; never retune on test labels.

The predeclared contrast is D = R_temporal - R_baseline; negative is favorable. This is an **operational** risk contrast between possibly different accepted sets, not a causal mechanism estimate. Report full-coverage error and intersection-only paired error separately.

## Inference choices and their assumptions

1. **Cluster bootstrap**: resample whole independent source families, retaining all their questions and both arms; recompute the pooled risk ratio and D for every draw. A bootstrap interval is descriptive and may be unreliable with few or highly unequal families. Record failed draws with zero acceptance; do not silently discard them.
2. **Paired family sign-flip randomization**: calculate pre-specified family-level contrasts d_j, such as within-family selective risk differences where both arms have accepted examples. Under the *sharp exchangeability/symmetry null* that swapping arm labels within each family leaves the joint outcome distribution invariant, enumerate 2^K sign patterns for K modest. Two-sided p = count(|T_flip| >= |T_obs|)/2^K with T = mean_j d_j. This is **not** an exact test merely because arms are paired: algorithmic outputs are generally not randomized assignments, and symmetry is an additional unverified assumption. Family exclusions for undefined contrasts must be declared and disclosed.
3. **Sensitivity**: compare equal-family and question-weighted estimands; leave-one-family-out contrasts; coverage gaps and acceptance overlap; the predeclared cost-matched comparison. Do not select the most favorable method after seeing results.

A source-family-aware bootstrap and a sign-flip procedure answer different questions and cannot be swapped opportunistically. If K is small, clusters overlap, or sign-flip exchangeability is implausible, report estimates and uncertainty descriptively, explicitly marking confirmatory inference **not established**.

## Falsification and mechanism limits

Run timestamp-shuffle and irrelevant-chronology controls using the same model, prompt budget, tokens, and decision rule. A similar gain under shuffled timestamps undermines a temporal-evidence explanation. Failure to beat matched-cost retrieval and non-temporal controls undermines incremental utility. A selective-risk gain with unchanged shared-set errors supports selection utility, **not** improved per-question predictive accuracy. None of these experiments alone proves mechanistic mediation.

Mathematics and physics tasks enter the temporal study only when the evidence available to the verifier genuinely changes over time (e.g., dated proof-state revisions or sequential measurements). Timeless theorem statements and physical laws must not be converted into artificial temporal tasks.

## Minimum reproducibility artifact

Publish anonymized family-level aggregates and, where licensing permits, item-level adjudications with source IDs, timestamps, arm outputs, acceptance flags, error labels, token/cost counts, manifest hash, model/version, and immutable code revision. Separate exploratory iterations from the one untouched confirmatory holdout. Disclose all failed and inconclusive comparisons.

## Publication gate

A claim of empirical superiority requires independently adjudicated held-out labels, source-family independence audit, prespecified analysis, matched compute, negative controls, and uncertainty compatible with the stated claim. Otherwise publish as methods/preregistration only. No free GPU inference, zero-card availability, or current cloud quota is asserted by this document. All compute must remain cloud-hosted and verified free before execution.
