# Protocol 163 — Cluster-level inference decision gate

Date: 2026-11-09. Status: preregistered analysis design; no empirical results.

## Source-level audit

Inspected `tests/test_protocol_159_paired_discordance_contract.py` and `tests/test_protocol_162_dependence_guard.py` at repository HEAD `9bd4ca6ca76a9d82cf545e22b0a65deaeda353a7`.

The paired oracle computes unconditional correct-answer yield on common original-problem IDs and an exact conditional binomial p-value for discordant outcomes. The dependence guard suppresses that p-value when two observations share a declared sampling-unit ID. **This guard is necessary but not sufficient**: even unique labels cannot establish independence; family-level shared shocks and reused templates may remain. The current code offers no valid cluster-adjusted p-value or confidence interval. Neither file supplies evidence of improved model performance.

## Primary estimand and unit of inference

For original problem i in cluster g, define Y_Agi and Y_Bgi as 1 only when the respective system returns a correct answer; abstention and wrong answers both score 0. Define d_gi = Y_Agi - Y_Bgi. The primary estimand is the average cluster-level effect, D = (1/G) sum_g [(1/n_g) sum_i d_gi], giving equal weight to independent source problems. Report case-weighted effect separately. Paraphrases and variants of one source problem must remain within a single cluster. Physics family is a higher grouping dimension and must not be conflated with source-problem clusters.

## Required analysis before significance claims

1. Freeze source-problem IDs, physics-family IDs, paraphrase lineage, data provenance, exclusions, and the sampling frame before scoring.
2. Report G, each cluster size, number of physics families, within-family cluster counts, selection overlap, abstentions, and both case- and cluster-weighted effects.
3. Use a paired **cluster bootstrap** that resamples whole source-problem clusters, never individual paraphrases. For an equal-family target, resample clusters within each family and aggregate family effects equally. Record failures/undefined replicates and use an explicitly specified interval method.
4. Run leave-one-family-out sensitivity. With few families, ordinary cluster-bootstrap intervals may have unreliable coverage; do not interpret a nominal 95% interval as calibrated without simulation or independent validation.
5. Treat the exact McNemar-style p-value as descriptive only when independence is not defensible. The current guard's non-null value is conditional on assumptions, not a verification of those assumptions.
6. Publish all predeclared metrics and failures, including negative results. No selective threshold tuning on the held-out test set.

## Falsification and stopping criteria

The proposed physics-aware verification advantage is not supported if it disappears under equal-family weighting, matched coverage, held-out source problems, or leave-one-family-out analysis; if performance is indistinguishable from matched random abstention; if paraphrase leakage is detected; or if uncertainty remains too wide to distinguish the effect from zero. If source clusters cannot be reconstructed, label the evaluation exploratory and do not report inferential significance.

## Closest methodological prior art (not novelty claims)

- McNemar (1947), *Note on the sampling error of the difference between correlated proportions*, Psychometrika, https://doi.org/10.1007/BF02295996 — paired binary comparison.
- Efron (1979), *Bootstrap methods: another look at the jackknife*, Annals of Statistics, https://doi.org/10.1214/aos/1176344552 — resampling foundations.
- Liang and Zeger (1986), *Longitudinal data analysis using generalized linear models*, Biometrika, https://doi.org/10.1093/biomet/73.1.13 — correlated observations.
- Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, NeurIPS, https://arxiv.org/abs/1705.08500 — coverage/risk tradeoffs.
- Angelopoulos and Bates (2023), *Conformal Prediction: A Gentle Introduction*, Foundations and Trends in Machine Learning, https://arxiv.org/abs/2107.07511 — uncertainty/coverage context.

These references identify substantial existing foundations. Their inclusion does **not** establish that a proposed AI verification system is novel. A dedicated search of physics-informed verification, process reward models, tool-augmented reasoning, and selective prediction is still required before writing a contribution claim.

## Execution and cost gate

This document is a design artifact only. No experiments, model inference, downloads, or local execution were performed. Run only on cloud infrastructure whose account-specific free quota, card requirements, billing settings, and current availability have been independently verified. Otherwise remain in design/review mode. No spend authorized.

## Immediate implementation acceptance criteria

Add a cluster-weighted descriptive oracle with strict group manifests; test that duplicating paraphrases within one cluster does not change the equal-cluster effect; test uneven family sizes; test empty/malformed clusters; and ensure no inferential p-value is emitted without a separately validated inference method. Tests must be executed in verified free cloud CI before reporting a pass.
