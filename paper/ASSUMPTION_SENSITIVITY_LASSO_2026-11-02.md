# Assumption sensitivity of proposition-alias agreement: exploratory methods note

Date: 2026-11-02. Evidence level: **exploratory, post-hoc, benchmark-relative**. Not a claim of new LTL theory, independently verified model errors, physical safety improvement or original frontier-model performance.

## Setup

Let φ and ψ be LTL formulas generated or recorded for a natural-language requirement. Let D assign metadata to atomic proposition symbols. An alias evaluator replaces symbols p and q when their complete metadata records D[p] and D[q] are identical. The resulting equality is conditional on the proposition-identity assumption: for every time t in every relevant physical trace, p(t)=q(t).

A robust equivalence claim under uncertain physical semantics requires φ and ψ to agree for every physically admissible trace and every interpretation in an independently justified uncertainty set. Equality of serialized metadata is insufficient to establish that constraint.

## Constructed falsifier

Take φ = F p and ψ = F q. A one-state infinite lasso with p=true and q=false satisfies φ and violates ψ. If an externally validated constraint enforces p(t)=q(t) for all t, this witness becomes inadmissible. The counterexample shows why an alias agreement depends on the physical assumption, not merely on the spelling of metadata.

This follows from established temporal logic and model checking, not a new theorem. A finite bounded lasso witness is conclusive for the stated interpretation; a bounded failure to find a witness is not a general equivalence proof.

## Pinned external observation

Protocol 024 partitioned 500 recorded lifted VLTL-Bench predictions into 485 exact string matches, 11 additional metadata-alias-only matches and four unresolved mismatches. Protocol 025 applied an explicitly restricted infinite-lasso LTL checker to the 15 nonexact pairs. The [verified cloud run](https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/41535056759) reported nine counterexamples under unconstrained proposition valuations among the 11 alias-only pairs; imposing recorded metadata equalities yielded no bounded witness for those nine. The other two alias-only pairs and all four unresolved pairs had unsupported syntax. All nine witnesses use at most three states and three proposition symbols. See [Protocol 025](../experiments/PROTOCOL_025_ASSUMPTION_SENSITIVE_LASSO.md) and [Session 028](../literature/SESSION_028_2026-11-02.md).

These counts are **not** estimates of translation correctness. The evaluation uses benchmark references and recorded grounding metadata whose independent semantic correctness and source-family independence have not been established. The post-hoc choice of mismatch subset prevents confirmatory inference.

## Claims explicitly excluded

- No claim that the nine cases are unsafe physical actions or incorrect AI interpretations.
- No claim that the other six cases are semantically equivalent, incorrect or even within the supported parser grammar.
- No claim that absence of a bounded witness proves equivalence.
- No claim that the reference formula is necessarily correct.
- No claim that the benchmark's model-generation provenance or reuse rights have been independently established.
- No claim of a novel formal-verification algorithm, risk bound or physics-aware AI result.

## Closest prior art

- Biere et al. (1999), *Symbolic Model Checking without BDDs*, https://doi.org/10.1007/3-540-49059-0_14 .
- English et al. (2025), VLTL-Bench, https://arxiv.org/abs/2507.00877 .
- Wang et al. (2025), ConformalNL2LTL, https://arxiv.org/abs/2504.21022 .
- Wang et al. (2026), SCP-NL2TL, https://arxiv.org/abs/2608.05439 .
- Wang et al. (2026), VerusEval, submitted October 19, https://arxiv.org/abs/2610.26464 .

## Required next experiment

A predeclared, source-disjoint, blinded study with independently adjudicated natural-language meanings and independently justified physical predicate constraints. Report unsafe acceptance at matched coverage, abstention, source-family uncertainty, assumption sensitivity and strong baseline comparisons. If this evidence cannot be obtained by the conditional November 22 target, limit the paper to a methodological or negative finding with full disclosure of AI assistance.
