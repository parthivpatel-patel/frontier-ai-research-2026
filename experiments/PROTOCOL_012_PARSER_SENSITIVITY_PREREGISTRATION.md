# Protocol 012 — Pre-registered parser sensitivity audit of recorded QSTRBench outputs

Date: 2026-11-02. Status at registration: **planned, results not yet observed**. This protocol is committed **before** running the new analysis on the pinned model-output files.

## Research question and primary estimand

For the **same** recorded model outputs and reference answers, how often does changing a narrowly specified answer-extraction rule change (a) the parsed relation set or (b) the strict correct/incorrect decision? The primary descriptive estimands are paired **gained-correct, lost-correct, and total flipped** rows, with distinct affected question IDs. Report both null and non-null outcomes. This is an evaluation-robustness replication, not an AI-model improvement or a claim of a new phenomenon.

## Frozen data, code and scope

Use QSTRBench by Cohn and Blackwell (2026), https://arxiv.org/abs/2605.18380, source commit `7da82bae3b1300e8f7fba8f448adca551e0a1f9a`, three pinned compressed JSONL files and SHA/size bounds already recorded in `src/qstr_schema_audit.py`. Use `src/qstr_scoring_replication.py` as the legacy scorer. Two upstream-attributed stored output groups: GPT-5 (1,806 questions x three repeats) and Claude Sonnet 4 (1,806 questions x one repeat). No new model inference, no independent model authentication and no claim of matched model conditions. Distinct question IDs, not repeats, are the observational units for source-level summaries.

## Pre-specified, isolated interventions

1. **Compact inequality only:** Before the *unchanged* upstream `parse_answers`, replace exactly delimited `identifier!=identifier` with `identifier != identifier` in the *already cleaned* answer line. Identifiers consist of an ASCII letter followed by ASCII letters, digits or underscores. Do not change any other operator, whitespace, punctuation, answer line selection or reference. This tests the known greedy-regex quirk and may have zero incidence.
2. **First marker only:** Replace selection of the last case-insensitive substring `answer:` with the first such substring, while retaining the upstream rule of taking the first nonblank following line, the same leading/trailing cleanup, and the same relation parser. If no marker exists, use the upstream fallback unchanged. Do not combine with intervention 1.

For each intervention compute parsed-set changes, strict-score gains, losses, total flips, and distinct affected question IDs. Separately count rows with no answer marker, more than one marker, at least one compact inequality candidate on the cleaned line, empty legacy parsed set, and duplicate legacy parsed relations. These diagnostics are **not** additional interventions.

## Integrity and interpretation

Require a complete join and exact repeat coverage for every question; reject duplicates and unexpected repeats. Keep question and model-output text in memory only during bounded cloud execution; print **aggregate counts only**. No source answers, response snippets, question IDs or raw data are committed or logged. No inferential significance claim: benchmark questions share generation templates and calculi, and model repeats are dependent. A score change establishes sensitivity to the parser, **not** which answer is semantically correct. Human adjudication would be required for the latter.

**Falsification:** If there are zero flips, the hypothesis that either specified parser change materially affects this pinned sample is not supported. Even if flips occur, do not claim a novel method, physical-grounding effect or model ranking. Do not select additional parser variants after viewing outcomes without separately labeling them exploratory.

## Prior art / novelty guardrail

- Cohn and Blackwell, QSTRBench (2026), https://arxiv.org/abs/2605.18380: original benchmark, scoring and recorded responses.
- Kamalloo et al., *Evaluating Open-Domain Question Answering in the Era of Large Language Models* (ACL 2023), https://aclanthology.org/2023.acl-long.307/: established evaluation limitations beyond string matching.
- Dwivedi and Soni, *Beyond Exact Match: How Evaluation Methodology Dominates Model Choice in LLM-Based Product Attribute Extraction* (July 24, 2026), https://arxiv.org/abs/2607.22949/: direct evidence that evaluation methodology can change scores, in a different domain.
- English et al., *VLTL-Bench* (2025), https://arxiv.org/abs/2507.00877/: trace-grounded formal-translation evaluation.
- Beer et al. (2001), https://doi.org/10.1023/A:1008779610539, and Kupferman and Vardi (2003), https://doi.org/10.1007/s100090100062: classical vacuity.

The broader claim that parser choice influences AI evaluation is **not novel**. Our central NL-to-formal/physics research still requires rights-cleared real outputs, independently adjudicated intent, >=30 source-disjoint requirements and matched existing baselines. This secondary audit cannot satisfy that gate.

## Compute, spending and publication

Run Python standard library only, on standard GitHub-hosted `ubuntu-latest` for this **public** repository, <=5 minutes, read-only network access to three pinned small files, no artifacts/cache/GPU/paid services. GitHub's current public documentation states that standard GitHub-hosted runners are free in public repositories: https://docs.github.com/en/actions/concepts/billing-and-usage . Larger runners are excluded. No user laptop compute or downloads, no card, no spend. Report source attribution, AI assistance and limitations in any manuscript. November 22, 2026 remains an internal conditional target.
