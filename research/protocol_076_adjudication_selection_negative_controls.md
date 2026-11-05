# Protocol 076 — Adjudication-selection negative controls

Date: 2026-11-05. Status: preregistered design; **not executed**. No empirical findings or novelty claim.

## Target estimand and missingness

For claim i, let A_i and B_i be binary acceptance decisions from two frozen verifiers, Y_i be independently determined physical unsafety (1 unsafe), and R_i indicate whether ground truth has been adjudicated. Define the *all-claims* paired unsafe-acceptance difference

D = N^{-1} sum_i (A_i - B_i) Y_i.

Do not substitute the adjudicated-only mean for D. Define d_i=A_i-B_i. Known Y contributions are fixed. For each R_i=0, d_i Y_i ranges over [min(0,d_i),max(0,d_i)]. Hence sharp no-assumption bounds are

L = [sum_{R=1} d_i Y_i + sum_{R=0} min(0,d_i)]/N,
U = [sum_{R=1} d_i Y_i + sum_{R=0} max(0,d_i)]/N.

A strictly safer A (lower unsafe acceptance) is identified only when U<0. If L<=0<=U, the sign is not identified. These are finite-population identification bounds, not confidence intervals. Acceptance coverage must be compared separately and matched using a preregistered threshold selection rule.

## Three deterministic negative controls (synthetic, not physics evidence)

NC1 — Differential missingness: four claims with (A,B,Y,R):
(1,0,1,0), (0,1,1,1), (1,0,0,1), (0,1,0,0).
Both methods accept two claims; true D=0. Adjudicated-only observed difference is -1/2, falsely favoring A. Full-population bounds: L=-1/4, U=+1/4. Expected: no identified winner.

NC2 — Shared unresolved truth: two claims (1,1,unknown,0) and (0,0,unknown,0). Bounds are [0,0] because both paired coefficients vanish. Expected: missing truth does not inflate the paired difference bound.

NC3 — All unadjudicated disagreement: two claims (1,0,unknown,0) and (0,1,unknown,0). Bounds are [-1/2,+1/2]. Expected: do not infer safety improvement from matching coverage alone.

## Executable acceptance criteria

Implement each control in a separate unit test using the production bounds API. Independently enumerate all 2^m assignments of unknown Y to obtain reference extrema; compare exact rational results or use a justified tolerance. Verify NC1's complete-data D and the biased adjudicated-only contrast as a separate diagnostic, without leaking complete-data Y into the bound estimator. Reject duplicate IDs and malformed binary decisions. Run on a verified zero-cost hosted environment only; preserve runner URL, commit SHA, command, test log, and UTC timestamp. No laptop execution.

## Actual physics benchmark protocol

1. Freeze claim text, provenance, model outputs, thresholds and physical assumptions before adjudication.
2. Group by source family, physical subfield, verifier disagreement and difficulty, then sample claims for independent adjudication with a recorded random seed and known nonzero inclusion probabilities.
3. Blind adjudicators to which verifier accepted each claim where practical; preserve derivations, units, boundary conditions, citations, and conflicts. Never use model agreement as physical truth.
4. Report adjudication fractions by verifier decision pair (00,01,10,11), source group, and difficulty. Compare no-assumption bounds with design-based estimates only when inclusion probabilities and adjudication compliance justify them.
5. Compare certificate verifier with direct answer, retrieval-based verification, calibrated abstention, and selective evidence escalation at matched coverage and evidence/compute budget; report all failures and unresolvable cases.
6. Source-disjoint evaluation and an adversarial unit/assumption perturbation suite are mandatory. If independent adjudication or baseline access is missing, report a methods result rather than empirical superiority.

## Falsification and novelty gates

Reject the central superiority claim if the certificate approach fails to improve unsafe acceptance at matched coverage, loses under source-family holdout, cannot survive assumption perturbations, or identification bounds span both signs. Treat partial identification, selective prediction and missing-data correction as established prior art. Audit against recent scientific claim verification and uncertainty-aware retrieval work before claiming a novel combination. Any paper must disclose AI assistance as required by its venue and distinguish synthetic controls from independently adjudicated physics observations.

**Cost guard:** No cloud job authorized by this document. Verify public-repository runner eligibility, account spending limits, and available free minutes before running; never enable billable larger runners or paid APIs.
