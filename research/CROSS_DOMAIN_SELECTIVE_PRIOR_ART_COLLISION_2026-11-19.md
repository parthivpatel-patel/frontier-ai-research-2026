# Additional 2026 prior-art collision: cross-domain selective prediction

Date: 2026-11-19. Status: literature screening, not empirical validation or a novelty certificate.

## Newly identified closest candidate

Basu, *Cross-Domain Uncertainty Quantification for Selective Prediction: A Comprehensive Bound Ablation with Transfer-Informed Betting* (arXiv:2603.08907, March 2026), https://arxiv.org/abs/2603.08907. The abstract reports nine selective-risk bound families, cross-domain transfer-informed betting, source/target experiments, and explicit baseline comparisons. **This directly challenges any claim that cross-domain selective risk, transfer-aware calibration, or comparative bound ablations are original to this project.** Claims in its abstract have not been independently reproduced here. Read the complete proof, experimental protocol, source/target split, and code before asserting distinction.

Other direct collisions requiring full-text review:

- Tayebati et al., *Learning Conformal Abstention Policies for Adaptive Risk Management in Large Language and Vision-Language Models*, arXiv:2502.06884 (2025), https://arxiv.org/abs/2502.06884. Learnable abstention and LLM-specific risk management already exist.
- Lin et al., *Domain-Shift-Aware Conformal Prediction for Large Language Models*, arXiv:2510.05566 (2025, revised 2026), https://arxiv.org/abs/2510.05566. Shift-aware calibration for LLMs already exists.
- Hu and Su, *Conformity Breaks Conformal Prediction*, arXiv:2609.04445 (September 2026), https://arxiv.org/abs/2609.04445. Score-mechanism shift and apparent reliability failures in multi-agent LLMs already exist.

## Narrow, falsifiable research question

Can a **frozen, independent verifier** outperform a frozen baseline confidence/abstention policy in held-out NLP, mathematical reasoning, and physics questions, **at matched family-conditional acceptance rates and measured total inference cost**, without advantage disappearing under source-family-balanced aggregation? This is an empirical question, not a novel theorem. It is not yet known whether the proposed comparison is itself novel; check benchmark and verifier papers.

## Pre-registered analysis and release gate

1. Freeze candidate responses and labels before verifier scoring; keep the same candidate per paired comparison. Document label provenance, adjudication, contamination checks, and source-family boundaries.
2. Predefine each family's acceptance-rate target, tolerance, and abstention convention. If exact deterministic matching is impossible because of score ties, disclose infeasibility; do not tune on the test labels.
3. Report per-family accepted errors / accepted count, acceptance count / total count, and undefined risk when acceptance is zero. Report pooled risk separately and never equate it with family-balanced risk.
4. Report all verifier calls, tokens, model weights/license, runtime, and monetary cost. Do not imply compute parity from call counts alone.
5. Use paired uncertainty with question/source-family clustering, source-held-out evaluation, frozen thresholds, and a prespecified negative-control verifier. No after-the-fact family selection.
6. Falsify superiority if effects reverse or disappear under family-balanced estimates, matched costs/coverage, held-out shifts, or independent labels; label inconclusive when intervals are too wide.
7. Do not claim distribution-free target risk guarantees under arbitrary unlabeled shift; require explicit assumptions and tests for any restricted guarantee.
8. If no real held-out evidence by 2026-11-22, release a transparent protocol/negative-result or methods preprint only, not a discovery paper.

## $0 execution boundary

GitHub's current official documentation says standard hosted runners in **public** repositories are free; larger runners are billed, and artifact/cache storage can incur charges beyond allowances: https://docs.github.com/en/actions/concepts/billing-and-usage and https://docs.github.com/en/billing/concepts/product-billing/github-actions. Use only standard public-repository runners for small CPU tests; no artifacts/caches, external paid APIs, GPU rental, or local model inference. Account-level settings, runner availability, and any card requirement have not been independently checked. Existing CI successes do not establish permission for unlimited model inference or compliance with Actions acceptable-use terms.

## Evidence status

This note is a documented prior-art and falsification checkpoint only. No new experiments, CI executions, verifier improvements, original mathematical results, or empirical novelty are asserted.
