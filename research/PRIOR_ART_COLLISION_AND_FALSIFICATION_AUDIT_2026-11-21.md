# Prior-art collision audit and falsifiable contribution boundary (2026-11-21)

Status: literature-screening memo, NOT a completed systematic review; no experimental result or priority claim. Scope: temporal evidence verification, selective abstention, scientific NLP/math/physics evaluation.

## Closest identifiable work and collision risk

1. **TIME: A Multi-level Benchmark for Temporal Reasoning of LLMs in Real-World Scenarios** (NeurIPS 2025 Datasets & Benchmarks; https://proceedings.neurips.cc/paper_files/paper/2025/file/84f1e188c2be52f89f6e206bc37d092d-Paper-Datasets_and_Benchmarks_Track.pdf ; project https://github.com/sylvain-wei/TIME). Reports 38,522 QA pairs and TIME-Lite 943 annotated examples, across wiki/news/dialogue. **Collision:** temporal reasoning benchmarks are not novel; compare against TIME-Lite rather than claiming to introduce time-aware evaluation. **Remaining distinction to test:** evidence-availability cutoffs, selective-risk decomposition and source-family robustness jointly; none is independently novel without further review.
2. **Time-Aware Language Models as Temporal Knowledge Bases / TempLAMA** (Dhingra et al., 2022; https://arxiv.org/abs/2106.15110). **Collision:** evolving factual answers and temporal knowledge probing. **Distinction to test:** evaluation of source-valid evidence *available as of query time*, rather than just historical truth.
3. **Inference-Time Conformal Reasoning with Valid Factuality Control for Large Language Models** (Wang et al., ICML 2026; https://proceedings.mlr.press/v306/wang26gw.html). **Collision:** factuality-risk calibration and abstention/generation control are established. Do not claim novel conformal guarantees. **Distinction to test:** chronology-constrained evidence admission plus matched-coverage, matched-cost diagnostics under clustered source dependence; any guarantee requires independently checked assumptions.
4. **TIME / temporal retrieval baselines** and **TimeAware** (https://github.com/vojtechbartek/timeaware). **Collision:** timestamp-aware retrieval and evaluation have existing implementations. Temporal filtering alone is not a novel algorithm.
5. **TempFinRAG** (2026; https://www.mdpi.com/2073-8994/18/9/1498). **Collision:** point-in-time retrieval with an evidence verifier and explicit temporal-leakage metrics exists in financial QA. Cross-domain transfer must demonstrate substantive new behavior rather than rename this mechanism.
6. **Is the Future Predictable? Modeling Future Predictability for Reliable Temporal Reasoning** (EMNLP 2026, secondary summary https://en.papernotes.org/EMNLP2026/llm_reasoning/is_the_future_predictable_modeling_future_predictability_for_reliable_temporal_reasoning_1640/). **Collision:** controlled retrieval and predictability-aware temporal reliability. Primary paper must be retrieved and checked before definitive novelty conclusions.

## Candidate narrow contribution (hypothesis, not discovery)

A **source-family-aware, point-in-time evidence admission evaluation** that jointly reports (i) selective error at fixed *global* coverage, (ii) paired errors on the intersection of accepted questions, (iii) full-coverage prediction errors, (iv) accepted-family concentration and zero-denominator families, and (v) chronology-negative-control sensitivity, with strictly held-out calibration. This is primarily an evaluation protocol. It must NOT be represented as a new theory of intelligence, a new conformal guarantee, or the first temporal-verification benchmark.

## Mathematical estimands and falsification

Let Y_i be independently adjudicated correctness, A_{mi} the binary acceptance of method m, and E_{mi}=1-Y_{mi}. For a fixed held-out set, define pooled selective risk R_m = sum_i A_{mi} E_{mi} / sum_i A_{mi}, only if denominator > 0. Coverage C_m = sum_i A_{mi}/n. Fix target coverage and computational budget before inspecting holdout results. Report R_T-R_B, plus accepted-set Jaccard and common-accepted paired error difference. Report family-level coverage and errors, including undefined family risks; never silently discard them.

**Primary falsifier:** no lower selective error for chronology-aware admission at matched coverage/cost with source-family uncertainty accounting. **Mechanistic falsifier:** shuffled or future-leaking timestamps perform as well as correctly constrained chronology, or chronology has no effect on genuinely time-varying examples. **Validity falsifiers:** unreliable source timestamps, answer leakage, nonindependent labels, family overlap across calibration/test, inadequate independent family count, or unstable zero-denominator behavior. A gain confined to a changed acceptance set is an operational selection effect, not a prediction-accuracy gain.

## Cross-domain construct validity

NLP: changing public facts and evidence-release timestamps. Mathematics: dated conjecture/proof *availability* only, never changing truth of a theorem. Physics: dated measurement/publication revisions and empirical claims, never changing physical laws by timestamp. Each item needs as-of query, source publication/availability time, canonical evidence, independent label, source family, and frozen split. Exclude any domain lacking these fields; do not infer universality from a single domain.

## Zero-cost execution and release gate

Run only tiny deterministic unit checks in an already verified free GitHub-hosted public-repository workflow. Do not trigger hosted inference or large data downloads until current free limits, signup/card requirements, and billing exposure are verified and a no-cost cap is documented. No local laptop workload. The November 22 checkpoint should yield a labeled methods/preregistration artifact unless genuinely independent held-out model results, controls, uncertainty, and complete prior-art screening are present. Disclose AI assistance as required by the target venue.

## Outstanding literature tasks

Read primary full texts of TIME, TempLAMA, ITCR, TempFinRAG and 2026 future-predictability work; search selective classification, conformal risk control, adaptive holdout reuse, bitemporal databases, temporal RAG, physics scientific QA and theorem-provenance benchmarks. Build claim-by-claim overlap matrix and mark unresolved overlaps. No novelty certification until complete.
