# Protocol 022 — Oracle firewall and external prediction-candidate eligibility

Date: 2026-11-02 (US Eastern). **Registered before implementation and test execution.** Session 025. This is a methodological safeguard and source-access audit, **not** a pre-registration of a real-model accuracy experiment.

## New source candidate and strict evidence limits

English et al., *Verifiable Natural Language to Linear Temporal Logic Translation: A Benchmark Dataset and Evaluation Suite* (2025), https://arxiv.org/abs/2507.00877 , describe VLTL-Bench, including grounding and trace-based verification. The public source https://github.com/Dubascudes/VLTL-Bench has recorded per-item `prediction` strings. Two directly inspected examples of file *locations* and Git blob identifiers (no data copied into our repository):

- `translation_eval/nl2tl/gt_lifting/navi.jsonl`, blob `c21575fca5e224968b56f0192b8bc0ddbaedac46`.
- `translation_eval/nl2tl/raw_nl/conformal.jsonl`, blob `2e340b8b8632dd212214e583d8b964043d7f15dc`.

A separate `t5_translation_evaluation/gpt4o_lifting/GLTL.jsonl` file has blob `a62e633e9105dc65b5c8cf66eaa170aeb545cbe4`. Source files expose `id`, `sentence`, `tl` and `prediction` fields, with variant-specific additional fields. The source's `evaluation/config.py` names API models, but **file location or configuration does not authenticate which model generated each prediction, the generation date, independence, or human-intent correctness**. Its public root `LICENSE` path was not found at inspection; this is not a legal conclusion about every file. Do not copy external rows, invoke paid model APIs, or run source evaluation notebooks until provenance and permissions are resolved.

This is a stronger **candidate** than the SecDev26 input-only source, but not a validated evaluation corpus. Its paper and scripts already study grounding, trace verification, and end-to-end reliability. Do not claim those methods as new.

## Frozen oracle-firewall checks

Implement a small standard-library-only, pure-Python evaluation interface using **constructed fixtures**:

1. The verifier-facing case must contain **exactly** `case_id`, `source_family_id`, `trial_slot`, `instruction`, `candidate_formula`, and `assumption_family_id`. All must be nonempty strings except `trial_slot`, which is a positive, non-boolean integer. Reject extra keys (including `gold`, `correct`, `ground_truth`, `tl`, `label`, `good_trace`, `bad_trace`) and missing fields. This interface is deliberately narrower than upstream datasets.
2. Require globally unique `case_id`, unique `(source_family_id, trial_slot)`, and a nonempty collection. Require a complete source-family-to-split map with values `train`, `calibration`, or `test`; all cases from one source family must remain in one split. Report counts of source families, not lexical instructions, as the candidate independence unit.
3. A frozen decision has exactly `case_id` and Boolean `accept`; a post-hoc gold record has exactly `case_id` and Boolean `correct`. Reject missing, duplicate, extra, or mismatched records. Never pass gold records into the verifier-facing case interface.
4. Post-hoc evaluation must separately report case-level coverage, case-level unsafe acceptance, conditional error among accepted cases (undefined when zero accepted), and source-family-level unsafe acceptance (a family is unsafe if **any** of its accepted cases is wrong). Do not interpret case-level counts as independent trials.
5. Construct two synthetic gold assignments for the **same** verifier-facing cases and frozen decisions to demonstrate that correctness cannot be deduced from the observable interface alone without independent semantics. This is a simple identifiability warning, not a novel theorem and not evidence of real-model failure.
6. Fail closed on malformed records and incomplete exposure. No network, external data download, API keys, GPU, training, inference, notebook, or new cloud account. Test with `python3 -m unittest discover -s tests -v` on the existing standard `ubuntu-latest` public GitHub runner; do not create Actions artifacts or caches.

## Falsification and future eligibility

- If the firewall accepts any hidden gold label, duplicates a trial slot, or permits an incomplete join, its claimed safeguards fail.
- A structural firewall **cannot prove** absence of gold leakage through developer code, side channels, memorized training examples, or evaluator-selected assumptions; future studies need independent auditing and a genuinely held-out source-disjoint evaluation.
- If the external predictions lack lawful reuse rights, verified model provenance, independently adjudicated human meanings, or source-family IDs, **do not** use them for confirmatory superiority claims.
- If a proposed physics-aware method does not improve unsafe acceptance over strong baselines at matched coverage and frozen budgets, reject the superiority claim. Negative results are publishable if properly framed.

## Prior art and resource policy

Relevant prior work: nl2spec (Cosler et al., 2023, https://doi.org/10.1007/978-3-031-37703-7_18), SynthTL (Mendoza et al., FMCAD 2024, https://github.com/dmmendo/synthTL), uncertain-system LTL checking (Gao et al., 2022, https://doi.org/10.1109/TAC.2021.3118335), VLTL-Bench (2025), SENTINEL (2025/2026), SCP-NL2TL (2026), and MANIGUARD (2026). Their existing methods sharply restrict novelty claims.

GitHub confirms standard hosted runners in public repositories remain free under its 2026 pricing: https://github.com/resources/insights/2026-pricing-changes-for-github-actions . Use only that runner; larger runners, private Actions, storage overages, paid APIs, and local laptop compute are excluded. No spending/card action authorized. Publication must disclose AI assistance as required. November 22 is conditional.
