# Protocol 139 — Rectangular relaxation versus coupled uncertainty: exact counterexample and audit gate

Status: mathematical specification only (2026-11-17). No code execution, cloud run, empirical finding, or novelty claim.

## Why Protocol 138 needs a stronger guard

The four-corner method is **exact** for a fixed policy or a policy mixture whose weights are fixed independently of the unknown parameters, when the only uncertain parameters are two conditionally independent feasible coupling coordinates in a full rectangle and the verifier marginals, prevalence, and losses are fixed. It is **not** generally exact for a coupled feasible subset of that rectangle. A maximum over the enclosing rectangle remains a valid *upper bound* on the true worst-case loss (when the rectangle contains the feasible subset), but can be conservative and should not be reported as the attainable worst case.

## Constructive exact-rational witness

Let truth prevalence be 1/2. For both truth states, each verifier has conditional positive probability 1/2. Thus each conditional joint-positive coupling t_y is feasible in [0,1/2]. Restrict the uncertainty set to the **diagonal line segment** t_0=t_1=t, 0<=t<=1/2. This models a common coupling parameter across truth states. Consider a deterministic decision rule that accepts only when (V1,V2)=(1,1); otherwise it abstains. Set false-accept loss to 2, abstention loss to 1, and correct-accept loss to 0. Then:

- Under Y=0, expected loss is 2t + (1-t)*1 = 1+t.
- Under Y=1, expected loss is t*0 + (1-t)*1 = 1-t.
- At prevalence 1/2, expected loss is exactly 1 for **every feasible t**.

However, if an implementation silently replaces the diagonal by the full rectangle [0,1/2]^2, the same policy has risk 1 + (t_0-t_1)/2, with rectangle maximum 5/4 at the infeasible point (t_0,t_1)=(1/2,0). The true worst-case risk is 1. This is a 1/4 absolute overstatement, not a demonstrated benefit of any AI verifier.

This witness uses the four joint cells (t_y,1/2-t_y,1/2-t_y,t_y), which are all nonnegative and sum to 1. It can be verified by symbolic algebra or exact rational enumeration.

## Mandatory acceptance checks

1. Recompute the witness using a separately written enumeration of Y, V1, V2 and the action loss, with fractions rather than floating point.
2. Evaluate both diagonal endpoints and at least three rational interior points; all feasible risks must equal 1.
3. Evaluate all four enclosing-rectangle corners; the maximum must equal 5/4, while the diagonal maximum equals 1.
4. Verify that any algorithm using the enclosing rectangle labels its output a conservative upper bound, not an attained worst-case value.
5. For arbitrary convex polytopes in (t_0,t_1) with fixed marginals/prevalence, maximize affine risk at **actual feasible vertices**, not invented rectangle corners.
6. If prevalence and conditional couplings are jointly uncertain, inspect the product terms prevalence*t_y. Risk is generally multi-affine or bilinear in the chosen parameterization; do not apply a linear-polytope vertex proof without proving the relevant geometry. A safe alternative is to parameterize the full joint distribution of (Y,V1,V2) and optimize linear expected loss over a precisely defined convex uncertainty set of joint distributions.
7. Record uncertainty-set construction and source of constraints before inspecting held-out outcomes; test coverage and calibration of the set itself. An upper bound is not a distribution-free guarantee unless the true deployment distribution lies in the set.

## Implication for the candidate paper

Report both (a) a transparent rectangular robust upper bound and (b) the tighter coupled-set value only when the coupling constraints have independent calibration support. If coupled-set gains vanish with uncertainty-set estimation error, retract any superiority claim. Neither the witness nor vertex maximization is a novel theorem; the contribution, if any, must come from a reproducible, well-calibrated application with held-out source-disjoint NLP, math and physics evaluation.

## Execution and integrity

This document is intentionally not test output. Run the exact-rational checks only on an account-verified zero-charge cloud runner, retaining workflow logs and commit identifiers. No user-laptop workload, paid resource, API charge, or model download is authorized. November 22 remains a conditional checkpoint.
