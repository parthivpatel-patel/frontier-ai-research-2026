# Publication decision gate — 2026-11-22 checkpoint

**Status: preregistration / methods only; empirical discovery NOT established.** This is a decision record, not a claim that the paper is publication-ready.

## What repository inspection establishes

On 2026-11-21, the default branch contained `research/paired_archival_oracle.py`, `research/test_paired_archival_metamorphic.py`, and `research/NOVELTY_FALSIFICATION_GATE_2026-11-21.md`. The paired oracle enumerates binary labels shared between two fixed prediction/abstention policies, uses exact fractions, and returns extrema of the difference of accepted-case error rates. It is a small-frame reference oracle, not a scalable estimator. Four metamorphic test *definitions* were inspected; this inspection does not establish that any tests ran or passed.

## Mathematical scope and interpretation

Let policy j have v_j accepted verified examples, e_j verified errors, and k_j accepted unresolved examples. For each unresolved item i, both policies must use the same latent binary truth y_i. Conditional on fixed predictions p_ji and acceptance indicators a_ji, define

r_j(y) = [e_j + sum_i a_ji 1(p_ji != y_i)] / [v_j + sum_i a_ji],

provided the denominator is positive. The exact finite-frame identification set for the risk difference is {r_A(y)-r_B(y): y in {0,1}^m}; the oracle returns its minimum and maximum, not a confidence interval. When either denominator is zero, a risk difference is undefined; a publication must report that fact, not silently substitute zero.

**Important qualification:** Even a sharp finite-frame interval does not account for uncertainty in verified truth labels, historical provenance, selection into the evaluation frame, stochastic model outputs, or population sampling. Nor does it prove that source publication timestamps were authentic. Confidence intervals, if eventually justified, require a separate sampling and clustering design. The number of label assignments is 2^m, making exhaustive enumeration unsuitable for large m.

## Minimum submission gates

| Gate | Required evidence | Current status |
| --- | --- | --- |
| Repository integrity | Exact default-branch commit SHA and file manifest | Partial: named files inspected; release SHA not frozen |
| Test verification | Public CI logs bound to the exact source SHA, all regression/metamorphic tests passing | Not established |
| Closest prior art | Primary-source bibliographic audit with direct comparison and explicit overlap | Incomplete |
| Novelty | Narrow, falsifiable distinction from existing temporal QA, retrieval, selective prediction, missing-data and bitemporal methods | Hypothesis only |
| Dataset | Publicly reproducible manifest, source timestamps, version hashes, annotation and license checks | Not established |
| Empirical comparisons | Frozen splits, matched retrieval/model budgets, cutoff-blind/aware baselines, coverage and risk with uncertainty | Not run |
| Cross-domain validity | Separate defensible labels for NLP, mathematics and physics; no forced equivalence | Not established |
| Compute | Verified current zero-cost cloud allowance, no card/billing surprises, usage limits, no laptop compute | Not authorized |
| Manuscript integrity | Negative results, limitations, AI-assistance disclosure, code/data provenance | Required before submission |

## Falsification and stop rules

1. If prior art already supplies the materially same joint protocol, reframe as replication or engineering extension.
2. If publication dates cannot be authenticated, restrict claims to the archived-capture population; do not assert historical public availability.
3. If joint risk-difference bounds cross zero, do not claim one policy outperforms the other based on these bounds.
4. If leakage controls, matched retrieval budgets, or label-adjudication checks fail, withhold performance claims.
5. If genuinely free cloud capacity cannot be verified without a payment method or risk of charges, do not execute the workload.
6. If empirical evidence is absent at the checkpoint, release at most a clearly marked *methods proposal / preregistration*, not a completed experimental research paper.

## Next reproducible actions

1. Inspect current GitHub Actions runs and freeze exact source SHA; add only a bounded, dependency-free test job if repository policy and current free allowance permit it.
2. Validate small synthetic examples against an independently derived oracle; distinguish structural metamorphic tests from independent correctness checks.
3. Complete primary-paper comparison matrix with precise citations and overlapping claims.
4. Draft the manuscript with **no fabricated performance numbers, novelty certification, or simulated experiment outcomes**.
5. Preserve strict separation from other projects and perform all future compute in verified free cloud services; never require laptop training, inference or downloads.

This decision record is itself a research-planning artifact; it does not satisfy the outstanding gates.
