# Point-in-time evidence leakage: a falsifiable paired evaluation protocol (2026-11-21)

Status: methodological proposal; NOT an experimental result or novelty claim. This document supplements, rather than replaces, the frozen confirmatory estimand and release gates.

## Specific identification problem
A temporal verifier may appear to outperform a baseline because the evidence corpus accidentally contains post-cutoff facts, because retrieved snippets disclose the answer, or because the verifier abstains on a different subset. Those are distinct mechanisms. The primary comparison remains the preregistered selective-risk contrast at matched coverage and compute; this protocol supplies an auxiliary *paired leakage stress test*.

For each item i define query cutoff t_i, answer target y_i(t_i), source publication time p_ij, source observation/validity interval [v_start,v_end), and archival capture time a_ij. An admissible evidence item must be published no later than t_i AND substantively describe information knowable at t_i. A page currently displaying a historical date is not automatically evidence of what was visible at that date. Store immutable snapshot hashes, URLs, and retrieval timestamps. If publication and archival provenance conflict, mark evidence uncertain and exclude from confirmatory claims.

## Counterfactual evidence arms
A: admissible point-in-time snapshots only.
B: same eligible snapshots with dates masked but all non-date tokens preserved (tests dependence on explicit temporal metadata; masking may itself change task difficulty).
C: matched volume of chronologically shuffled metadata with unchanged text (negative control, not an exchangeable causal intervention).
D: deliberately future-contaminated evidence, **diagnostic only**; never treat D as a valid test-time system or use it to calibrate thresholds.
E: no retrieval, same base model and fixed inference budget.

Freeze question IDs, base model, decoding, prompt templates, retrieval candidates, token budgets, costs, acceptance coverage targets, and scoring before opening held-out labels. When equal token budgets are infeasible, report a Pareto frontier and do not claim matched-compute superiority.

## Outcome decomposition
Let L_i^k be independently adjudicated loss for arm k and S_i^k in {0,1} be acceptance. Report coverage C_k = mean(S_i^k) and selective risk R_k = sum(S_i^k L_i^k)/sum(S_i^k), undefined if denominator zero. For A versus B, also report the common-acceptance paired difference
D_AB = sum_i S_i^A S_i^B (L_i^A - L_i^B) / sum_i S_i^A S_i^B,
and acceptance-set Jaccard overlap. D_AB is descriptive of the intersection, not a replacement for the primary estimand and not proof of causal mediation.

Aggregate uncertainty at independent source-family level. Family counts, family-specific coverage, missing labels, denominators, and failed resamples must be published. No question-level IID significance claims when families share sources.

## Cross-domain validity
NLP: dated claims with source snapshots and independently adjudicated answers.
Mathematics: a time-dependent proof-status or theorem-database release question; an immutable theorem truth value alone is not temporal.
Physics: time-indexed measurement or dataset revision, not time-dependent truth of a physical law. Document units, uncertainty, and versioned observations. If genuine time-indexed gold labels cannot be sourced, remove that domain from confirmatory analysis instead of relabeling static questions.

## Failure and falsification
- If A does not outperform E at the preregistered operating point, no incremental retrieval benefit is established.
- If A and B are indistinguishable with adequate power, no explicit timestamp benefit is established.
- If C matches A, temporal-metadata-specific interpretation is unsupported.
- If performance requires D or unverifiable snapshots, reject the point-in-time validity claim.
- If improvements disappear under common-acceptance comparisons, describe selection effects rather than prediction improvements.
- If source-family uncertainty spans zero or effective independent family count is inadequate, report inconclusive.
- If labels or thresholds were adjusted after inspecting the confirmatory holdout, relabel the analysis exploratory.

## Closest established work and novelty boundary
Geifman & El-Yaniv (NeurIPS 2017), *Selective Classification for Deep Neural Networks*, already establish risk-coverage evaluation and rejection; do not claim these as novel: https://papers.nips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html
Wei et al. (NeurIPS 2025), *TimE: A Multi-level Benchmark for Temporal Reasoning of LLMs in Real-World Scenarios*, already provide a large temporal QA benchmark: https://proceedings.nips.cc/paper_files/paper/2025/hash/84f1e188c2be52f89f6e206bc37d092d-Abstract-Datasets_and_Benchmarks_Track.html
Kenneweg et al., *TRAVELER* (2025), evaluate explicit, implicit, and vague temporal references: https://arxiv.org/abs/2505.01325

Potential incremental contribution, still unverified: the **joint** point-in-time source-provenance, abstention-set and family-dependence audit across genuinely dynamic NLP/math/physics evidence. This may be a useful evaluation protocol even if not algorithmically novel. A comprehensive literature comparison is still required before any novelty assertion.

## Zero-cost execution gate
Do not run model inference until a provider's current free allowance, card/billing requirement, available capacity, geographic eligibility, and spending safeguards have been independently verified. GitHub-hosted lightweight tests may validate schema and deterministic arithmetic only, subject to current quota verification. No local compute, model downloads, GPU use, paid services, or unapproved billing.

## Release gate
Publish as methods/preregistration only until immutable data manifests, frozen protocols, cloud provenance, independent labels, matched baselines, negative controls, family-aware intervals, and a full literature audit are available. Disclose AI assistance as required by publication venue.