# Archival missingness: partial-identification bounds and publication gate
Date: 2026-11-21. Status: analytical protocol; not an empirical result.

## Problem
A historical source absent from a pre-cutoff archive is not necessarily a source that was unavailable at the cutoff. Conditioning evaluation on archived versions changes the target population, potentially in a domain-dependent way. The existing `bitemporal_admission_preflight.py` enforces a deliberately strict archived-evidence rule; its rejection is **not** evidence of historical non-publication.

## Two distinct estimands
1. **Archived-version population:** performance on examples with independently verifiable, pre-cutoff archived versions. Identify and report this as a restricted population, never as all historically public evidence.
2. **Historically-public population:** performance on all examples for which publication by the cutoff can be independently established. A post-cutoff capture alone does not establish the content of the earlier version. Require independently authenticated version-level proof; otherwise retain the example as unresolved, not as eligible or ineligible by fiat.

## Worst-case bounds when archival eligibility is unresolved
Fix a verifier policy, domain, cutoff, and acceptance threshold *before* looking at outcomes. Among independently adjudicated, archive-verified examples let `a` be the number accepted and `e` the number of erroneous accepted answers. Let `m` be the number of unresolved examples that could be part of the target population. Assume only that each unresolved example could be accepted or rejected and, if accepted, could be correct or incorrect. For `a>0`, the selective error risk for the enlarged population is bounded by

`L = e/(a+m)` and `U = (e+m)/(a+m)`.

These are sharp under the stated unconstrained missingness model: the lower endpoint accepts all unresolved examples correctly; the upper accepts all incorrectly. With `a=0`, the conditional error rate is undefined if none of the unresolved examples is accepted; if any is accepted, its risk can span [0,1]. Report undefined rather than inventing a zero-risk result.

For `n` verified examples, the corresponding acceptance coverage in the enlarged population lies between `a/(n+m)` and `(a+m)/(n+m)`, provided the unresolved set is a fixed, enumerated part of the target sampling frame. Do not use these bounds if the number of missing examples itself is unknown.

For two verifiers A and B evaluated against the *same* enumerated unresolved frame, a conservative risk-difference interval for `R_A-R_B` is `[L_A-U_B, U_A-L_B]`. It is generally not sharp because the same unresolved examples induce dependence; paired joint feasible assignments can tighten it. A positive advantage is not robust if this conservative interval crosses zero. Do not treat it as a confidence interval: it is an identification interval, before sampling uncertainty.

## Required sensitivity table
For each domain (NLP, mathematics, physics), report `n, m, a_A, e_A, a_B, e_B`, verified-source family counts, risk bounds, coverage bounds, and the number of unresolved examples with independently adjudicated labels. Include a missingness sensitivity curve at prespecified plausible values of `m`, **without** choosing the value that favors the hypothesis. Do not silently drop an unresolved source family.

## Falsification and release rules
- If an apparent gain disappears when unresolved examples are included under plausible adverse assignments, restrict the claim to the archived-version population.
- If source families with missing archives differ materially by domain, period, or outcome, report selection diagnostics and do not generalize the archived estimate to all historically public evidence.
- If both policies have near-zero acceptance, do not interpret lower selective risk as improved verification.
- If the number of unarchived examples cannot be enumerated, these bounds are not population bounds; state the sampling-frame limitation.
- Matched coverage, compute budget, chronology shuffling, placebo evidence, family-aware uncertainty, and independently adjudicated labels remain mandatory for an empirical claim.
- These bounds are elementary missing-data partial identification, not a claimed novel theorem. Cite and compare the missing-data/partial-identification literature before publication.

## Deterministic arithmetic examples (not model results)
With `n=100, m=20, a=40, e=4`, verified selective risk is 10%, while the enlarged-population identification interval is `[4/60, 24/60]=[6.67%,40%]`; coverage is between `40/120` and `60/120`. With `m=0`, both bounds equal `e/a`. These are illustrative calculations only.

## Next implementation gate
Add a dependency-free validator for `0<=e<=a<=n`, `m>=0`, explicit undefined risk when `a=0`, and paired bound reporting. Execute it only on free, explicitly verified cloud CI capacity; no laptop execution, model downloads, paid compute, or billing activation. Verify CI availability and usage quotas before running any heavier experiment.

## Integrity
No inference, dataset, model benchmark, cloud quota, or CI result was generated by this document. Do not represent protocol publication as a discovery paper.
