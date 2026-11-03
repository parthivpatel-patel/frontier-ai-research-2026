# Protocol 028 — Source-grounded dialect test and semantic-coverage bounds

Date: 2026-11-02 (US Eastern). Status: **preregistered design only, not executed**. This protocol follows Sessions 029–031 and deliberately does not claim a new experimental result.

## Motivation and frozen evidence

The pinned lifted VLTL-Bench file has 500 nonblank recorded predictions: 485 exact reference strings and 15 nonexact strings. Of the latter, nine are parsable by the restricted grammar and six pairs fail parsing on both sides. The twelve unsupported formula strings contain 16 unknown-word token occurrences (not necessarily 16 distinct tokens). A frozen conventional-operator dictionary matched zero of those 16 occurrences. The NL2TL project documents an alternative English-word dialect, including `imply`, `equal`, `until`, and interval-qualified temporal operators. This is a **source-supported hypothesis**, not evidence that the six formulas contain any of those spellings.

Sources: [NL2TL upstream project](https://github.com/yongchao98/NL2TL), [VLTL-Bench manuscript](https://openreview.net/pdf/f16808d741347403f89f359665278fe47be943b2.pdf), [prior Session 031](../literature/SESSION_031_2026-11-02.md), [Protocol 027](PROTOCOL_027_FROZEN_OPERATOR_VOCABULARY.md).

## Frozen lexical hypothesis (before examining unsupported tokens)

Case-folded whole-word candidate tokens: `imply`, `equal`, `until`. A separate lexical pattern for bounded operators is `F[integer,integer]`, `G[integer,integer]`, `U[integer,integer]` with optional whitespace; bounded operators are **not** assumed to occur within the 16 unknown-word occurrences. Preserve counts for `imply`, `equal`, `until`, remaining unknown words, and bounded-operator patterns separately. This vocabulary is not extended after seeing outcomes.

**Null:** no unrecognized word occurrences match the three frozen candidates. **Alternative:** at least one matches. Even a positive result only identifies lexical compatibility; it does not establish grammar, intended meaning, correctness, or physical validity.

## Source and privacy firewall

Before running any external-data test, record the upstream repository commit for both the NL2TL grammar and VLTL-Bench dataset; verify source licensing, evaluator semantics and provenance. Retain existing pinned input `translation_eval/nl2tl/gt_lifting/navi.jsonl`, upstream revision `383baea8210b93fe9fa7d14edd4757e5b3464e82`, byte count 356248 and Git blob `c21575fca5e224968b56f0192b8bc0ddbaedac46`. Do not commit or log individual external sentences, model outputs, formulas, proposition dictionaries, raw unknown words, identifiers or per-row examples. Only aggregate counts may leave the runner. Fail closed on changed hash, missing license/provenance, unmatched accounting or any raw content in logs.

## Execution plan ($0 cloud only)

1. On the existing public repository's standard GitHub-hosted Ubuntu runner, run constructed-only, network-free lexical tests first. No GPU, local workload, model download, paid API, larger runner, persistent artifact or cache. Reverify current GitHub public-runner billing and repository settings before triggering.
2. Use the frozen dictionary on the **same six** unsupported pairs, not a new selected sample. Report the exact partition: candidate token occurrences by word, other unknown-word occurrences, unknown-symbol occurrences, number of pairs with all unknown words accounted for, number of pairs with residual unknowns. Independently reconcile 16 total unknown-word occurrences and six pair/twelve-side failures.
3. Do **not** extend the parser or rerun bounded model checking in this lexical experiment. A subsequent protocol must freeze a complete grammar, precedence, associativity, Boolean interpretation of `equal` and `imply`, time domain, interval endpoint convention and metric-temporal semantics; then cross-check two independent implementations on constructed counterexamples before touching external formulas.
4. Keep the nine earlier bounded counterexamples and original 485/500 exact-match metric unchanged.

## Identification and reporting bounds

A lexical match is not a parse success; parse success is not semantic equivalence; semantic equivalence is not agreement with human intent; agreement with a reference is not proof of physical safety. Never report the 496/500 metadata-conditional agreement as independent semantic accuracy.

For the 15 nonexact pairs, even if all nine restricted-grammar pairs are adjudicated, six unparsed pairs remain missing-not-at-random. For any binary correctness property on these 15, if `k` of the nine supported pairs are independently adjudicated correct, the unconditional correctness fraction across the 15 is bounded by **k/15 to (k+6)/15** without assumptions on the six. These are logical bounds, not measured confidence intervals. A benchmark-wide fraction would additionally require independent adjudication of the 485 exact-string cases and reference validity. Do not treat identical strings as proof of correct physical interpretation.

## Closest prior art and originality gate

NL2TL already develops natural-language-to-temporal-logic translation. VLTL-Bench studies lifting/grounding; ConformalNL2LTL and SCP-NL2TL address calibrated/selective evaluation; NeuroNL2LTL combines neural translation and formal checks; VerusEval studies specification validity beyond verifier acceptance. Source-grounded parser coverage and bounded counterexamples alone are **not** novel. A publishable distinct claim requires blinded, independently adjudicated physical predicates/dynamics, provenance-separated test families and matched-coverage comparison with formal and calibrated-abstention baselines. Predeclare unsafe-acceptance metric and uncertainty intervals at the independent source-family level. If the effect vanishes, report a negative/methodological study.

## Decision rules

- Zero frozen-token matches: reject this particular dialect-token explanation for the unknown-word census.
- Positive lexical matches: proceed only to independent grammar specification and constructed semantic tests; do not infer recovered correctness.
- Any source or privacy check failure: stop and mark experiment invalid.
- Insufficient independent adjudication or source families by November 22: do not claim original model superiority or submission readiness; preserve a transparent methods report.

No user laptop computation, no incurred costs, no model inference. Disclose AI assistance in manuscripts according to venue policy.
