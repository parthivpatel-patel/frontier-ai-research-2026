# Protocol 095 — Coverage-aware safety comparison and falsification fixture

Date: 2026-11-06. Status: preregistered design and hand-calculated synthetic fixture. No empirical result or cloud execution is claimed.

## Critical identification issue

Protocols 089–094 compare selective unsafe-acceptance risk among claims a method accepts. Even when two methods have the same **overall** acceptance count, family-specific acceptance denominators can differ. Consequently, a favorable pooled risk comparison cannot establish lower risk for every physics family, and a favorable standardized comparison cannot establish a favorable pooled risk comparison. Neither quantity is a causal effect.

For claim i, let A_i and B_i denote binary acceptance decisions and Y_i denote an independently adjudicated binary indicator of unsafe acceptance under a *frozen* mapping from physical evidence to unsafe/safe. The selective risk is R_A = sum(A_i Y_i)/sum(A_i), defined only if the denominator is positive. Overall coverage is C_A = sum(A_i)/N. Family coverage C_Ak = sum_{i in k} A_i/N_k. Report C_A, C_B and all C_Ak, C_Bk, even if overall coverage is matched.

A four-way classifier output (supported, refuted, underdetermined, outside scope) is **not** itself an adjudicated Y_i. A contradictory-evidence quarantine state must be kept separate. Unsafe acceptance requires a prespecified operational definition, such as accepting a proposition that an independent adjudicator judges unsupported or inapplicable; do not label abstentions as unsafe acceptance.

## Hand-checkable Simpson-style synthetic fixture

Two equally sized families contain 100 claims each. All accepted claims in this illustration have observed binary unsafe labels. The following are *synthetic counts*, not benchmark measurements.

| Family | A accepted | A unsafe | B accepted | B unsafe |
|---|---:|---:|---:|---:|
| Mechanics | 90 | 9 | 10 | 0 |
| Circuits | 10 | 9 | 90 | 72 |
| Total | 100 | 18 | 100 | 72 |

Overall coverage is 100/200 = 0.5 for both. Pooled unsafe-acceptance risks are R_A=18/100=0.18 and R_B=72/100=0.72, so D_pooled=R_A-R_B=-0.54. Yet in mechanics D_mech=9/90-0/10=+0.10; in circuits D_circuits=9/10-72/90=+0.10. Under a prespecified 50/50 family mixture, D_standardized=0.5(0.10)+0.5(0.10)=+0.10. Thus A looks safer pooled despite being *worse in each family*. The arithmetic can be verified without software.

The fixture demonstrates why equal overall coverage is insufficient and why family-specific selective risk, coverage, and mixture-standardized risk must be reported. It does not imply that either real verifier exhibits this failure.

## Matched-comparison design

1. Freeze claim-family taxonomy, evidence budget, unsafe-label rubric, and acceptance thresholds before held-out adjudication.
2. For each baseline, report pooled selective risk and coverage at prespecified matched overall coverage; additionally compare matched **within-family** coverage where feasible. If within-family coverage cannot be matched, report the mismatch rather than silently interpolating.
3. Report exact partial-identification intervals for missing unsafe labels at pooled and family levels; for a fixed target mixture, report the standardized interval. Report the missing-label fraction by family and acceptance group.
4. Use independent, blinded physical adjudication, with disagreement and unresolved cases recorded rather than assigned convenient labels. Keep adjudication separate from model-produced certificates.
5. Prevent source leakage by grouping variants of the same underlying physical scenario and source family before train/test separation. Predefine adversarial assumption shifts.
6. Do not claim superiority when the prespecified relevant upper risk-difference bound is nonnegative, when a safety-critical family is non-comparable, or when strong competitive baselines have not been evaluated.
7. Distinguish sharp fixed-dataset identification intervals from uncertainty due to finite sampling. If generalizing beyond the fixed evaluation set, separately construct an appropriate clustered or source-family-aware uncertainty analysis.

## Executable test requirements

Implement a dependency-free synthetic fixture test that asserts the exact fractions D_pooled=-27/50, D_mech=1/10, D_circuits=1/10, D_standardized=1/10, and both overall coverages=1/2. Check zero acceptance, non-disjoint family assignment, inconsistent unsafe-label mapping, and unknown family weights as hard errors. Run only on a cloud service whose free quota, billing prerequisites, and account eligibility have been verified; retain run URL, commit, exit status, and logs. The fixture is a regression oracle, **not** empirical validation.

## Novelty and stop criteria

Simpson's paradox, selective prediction, risk standardization, and missing-outcome partial identification are prior statistical ideas, not novel contributions here. The prospective contribution remains an independently adjudicated assumption-sensitive scientific-language benchmark plus an empirically validated safety intervention against strong prior methods at matched coverage/evidence budgets. Failure to beat baselines, unresolved physical adjudication, leakage, or an inability to establish novelty should trigger a narrower negative-results or methods paper rather than a breakthrough claim.

No paid infrastructure, local compute, model inference, or model downloads are authorized by this protocol. Maintain venue-appropriate disclosure of AI assistance.
