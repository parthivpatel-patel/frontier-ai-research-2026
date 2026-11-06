# Protocol 089 — Identifiability of scientific-verification risk under selective adjudication

Date: 2026-11-05
Status: preregistered analysis plan; no empirical results claimed.

## Research question

Does assumption-explicit verification lower unsafe acceptance relative to strong baselines at equal acceptance coverage, evidence access, and evaluation cost? This protocol addresses a measurement problem that can invalidate an apparent gain: independently adjudicated scientific truth may be unavailable for a nonrandom subset of examples.

## Definitions

For each held-out claim i, define a fixed reference truth Y_i in {supported, refuted, underdetermined, outside_scope}; reserve conflict as a data-quality quarantine state, not a fifth truth label. Let A_i(m,t) be acceptance by method m at threshold t, with a preregistered policy defining exactly which outputs count as acceptance. Let U_i=1 if accepting the claim is unsafe according to the adjudicated reference and U_i=0 otherwise. Let R_i=1 if an independent reference adjudication is available.

At a fixed acceptance coverage c, the target is selective risk

  rho_m(c) = E[U_i A_i(m,t_m(c))] / E[A_i(m,t_m(c))],

where thresholds are selected on validation data only and frozen before the held-out test. Compare Delta(c)=rho_proposed(c)-rho_baseline(c). Lower is better.

## Partial-identification bound (no missing-at-random assumption)

For a fixed method and frozen threshold, let N_A be the number of accepted test claims, K the accepted claims with independently observed truth, H the observed unsafe accepted claims, and M=N_A-K. Without assumptions on the missing labels,

  H/N_A <= rho_m <= (H+M)/N_A

for N_A>0. The lower bound assumes all missing accepted claims are safe; the upper assumes all are unsafe. These are worst-case finite-sample identification bounds, not confidence intervals. If N_A=0, risk is undefined and must not be reported as zero.

For a difference between methods, a conservative interval is

  [L_proposed-U_baseline, U_proposed-L_baseline].

Because the same cases may be accepted by both methods, this interval need not be sharp. Claim superiority without missing-label assumptions only if its upper endpoint is strictly below zero; otherwise report inconclusive. A sensitivity analysis may posit bounded differences in missing-versus-observed unsafe rates, but must state assumptions and cannot replace the assumption-free result.

## Worked arithmetic example (illustrative only)

Suppose 100 accepted claims, 70 adjudicated, 7 observed unsafe, 30 unadjudicated. Then the unsafe-acceptance risk is bounded by [0.07,0.37]. Reporting 7/70=0.10 as the overall risk assumes selection into adjudication is ignorable and is not justified by these counts alone. These are invented pedagogical numbers, not study observations.

## Experimental safeguards

1. Freeze datasets, provenance hashes, adjudication rubric, accepted-output policy, and method thresholds before held-out evaluation.
2. Separate training, prompt development, validation, and test by source family and near-duplicate semantic clusters; document potential benchmark contamination.
3. Record refusal, abstention, out-of-scope, conflict, and malformed outputs separately; never count an unadjudicated label as safe.
4. Compare equation-only checks, retrieval plus citation checks, strong LLM judges where legitimately available at zero cost, and assumption-aware certificates using identical evidence budgets.
5. Report acceptance coverage, selective risk bounds, stratified physical-domain errors, calibration where meaningful, and computational/evidence cost. Bootstrap at source-family or claim-cluster level, not by individual paraphrases.
6. Include adversarial tests for false assumptions, correct algebra with wrong units, inconsistent measurements, evidence omission, misleading citations, and counterfactual changes that preserve the conclusion.
7. Disclose all adjudicator disagreements and escalation rules. No candidate fixtures are promoted to ground truth solely because deterministic arithmetic tests pass.
8. Maintain an experiment ledger with date, code commit, environment, dataset hash, run command, cost verification, and immutable raw outputs.

## Falsification and publication gate

The proposed approach fails its primary claim if it does not lower unsafe-acceptance risk against the strongest feasible baseline at matched coverage; if the gain disappears under source-family separation; if independent adjudicators cannot reliably distinguish categories; or if partial-identification bounds cannot establish direction. A null result remains publishable if the design is sound, but must not be marketed as a verified improvement.

## Novelty positioning

The combination of symbolic checking, scientific QA, assumption verification, selective prediction, and partial identification is not itself established as novel. Novelty requires a documented comparison with prior work (including SCI-Verifier, TPBench, ABench-Physics, selective prediction, and partial-identification literature), precise differentiating claims, and experimental evidence. Bibliographic metadata and priority claims must be verified against primary sources before manuscript submission.

## Execution and financial safety

This file is a specification only. No local model inference, training, large downloads, or laptop simulation is required. Do not trigger cloud jobs until the exact repository/account GitHub Actions entitlement, usage and billing settings, and potential charges are verified. Do not assume that public-repository hosted runners are available or cost-free for this account. If free eligibility cannot be confirmed, leave execution pending and preserve the zero-dollar constraint.

## Reproducibility acceptance checks (to implement)

- Given (N_A,K,H)=(100,70,7), assert bounds equal (0.07,0.37).
- Reject K>N_A, H>K, negative counts, and N_A=0 as undefined.
- For zero missing labels, both endpoints equal H/N_A.
- For no adjudicated labels, bounds equal [0,1].
- Verify conservative difference interval endpoints and the strict-upper-bound superiority rule.
- Verify validation-only threshold selection and deterministic tie handling.

This document does not report a completed experiment, validated novelty, or independently adjudicated physics benchmark.
