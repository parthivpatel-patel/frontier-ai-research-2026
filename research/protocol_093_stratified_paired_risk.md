# Protocol 093 — Stratified paired-risk identification and deployment-shift guardrails

Date: 2026-11-06. Status: theoretical extension and preregistration only; no execution or empirical claims.

## Research question

Can a scientific claim verifier maintain low unsafe-acceptance risk across *assumption-sensitive physics families* rather than merely obtain a favorable pooled selective-risk bound? The primary failure mode is Simpson-style aggregation: pooled acceptance can improve while a critical family becomes worse or loses coverage.

## Fixed-stratum identification

Freeze a disjoint partition of the held-out evaluation set into K scientific families before inspecting outcomes: e.g. mechanics, circuit laws, thermodynamics, dimensional analysis, and out-of-model claims. Freeze acceptance vectors a_i,b_i and partial binary unsafe labels y_i (missing or adjudicated). Within each family k, if n_Ak=sum_{i in k} a_i >0 and n_Bk>0, define

D_k = sum_{i in k} (a_i/n_Ak - b_i/n_Bk) y_i.

Let c_ik = a_i/n_Ak - b_i/n_Bk. The sharp identified interval under independently unconstrained missing binary labels is

L_k = sum_{observed i in k} c_ik y_i + sum_{missing i in k} min(0,c_ik);
U_k = sum_{observed i in k} c_ik y_i + sum_{missing i in k} max(0,c_ik).

Proof: the objective is affine and separable in missing binary coordinates, so choosing each coordinate at its minimizing/maximizing endpoint attains the extrema. Runtime O(n+K) arithmetic operations after strata assignment. Exact rational arithmetic is preferred for reference tests.

**Do not silently drop undefined strata:** if either method accepts zero examples in stratum k, D_k is undefined. Report both methods' denominators and coverage; classify that stratum as non-comparable, not a tie or zero risk.

## Fixed deployment mixture

If the target deployment mixture w_k >=0, sum_k w_k=1 is specified *before* outcome inspection, and every stratum is comparable, the standardized difference is D(w)=sum_k w_k D_k, with sharp interval [sum_k w_k L_k, sum_k w_k U_k] when missing labels belong to disjoint strata and have no cross-stratum restrictions. This compares *conditional selective risks standardized by family*, not the pooled selective-risk difference, which weights families by method-dependent acceptance counts.

If the deployment mixture is unknown but belongs to a preregistered simplex set W, compute lower=min_{w in W} sum w_k L_k and upper=max_{w in W} sum w_k U_k. For an unrestricted simplex, this reduces to [min_k L_k,max_k U_k]. For a constrained mixture, use a transparent linear program or exact vertex enumeration on small K. These are partial-identification bounds, not sampling confidence intervals.

## Falsification and anti-gaming gates

1. Compare pooled and stratum-level conclusions. If pooled superiority masks any preregistered safety-critical stratum with U_k >= 0, do not claim universal improvement.
2. Freeze family assignment, acceptance thresholds, mixture weights, and evidence budget before outcome inspection. Report any exploratory changes separately.
3. Include family-specific coverage and non-comparable strata, with no selective omission.
4. Verify small-stratum bounds against exhaustive missing-label enumeration; check identical acceptance decisions imply [0,0].
5. Construct a toy Simpson reversal to test the reporting pipeline, clearly marked synthetic rather than empirical.
6. Include adversarial out-of-scope and contradictory-evidence cases. The classifier's four-way labels must not be silently collapsed into unsafe/safe without an explicit independently adjudicated mapping.
7. Report how many labels remain unadjudicated in each family; if any target-mixture bound includes zero, do not claim established superiority.
8. Do not optimize deployment weights using test labels or model outputs; if weights are estimated, account separately for their uncertainty.

## Novelty boundary and experimental plan

Stratification, standardization, partial identification, and simplex optimization are established statistical ideas. This protocol does **not** establish a novel theorem. A potentially publishable contribution would require a genuinely challenging independently adjudicated NLP-to-physics benchmark, competitive baselines, preregistered assumption shifts, and a verified safety gain at matched coverage and evidence budgets. Search for closest prior art in selective prediction, domain generalization, distributionally robust evaluation, and scientific verification before claiming novelty.

Next implementation: a dependency-free Python reference function that validates disjoint strata, computes exact per-stratum rational intervals, refuses zero-denominator comparisons, and computes fixed-mixture bounds. Tests must cover label conflicts, malformed weights, missing labels, and pooled-versus-standardized disagreement. Execute only on a verified eligible zero-cost cloud runner; record runner, commit, exit status and logs. No laptop computation or paid resources.

Publication gate: no claims of empirical model performance, independent adjudication, or verified execution until evidence exists. Maintain explicit AI-assistance disclosures according to venue policy.
