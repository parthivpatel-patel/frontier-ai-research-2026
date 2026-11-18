# 2026 prior-art collision and feasibility decision (18 November 2026)

**Status:** literature-screening update, not a completed systematic review, empirical result, or amendment to any frozen preregistration. This memo complements the existing cross-domain falsification and matched-budget audit. All findings below are based on publisher/abstract pages; full-text method and code comparisons remain outstanding.

## High-priority collisions found

| Work (public source) | Relevant overlap | Required discrimination |
|---|---|---|
| Li et al., *VerifyBench: A Systematic Benchmark for Evaluating Reasoning Verifiers Across Domains*, AAAI 2026, published 14 March 2026, https://doi.org/10.1609/aaai.v40i38.40448 | ~4,000 questions spanning math, physics, chemistry and biology; cross-domain verifier generalization and input-format sensitivity | **Do not claim first cross-domain verifier benchmark or first physics/math verifier comparison.** Check their annotation, split and cost protocols; evaluate added NLP and source-family shift only as incremental hypotheses. |
| Phillips et al., *Entropy Alone is Insufficient for Safe Selective Prediction in LLMs*, arXiv March 2026, https://arxiv.org/abs/2603.21172 | Abstention, selective risk, entropy plus correctness probes across QA benchmarks | **Do not claim novelty for combining uncertainty and correctness signals.** Reproduce matched-budget probe baseline. |
| Salem et al., *Hierarchical Group-Conditional Conformal Risk Control for Selective Prediction in Language Models*, arXiv July 2026, https://arxiv.org/abs/2607.24562 | Domain/group risk controls and group-shift failures | **Do not claim group-conditional selective-risk control as new.** Compare against hierarchical group thresholds where assumptions permit; distinguish empirical coverage from guarantees. |
| Sedoc et al., *Trust but Verify: Prover-Verifier Deliberation for Selective LLM Prediction*, arXiv May 2026, https://arxiv.org/abs/2605.25133 | Structured prover-verifier challenges and abstention; cross-provider and difficult-science evaluations | **Do not claim challenge-based verification or deliberation as new.** Match extra calls/tokens and include an abstention baseline. |
| Zhou et al., *Variation in Verification: Understanding Verification Dynamics in Large Language Models*, 2025; revised April 2026, https://www.alphaxiv.org/abs/2509.17995 | Verification across math, knowledge and natural-language reasoning | **Do not claim that math+NLP verifier analysis alone is novel.** Check model, response-format and difficulty effects. |
| Richardson, *What Predicts Correctness in Text-to-SQL? A Selective-Prediction Study*, July 2026, https://arxiv.org/abs/2607.06799 | Verifier generalization under unseen schema/source shift, selective risk and cross-provider ensembles | Source-family shift is itself prior art; the proposed test must isolate a new mechanism, theorem, or reproducible failure boundary. |

## Stronger falsification and reporting safeguards

1. A three-domain score is **not** a novelty claim. Require a precise method-level distinction from existing verifier ensembles, group-conditional conformal methods, correctness probes and verifier deliberation. If no distinction survives full-text comparison, publish a replication or negative-result paper instead.
2. Existing coverage-quantile thresholds are selected on calibration families. For tied scores, predeclare stable hash-based ranking *within calibration*, then apply a frozen acceptance policy to test items without choosing a test-set top-k. Report achieved test coverage, including deviations from target.
3. At fixed coverage, the selective-risk contrast is undefined if either method accepts zero items. Mark undefined rather than imputing zero. A paired family bootstrap must carry all methods jointly, report the fraction of undefined replicates, and never silently discard them. If undefined replicates are substantial, withhold inferential superiority claims.
4. Baseline selection using a validation set and superiority margin selection must precede held-out labels. Report both equal-weight domain macro results and each domain's harm, and account for the three target coverages in the multiplicity plan.
5. Distinguish three hypotheses: (H1) domain-specific verifier signal predicts correctness, (H2) a *shared* decision rule transfers to unseen source families, (H3) the shared rule improves risk at matched verifier budget over the strongest eligible baseline. Evidence for H1 does not imply H2 or H3.
6. Dimensional analysis is not a physics truth oracle; symbolic math checking does not validate informal reasoning; evidence entailment does not prove source truth. Keep independently adjudicated error labels.

## $0 cloud feasibility

GitHub's official Actions billing documentation (accessed 18 November 2026) says **standard GitHub-hosted runners in public repositories are free**, whereas **larger runners are charged even in public repositories**: https://docs.github.com/en/billing/concepts/product-billing/github-actions . The free standard-runner rule is a service policy, **not** verification that this account currently has Actions enabled, available capacity, a usable runner, or unrestricted experimental usage. The 2,000-minute GitHub Free allowance refers to plan-included usage, not a guaranteed GPU allotment. No card or billing requirement for the individual account has been established; check account billing status and actual workflow acceptance before any execution. Avoid larger runners, third-party paid APIs, hosted GPUs and long-running compute. GitHub Actions must comply with its terms and should not be repurposed as an unrestricted training service.

**Execution decision: NO-GO for new model experiments.** Continue source-only CI, code review and preregistration checks; authorize a tiny bounded standard-runner evaluation only after repository Actions availability, dataset licensing, exact resource ceiling and zero-charge eligibility are verified. Do not run anything on the user's laptop.

## Publication gate

The 22 November checkpoint is an internal decision date, not a guaranteed paper release. No new model results, validated novelty or complete full-text audit are established here. Record AI assistance accurately in any submission and retain negative findings.
