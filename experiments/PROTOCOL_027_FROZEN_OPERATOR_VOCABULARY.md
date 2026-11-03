# Protocol 027 — Frozen candidate-operator vocabulary diagnostic

Date: November 2, 2026. Session 030. **Exploratory, post-selected** follow-up to Protocol 026. This document is committed before running the new external-data audit. It does not assert novelty, model accuracy, or correct physical grounding.

## Research question

Protocol 026 found six nonexact lifted VLTL formula pairs unsupported on **both** sides, with 16 unrecognized word-token occurrences across twelve formula strings. Before changing parser semantics, ask whether a *fixed, independently documented* vocabulary of classical LTL operators accounts lexically for those tokens. Do not inspect or publish the token spellings from the external dataset.

## Pinned input and permitted compute

Reuse VLTL-Bench `translation_eval/nl2tl/gt_lifting/navi.jsonl` at upstream commit `383baea8210b93fe9fa7d14edd4757e5b3464e82`, 356248 bytes, Git blob `c21575fca5e224968b56f0192b8bc0ddbaedac46`. Fetch it transiently, with existing byte/size checks, on the existing **standard** GitHub-hosted `ubuntu-latest` runner for the public repository. No laptop workload, GPU, paid API, card, paid runner, artifacts, dataset redistribution, or new account. Five-minute job timeout.

## Frozen candidate dictionary (case-insensitive, whole tokens only)

- **Release:** `r`, `release`, `v` (V is an alternative release notation in some LTL tools).
- **Weak until:** `w`, `weakuntil`, `weak_until`.
- **Strong release:** `m`, `strongrelease`, `strong_release`.
- **Boolean xor:** `xor`.
- **Boolean equivalence:** `iff`, `equiv`, `equivalent`.

The names and meanings are established in [Spot's temporal-logic reference](https://spot.lre.epita.fr/concepts.html), [Spot's examples](https://spot.lre.epita.fr/ltldo.html), and [Spot's LTL operators paper](https://spot.lre.epita.fr/tl.pdf). This is an *operator-token hypothesis*, not an assertion that a candidate word actually serves as an operator in the benchmark. Any other word is **unclassified**. Existing supported operators, `prop_N` identifiers, Boolean constants, and parentheses are not counted as unknown words. Punctuation unknown to the original lexer is counted separately and never silently reinterpreted.

## Analysis locked before running external data

1. Reuse Protocol 026's validated records, exact-match partition, metadata alias grouping and restricted parser unchanged.
2. Inspect only the six previously unsupported nonexact pairs; classify unrecognized whole-word tokens into the five candidate families above or **unclassified word**, and other unrecognized tokens as **unclassified symbol**.
3. Emit aggregate counts of candidate occurrences by family; unclassified word/symbol occurrences; the number of unsupported pairs whose entire unknown vocabulary is covered by the frozen candidates; and pairs with remaining unknown tokens. Never emit raw source tokens, predictions, instructions, proposition mappings, IDs, or per-row results.
4. Reconcile the aggregate unknown-word and unknown-symbol counts exactly with Protocol 026. Fail closed if the pair partition or lexical counts disagree. No operator parsing, formula reinterpretation, or bounded equivalence rerun is permitted here.
5. Add network-free constructed tests for all candidate families, case folding, unknown words, symbols, privacy and malformed input. Run the pinned audit and regression tests on GitHub Actions only.

## Falsification and interpretation

- **If zero tokens match:** the frozen candidate vocabulary did not explain the observed syntax gap; do not invent alternative spellings post hoc.
- **If some match:** this establishes only lexical coverage, *not* that the strings parse, that the operators have the intended precedence, or that any formulas are equivalent.
- **If all match:** still do not report semantic accuracy; independently implement and cross-check operator semantics before interpreting any of the six pairs.
- **If accounting fails or source hashes differ:** invalidate the run and investigate.
- **If any source string or raw unknown token appears in output:** the privacy/reproducibility protocol fails.

The broader physical-assumption-uncertainty hypothesis remains unproven. Independent human meaning adjudication, source-family grouping, blinded comparisons and matched-coverage baselines are required for an original empirical contribution. Strong related work includes [VLTL-Bench](https://arxiv.org/abs/2507.00877), [ConformalNL2LTL](https://arxiv.org/abs/2504.21022), [SCP-NL2TL](https://arxiv.org/abs/2608.05439), [NeuroNL2LTL](https://arxiv.org/abs/2605.22874), and [VerusEval](https://arxiv.org/abs/2610.26464). No results of those methods are claimed as ours.

## Cost and publication constraints

[GitHub's billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-actions) states that standard hosted runners are free in public repositories; larger runners and storage beyond included quotas are not. This protocol uses no stored artifacts or caches. November 22, 2026 is a conditional manuscript target, not a guaranteed submission. Disclose AI assistance according to venue requirements.
