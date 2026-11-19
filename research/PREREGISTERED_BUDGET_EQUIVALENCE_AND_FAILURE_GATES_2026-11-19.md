# Preregistered verification-budget equivalence and failure gates (2026-11-19)

Status: prospective methodological contract; **not** a result, validated novelty claim, or evidence that a model has been evaluated.

## Motivation and estimand

The existing `audit_verification_costs` reports observed costs on a complete held-out roster, including abstentions and failed verifications. That is necessary but not sufficient for a matched-budget comparison. A verifier can have the same total cost as a competitor while allocating work very differently across questions or source families.

For fixed held-out items `i=1,...,N`, candidate answers and binary correctness labels `Y_i`, define method-specific frozen acceptance decisions `A_im` and measured costs `C_im >= 0`. Report:

- Achieved coverage `q_m = sum_i A_im / N`.
- Selective error `r_m = sum_i A_im (1-Y_i) / sum_i A_im`, undefined if the denominator is zero.
- Full-roster cost `B_m = sum_i C_im`, **including** failed verification and abstention.
- Family-specific coverage and selective error, retaining undefined denominators.
- The paired descriptive risk contrast `r_A-r_B` **only with both achieved coverages displayed**. At different coverages this contrast does not isolate verifier quality.

All comparisons use identical held-out candidate answers, correctness adjudications and item identifiers. Methods that regenerate candidate answers belong to a separate end-to-end-system experiment.

## Freeze before held-out evaluation

1. Fix dataset provenance, source-family partition, duplicate-detection rule, correctness adjudication protocol and question roster.
2. Freeze each verifier's prompt, tools, acceptance score, thresholds, retry cap, timeout, model version and all fallback behavior using development/calibration families only.
3. Freeze a single primary resource unit, measurement procedure, hardware class and cost tolerance. CPU-seconds, tokens, elapsed seconds and money are **not interchangeable**; record additional units separately.
4. For a proposed prospective primary equivalence rule, require `abs(B_A-B_B)/max(B_A,B_B) <= 0.05` when `max(B_A,B_B)>0`; both zero totals qualify as equal-cost only when the measured protocol actually incurred no verification work. The 5% threshold is a **proposed design choice**, not a retrospectively selected threshold or an established community standard.
5. Predefine a minimum achieved coverage (proposed 0.20 for a feasibility pilot), target coverage(s), a source-family resampling plan, and the number of planned primary comparisons. Freeze these choices before looking at held-out labels.
6. Any missing cost entry, unit mismatch, budget overrun, unequal candidate roster, or outcome-informed threshold change disqualifies a confirmatory claim. Retain results as exploratory with the failure recorded.

## Inference and falsification

Use paired source-family-cluster bootstrap resampling when sufficient independent families exist; do not bootstrap questions as if within-family observations were independent. If too few families are available for reliable clustered inference, report descriptive estimates and sensitivity analyses without a nominal confirmatory confidence interval. Report confidence intervals for both risk and coverage differences, family-wise diagnostics, and multiplicity adjustment for prespecified primary comparisons.

Falsify a claimed general cross-domain advantage when any of the following applies: the effect reverses under an appropriate matched-budget baseline; the advantage vanishes after leakage-safe source-family splitting; accepted-answer error is reduced only by material loss of achieved coverage; a purported physical check accepts dimensionally valid but physically false assertions; a mathematical verifier accepts invalid derivations solely because final answers match; an NLP verifier accepts unsupported fluent claims; or provenance and costs cannot be independently reproduced. A null or negative result must be reported, not hidden.

## Feasibility and publication gate

Run synthetic tests on a verified free public-repository CI runner first. Before *any* cloud inference or new experiment, independently confirm account-specific quota, card/billing prerequisites, job limits and cost controls. Do not use the user's laptop for training, inference, downloads or simulations. Do not assume GitHub Actions provides a free GPU or that a public repository automatically guarantees eligibility for every runner.

By the conditional November 22 checkpoint, a methods-only artifact may be released with transparent limitations; a paper claiming an empirical verifier improvement requires independent held-out measurements, prior-art comparisons, executable tests, uncertainty analysis and full disclosure of AI assistance as required by the publication venue. Novelty remains an open question.

## Prior-art comparison still required

Perform a claim-by-claim full-text comparison against cross-domain verifier benchmarks (including VerifyBench), selective classification/risk-coverage work, calibration under distribution shift, process reward models, and test-time compute allocation. Record the closest identical estimand, closest method, closest evaluation protocol and what remains substantively different. Do not claim a first-of-its-kind benchmark or theorem without supporting evidence.
