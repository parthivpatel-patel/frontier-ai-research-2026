# Protocol 015 — Alignment-free cardinality bounds for repeated NL2MTL extraction

Date: 2026-11-02 (US Eastern). **Registered before implementation of this audit.** The complete five-run count vectors were already published in Session 018; this is a *retrospective descriptive calculation*, not a blind or prospective hypothesis test.

## Scientific question

How much cross-run agreement is mathematically possible given only the number of generated formal-expression records, **without** assuming positional or identifier-based semantic alignment? We explicitly do **not** infer that different records mean different requirements or that any formula is correct.

## Locked estimands

For each of the four original source documents, and each of its ten unordered pairs of five recorded runs (40 within-document comparisons total), let counts be `n` and `m`. Under a hypothetical **one-to-one matching of expression records**, report:

1. The unavoidable number of unmatched record *occurrences* `abs(n-m)`, a lower bound on unmatched occurrences for any matching. This is not the number of semantic errors or unique requirements.
2. The maximal possible pairwise matched-record fraction relative to the larger output, `min(n,m)/max(n,m)`. This is an **upper bound** on one-to-one record overlap; the actual fraction may be anywhere from zero to this bound. If both counts are zero, do not report a non-vacuous agreement fraction.
3. Number of pairs with unequal counts, sum of lower-bound unmatched occurrences, and arithmetic mean of the pairwise overlap upper bounds (excluding both-empty pairs).
4. For the four adjacent-run comparisons per document (16 total), sum the same unavoidable unmatched-occurrence lower bounds separately.

Use the already published five count vectors:
- `article_78`: [4,6,6,5,3]
- `article_80`: [2,1,4,2,2]
- `cara_pump_requirements`: [8,4,5,8,8]
- `harvesting_process`: [7,7,5,7,4]

No independence assumptions, p-values, confidence intervals, accuracy claims, or causal interpretation. These counts are repeated outputs for four documents, not 40 independent human instructions.

## Mathematical proof obligations

For any one-to-one matching of two sets of sizes `n` and `m`, at most `min(n,m)` pairs can match. Hence at least `max(n,m)-min(n,m)=abs(n-m)` occurrences remain unmatched, and the matched fraction relative to the larger set is at most `min(n,m)/max(n,m)`. Both bounds are tight for an abstract matching: choose all members of the smaller set to match distinct members of the larger set. **No evidence of a true semantic correspondence is implied by tightness.** A separate synthetic example with equal counts but opposing semantic assignments must demonstrate non-identifiability from counts alone.

## Engineering and integrity

Implement a pure Python standard-library module and synthetic-only unit tests, including symmetry, zero-count behavior, permutation of runs, and the equal-count counterexample. Use **only** the published count vectors; no upstream source text or generated formulas need to be downloaded or redistributed. Execute on the existing standard `ubuntu-latest` GitHub Actions runner in the public repository, with read-only permissions, five-minute timeout, no artifact/cache/paid services, and no laptop workload. Verify CI before claiming passing results.

## Falsification / reporting rules

- A failure of the arithmetic identity or tests invalidates the analysis.
- If the observed count vectors are inconsistent with the published Session 018 values, stop and disclose rather than silently correcting.
- If all counts had been equal, cardinality would provide **no positive evidence of semantic stability**; report the uninformative result.
- Even if many comparisons have low overlap upper bounds, this does **not** prove model semantic instability: splitting/merging requirements, differing extraction granularity, and ambiguous source interpretation remain alternative explanations.
- Compare the *diagnostic purpose* with classical matching/identifiability reasoning, may/must verification (Godefroid 2013), and grounded NL-to-temporal-logic evaluations (VLTL-Bench 2025). The arithmetic result is elementary prior knowledge, **not a novel theorem**.

## Decision gate

This audit is a data-validity safeguard. It cannot replace independent human intent adjudication, lawful access to model predictions, source-disjoint evaluation with >=30 independent requirements, and matched existing-method baselines. If those cannot be obtained, pursue a transparent reproducibility/limitations report rather than a claimed novel frontier-model improvement.

GitHub's official 2026 policy states standard hosted runners on public repositories remain free: https://github.com/resources/insights/2026-pricing-changes-for-github-actions . No card, paid API or local computation required. Spending target: $0.