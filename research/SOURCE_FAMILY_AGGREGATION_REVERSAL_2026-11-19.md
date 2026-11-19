# Source-family aggregation can reverse verifier rankings (2026-11-19)

**Status:** mathematical design note; all numbers below are constructed examples, not model measurements or a novel theorem.

## Why this matters

The project compares selective verification across NLP, mathematics, and physics. Pooling accepted answers into one micro-averaged error rate can conceal opposite within-family conclusions, because the methods may accept different numbers of questions from each family. Even when the held-out *candidate* roster is identical, method-dependent acceptance changes the mixture of accepted questions.

Let family (g) contain (n_g) fixed candidates. For verifier (m), define (a_{mg}) accepted candidates and (e_{mg}) erroneous accepted candidates. Family coverage is (c_{mg}=a_{mg}/n_g); selective risk is (r_{mg}=e_{mg}/a_{mg}) when (a_{mg}>0). The pooled selective risk is

[
R_m^{micro}=\frac{\sum_g e_{mg}}{\sum_g a_{mg}}
=\sum_g \frac{a_{mg}}{\sum_h a_{mh}}r_{mg}.
]

The weighting distribution depends on the verifier. Thus a lower pooled risk does not imply lower risk in each family or a superior verifier at matched family coverage.

## Explicit constructed reversal

Consider two families with **100 identical candidate questions per family** and the following *hypothetical* acceptance/error counts:

| Family | A accepted | A accepted errors | A risk | B accepted | B accepted errors | B risk |
|---|---:|---:|---:|---:|---:|---:|
| NLP | 90 | 9 | 10% | 10 | 0 | 0% |
| Physics | 10 | 8 | 80% | 90 | 63 | 70% |
| **Pooled** | **100** | **17** | **17%** | **100** | **63** | **63%** |

B has lower within-family accepted-error rates in **both** families, yet A has a much lower pooled rate. Both methods accept 100/200 candidates overall, so matching *global* coverage alone does not prevent this reversal. The accepted-answer family mixtures are different (A: 90% NLP; B: 10% NLP). These marginals can coexist with a shared candidate roster; candidate error labels must be held fixed across methods, and acceptance assignments must be constructed consistently.

This is a form of aggregation/selection reversal, not a discovery about real AI systems. A family-macro risk computed as an unweighted average of the two defined family risks would be 45% for A and 35% for B, reversing the pooled ranking. Macro risk is itself a choice of estimand, not a universal correction.

## Preregistered analysis implications

1. Freeze candidate IDs, answer text, correctness labels, family labels, and method decisions before evaluation; no method-specific relabeling.
2. Report each family’s candidate count, acceptance count, accepted-error count, coverage, and risk, including undefined risks when acceptance is zero.
3. Report pooled micro risk **and** family-macro risk only for a prespecified family set and weighting scheme. Never silently drop a family with zero acceptance; report macro risk as undefined or specify an explicit alternative estimand in advance.
4. Compare within-family coverage as well as global coverage. A global 5% verification-cost tolerance does not control acceptance mixture.
5. Present coverage–risk curves and budget accounting with frozen, predeclared thresholds; retrospective equal-coverage plots are descriptive, not prospective deployment results.
6. Use source-family-aware uncertainty intervals and examine method-by-family interaction. Small samples and dependence between questions from one source can invalidate naive independent-question intervals.
7. Require a primary-source prior-art comparison of selective prediction, dataset shift, abstention, and Simpson-type aggregation before making any novelty claim.

## Falsification / claim restriction

If a claimed pooled gain disappears or reverses under prespecified family weighting, the result cannot be described as uniformly better verification. If one family has undefined selective risk, a complete three-domain superiority claim is unsupported. If method-specific acceptance mixtures differ substantially, global coverage parity is insufficient for a domain-balanced superiority claim. Any empirical improvement must be demonstrated on held-out data, not on this constructed example.

## Scope and resources

This note requires no training, inference, simulation, download, or laptop computation. Any executable validation should run only on confirmed no-charge standard cloud CI, after checking account-specific eligibility. No compute or billing authorization is implied. The November 22, 2026 checkpoint remains conditional on evidence.
