# Protocol 004 — Pinned external label-inheritance audit and next evaluation gate

**Status (2026-11-01 US Eastern):** Completed narrow real-data audit; GitHub Actions **70/70 tests passed**, run https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/41375728072 . **No LLM was queried or evaluated. No novelty claim.**

## Source and immutable provenance

Chiari and Mateis, *Datasets supporting automated requirement formalization from natural language to temporal logic*, released 2026-10-25, https://zenodo.org/records/23649257 , DOI 10.5281/zenodo.23649257 . Source GitHub repository https://github.com/michiari/requirements-datasets .

- Exact upstream commit: a38a73a351c07a3d17cb561098485cd4416c5375.
- File: nl2spec-augmented/nl2spec_WordEditDistance_RandomWordsMutation_WordSwapChangeNumber_eps2_n5.csv.
- Git blob SHA-1: 6f6d2e01707e777be9cd0197698f8f19b4381fc8; checked byte-for-byte in CI.
- 5,682 bytes; 25 data rows. Full file is vendored as data/external/robustifai_number_mutations.csv with upstream MIT license notice in data/external/requirements_datasets_LICENSE.
- Original dataset authors explicitly state that semantic validation has NOT been completed. Do not call this a gold-standard dataset.

## Strict adjudication rule, frozen before broader audit

Only assess rows with:
- Original English: exact template "Whenever a is enabled, b is enabled N steps later."
- Mutated English: same template with a potentially changed number.
- Formula: exact grammar G(a -> X (X (X b))) after whitespace normalization.
- Original N = 3, consistent with three nested next-time operators.

If any condition fails, ABSTAIN. Do not extrapolate to other temporal constructs, pronouns, ambiguity, or free-form paraphrases.

Under standard infinite-trace LTL semantics, let a be true only at t=0, b only at t=k, and all other times both false. If k != 3, this trace satisfies the mutated English temporal requirement but violates the inherited G(a -> X^3 b). This is a constructive counterexample, not a learned-model output.

## Independently verified results

| Quantity | Result | Interpretation |
| --- | ---: | --- |
| External CSV rows | 25 | Source subset, not full release |
| Strict template rows | 5 | All from one original requirement |
| Witnessed inherited-label mismatches | 5 | Under the exact temporal interpretation |
| Distinct mutated step counts | 4 | 1, 2, 4, 6; four appears twice |
| Distinct original requirements | 1 | NOT five independent statistical samples |
| Other CSV rows semantically adjudicated | 0 | Explicit abstention |
| GitHub cloud tests | 70/70 passed | Engineering checks, not an AI accuracy study |

The authors' retained source labels are intentional dataset construction and explicitly unverified. This audit documents a known-risk mechanism in an actual public artifact, not wrongdoing or a novel discovery by itself.

## Pre-registration for next genuine ML/NLP experiment (NOT RUN)

1. Inspect licenses and model-output availability for TLA+-Bench, VLTL-Bench, original nl2spec, and the 2026 RobustifAI data. Do not train on or republish data without rights and attribution.
2. Define independent semantic labels on a **strictly preselected** subset; distinguish fully validated, ambiguous, and abstained rows. For numeric temporal offsets, use formal counterexample traces; for other language, do not infer intent automatically.
3. Acquire openly released actual model predictions where possible, to avoid paid inference and model downloads. If unavailable, train a genuinely learned, lightweight text baseline on free public GitHub-hosted CPU only. A deterministic grammar is a control, not an ML model.
4. Split by **source requirement**, not by individual mutation rows, and hold out transformation families. Do not let near-duplicate variants of one original cross train/test boundaries.
5. Baselines: inherited-reference exact-match, strict temporal witness checker, oracle-aware scorer, and abstention. Match access to reference meanings; do not compare a model with extra truth against one without it.
6. Outcomes: confirmed semantic disagreements on independently justified examples, coverage, abstention, false-positive rate, and changes in model ranking (if real model outputs available). Report uncertainty clustered by independent source requirement; never treat the five same-source mutations as five independent observations.
7. Negative controls: unchanged numbers, equivalent paraphrases when independently verified, unsupported grammar, corrupted source hash, and intentionally incorrect source labels.
8. Stop conditions: no independent ground truth; all effects explained by simple label leakage; prior work already covers the same method/benchmark; insufficient independent samples; no learned-model results.

## Physics integration limitation

The separate exact reflecting-particle and damped-motion suites establish physically reachable counterexample trajectories, but the external numeric-mutation dataset concerns temporal propositions, not physical motion. **No combined physical-NLP experiment has been performed.** Future integration must use independently justified natural-language interpretations and physically admissible interventions, and distinguish physical hypothesis separation from human-intent identification.

## Compute, costs and disclosure

All code uses the Python standard library on standard GitHub Actions runners for this public repository. No GPU, paid API, card, user laptop, or large download. GitHub Actions run 41375728072 succeeded. The dataset snapshot is 5.7 kB. No spend initiated. Internal target 2026-11-22 is conditional on novelty, fair baselines, reproducibility and publication standards. Disclose AI assistance where required.
