# Evaluation sensitivity to grounded proposition aliases

Working manuscript methods note — 2026-11-02. Exploratory analysis only; not a confirmed original scientific contribution.

## Question

Does exact token-string matching undercount agreement when a lifted temporal-logic benchmark assigns different proposition identifiers to the same recorded grounded predicate? This question arose *after inspecting* mismatches in a pinned VLTL-Bench file. We therefore do not describe the diagnostic as preregistered.

## Operational definitions

Let `s` be a recorded prediction, `r` the associated reference, and `D` the recorded proposition dictionary. Let `C_D` replace a whole proposition token by the numerically first symbol in its group of identifiers with **exactly equal complete grounding dictionaries**. If `D` is missing or malformed, or any referenced proposition is undeclared, `C_D` is undefined and the mismatch is unresolved. We do not rewrite operators, parentheses, scope or other tokens.

Define `E_exact = 1[s = r]` after whitespace normalization and `E_alias = 1[C_D(s) = C_D(r)]` when `C_D` is defined. The second indicator describes *conditional equality under recorded metadata*, not correctness against human meaning.

## Observations

In the pinned VLTL-Bench lifted Navi predictions (500 recorded rows), 485 strings matched exactly, 11 additional nonmatching strings became identical under `C_D`, and 4 remained unresolved. Thus exact string identity was 485/500 = 97.0%; the conditional metadata-level agreement count was 496/500 = 99.2%. The additional 11 do not represent measured model improvement.

Data source: English et al. (2025), https://arxiv.org/abs/2507.00877 . Reproduction: [Protocol 024](../experiments/PROTOCOL_024_POSTHOC_GROUNDED_ALIAS_DIAGNOSTIC.md) and [Session 027](../literature/SESSION_027_2026-11-02.md); verified cloud run https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/41525885211 .

## Conditional correctness of substitution

Assume for every time t that two proposition symbols p and q have identical truth values under a trace interpretation I. The LTL satisfaction of formulas that differ only by replacing occurrences of p with q is identical. The atomic case follows from the assumption; Boolean and temporal cases follow by induction over subformulas and future positions. This is classical substitutivity, not a new theorem.

Equality of `D[p]` and `D[q]` only asserts that the dataset recorded the same grounding. It does not independently establish the assumption, verify physical-world equivalence, or validate the original instruction. An independent ground-truth adjudication is needed before interpreting the conditional result as semantic agreement.

## Limits, falsifiers and publication policy

The diagnostic uses reference-side metadata, and therefore **cannot** be presented as a deployable verifier or a blind baseline. The file lacks authenticated independent human source-family grouping and verified redistribution rights. The four unresolved cases are not automatically errors. A confirmatory study must blind the verifier to reference and oracle fields, adjudicate intended semantics, use independent source families, match coverage and inference budgets, and compare against existing conformal and formal-verification baselines. Null or negative findings are acceptable; scientific novelty is not established.

This note is part of an AI-assisted research process. Authorship and assistance disclosures must follow publication requirements.
