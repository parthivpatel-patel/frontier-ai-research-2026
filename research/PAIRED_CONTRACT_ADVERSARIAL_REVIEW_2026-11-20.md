# Paired-contract adversarial review — 2026-11-20

Status: source-code review only; **no new cloud test execution or model evaluation claimed**.

## Concrete implementation gaps in `tests/test_paired_contract_guardrails.py`

1. **Nonfinite resource counters pass structural validation.** For `input_tokens`, `output_tokens`, and `verifier_calls`, the predicate `type(v) in (int,float) and v < 0` does not reject `float('nan')` or `float('inf')`. A finite, nonnegative integer requirement is needed for token/call counters. Cost must be exactly zero and finite. A fractional token count such as 0.5 currently passes.
2. **Item identity is not globally stable.** The `by_item` comparison checks domain, split, answer hash, correctness and family, but does not compare `source_id`. Two policies can evaluate an identical `item_id` while claiming different provenance. Also, `item_id` is not checked for a unique answer across all datasets beyond the selected attributes.
3. **Matched computation is not enforced by the estimand.** `paired_selective_error_difference` checks equal accepted counts and identical item IDs but does not verify matched total input/output tokens or verifier calls. Its result is a descriptive matched-coverage error difference, **not** evidence of matched-cost improvement.
4. **The metric alone is insufficient for policy evaluation.** Equal coverage can hide differences in rejection errors, subgroup risk, and confidence intervals. Report false rejection and accepted-answer risk separately, with paired uncertainty and prespecified decision rules.
5. **Temporal and adjudication provenance are self-reported.** Numeric `feature_available_at_decision <= decision_time` and a boolean blinding flag are not external proof of timestamp authenticity or independent adjudication. Preserve immutable source hashes, adjudicator logs and leakage audit evidence.

## Required adversarial fixtures before empirical use

- Reject `float('nan')`, `float('inf')`, negative, fractional, and boolean token/call counts; require integer counters.
- Reject two rows sharing `item_id` with different `source_id`.
- Construct equal-coverage policies with unequal token/call totals; reject a **matched-cost** claim while allowing a clearly labeled descriptive matched-coverage comparison.
- Reject mixed or unresolved labels, empty pools and zero acceptance; verify accepted-only error identity against exhaustive finite-population enumeration.
- Require evidence of held-out family/source/answer separation, plus frozen policy versions and blinded adjudication artifacts.

## Publication and falsification gates

The core mathematical identity is algebraic and not novel by itself. The scientific hypothesis is that temporal-consistency features improve held-out, independently adjudicated verifier decisions across NLP, mathematics and physics **beyond** conventional confidence/feature baselines at matched budget. Shuffled temporal features, mismatched evidence, and held-out-domain transfer are mandatory negative controls. If matched-cost gains vanish, if source-family leakage is found, if independent adjudication is unavailable, or if performance is no better than negative controls, do not claim mechanistic or cross-domain reliability improvements.

This review is a proposed repair checklist, not proof that fixes were implemented. No local laptop compute, downloads, model inference, paid resources or billing actions are needed. Only explicitly confirmed free hosted CI should run eventual lightweight tests.
