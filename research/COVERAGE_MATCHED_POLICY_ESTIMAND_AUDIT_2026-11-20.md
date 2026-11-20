# Coverage-matched verifier comparison: estimand and selection audit
Date: 2026-11-20
Status: preregistration / analytical note; no empirical results; no novelty claim.

## Why this gate is necessary
Two verifiers can accept different answers even when they accept the same number. Comparing error rates only on the intersection of their accepted sets answers a different question from comparing the operational policies. A model can look superior on the shared subset while making more errors on its unique accepted subset. This note prevents that estimand switch.

## Frozen paired design
For each held-out item i in domain d (NLP, mathematics, physics), freeze the candidate answer, source identifier, independently adjudicated binary error Y_i, verifier scores S_Ai and S_Bi, and predeclared inference-cost measurements. Candidate generation must be identical for both policies. Thresholds are selected on a disjoint calibration split, with prespecified target coverage c_d and a documented tie rule. Evaluation split must not be used to retune thresholds.

Define a_Ai and a_Bi in {0,1} for acceptance. At exact equal realized coverage n_A=n_B=m>0 within a domain, the operational risk contrast is
Delta_d = [sum_i Y_i a_Ai - sum_i Y_i a_Bi]/m
= [sum_{i: A-only} Y_i - sum_{i: B-only} Y_i]/m.
Shared-accepted errors cancel exactly. Thus intersection-only comparison is *incapable* of measuring the policy contrast at matched coverage. This is a finite-sample identity, not an original theorem.

When realized coverages differ, use each policy's own denominator and report coverage difference; do not apply the cancellation identity. Never silently interpolate risk to a coverage value without a preregistered interpolation rule.

## Minimal adversarial example (constructed, not experimental)
Six items, two accepted by each verifier. A accepts items {1,2}; B accepts {1,3}; Y_1=0, Y_2=1, Y_3=0. Shared-accepted risk is zero for both, yet operational accepted-answer risks are R_A=1/2 and R_B=0. This example is synthetic and demonstrates estimand mismatch, not actual verifier performance.

## Statistical analysis
Primary estimand: domain-specific risk difference at calibrated target coverage, with realized coverages and uncertainty displayed. Pairing is by held-out item and frozen candidate answer. Use a preregistered paired bootstrap clustered at source/problem family (not independent answer rows) to reflect dependence. If exact finite-population audits rather than complete labels are used, report the inclusion mechanism and use appropriate design-based inference; never treat partially observed errors as fully labeled. Randomized auditing must cover A-only, B-only, shared-accepted, and rejected-by-both strata with positive known inclusion probabilities for any claimed full-population estimand. Record all strata counts and separately audit rejected answers when claiming missed-correct-answer performance.

## Source shift, physics, and domain integrity
For NLP, stratify by dataset/source and document ambiguity adjudication. For mathematics, require a proof/checker or independent expert adjudication rather than model self-grading alone. For physics, record units, assumptions, numerical tolerances and symbolic equivalence criteria. Hold out source families, not only random items. Domain macro-average is secondary to reporting each domain's risk and coverage; an aggregate gain cannot compensate for a preregistered unacceptable domain-level loss.

## Falsification and release gates
1. If policy rankings change materially when intersection-only evaluation is replaced with full-policy evaluation, retract the intersection-based conclusion.
2. If coverage or computational cost cannot be matched within preregistered tolerances, do not claim equal-budget superiority.
3. If held-out source shifts reverse the effect or any domain fails its risk criterion, disclose and withhold general cross-domain claims.
4. If label adjudication, leakage controls, or audit inclusion probabilities are unavailable, mark conclusions unidentified.
5. If confidence intervals include zero, do not claim demonstrated superiority.
6. If closest prior art already states the same identity or design, cite it; novelty must come from a separately established contribution.

## Prior-art categories requiring full-text comparison
Selective classification and risk-coverage curves; conformal risk control; paired policy evaluation; survey sampling / Horvitz-Thompson auditing; selective prediction under shift. This note supplies an identification safeguard, not a claim to invent any of these fields.

## Zero-cost execution plan (not executed)
Implement deterministic tiny synthetic fixtures and assertions for the cancellation identity and unequal-coverage branch in a standard GitHub-hosted public-repository runner only after checking account billing/Actions eligibility and repository settings. No GPU, paid runner, large model download, laptop computation, or external inference API is necessary for these tests. Independent held-out model experiments are a separate later gate. Verify GitHub policy and account-specific free quota before triggering workflows.

## Publication status
Analytical argument drafted; no cloud run, independent replication, model evaluation, or scientific novelty established. Target date November 22 is a checkpoint, not a guaranteed publication.
