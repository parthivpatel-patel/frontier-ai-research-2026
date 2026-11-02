# Protocol 021 — Pinned SecDev 2026 NL-to-LTL access and leakage audit

Date: 2026-11-02. **Pre-specified before executing the new cloud audit.** Exploratory dataset eligibility assessment, not a model-performance study, human annotation, or novelty claim.

## Motivation and external source

Danso, Hasan, Balasubramanian, and Chowdhury (ACM SecDev 2026), *Syntax Is Easy, Semantics Is Hard: Evaluating LLMs for LTL Translation*, DOI https://doi.org/10.1145/3805773.3806005 , release a benchmark with six tasks and an NL2FutureLTL input file. The paper's use of semantic equivalence checking is direct prior art, not a technique to claim as ours.

Pinned public repository: https://github.com/ochowdhu/NL2LTL-SecDev26 at commit \`35b2b28069531f3ca5cea938182f652bacd4922a\`, branch \`main-branch\`. Input: \`input_data/nl2ltl_finalized.csv\`, Git blob SHA-1 \`9a0939aad2ecce0a20094f29e7cc87dd2e88d731\`, GitHub metadata size 39,432 bytes. Download only this pinned small text file in a standard public GitHub Actions job; reject changes in bytes, size, or schema. Do not copy the source dataset into our repository or publish its rows.

The upstream README says **CC BY-NC-ND 4.0**, whereas the root \`LICENSE\` file contains **GPL-3.0** text. This is an unresolved scope conflict; do not assume either license alone authorizes derivative dataset redistribution. The audit publishes aggregate metadata and attribution only. Any further redistribution or adaptation requires a rights review and, where needed, author permission.

## Frozen checks

1. Require exact Git blob SHA-1 using Git's \`blob <length>\\0\` prefix, a 60,000-byte upper bound, UTF-8 decoding, and exact CSV columns \`Natural Language\`, \`Ground Truth\`, \`Atomic Proposition\`. Fail closed on malformed rows, empty NL/formula, missing columns, or altered upstream bytes.
2. Report row count, unique whitespace/case-normalized NL strings, unique formulas, distinct normalized NL/formula pairs, exact duplicate pair occurrences, number of normalized NL strings mapped to multiple formulas, and number of formulas paired with multiple NL strings. These are descriptive and do **not** certify semantic errors or author independence.
3. Source-level independence remains **unverified**. Multiple paraphrases or templates may derive from the same source. Do not use unique NL count as the independent sample size or as a risk-bound denominator.
4. Inspect the pinned upstream output tree separately. At inspection time, \`output_data/\` contains only WFF result files (and an essentially empty NL2PL placeholder), **not** NL2FutureLTL model-prediction files. Do not infer model outputs from README's statement that the benchmark includes experiment scripts.
5. No model calls, paid APIs, OCaml/NuSMV compilation, GPU, large download, laptop execution, caches, or stored artifacts. The code's test fixtures are constructed, not empirical predictions.

## Falsification and decision criteria

- If hash/schema/network validation fails, report **no empirical audit result**; do not silently fall back to invented or unpinned data.
- If any normalized NL string maps to multiple formulas, flag an *annotation review candidate*, not an error: formulas might be semantically equivalent or context-dependent.
- If unique NL strings exceed 59, do **not** declare the source-level 5% risk gate satisfied: the count is not independently adjudicated original requirements, and genuine model predictions are absent.
- Treat this source as a potential benchmark/input candidate only. Confirm independent human meanings, source-family grouping, legal reuse, and authenticated per-item model predictions before confirmatory testing.
- If a new physical-constraint method does not outperform strong existing semantic verification and selective prediction at predeclared matched coverage on source-disjoint data, reject the superiority claim. The Nov 22 deadline is conditional.

## Cloud and integrity

Use the existing **public** repository's standard \`ubuntu-latest\` GitHub-hosted runner, with its five-minute timeout and standard-library Python. GitHub's 2026 policy says standard public-repository hosted runners remain free: https://github.com/resources/insights/2026-pricing-changes-for-github-actions . No payment card or new cloud account is needed for this existing setup. This is not a guarantee of future service availability. Preserve citations and disclose AI assistance as required by the eventual venue.
