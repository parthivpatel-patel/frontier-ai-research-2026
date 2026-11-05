# Protocol 068 — Adjudication selection and the coverage denominator

Status: preregistered methodological analysis, **not an empirical finding**. Date: 2026-11-04.

## Problem

A verifier can appear safe if its accepted claims are more likely to receive independent adjudication than its rejected claims. Conversely, restricting evaluation to adjudicated claims can invert a comparison between two verifiers. The physics pilot must not condition its primary denominator on post-decision adjudication availability.

Let each eligible, source-disjoint claim i have fixed candidate decisions A_i and B_i in {0,1} (1 means accept), truth T_i in {0,1} (1 means physically incorrect), and independent adjudication indicator R_i in {0,1}. An unknown truth is not assumed correct or incorrect. Freeze the complete eligible cohort before reviewing decisions or labels. The primary unsafe-acceptance rate for method M is U_M = n^{-1} sum_i M_i T_i; its acceptance coverage is C_M = n^{-1} sum_i M_i. The conditional risk among accepted claims is U_M / C_M when C_M > 0. Report both; conditional risk alone hides reject-all behavior.

## Deterministic partial-identification interval

For a fixed method M, define K_M = sum_{i:R_i=1} M_i T_i and Q_M = sum_{i:R_i=0} M_i. With no assumptions on missing truth, the **sharp finite-cohort interval** for U_M is [K_M/n, (K_M+Q_M)/n]. This is an identification interval, not a confidence interval.

For the paired difference D = U_A - U_B, let d_i=A_i-B_i. The observed contribution is S=sum_{i:R_i=1} d_i T_i. The sharp lower bound is (S + sum_{i:R_i=0} min(0,d_i))/n and upper bound is (S + sum_{i:R_i=0} max(0,d_i))/n. These paired bounds preserve the same unknown truth across both methods; subtracting two marginal intervals generally produces unnecessarily loose bounds.

For conditional accepted-claim risk, divide the method-specific bounds by its fixed number of accepted claims, **not** by the number of adjudicated accepted claims. If coverage is zero, conditional risk is undefined, not zero.

## Preregistered stress tests

1. Report missing-label fractions separately for accepted/rejected claims and by method, domain, source family and difficulty. These are descriptive diagnostics; they do not establish missing-at-random.
2. Construct a deliberate missing-not-at-random negative control: remove adjudication preferentially for accepted incorrect claims in synthetic data. An analysis using only adjudicated claims should be flagged as biased; the full-cohort bounds must still contain the known synthetic truth.
3. Construct a paired discordance case: A accepts, B rejects, truth unknown. The difference interval must include both 0 and 1/n, not a point estimate.
4. Freeze decisions, thresholds, inclusion criteria and source-family grouping before any test-label adjudication. Record reviewer independence, evidence source, disagreements and unresolved cases. Never promote placeholder reviewer names into verified independent adjudication.
5. Compare methods at equal **full-cohort** acceptance coverage. Where exact equality is impossible, report the prespecified coverage tolerance and the complete risk-coverage curve; never tune thresholds on the held-out test set.
6. Report cluster-aware uncertainty separately from identification bounds. Cluster bootstrap resampling cannot resolve missing physical truth; confidence intervals must not be mislabeled as sharp identification intervals.

## Falsification and publication decision

A strict safety improvement is not identified if the paired difference interval contains zero. Even if it excludes zero, independent source-family adjudication, physical-assumption validity, matched coverage and uncertainty assessment are still required before any performance claim. If unknown-truth prevalence makes intervals too wide, report **inconclusive**, not a favorable point estimate. Publish a methods/preregistration report rather than a performance paper if these gates remain unmet by November 22.

## Related work and novelty boundary

Selective classification and risk-coverage curves, conformal risk control, partial identification with missing outcomes, and selective labels are established ideas. This protocol makes no claim that the bounds are new. A potential contribution must be demonstrated in independently verified, assumption-explicit physical claims and compared with existing verifiers; software admission tests are not evidence of such a contribution.

## Reproducibility and compute

This protocol requires no model calls or GPU work. Any future execution must use a standard public-repository GitHub-hosted runner only after confirming repository-specific billing and available free quota; do not trigger paid or larger runners. Preserve exact commit, workflow run URL, raw outputs and checksums. No laptop execution is authorized.
