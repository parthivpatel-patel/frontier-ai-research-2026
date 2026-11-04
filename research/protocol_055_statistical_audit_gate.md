# Protocol 055 — Statistical audit gate before physics benchmarks

Date: 2026-11-04. Status: design and review only; no execution results claimed.

## Objective

Audit the paired source-cluster bootstrap implementation (Protocol 053) and regression tests (Protocol 054) before reporting scientific performance. This protocol does not establish novelty, correctness, or a positive result.

## Mathematical estimands

For held-out claims i=1,...,N, method m, binary acceptance A_im, and adjudicated unsafe indicator U_i (only when independently established), define coverage C_m = sum_i A_im/N and unconditional unsafe acceptance R_m = sum_i A_im U_i/N. Compare paired differences ΔC=C_certificate−C_baseline and ΔR=R_certificate−R_baseline. If U_i is unknown, report the unknown count and bounded ΔR under all feasible assignments rather than silently treating unknown as safe. Conditional error among accepted claims has a zero-denominator undefined case, not an observed zero.

## Required audit cases

1. Identical decisions and identical outcomes yield exactly zero paired point differences, with degenerate bootstrap differences at zero.
2. Whole source clusters, not individual claims, are resampled together, using the same sampled clusters for both methods.
3. A single source cluster or too few independent clusters triggers an explicit insufficient-inference warning; never present a narrow interval as reliable.
4. Large unequal cluster sizes are disclosed; compare cluster-weighted versus claim-weighted estimands as a sensitivity analysis.
5. Validation thresholds are fixed before test evaluation. No test-label-informed tuning, test-set quantile thresholding, or post hoc coverage matching is allowed in prospective claims.
6. Confidence ties are accepted or rejected together under the declared threshold rule. Report realized coverage, not only nominal target.
7. Source leakage is prevented across train, validation, and test, including paraphrases, template families, and derived simulations.
8. Source-cluster bootstrap intervals are percentile descriptive intervals; with few clusters, extreme imbalance, or rare unsafe events, coverage can be poor. Report cluster counts and run leave-one-source-out sensitivity.
9. Bootstrap randomness must use an explicit seed and recorded code revision. A stable seed establishes reproducibility, not validity.
10. Independent physical adjudicators must be blinded to model identity where feasible; mathematical consistency and empirical physical fidelity are separate labels.

## Falsification gate

The central hypothesis fails to gain support if certificate verification does not reduce unsafe acceptance relative to competitive baselines under prespecified evaluation, or if any improvement disappears after accounting for abstention, source-level dependence, adjudication uncertainty, or assumption misspecification. Do not claim a novel algorithm solely from combining known verification, calibration, and selective-prediction components.

## Prior-art audit queue (not a completed systematic review)

Review and cite primary sources before writing novelty claims: counterexample-guided abstraction refinement (Clarke et al., 2000); selective classification and risk-coverage evaluation (Geifman & El-Yaniv, 2017); conformal risk control (Angelopoulos et al., 2024); formal-language translation and theorem-proving benchmarks; physics-informed machine learning and scientific consistency checks. For each, document precise overlap, differences, assumptions, and a baseline that could falsify the proposed advantage. Bibliographic details and current 2026 follow-up work require independent verification.

## Zero-cost execution gate

Do not launch any cloud workflow until repository visibility, runner eligibility, account billing/spending settings, minute and storage quota, and current policy are verified for the actual account. A public repository alone does not prove an individual run is cost-free. No paid upgrades, card registration, hosted inference, or laptop compute. If verification cannot be completed, retain the tests as unexecuted.

## Required evidence for next milestone

Archive exact commit SHA, workflow URL, runner OS, Python version, command, exit code, complete test output, and artifacts. Separate authored tests from passed tests, synthetic controls from empirical physics benchmarks, and retrospective analysis from prospective deployment evaluation.

Publication target November 22, 2026 is conditional on independent evidence; release a limitations-first technical report instead of a positive-results paper if the hypothesis fails.
