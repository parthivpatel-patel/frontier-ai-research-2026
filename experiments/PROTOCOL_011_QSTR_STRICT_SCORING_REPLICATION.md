# Protocol 011 — Recorded-model QSTRBench strict-score replication

Date: 2026-11-02. Status: **completed exploratory replication**, not a new model evaluation or a paper-level novelty claim.

## Question and scope

Can we reproduce the published QSTRBench scoring *procedure* on a pinned, openly licensed subset of recorded model outputs, with complete joins and repeat accounting, without purchasing inference or redistributing source text? This is a secondary qualitative spatial/temporal reasoning task. It is **not** an NL-to-LTL benchmark, physics simulation, robot experiment, or independently authenticated run of the named models.

## Source and rights

- Cohn and Blackwell (2026), *QSTRBench*: https://arxiv.org/abs/2605.18380
- Dataset and code: https://github.com/RobBlackwell/QSTRBench/tree/7da82bae3b1300e8f7fba8f448adca551e0a1f9a
- Source scoring: https://github.com/RobBlackwell/QSTRBench/blob/7da82bae3b1300e8f7fba8f448adca551e0a1f9a/bin/process.py
- Upstream README claims University of Leeds dataset is CC BY 4.0. Third-party SparQ, GQR, Hunspell, and Gutenberg materials have distinct terms and are not imported.
- Three source files, compressed sizes and Git blob SHA-1s are pinned in `src/qstr_schema_audit.py`. No raw questions, responses, or prompt bodies are committed or printed.

## Method

1. On a public GitHub-hosted standard `ubuntu-latest` runner, download only the three pinned files. Check exact compressed byte size and Git blob SHA-1, then decompress under explicit row, line, and cumulative size bounds.
2. Join model rows to source questions by string-normalized ID. Reject duplicate question IDs, duplicate (question, repeat) rows, unmatched IDs, missing repeats and unexpected repeats.
3. Replicate upstream `clean_answer`, `parse_answers`, `extract_relation`, and exact set equality `set(cleanAnswer) == set(correctAnswer)`. The upstream parser takes the first nonblank line after the *last* `answer:` marker; otherwise the final nonblank line.
4. Preserve upstream parser quirks rather than silently changing the scoring rule. The upstream regex parses compact `A!=B` as `=`, but spaced `A != B` as `!=`; the regression tests explicitly capture this. This is a parser limitation, not proof that any dataset row is affected.
5. Print only aggregate strict correct/total counts, type and calculus breakdowns, and question-level repeat variation. Never log individual prompts or answers.
6. For GPT-5, three repeats per question are *not* three independent questions. Compute the fraction of distinct parsed predictions and all/any repeat correctness over 1,806 question IDs.

## Verified exploratory output

Cloud run: https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/41419287326

| Upstream model label | Recorded rows | Unique questions | Strict correct | Strict score |
| --- | ---: | ---: | ---: | ---: |
| openai-gpt-5 | 5,418 | 1,806 | 4,892 | 90.2916% |
| claude-sonnet-4-20250514 | 1,806 | 1,806 | 866 | 47.9513% |

For GPT-5: repeat-0 correct 1,623/1,806, repeat-1 1,637/1,806, repeat-2 1,632/1,806; 229/1,806 questions have at least two distinct parsed predictions across repeats; 1,532/1,806 correct in all three repeats; 1,715/1,806 correct in at least one. These values describe *upstream-attributed stored responses* scored with the source procedure, not independently verified current models.

These percentages must **not** be presented as a controlled head-to-head comparison. The model versions, providers, prompting conditions, sampling and inference provenance were not independently authenticated, and the repeated-measure structures differ. The reference answers were not independently adjudicated. The upstream strict score is not a semantic equivalence proof.

## Falsification and next gate

- Confirm score agreement with the upstream published table or executable reference environment before claiming faithful end-to-end reproduction; the current test suite matches documented parser fixtures and source code, but not a separately run upstream Pandas pipeline.
- Audit whether compact inequalities, multiple `answer:` markers, empty answers, or duplicate relation tokens materially change any real scored outcomes. Any alternative parser must be declared *before* examining its outcomes and compared on the same question IDs.
- If there is no measurable scorer sensitivity, report that null result. If sensitivity exists, determine whether it is already covered by benchmark parsing literature; do not claim novelty from a parsing quirk.
- Main NL-to-formal research remains gated on at least 30 independently authored source requirements, rights-cleared model outputs, independently adjudicated meanings, source-disjoint evaluation and matched classical baselines. No result from this QSTR study substitutes for that gate.

## Research integrity and $0 constraints

The only computation was on GitHub's standard hosted runner in this public repository, using Python's standard library. GitHub's official docs state standard runners in public repositories are free: https://docs.github.com/en/actions/concepts/billing-and-usage . No credit card, paid API, GPU, paid runner, local laptop workload, artifact upload, cache or model inference was required. Availability was confirmed by successful run; no guarantee of future capacity is implied.

The project is AI-assisted. All authorship, dataset attribution, benchmark limitations and venue-specific AI-use disclosures must be reported honestly. The November 22, 2026 target remains conditional on evidence and novelty.
