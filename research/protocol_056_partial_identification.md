# Protocol 056 — Partial identification under unknown physical truth

Date: 2026-11-04. Status: methodological audit, not an empirical finding.

## Identified defect in interpretation

The existing `research/paired_cluster_bootstrap.py` reports `unsafe_acceptance_known` using only adjudicated examples. This is a complete-case estimand, **not** the unconditional probability of accepting an unsafe claim in the full held-out population unless missingness assumptions hold. Physical truth may be unresolved precisely for the most difficult claims. The estimator can therefore reverse the apparent ranking of two methods.

Do not label `unsafe_acceptance_known` as full-population unsafe acceptance in the manuscript. Do not assume missing at random without an explicit, testable sensitivity model.

## Sharp finite-sample bounds (no missingness assumptions)

For method m let N be all held-out claims, U_m the count of *known unsafe and accepted* claims, and Q_m the count of *unknown-truth and accepted* claims. Its full-population unsafe acceptance rate R_m satisfies

    U_m/N <= R_m <= (U_m+Q_m)/N.

These bounds are sharp when unresolved truth can independently be safe or unsafe. For the **paired difference** D = R_certificate - R_baseline, tighter sharp bounds account for shared unknown claims. Let c_i and b_i be binary acceptance decisions on unknown-truth claim i, and d_i=c_i-b_i. Let K=sum_known truth_i*(c_i-b_i). Then

    [K + sum_unknown min(0,d_i)]/N <= D
      <= [K + sum_unknown max(0,d_i)]/N.

The shared unknown truth variable must be assigned consistently across methods; subtracting marginal upper and lower bounds generally produces unnecessarily wide intervals.

Coverage A_m/N is fully observed if decisions are observed, regardless of truth. Conditional unsafe risk among all accepted examples has bounds U_m/A_m to (U_m+Q_m)/A_m when A_m>0, and is undefined for A_m=0. These are identification bounds, **not confidence intervals**.

## Worked synthetic counterexample (not research evidence)

Ten claims; eight known, two unknown. Both systems accept five. On known claims, certificate accepts zero unsafe and baseline accepts one unsafe. Of the two unknown claims, certificate alone accepts one, baseline alone accepts the other. Then the known-label point comparison favors certificate by 0.1 per claim, but the sharp full-population difference spans -0.2 to 0.0. No superiority claim follows without adjudication or assumptions.

## Required experiment changes

1. Report N, number unknown, unknown accepted by each method, and discordant acceptance counts among unknowns.
2. Report the sharp bounds for each method and the paired difference alongside complete-case estimates and clustered uncertainty.
3. Obtain blinded adjudication of unresolved examples where possible; record unresolved reasons and adjudicator disagreement.
4. Stress-test missing-not-at-random scenarios by physics domain, source, and claim difficulty.
5. If paired difference bounds include zero, do not claim superiority on full-population unsafe acceptance, even when complete-case bootstrap intervals exclude zero.
6. Freeze thresholds on source-disjoint validation examples before any held-out evaluation; preserve original artifacts and random seeds.
7. Bootstrap identification-bound endpoints by independent source cluster for sampling uncertainty, clearly distinguishing confidence bands for bounds from the bounds themselves. With few independent clusters, mark intervals exploratory.

## Falsification gate

Reject the safety-superiority claim if the favorable result disappears under plausible unresolved-truth assignments, if coverage differences explain the effect, if source-disjoint replication fails, or if certificate validity relies on incorrect physical assumptions. No claim of novelty is established by these bounds: partial identification and missing-data sensitivity analysis are established statistical ideas.

## Prior-art anchors for audit

- Manski, *Nonparametric Bounds on Treatment Effects*, American Economic Review (1990): https://www.jstor.org/stable/2006592
- Little and Rubin, *Statistical Analysis with Missing Data* (2002), missingness mechanisms.
- Geifman and El-Yaniv, *Selective Classification for Deep Neural Networks* (NeurIPS 2017): https://arxiv.org/abs/1705.08500
- Angelopoulos and Bates, *A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification* (2021): https://arxiv.org/abs/2107.07511

These are relevant conceptual anchors, not a completed exhaustive literature review. Independently verify citations and more recent work before a novelty claim.

## Execution and cost

This is a paper-and-code audit only. No training, inference, simulation, laptop workload, or paid compute is authorized. Any future cloud execution requires verified account-specific no-charge eligibility and billing controls.
