# Protocol 016 — Source-disjoint evaluation gate (design only; no real labels)

Date: 2026-11-02. **Pre-data protocol and evaluation infrastructure design, not a completed model experiment.** The existing NL2MTL collection contains only four independent original documents and therefore **fails** the minimum sample-size gate below.

## Purpose and exact unit of independence

The independent unit is the original human-authored source requirement/document cluster, **not** a generated formula, proposition, output JSON file, prompt, model run, or repeated answer. All repeated generations, extracted formulas, paraphrases, and adjudications derived from a source must share its source ID and belong to the same fold. If provenance is unknown, mark it unassignable and exclude from evaluation until resolved.

## Minimum eligibility gate

Do not produce confirmatory model-quality estimates unless at least 30 independently authored source requirements are available, predictions and original instructions are lawfully usable, and the source-to-formula mapping and human-intended semantics have been independently adjudicated. Thirty is a **practical minimum for piloting**, not a statistical power guarantee. A power calculation and precision analysis are required before inferential claims.

The 20 external NL2MTL files / 98 expressions from four sources cannot satisfy this gate. Never inflate N by treating repeats as independent.

## Locked leakage prevention algorithm

Build deterministic five-fold *group* partitions from unique source IDs, using SHA-256 of `seed || source_id` for stable ordering and round-robin fold assignment. Require >=30 nonempty, unique source IDs and no duplicate IDs; verify that every source occurs in exactly one test fold and never in another fold's training set. This grouping is for future **source-disjoint evaluation**, not a claim of balanced domain or class strata. If domains are too imbalanced, specify an additional grouped-stratified protocol *before* inspecting outcomes. Do not fit, tune, or calibrate using a held-out source's annotations.

## Annotation requirements before testing

For each independent source, two blinded reviewers independently record: (1) literal instruction and its provenance/rights; (2) atomic requirements with explicit text spans and a declared temporal semantics; (3) proposition grounding and admissible physical states/transitions, including an uncertainty set where justified; (4) a human-intended interpretation or an explicit `ambiguous / cannot adjudicate` label; (5) source-to-generated-formula mapping with `one-to-many`, `many-to-one`, or `unmatched` options; and (6) confidence and disagreement reasons. Resolve differences by a third reviewer or report unresolved items separately. Reviewers must not see the model identity or candidate score while judging intent. Do not use AI-generated annotations as independent human ground truth.

## Required baselines and estimands (future work)

- Exact logical/trace equivalence under a fixed declared physical model.
- May/must verification under an explicit set of admissible physical models.
- Grounded verification following VLTL-Bench-style methodology.
- Semantic dispersion/back-translation with abstention following SCP-NL2TL where reproducible.
- A clarification-only or abstain-all safety baseline, with matched coverage.

Report source-clustered false-accept rates, acceptance/coverage, semantic error severity, calibration, and abstention tradeoffs, with confidence intervals resampled by **original source**, not by output rows. A proposed method must improve against the strongest relevant baseline at matched false-accept risk on source-disjoint data; otherwise report the null. Predefine any domain shifts and stop rules before seeing test outcomes.

## Integrity and zero-cost constraints

This file is a research plan, not evidence of independent labels, novelty, or improved AI reliability. No inference, training, paid APIs, human hiring, or data redistribution is authorized. Source-split guard implementation and synthetic-only tests can run in the existing public GitHub repository on standard hosted runners at $0 incremental cost. The laptop is for browser access only.

Prior art: https://arxiv.org/abs/2507.00877 (VLTL-Bench); https://arxiv.org/abs/2608.05439 (SCP-NL2TL); https://arxiv.org/abs/2603.28426 (ambiguity-preserving STL); https://aclanthology.org/2026.findings-emnlp.469/ (roundtrip verification and repair); Godefroid 2013 may/must abstraction.
