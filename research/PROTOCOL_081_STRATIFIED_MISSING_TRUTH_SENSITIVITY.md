# Protocol 081 — Stratified missing-truth sensitivity and nonidentification gate

Date: 2026-11-14. Status: mathematical specification, not executed or empirically validated. No novelty claim.

## Why this is necessary

Protocol 079 correctly obtains sharp unrestricted census bounds, but a pooled bound does not show *where* unresolved scientific truth is concentrated. A proposed cross-domain verifier could appear safer simply because its mathematics or physics claims are more frequently left unresolved. Stratification does not identify those labels, but makes this failure mode visible.

Freeze a finite released-claim census before adjudication. Assign each released claim to exactly one **predeclared** domain (NLP, mathematics, physics) and one provenance-family identifier. For domain d let K_d > 0 be released claims, F_d be resolved false claims, U_d unresolved claims, and T_d the unknown true false count. Without assumptions about missing labels,

F_d <= T_d <= F_d + U_d.

The pooled false-release fraction R = (sum_d T_d)/(sum_d K_d) therefore belongs to the sharp interval

L = (sum_d F_d)/(sum_d K_d), H = (sum_d (F_d+U_d))/(sum_d K_d).

For domain d, the sharp interval is [F_d/K_d, (F_d+U_d)/K_d]. This pooled interval is algebraically identical to Protocol 079's unrestricted interval: stratification alone cannot narrow it. Every endpoint is attainable by completing all unresolved labels as true or false respectively. A domain with K_d=0 has an undefined domain-specific rate; it must not be assigned zero risk.

## Sensitivity analysis, explicitly assumption-dependent

Let q_d be the unknown fraction of unresolved claims that are false in domain d. For 0 <= q_d <= 1, the completed rate is

R(q) = (sum_d (F_d + q_d U_d))/(sum_d K_d).

This is a sensitivity *curve*, not an estimator or confidence interval. If investigators impose externally justified ranges a_d <= q_d <= b_d, the corresponding bounds replace q_d by a_d and b_d; they are conditional on those assumptions, not identified by the observed data. Do not estimate q_d from resolved labels without a missing-at-random assumption and supporting diagnostics. Report the full unrestricted range first.

## Exact synthetic witness (not AI data)

Domain NLP: K=2, F=1, U=0. Mathematics: K=2, F=0, U=2. Physics: K=2, F=1, U=1. Then the unrestricted pooled interval is [2/6, 5/6]. Domain-specific intervals are NLP [1/2,1/2], mathematics [0,1], physics [1/2,1]. If q_math=0 and q_physics=1, R=3/6. If q_math=1 and q_physics=0, R=4/6. Both assignments preserve the same observed records. The example illustrates why reporting only resolved-label error rates can mislead.

## Required falsification tests

1. Exhaustively enumerate all 2^3 completions of the three unresolved labels in the witness; every completion must lie within [2/6,5/6], and both endpoints must be attained.
2. Check that stratified pooled bounds equal unstratified census bounds for every valid partition of the same records.
3. Reject duplicate claim IDs, missing domain assignments, overlapping strata, invalid binary labels, and zero total releases.
4. Confirm that adding an unresolved claim can widen the logical interval, rather than spuriously improve the estimated safety rate.
5. Repeat all reported comparisons with a frozen provenance-family aggregation; document within-family dependence, and do not use independent-claim standard errors.
6. Distinguish released-claim census results from sampled-claim inference. Never label these logical bounds as 95% intervals.
7. Require held-out NLP, mathematics, and physics examples with independent truth adjudication, explicit unresolved-label reasons, and equal verification-cost accounting across baselines.

## Closest prior art and novelty gate

This decomposition is a direct application of established partial-identification reasoning (Manski), not a new theorem. Selective-label/verification-bias research, active testing, selective classification, and conformal risk control are required comparators. A defensible new claim would need an independently verified *incremental* contribution, such as a preregistered provenance-aware allocation policy that reduces worst-case error-bound width at equal adjudication cost, with no loss of coverage under adversarial missingness. This is a hypothesis only; it could fail, and a trivial strategy that merely avoids difficult claims is not an acceptable gain.

## Execution and integrity

No local training, inference, downloads, or simulations on the user's laptop. Before cloud execution verify public-repository standard-runner zero-cost eligibility and repository/account billing restrictions. Keep immutable code revisions, environment details, logs, all negative controls, and a separate disclosure of AI assistance. November 22 is conditional on validated evidence, not a publication guarantee.
