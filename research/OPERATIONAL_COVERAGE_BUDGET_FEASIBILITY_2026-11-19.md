# Operational coverage and resource parity: feasibility and estimand audit

Date: 2026-11-19. Status: theoretical and design audit; **not** an empirical finding or originality claim.

## The constrained comparison problem

For fixed held-out candidate answers indexed by i=1,...,n, let a_m(i;t_m) be the binary acceptance decision of verifier m under a threshold t_m frozen on calibration data. Define achieved coverage C_m=n^{-1} sum_i a_m(i;t_m), accepted-answer risk R_m=(sum_i a_m(i;t_m) E_i)/(sum_i a_m(i;t_m)) when at least one answer is accepted, and full-roster cost K_m=sum_i k_m(i), including rejected and failed attempts. E_i is the same independently established correctness/error label for both methods.

An operationally comparable pair would satisfy |C_A-C_B| <= delta_C and |K_A-K_B|/max(K_A,K_B) <= delta_K for positive measured costs, with tolerances fixed before evaluation. The existing proposed cost tolerance is delta_K=0.05; **no universal coverage tolerance is established by that choice**. Costs must use the same physical or billable unit, and a zero/zero cost report does not prove equivalent work.

These constraints can be **infeasible** for frozen thresholds. A comparison cannot make them true by selecting favorable held-out thresholds, removing expensive failures, or reweighting held-out items after inspecting labels.

## Elementary infeasibility example (synthetic)

Suppose calibration-frozen verifier A accepts 80 of 100 held-out items at total measured cost 100 units; verifier B accepts 60 at cost 102 units. The measured-cost gap is 2/102 = 1.96%, within the proposed 5% gate. However achieved coverage differs by 20 percentage points. No selective-risk contrast between these two frozen decisions is an equal-coverage comparison, regardless of which method has fewer accepted errors.

Even if both methods accept 80, costs of 100 versus 120 units yield a relative gap of 20/120 = 16.67%, failing the 5% cost gate. Equal coverage alone cannot rescue budget parity. These are arithmetic counterexamples, not measurements of any AI system.

## Distinct estimands that must not be conflated

1. **Deployment estimand:** evaluate each calibration-frozen threshold on the held-out distribution; report achieved coverage, selective risk and full-roster cost. Thresholds must not change after seeing held-out scores, labels or source-family identities.
2. **Retrospective ranking estimand:** at a predeclared k, sort each method's held-out scores and accept exactly k using deterministic ID tie-breaking. This forces equal achieved coverage but is transductive and cannot demonstrate deployment coverage for frozen thresholds. Cost parity still needs independent measurement.
3. **Budgeted prospective policy estimand:** predeclare a resource budget and an execution/stopping policy before observing held-out outcomes. Measure all attempted and unattempted items according to a declared intention-to-evaluate convention; do not quietly change the candidate roster. A budget cap can change coverage and introduce informative missingness.
4. **Verifier-only estimand:** both methods receive identical frozen candidate answers and reference labels. If generation differs, label the result end-to-end system performance instead.

AUC-style summaries over risk–coverage curves are useful secondary descriptive metrics but do not replace an operational threshold and matched-cost claim.

## Required decision table

| Coverage gate | Cost gate | Permissible claim |
| --- | --- | --- |
| Pass | Pass | Descriptive paired risk contrast under the prespecified tolerances; causal or generalization claims still require additional design and inference |
| Pass | Fail | Equal-coverage descriptive comparison only; no cost-matched superiority |
| Fail | Pass | Cost-comparable operational outcomes with unequal coverage; no equal-coverage superiority |
| Fail | Fail | Unmatched operational comparison; do not rank as a fair head-to-head win |
| Undefined (zero acceptance) | Any | Accepted-answer risk undefined; report abstention and costs without imputing zero error |
| Unmeasured/incomparable cost | Any | Resource equivalence unverified, regardless of coverage |

## Falsification and reproducibility checks

- Freeze the roster, source-family split, score orientation, thresholds, primary outcome and both tolerances before test labels are examined.
- Publish numerator/denominator for coverage and risk, and each cost component and unit; include failures and abstentions.
- If achieved coverage matches exactly, reconcile the paired n11/n10/n01/n00 table and verify that the selective-risk difference equals (e10-e01)/(n11+n10).
- Do not treat a retrospective top-k comparison as deployment validation. Report it under a separate heading.
- Report domain/family-level failures and the number of independent discordant source families. With few independent families, refrain from overconfident bootstrap intervals.
- Audit evidence/tool-call budgets separately from wall-clock time, token counts and dollar cost; these are not automatically interchangeable.
- If either constraint fails, report it explicitly; do not silently tune the held-out thresholds to pass.
- Require domain-specialist checks: grounded evidence for NLP, independently verified derivations for mathematics, and stated physical assumptions plus substantive physical correctness for physics.

## Closest methodological precedents and novelty boundary

Risk–coverage and reject-option comparisons are established in selective classification (Geifman and El-Yaniv, 2017; SelectiveNet, 2019). Calibration and exchangeability limitations are central to conformal prediction (Angelopoulos and Bates, 2023; Barber et al., 2023). Process verification for mathematical reasoning is addressed by Lightman et al., 2023. The distinction between fixed-threshold operation and held-out top-k ranking, and the infeasibility examples above, are elementary methodological observations. **Neither is presented as a novel theorem.** Full-text, version-specific and newer-paper comparisons remain necessary before making a publication novelty claim.

## Cloud execution gate and publication status

The pure arithmetic can be reviewed without running model inference. Automated regression tests should run only after confirming repository-specific free GitHub Actions entitlement, usage limits, billing exposure and that no paid runner is selected. Other cloud services require separately verified current free quota and payment/card rules; do not assume they are available. No laptop workload is necessary.

As of this note, there is no claimed held-out model result, independent CI pass, verified cloud quota, or established novelty. The 2026-11-22 checkpoint is conditional; a methods/preregistration paper is the fallback if empirical requirements are unmet.
