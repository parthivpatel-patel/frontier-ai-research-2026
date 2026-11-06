# Protocol 100 — Lineage validator adversarial audit

Status: static source audit, 2026-11-06. No test execution or physics adjudication is claimed.

## Scope

Inspected `research/lineage_validator.py` and `research/test_lineage_validator.py` as committed after Protocol 099. The validator currently verifies schema presence, split exclusivity by scenario and source, duplicate identifiers, and consistency of observed labels for an exact scenario/assumption/claim tuple. These checks are useful but are not evidence that a label is physically correct.

## Concrete failure modes requiring regression tests

1. **Unhashable labels.** The expression `row["label"] not in LABELS` can raise `TypeError` for a list or dictionary, rather than the documented `ValueError`. Validate `type(label) is str` before set membership, except for `None`.
2. **Unhashable assumption keys or nested mapping keys.** `json.dumps(..., sort_keys=True)` may raise `TypeError` (caught), but JSON's treatment of mixed key types and key coercion can make canonicalization ambiguous. Require string keys recursively and reject nonfinite numbers, tuples, and unsupported objects.
3. **Boolean/numeric ambiguity.** JSON encodes `true` differently from `1`, but Python treats `True == 1`. The validator should define whether physical assumption types are semantic and prohibit accidental type coercion.
4. **Whitespace normalization.** Identifiers are checked using `.strip()` but stored without stripping. Thus `"scenario-1"` and `" scenario-1 "` are distinct lineages. Either reject leading/trailing whitespace or normalize identifiers consistently before grouping.
5. **Unresolved adjudication.** `label=None` permits any non-null adjudicator value. Define whether an unresolved record may carry reviewer assignment but not a verdict, and enforce a stable schema.
6. **Truth consistency is conditional on exact claim text.** Paraphrases with identical physical meaning but different wording are not checked against each other. Add a stable `proposition_id` and `scenario_version` with externally adjudicated equivalence rather than relying on string matching.
7. **Intervention semantics.** The same `intervention_id` can appear with different assumptions under distinct claim text, and different interventions can silently share assumptions. Introduce a manifest of permitted interventions, expected changed variables, and counterfactual label relations.
8. **Source-family granularity.** Source IDs alone may not capture derivative textbooks, copied problem banks, or shared template families. Maintain an auditable `source_family_id` and block family overlap across splits.
9. **Adjudicator independence.** A nonempty string is not evidence of independent blinded review. Require a separate adjudication ledger, reviewer conflicts policy, and disagreement resolution; avoid exposing held-out labels to model prompts.

## Minimal acceptance gate

Before using these records in an empirical paper:

- Add deterministic negative tests for each malformed type and whitespace variant; expected result is a documented `ValueError`, not an uncaught `TypeError`.
- Add positive tests for controlled interventions, source-family holdouts, and adjudicated paraphrase equivalence.
- Run the complete standard-library suite on a confirmed zero-cost cloud runner; archive the workflow URL, commit SHA, Python version, exact command, and pass/fail counts.
- Keep synthetic fixtures separate from independent physics records; do not report fixture behavior as model performance.
- Freeze benchmark split manifests and acceptance criteria before comparing verifiers.

## Novelty and falsification

These are research-integrity controls, not novel AI methods. A contribution requires independently adjudicated physics tasks and competitive baselines. Falsify claims of generalizable improvement if gains disappear under source-family holdout, equal-coverage comparison, or evidence ablation, or if adjudicators cannot agree on the target truth. Report missing-label bounds and family-specific outcomes, including unfavorable ones.

## Compute and budget

This audit used source inspection only. No local laptop workloads, cloud jobs, model inference, or billable resources were started. GitHub-hosted execution must not be triggered until repository visibility, account quota, runner eligibility, billing settings, and potential overage controls have been verified. Publication target 2026-11-22 is conditional, not a deadline for unsupported claims.
