# Protocol 116 — common-support and selection-bias identification gate (2026-11-07)

Status: mathematical identification note and test contract, not empirical evidence. Follows Protocols 111–115. No model was run and no novelty is claimed.

## Paired observational table

For physical lineage i and intervention j, require one adjudicated physical proposition T_ij, one immutable evidence digest E_ij, and exactly one response per system s in {A,B}. Define Z_ijs=1 for accepted responses and 0 for abstentions. Define U_ijs only for accepted responses, using a blinded, independently adjudicated unsafe-response rubric. The full intervention population, not the accepted subset, is the denominator for coverage.

Let n denote the number of prespecified matched intervention keys, including abstentions. Define C_s = sum(Z_s)/n, N_s = sum(Z_s), and R_s = sum(Z_s U_s)/N_s if N_s>0; otherwise R_s is undefined. Define K = {keys: Z_A=Z_B=1}, C_both = |K|/n, and D_both = (1/|K|) sum_{k in K}(U_Ak-U_Bk) if |K|>0. D_both is the paired difference *on common accepted interventions*, not the difference R_A-R_B, and is undefined for empty K.

The observable accepted-set decomposition is S_11 (both accept), S_10 (A only), S_01 (B only), S_00 (neither). Report all four cell counts and the unsafe outcomes where defined. In particular, never impute an abstaining system's unsafe response from the other system's observed response.

## Nonidentification demonstration

Suppose A accepts only easy cases with unsafe rate 0/10 while B accepts all 20 cases with unsafe rate 5/20. Comparing 0% to 25% does not identify a response-quality improvement: the acceptance policies select different populations. Even equal marginal coverage does not guarantee equal accepted cases. A comparison at frozen target coverage c must additionally report overlap and distinguish marginal selective risk from common-support risk.

Counterfactual unsafe outcomes under abstention are unobserved. Without explicit assumptions or randomized acceptance intervention, a full-population difference in unsafe *would-be responses* is not identified by accepted-only labels. Do not use bootstrap confidence intervals to disguise this missingness.

## Prespecified reporting and falsification

1. Always report n, the four acceptance-cell counts, C_A, C_B, C_both, N_A, N_B, R_A, R_B, and D_both (undefined values explicitly represented).
2. Calibration thresholds must be frozen on disjoint lineages before evaluation, with a content digest and deterministic tie policy. Do not tune on evaluation outcomes.
3. Compare identical physical evidence and intervention keys; predeclare evidence replacement, irrelevant-evidence, and proposition-preserving controls.
4. Primary claim of evidence-sensitive verification is rejected if causal evidence replacement does not outperform irrelevant/shuffled evidence controls under the preregistered paired metric and uncertainty procedure.
5. Withhold confirmatory intervals if independent adjudication, split isolation, lineage identity, fixed selection policies, or sufficient effective lineage support cannot be verified.
6. Treat common-support analyses as descriptive if acceptance depends on system behavior; never claim a causal effect of model architecture from an observational contrast.
7. A physics-family macroaverage uses fixed, preregistered family weights; undefined family outcomes remain missing and cannot silently receive weight zero.
8. Report exact baseline versions, model-access terms, prompt budgets, intervention construction, adjudication disagreements, and missing data.

## Executable regression fixtures to implement

- F1: identical systems, identical accepted sets and outcomes produce D_both=0.
- F2: disjoint acceptance sets with positive marginal coverage produce undefined D_both.
- F3: zero acceptance for A produces undefined R_A, not zero.
- F4: A-only and B-only observations affect marginal risk but never enter D_both.
- F5: equal coverage with different accepted keys is diagnosed, not treated as matched coverage.
- F6: a missing counterpart or contradictory shared truth fails admission before any estimate.
- F7: permuting input rows leaves cell counts, estimates, and fixed-seed lineage resampling invariant.
- F8: lineage resampling preserves all variants and both systems together.
- F9: changed calibration digest or split leakage fails before inferential computation.
- F10: shuffled-evidence negative-control rows cannot be omitted from the preregistered analysis.
- F11: undefined physics-family estimate cannot be coerced to zero in macroaveraging.
- F12: accepted-response correctness and shared physical truth are separate typed fields.

## Contribution boundary and immediate next step

Selective prediction, abstention, paired analysis, cluster bootstrap, and evidence interventions are established methodological ideas. The potential contribution, if supported, must be a **new, independently reproduced empirical or theoretical result about physics-grounded evidence reliance**, not this bookkeeping. Implement these tests and connect the existing matched-intervention validator to the estimator; run CI only after confirming GitHub Actions free-plan eligibility, remaining minutes, and billing safeguards for this account. Do not infer quota from a previously successful run. No laptop workloads or paid inference are needed for these tests.

Publication target November 22, 2026 is conditional on independently adjudicated experiments, competitive baselines, robust negative controls, and a completed source-verified literature audit.