# Protocol 155 — Paired improvement feasibility and multiplicity audit (2026-11-17)

## Status
Mathematical design audit only. No model evaluation, cloud run, novelty proof, or empirical performance claim. This protocol supplements Protocol 154, which addresses *absolute* source-weighted risk, not evidence that a proposed verifier improves upon a baseline.

## Paired estimand and finite-sample bound
For each independently sampled source cluster i, let A_i be the prespecified aggregate loss of the proposed policy and C_i the aggregate loss of a cost-matched baseline on the **same** source. Both lie in [0,B]. Define D_i = C_i - A_i in [-B,B]; positive values favor the proposed policy. The population improvement is Delta = E[D_i], estimated by the average paired difference. If the M proposed policies were fixed before observing evaluation labels, Hoeffding and a union bound imply simultaneously, with probability >= 1-delta,

Delta_h >= mean(D_i(h)) - B sqrt(2 log(M/delta)/n).

The radius differs from Protocol 154's absolute-risk radius B sqrt(log(M/delta)/(2n)): the paired difference has range width 2B, not B. The certificate supports an improvement claim only when its lower bound is strictly above zero. It requires independent identically distributed *source clusters*, fixed policies and baseline, valid bounded source-level losses, and nonadaptive evaluation. Dependence within a source is allowed.

## Quantitative planning example
For B=2, M=10 and delta=.05, the paired improvement uncertainty radius is sqrt(8 log(200)/n). A desired radius <= 0.25 requires n >= 679 independent sources; <= 0.10 requires n >= 4,239; <= 0.05 requires n >= 16,955. These are conservative sufficient counts for radius alone, not power calculations. The actual observed mean improvement must exceed the radius. The thresholds should be independently checked before publication.

## Interpretive restrictions
1. A positive mean paired improvement is not sufficient: require a positive lower confidence bound under the prespecified analysis.
2. Reusing one baseline on the same source does not require independence between baseline and proposed-policy losses; their pairing is precisely why source-level differences are appropriate.
3. Multiplicity M counts all eligible policies selected using the held-out labels, not merely the eventual winner. Adaptive creation after examining test labels invalidates this finite-family correction.
4. A single pooled certificate does not establish separate NLP, mathematics, and physics improvements. For claims in each domain, define domain-specific estimands and a multiplicity plan in advance; report domain-wise sample sizes and uncertainty.
5. A fixed finite-family Hoeffding bound is standard probability theory. Do not claim theorem novelty. Paired empirical Bernstein or anytime-valid methods may tighten bounds under extra conditions, but require independent proofs and a literature audit.
6. Source sampling bias, mislabeled ground truth, dataset contamination, changes in model versions, unequal inference budgets, and unmeasured abstention costs can defeat the intended interpretation even if the arithmetic is correct.

## Falsification and publication gate
Precommit source sampling, abstention cost, aggregation, baseline, candidate family, domain claims, and evaluation labels before held-out testing. Reject improvement if the lower bound is nonpositive; reject cross-domain generality if any prespecified domain fails its criterion; downgrade to exploratory if source provenance or independent-source counts are insufficient. Compare against selective classification, conformal risk control, multiple comparisons, and paired evaluation literature before asserting originality.

## Resource and provenance constraints
No user laptop compute, downloads, training, or inference. Do not run paid infrastructure or unverified free cloud model hosting. This document is a theoretical planning record, not an experiment or an authorization to spend. AI assistance must be disclosed where required.
