# Protocol 014 — Pinned NL2MTL output structure audit (registered before full inventory)

Date: 2026-11-02. **Pre-analysis protocol.** This audit is descriptive and schema-level, not a test of model correctness, novelty, or independent human intent.

## Source and prior inspection

Upstream: https://github.com/marisol-barrientos/nl2mtl at commit `c8cd92f7f46da57848cf9f6af494219f8683d1b3`. Git tree inspection identified four original source documents and five output runs, each with one JSON output per document (20 JSON files). Pilot inspection of `test_1/article_78.json`, `test_2/article_78.json` and `test_1/cara_pump_requirements.json` revealed a top-level `MTL_expressions` array with variable lengths (4 vs 6 for the first source); this variability is **already known before registration** and is not a prospective discovery.

## Locked descriptive estimands

For all 20 JSON outputs, report: count of JSON files successfully verified against Git blob hashes; per-source five-run expression counts (min, max, mean); total expressions (not independent source requirements); number of documents with varying extraction counts; number of empty formula strings; number of expression records with at least one proposition; number of proposition records with nonempty ambiguity or assumption fields (record exact JSON types, do not infer semantics); number of dependency edges and references that fail to match local expression IDs; count of non-formalized parts. Preserve the four-document clustering; do not align expression records by index or ID across runs.

No p-values or confidence intervals: this is a complete descriptive audit of a small, selected artifact collection. Do not convert annotation presence to correctness, and do not call upstream-attributed outputs authenticated GPT-4 inference. Unknown rights over source texts and generated outputs mean **no copied source texts, formulas, predictions or JSON files** are committed or printed. Only aggregate counts and structural diagnostics may appear in logs/reports.

## Reproducibility and fail-closed constraints

Fetch 20 pinned raw GitHub files on the **public repository's standard GitHub-hosted Ubuntu runner only**, via Python standard library, with per-file size <= 20 KB and per-request timeout <= 10 seconds. Verify each file's Git blob SHA-1 against its expected SHA recorded in this protocol's companion implementation; refuse mismatches, missing files, wrong types or malformed JSON. Never use a token, model API, GPU, user laptop, paid runner, artifacts, cache or package installation. Unit tests use synthetic in-memory fixtures and never contact the network. Runner job timeout <= 5 minutes, read-only `contents` permission.

## Falsification / stopping rules

- If any pinned file or hash cannot be verified, report **incomplete** and do not claim a complete 20-file census.
- If all schema fields are present but extraction counts vary, classify *alignment ambiguity* only, not semantic/model failure.
- If all output counts were identical, report that negative outcome; even equal counts do not prove alignment.
- A source-disjoint model evaluation remains blocked until >=30 independently authored requirements, legally reusable predictions, independent intended-meaning adjudication, and matched verification/abstention baselines are available.
- Compare against Barrientos et al. (2025), English et al. VLTL-Bench (2025), Wang et al. SCP-NL2TL (2026), Newcomb and Ochoa (2026), and classical model checking; no originality claim from output instability alone.

## Spending and integrity

GitHub documentation verified 2026-11-02: standard GitHub-hosted runners for public repositories are free; larger runners are billed (https://docs.github.com/en/billing/concepts/product-billing/github-actions). This public repository already uses standard `ubuntu-latest` with successful free runs. No payment method or card is needed for this eligible standard-runner workflow; no new cloud service is introduced. Additional spending $0. Disclose AI-assisted development in the eventual paper as required; preserve negative results. November 22 target conditional.
