# Confirmatory power and identifiability preflight (2026-11-21)

Status: methodological preflight, **not** an experimental result or novelty claim.

## Why this gate is necessary
A matched-coverage comparison can be precisely calculated yet scientifically inconclusive when the independent units are source families rather than individual questions. Increasing questions per family cannot substitute for independent families when within-family correlation is substantial. Likewise, the observed selective-risk contrast may reflect a different acceptance set, not improved predictions on the same accepted items.

## Fixed estimand and decomposition
For verifier v in {T,B}, let a_vi in {0,1} be acceptance, e_vi in {0,1} be error, and n be the number of held-out items. At equal positive coverage c, R_v = (sum_i a_vi e_vi)/(nc). Define d_i = a_Ti e_Ti - a_Bi e_Bi. Then

    Delta = R_T - R_B = sum_i d_i/(nc).

For the shared accepted set S, T-only accepted set U, and B-only accepted set V:

    nc Delta = sum_{i in S}(e_Ti-e_Bi) + sum_{i in U}e_Ti - sum_{i in V}e_Bi.

This is an exact accounting identity, not causal mediation. If empirical coverage is not exactly equal, report each verifier's own denominator; do not apply this decomposition with a common denominator. Report sizes of S,U,V, error totals and full-coverage paired accuracy alongside Delta.

## Independent-unit uncertainty
Define family contributions D_g = sum_{i in family g} d_i, and family sizes n_g. A family-cluster bootstrap resamples **entire families jointly across both verifiers**, recomputes coverage and risk, and preserves the matched comparison. For unequal family sizes, report both question-weighted and equal-family estimands; never silently switch between them. A bootstrap CI with very few independent families is not reliable merely because item count is large. Predeclare a minimum number of families, or label inference exploratory and withhold a confirmatory claim.

As a rough planning diagnostic only, under exchangeable intraclass correlation rho and average m items per family, the design effect is 1+(m-1)rho and effective sample size approximately n/[1+(m-1)rho]. This approximation is not a substitute for family-level power simulation or a guarantee of validity.

## Cloud-only preflight, before inference
1. Freeze data manifest, labels, provenance, domain definitions, source-family keys, predictions, acceptance scores, thresholds, cost accounting and code hashes before the final holdout is inspected.
2. On a verified no-charge public-repository GitHub Actions runner, execute small synthetic fixtures only to verify the identity above, zero coverage behavior, family-resampling logic and unequal-family-size reporting. Do not use synthetic results as empirical evidence.
3. Estimate power using *calibration or pilot families only*, not the confirmatory holdout. Predeclare the smallest effect worth detecting, family count, heterogeneity assumptions, alpha and multiplicity policy. If power is insufficient, mark the planned empirical study inconclusive rather than relaxing thresholds post hoc.
4. Confirm zero-dollar runner eligibility, repository Actions settings and any billing/account restrictions immediately before running; never enable paid runners, credits or cloud services without approval.
5. If no independently adjudicated held-out labels and admissible free inference are available, release a preregistration/methods artifact, not a discovery paper.

## Negative controls and failure conditions
- Timestamp shuffle preserves source content and model budget but destroys meaningful chronology. A similar gain under shuffle undermines a chronology-specific explanation.
- Placebo evidence with non-informative dates tests whether metadata or formatting drives apparent improvements.
- Report matched-cost and no-temporal-evidence baselines. Any extra retrieval or verifier calls must count toward the budget.
- Reject a chronology-specific claim if gains are confined to timeless mathematics or physical laws whose truth does not vary with date.
- If improvement disappears under family-level uncertainty, leave-one-family-out checks, or multiplicity correction, report inconclusive evidence.
- If selective risk improves only through acceptance-set changes, report that operational gain separately from paired prediction improvement.

## Literature collision check still required
Compare explicitly against selective classification/risk-coverage evaluation, conformal risk control, adaptive holdout reuse, temporal fact verification, and verifier calibration. The decomposition above is elementary algebra and is **not claimed as novel**. A potential contribution requires an independently demonstrated effect or a rigorously differentiated protocol that prior art does not already provide.

## Publication gate
No new model outputs, labels, empirical gains, cloud quota verification or completed systematic novelty review are asserted by this document. The November 22 target is a checkpoint, not a reason to waive evidence standards.
