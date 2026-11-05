# Protocol 074 — Adjudication-selection stress test (preregistered design)

Status: methodological design only. No model runs, benchmark measurements, or novelty claim.

## Problem

A scientific verifier can appear to reduce false acceptance when adjudication is preferentially available for easy, short, or already accepted claims. Let A and B denote binary acceptance decisions, Y=1 denote a physically false claim, and R=1 denote an independently adjudicated truth label. The desired population contrast is E[(A-B)Y], **not** E[(A-B)Y | R=1]. The latter is generally biased if R depends on claim difficulty, verifier decisions, or physical truth.

## Constructive counterexample

Consider 100 claims. Both verifiers accept 50. On 20 independently adjudicated claims, A accepts 2 false claims and B accepts 8 false claims. On the remaining 80 unadjudicated claims, A and B can have the opposite ordering. Thus the adjudicated-only ranking does not identify the population ranking. Do not assign truth labels to these 80 claims when reporting actual data.

## Prespecified evaluation

1. Freeze claim IDs, source-family IDs, physics domain, difficulty strata, acceptance decisions and the adjudication plan **before** inspecting verifier performance.
2. Adjudicate a random sample within prespecified strata, including accepted and rejected claims from both verifiers. Record the sampling probability for every stratum. Adjudicators must be blinded to the verifier identity and decision where feasible.
3. Report all-claim sharp paired bounds: for known Y use (A-B)Y; for missing Y use min(0,A-B) and max(0,A-B), summed and divided by N. These are finite-sample logical bounds, not confidence intervals.
4. As a sensitivity analysis only, if the sampling design makes inclusion probabilities known and positive, compute inverse-probability-weighted estimates and design-based uncertainty. Never substitute weighting for sharp bounds without checking the missingness assumptions.
5. Run a deliberate selection-bias negative control: retain adjudicated records disproportionately from claims where A and B disagree, then from cases favoring A, then from cases favoring B. The adjudicated-only estimator should move; the complete-data oracle (in synthetic tests) should not.
6. Evaluate at matched acceptance coverage using a frozen calibration set. Show both unconditional unsafe acceptance per claim and unsafe fraction among accepted claims; never confuse these denominators.
7. Cluster resampling by original source family (and, where possible, problem template), not by duplicated paraphrase. Keep train/calibration/test source families disjoint.
8. Report missing-truth fraction overall and by A/B acceptance pattern, source family, domain, difficulty, and adjudicator. Include adjudicator disagreement and unresolved outcomes.
9. Publish the decision rule in advance: claim superiority only if the uncertainty analysis and the sharp identification interval jointly support the claimed direction under the prespecified assumptions. Otherwise report *not identified*.

## Falsification gates

- The advantage reverses under source-family-disjoint testing or matched coverage.
- Bounds include both positive and negative contrasts, making the sign unidentified.
- The adjudication procedure is not independent of the system under test, or evidence provenance cannot be audited.
- A strong baseline matches or exceeds performance within the uncertainty interval.
- A result depends on post-hoc exclusion of unresolved physical claims.

## Closest established methods to credit

- Manski, *Nonparametric Bounds on Treatment Effects*, American Economic Review (1990): partial identification rather than imputing unknown outcomes.
- Little and Rubin, *Statistical Analysis with Missing Data*: missing-data mechanisms and assumptions.
- Geifman and El-Yaniv, *Selective Classification for Deep Neural Networks* (NeurIPS 2017): risk/coverage tradeoffs.
- Angelopoulos and Bates, *A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification* (2023): uncertainty and coverage guarantees, not physics ground truth.

These references are methodological anchors, not an exhaustive or current novelty search. Verify bibliographic metadata and survey contemporary scientific verification / process-reward / theorem-proving literature before asserting novelty.

## Cloud and integrity gate

No workflow may be launched until the account-specific GitHub Actions allowance, billing controls, and runner eligibility are checked and the action is guaranteed to remain within the user's strict $0 limit. No local laptop computation, paid API, GPU inference, or synthetic result passed off as empirical evidence is authorized.

## Deliverable status

This file preregisters a bias stress test. It does not demonstrate that the proposed verifier works or that a new scientific contribution exists.
