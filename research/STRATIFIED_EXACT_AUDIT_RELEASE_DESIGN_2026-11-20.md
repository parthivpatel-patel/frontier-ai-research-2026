# Stratified finite-population audit design: an executable release decision

Status: preregistered design proposal; no empirical model results. 2026-11-20.

## Problem and estimand

For each held-out domain d in {NLP, mathematics, physics}, freeze a verifier and its acceptance threshold **before** looking at correctness labels in that domain. Let N_d be the number of accepted answers, E_d the (unknown) number of incorrect accepted answers, and R_d = E_d/N_d the finite-population accepted-answer error rate. If N_d = 0, reliability is **not evaluable**: report zero coverage, not zero risk.

Randomly sample n_d distinct accepted answers uniformly without replacement. Let X_d be the number of errors found. The design-based distribution is X_d ~ Hypergeometric(N_d,E_d,n_d). This is a statement about random auditing conditional on a fixed population, not a guarantee under future distribution shift.

## Exact one-sided upper confidence bound

For each observed x, define U_d(x) as the largest integer e in {0,...,N_d} for which P_{E=e}(X_d <= x) >= alpha_d, with careful discrete boundary handling. More conservatively use the largest e for which the probability is strictly greater than alpha_d; at equality, either convention must be preregistered and the resulting coverage checked. The exact tail is

P_E(X <= x) = sum_{j=0}^x [C(E,j) C(N-E,n-j) / C(N,n)]

with impossible terms equal to zero. To avoid ambiguity, an implementer may invert the test with rejection only when P_E(X <= x) < alpha_d; the upper set consists of all E not rejected. Verify monotonicity in E and compute using integer combinatorics or stable log-space arithmetic, not naive factorial floating point.

The interval [0,U_d(X_d)/N_d] has at least 1-alpha_d design-based coverage for every fixed E_d. To claim all three domains simultaneously at familywise level 1-alpha, allocate alpha_d = alpha/3 (Bonferroni). This does not assume independence across domains. A pooled aggregate cannot replace these three separate claims.

## Zero-error case and feasibility

When x=0, P_E(X=0) = C(N-E,n)/C(N,n). This is decreasing in E. If the unacceptable rate is r*, define E_bad = ceil(N*r*). A zero-error sample excludes all populations with E >= E_bad at level alpha_d only if

C(N-E_bad,n)/C(N,n) < alpha_d.

This condition can be checked **before** any model inference, using proposed N, n, r* and alpha_d. If it cannot be satisfied within the free-cloud label budget, the study must report an inconclusive certification result, not relax the threshold after inspecting labels.

Illustration, not data: for a large population and a 5% unacceptable error rate, the approximation (0.95)^n < 0.05/3 requires n >= 80 for three simultaneous domains at overall alpha=0.05. This is only an approximation; actual release decisions must use the exact finite-population hypergeometric expression. The audit must independently label at least n accepted answers per domain; a smaller accepted population requires the exact finite-population calculation, potentially a census.

## Bias and leakage controls

- The accepted population must be defined and frozen before audit sampling; no replacement of difficult cases, missing labels, or post-hoc selection.
- Draw indices with a published deterministic pseudorandom seed, retain the manifest, and hide verifier scores and arm assignments from independent adjudicators where feasible.
- Adjudicate mathematical answers by proof or exact check where appropriate; physics by stated units, assumptions and independent solution; NLP by source-grounded rubric and ambiguity flags.
- Treat unresolved adjudications as unknown: report sharp worst-case bounds and a sensitivity analysis. Never count unresolved answers as correct.
- Freeze thresholds using disjoint calibration material; exclude benchmark contamination and near-duplicate source questions.
- Report per-domain acceptance counts, total source counts, audit fractions, error counts, coverage, runtime/compute budget and all exclusions.
- If the audit is inspected repeatedly, fixed-sample confidence intervals cannot be reused at each look without an anytime-valid or alpha-spending design. Prefer one prespecified final inspection.

## Comparator and falsification plan

Compare proposed verifier against confidence-only, random selection, and relevant selective-risk/conformal baselines on the **same questions and underlying generated answers**. Match domain-specific acceptance coverage and account for total verifier inference cost. Evaluate each method's own accepted population; overlap-only comparisons answer a different question. Use paired resampling at the source-question level for estimated risk differences, and disclose when uncertainty is too wide to distinguish methods.

Reject an improvement claim if any domain worsens materially, if the gain disappears under matched acceptance coverage or compute budget, if the source-held-out result fails, or if correctness-label uncertainty reverses the conclusion. A confidence bound that fails to certify is an inconclusive result, not evidence of model failure.

## Scientific novelty boundary

Hypergeometric inversion, stratified auditing, and multiple-testing corrections are established statistical methods. This design contributes methodological rigor, **not** a new mathematical theorem. The project's remaining candidate contribution is a specific verifier mechanism and independently replicated cross-domain evidence beyond selective prediction, conformal risk control and cross-domain uncertainty calibration. No novel mechanism or improvement is asserted here.

## Zero-cost cloud gate

Only standard GitHub-hosted runners for this public repository are candidates for small CPU-only unit tests. Before triggering workflows, verify repository Actions permissions, billing configuration, runner eligibility, quota and the workflow's runner labels. Do not use larger paid runners, hosted GPUs, cloud accounts requiring a card, or local laptop compute. Do not launch model experiments until dataset rights, independent labeling capacity, and zero-cost execution have been verified.

## Release gates

1. A source-specific literature matrix identifies exact prior theorems and methods, not merely titles or abstracts.
2. Code implements the exact hypergeometric tail with exhaustive small-N coverage tests and monotonicity checks.
3. At least one GitHub-hosted **free** CI run verifies the code at its exact published commit.
4. The model, question sources, accepted sets, audit seeds and adjudication protocol are archived reproducibly.
5. Independently adjudicated held-out NLP, mathematics and physics results meet preregistered coverage, risk and cost gates.
6. The paper labels theory, synthetic tests and actual model evidence distinctly and discloses AI assistance as required.

If gates 3–5 are unmet by 2026-11-22, publish a methods/preregistration preprint or defer the discovery paper; do not fabricate results.
