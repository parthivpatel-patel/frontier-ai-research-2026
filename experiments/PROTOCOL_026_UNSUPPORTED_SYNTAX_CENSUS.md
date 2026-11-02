# Protocol 026 — Fixed-vocabulary unsupported-syntax census

Date: November 2, 2026. Session 029. **Exploratory, post-hoc** follow-up to Protocol 025; freeze this protocol before running its new external-data analysis. The six previously unsupported nonexact pairs were observed in Session 028, so no confirmatory inference or independent sampling is claimed.

## Question and data

Why were six of the fifteen nonexact lifted VLTL-Bench formula pairs not handled by our deliberately restricted LTL parser? Audit only **aggregate lexical and parse-failure categories**. This is a diagnostic for planning a future parser extension, not a claim that any model or reference is incorrect.

Reuse only the pinned VLTL-Bench upstream commit `383baea8210b93fe9fa7d14edd4757e5b3464e82`, lifted file `translation_eval/nl2tl/gt_lifting/navi.jsonl`, 356248 bytes, Git blob `c21575fca5e224968b56f0192b8bc0ddbaedac46`. The byte-verified data are fetched transiently on the existing public GitHub standard runner; no external records are committed, uploaded as artifacts, or printed.

## Frozen analysis and stopping rules

1. Reuse Protocol 024's exact-match and metadata-alias partition, and Protocol 025's existing parser **without modifying it**. For every nonexact pair, try parsing prediction and reference separately. Only pairs where either side fails enter the unsupported census.
2. Emit counts for unsupported pairs by previous alias-only/unresolved category; which side fails (prediction, reference or both); and fixed failure classes: unknown character, unknown word/operator, length/token limit, or grammar/operand.
3. Count operator occurrences over **both sides** of unsupported pairs using a fixed vocabulary: not, and, or, implies, until, next, finally, always. Count proposition tokens, parentheses, Boolean constants, unknown-word tokens and unknown-symbol tokens. Never emit raw unknown tokens, individual formulas, IDs, sentences, proposition mappings or traces.
4. Check the partition: supported + unsupported = all nonexact pairs; failure-side totals must agree with unsupported counts. Preserve syntax-unsupported cases as unsupported. **No parser extension or rerun of bounded semantic checking in this session.**
5. Run network-free constructed tests and the pinned aggregate audit only on standard `ubuntu-latest` GitHub Actions with a five-minute timeout, Python standard library and no model inference, GPU, paid API, credit card, or laptop compute.
6. If counts differ from Protocol 025's 15 nonexact and six unsupported, stop interpretation and investigate the source/pipeline. Do not cherry-pick parseable rows.

## Scientific interpretation and falsification

The diagnostic is descriptive and post-selected. Operator occurrence counts are not independent source counts, model-error counts, or estimates of correctness. A formula may be unsupported because our parser is narrow rather than because it is malformed. A future parser extension must specify exact grammar, operator precedence and infinite-trace semantics *before* evaluating the six cases, and must include metamorphic tests and comparison with an independent LTL implementation if available at zero cost.

If the parser's unsupported set is nonreproducible, if source bytes fail integrity checks, or if any external text is printed, this protocol fails. Do not claim semantic equivalence from a bounded search with no witness.

## Literature and novelty boundary

The general combination of NL-to-temporal-logic translation and formal checking is already covered by [VLTL-Bench (2025)](https://arxiv.org/abs/2507.00877), [ConformalNL2LTL (2025)](https://arxiv.org/abs/2504.21022), [NeuroNL2LTL (May 20, 2026)](https://arxiv.org/abs/2605.22874), [SCP-NL2TL (August 5, 2026)](https://arxiv.org/abs/2608.05439), and [VerusEval (October 19, 2026)](https://arxiv.org/abs/2610.26464). NeuroNL2LTL's reported verification results are **author claims in a different evaluation**, not replicated by us. Our narrower physics-assumption uncertainty hypothesis remains unproven.

**Publication gate:** independently adjudicated physical meanings, blinded source-disjoint authentic predictions, and matched-coverage comparisons are mandatory before claiming improved safety or originality. November 22 remains conditional.
