# Paired selective-risk comparison: identification and falsification gate (2026-11-18)

Status: prospective methodological specification. No empirical verifier outcomes are reported.

## Why pooled selective risk alone cannot rank methods

For a fixed held-out roster of N adjudicated questions, let E_i be the binary error of the *same underlying candidate answer* on question i, and A_im be the frozen accept/abstain decision of method m. Define coverage C_m = N^{-1} sum_i A_im and selective risk R_m = (sum_i A_im E_i)/(sum_i A_im), undefined when no items are accepted.

The existing accounting module correctly reports C_m and R_m, but an apparent risk advantage at different coverages is not a matched-coverage comparison. In particular, abstaining on hard cases can reduce observed error while leaving most questions unanswered. A comparison at a predeclared coverage target must use calibration-set thresholds, report realized test coverage, and must not retune thresholds on test labels or scores.

## Shared-answer requirement

The simple E_i notation is valid only when the compared verifiers assess the same candidate answer, under the same fixed correctness adjudication. If methods generate different answers or use different evidence, store E_im separately and do not use a shared-error implementation. All verification cost, retrieval, tool calls, and generation cost must be counted consistently. If a method cannot operate at the budget cap, report infeasibility; do not silently drop its items.

## Paired diagnostics

For methods a and b, report the 2x2 acceptance table: both accept, only a accepts, only b accepts, neither accepts. For both-accepted items, report common-subset error (descriptive, not a primary comparative win). With a shared E_i, error discordance among accepted items is driven by the *acceptance decisions*, not different answer correctness. Therefore McNemar tests on correctness of the both-accepted subset are inappropriate: correctness is identical by construction.

Report per-source-family coverage and selective risk, retaining undefined values when accepted count is zero. The primary source-family unit must be chosen before viewing held-out results. Do not mistake item-level bootstrap samples for independent source-family draws.

## Statistical decision rule

Predeclare one primary coverage target, a minimum tolerable realized coverage, one baseline family, and one direction of improvement. Compare selective risk only if realized coverages are within a preregistered tolerance and budget accounting passes. Use paired resampling by source family for uncertainty; if the number of independent families is too small for stable inference, report descriptive estimates and no confirmatory p-values. Any additional coverage targets, domains, or baselines require multiplicity control or explicit exploratory labels.

## Falsification and stop conditions

- **F1:** Any threshold, source family, adjudication rule, or budget cap is chosen after viewing held-out outcomes: confirmatory claim invalid.
- **F2:** A method's lower risk depends on materially lower realized coverage or higher total verification cost: no matched-condition win.
- **F3:** Improvements vanish or reverse on independently sourced families: reject a general cross-source robustness claim.
- **F4:** Physics dimensional consistency accepts a false physical statement, mathematical final-answer matching accepts invalid reasoning, or NLP fluency substitutes for evidence support: report failure modes, not unified verification.
- **F5:** Results cannot be reproduced from frozen item IDs, answers, labels, decisions, source families, budgets, and code revision: do not publish performance claims.
- **F6:** Closest prior work already implements the same scoring rule and evaluation conditions: narrow or withdraw novelty claim.

## Novelty boundary

Selective prediction, risk-coverage curves, conformal risk control, verifier evaluation, and out-of-distribution testing are established research areas. A new combination of NLP, mathematics, and physics is not by itself a new algorithm or theorem. The possible contribution is an empirically defensible, matched-cost, source-family-shift evaluation **if** it reveals a reproducible failure mode or improvement beyond established baselines. This is a hypothesis until independent held-out evidence exists.

## Cloud-only execution plan

1. Run standard-library unit tests on a standard GitHub-hosted public-repository runner only after checking the repository's Actions settings, run eligibility, and current billing restrictions. Do not select larger runners.
2. Freeze the roster, adjudication, baseline methods, thresholds, and cost policy before held-out scoring. Record Git object provenance; Git timestamps alone are not independent preregistration timestamps.
3. Use small, openly licensed, pre-existing scored examples first. Do not download or infer large models on the user's laptop. Verify dataset licenses, external download limits, and any cloud service payment requirements before execution.
4. Publish code, frozen manifests, disaggregated diagnostics, failures, and complete uncertainty assumptions. Clearly disclose AI assistance as required.

This specification adds safeguards; it is not a claim of a new scientific result, passing CI, or free-cloud account entitlement.
