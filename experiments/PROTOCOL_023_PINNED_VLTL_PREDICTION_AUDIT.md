# Protocol 023 — Pinned VLTL-Bench prediction-string integrity pilot

Date: 2026-11-02 (US Eastern). Session 026. Registered **before** running the new cloud audit. This is a descriptive, exploratory audit of public stored records, not a preregistered model-performance comparison.

## Research question

Do two pinned VLTL-Bench prediction files contain structurally usable, uniquely identified records and how frequently do their recorded prediction *strings* exactly match their associated reference *strings*? This is a feasibility gate for future work, not a measure of semantic correctness, physics safety, or source-independent model accuracy.

Upstream: English et al., *Verifiable Natural Language to Linear Temporal Logic Translation: A Benchmark Dataset and Evaluation Suite* (2025), https://arxiv.org/abs/2507.00877 ; public source https://github.com/Dubascudes/VLTL-Bench . Upstream already studies grounding and verification, so neither is claimed as new.

Pinned upstream commit: `383baea8210b93fe9fa7d14edd4757e5b3464e82` (GitHub commit dated 2026-05-20). Exactly two files:

1. `translation_eval/nl2tl/gt_lifting/navi.jsonl`, Git blob SHA `c21575fca5e224968b56f0192b8bc0ddbaedac46`, 356248 bytes. Compare `prediction` with `masked_tl` (lifted proposition symbols).
2. `translation_eval/nl2tl/raw_nl/conformal.jsonl`, Git blob SHA `2e340b8b8632dd212214e583d8b964043d7f15dc`, 294840 bytes. Compare `prediction` with `tl` (grounded symbols).

**No pooled accuracy estimate** across these files: they represent different tasks, datasets, representations, and potentially different model pipelines. Exact string matching is sensitive to equivalent syntax, operator aliases, and parentheses. A match is not independent validation of the natural-language meaning. A mismatch is not necessarily a semantic error.

## Frozen implementation and reporting rules

- Run **only** on the existing public GitHub standard `ubuntu-latest` hosted runner. Python standard library only; no model/API inference, GPU, paid services, notebook, artifacts, cache, or user-laptop execution.
- Fetch only the two pinned public raw URLs in the runner, in memory, with a 1 MiB per-file upper bound, a 20-second timeout, and an exact byte-count and Git-blob SHA-1 check. Reject changed/missing/malformed content. No external rows or verbatim predictions are committed, logged, or published.
- Parse UTF-8 JSONL; require nonempty file, unique non-boolean integer `id`, nonempty token arrays for `tl` and `masked_tl`, a nonempty `sentence` token array, and a `prediction` field. Report missing/blank predictions separately and do not silently count them as mismatches.
- Normalize only whitespace: `" ".join(prediction.split())` versus `" ".join(reference_tokens)`. No semantic equivalence checker or gold-assisted verifier is run. Report record count, unique IDs, blank predictions, nonblank exact matches, nonblank nonmatches, and per-file exact-match fraction among nonblank predictions. Reject unexpected reference schema.
- No cross-file deduplication or sample-size claim: IDs and token-level records cannot establish common human-source families. Do not infer a model's identity, sampling parameters, or provenance from a path name or a present-day config file.
- Test parsing and validation with constructed in-repository fixtures **without network**. Run the entire existing regression suite first. Print only aggregate audit JSON on successful cloud execution.

## Precommitted interpretation and falsification

- If a file has duplicate IDs, invalid schema, a byte/SHA mismatch, or missing/blank predictions, flag the issue; never silently repair records.
- Any observed exact match/mismatch rate remains descriptive string identity. **No accuracy, robustness, independent-source, causal, or novelty claim** follows from it.
- A high match fraction could reflect task simplicity, deterministic generation, or other mechanisms; it is **not evidence of oracle leakage**. A low match fraction could reflect formatting differences. Only independent semantics and controlled blinded baselines could adjudicate correctness.
- Upstream repository metadata has `license: null` and no root LICENSE file in the pinned tree. Public access does not establish redistribution permission. Transient analysis of two public files must not become a dataset release; stop if access or permission is withdrawn.
- Pilot eligibility for a future confirmatory paper remains **NO** without lawful reuse rights, verifiable model-generation provenance, independent human semantic labels, source-family identification, and strong matched-coverage baselines.

## Resource and disclosure

GitHub's public-repository standard hosted runners are documented as free (https://github.com/resources/insights/2026-pricing-changes-for-github-actions). No billing/card action is requested. The repository remains public and separate from all other projects. Any eventual publication must disclose AI assistance as required. The November 22, 2026 deadline is conditional on defensible results.
