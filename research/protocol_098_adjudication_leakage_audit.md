# Protocol 098 — Adjudication leakage and unit-of-analysis audit

Date: 2026-11-06. Status: preregistered methodological design; no empirical results or cloud execution.

## Research question

Can an AI scientific-language verifier reliably distinguish supported, refuted, underdetermined, and outside-model propositions when physical assumptions change, without leaking the answer through claim wording, source duplication, or adjudicator knowledge?

This is a proposed evaluation question, not a demonstrated novel method. Prior work on selective prediction, calibration, abstention, natural-language inference, scientific fact verification, dataset contamination, and physics reasoning must be compared before any novelty assertion.

## Unit of analysis and split

The independent unit is a **physical scenario lineage**, not an individual paraphrased sentence. Each lineage records a source reference, governing equations, parameter regime, boundary/initial conditions, approximation validity, observable, and adjudication method. Multiple natural-language claims, counterfactual perturbations, and paraphrases derived from that lineage must remain in the same split. A source-document lineage identifier also groups near-duplicate exercises and derivative datasets. Freeze the train/development/test partition before model prompts or thresholds are tuned.

An evidence item may be admissible only when its provenance and physical applicability are independently checkable. A model-generated explanation is not ground truth. Any claim whose verdict depends on unreported conventions must be marked unresolved, not force-labeled.

## Paired assumption interventions

For each eligible lineage, preregister one assumption-preserving paraphrase and, where physically valid, one controlled assumption change that flips the adjudicated verdict or changes it to underdetermined/outside scope. Examples to design and adjudicate (not asserted as benchmark records):

- Mechanics: change negligible drag to non-negligible drag while holding the proposition about constant horizontal velocity fixed.
- Circuits: change a steady-state ideal capacitor circuit to a transient regime while holding a DC-open-circuit claim fixed.
- Thermodynamics: change a closed system to an open system while testing an energy-balance statement.

A flip is valid only if an independent derivation documents the changed premise and resulting conclusion. If a change does not imply a unique verdict, retain it as underdetermined rather than manufacture a flip.

## Leakage and shortcut tests

1. **Paraphrase consistency:** compare verdicts on equivalent claims within a lineage, with exact paired denominators.
2. **Premise sensitivity:** score whether the verifier changes its decision appropriately when only the physical assumption changes.
3. **Label-only shortcut:** train or evaluate a lightweight lexical baseline using claim text alone; if it matches the full method, evidence-grounding claims are weakened.
4. **Evidence ablation:** remove governing-equation evidence while preserving the claim; if accuracy is unchanged, investigate shortcut learning.
5. **Source-family holdout:** hold out entire textbook/problem-generator/source lineages, not just rows.
6. **Adjudication blindness:** independent adjudicators must not see model predictions or intended intervention direction.
7. **Unresolved-label audit:** publish counts by family, perturbation type, and model decision; do not drop unresolved cases without missing-label risk bounds.
8. **Threshold lock:** freeze abstention thresholds on development data; never select test thresholds to make matched-coverage plots favorable.

## Primary and secondary estimands

Primary: difference in independently adjudicated unsafe-acceptance risk at prespecified family-specific coverage and evidence budgets. Report family risks and a frozen mixture-standardized risk, with sharp missing-label identification bounds and separate sampling uncertainty. A risk comparison is undefined when either comparator accepts zero examples in a required stratum.

Secondary: paired premise-sensitivity accuracy, paraphrase inconsistency rate, unresolved adjudication fraction, evidence-ablation degradation, and computational cost measured on a verified zero-cost cloud runner. Report both error types: false acceptance and avoidable abstention. Do not treat a classifier's own labels as independent adjudication.

## Falsification gates

The research claim fails or must be narrowed if (a) strong baselines match or exceed the proposed method at comparable family coverage and evidence budget; (b) source-family holdout eliminates gains; (c) evidence ablation does not materially affect performance; (d) apparent gains depend on unresolved labels or post-hoc mixtures; (e) physical adjudicators cannot agree on the governing assumptions; or (f) the closest prior literature already demonstrates the claimed contribution.

A methods or negative-results paper is acceptable if these gates fail. Do not claim a novel algorithm from standard stratification, Simpson's paradox, partial identification, or exact rational arithmetic.

## Execution and cost gate

Before any cloud execution, record provider, current published free-tier quota, whether a payment card/billing account is required, account-specific eligibility, repository visibility, and safeguards preventing chargeable runners or services. If any gate is unknown, do not launch. No local laptop computation, downloads, training, inference, or simulation.

## Immediate implementation acceptance criteria

Add a machine-readable lineage schema with immutable scenario/source identifiers, family, assumption set, claim text, intervention identifier, adjudicator provenance, independent label or explicit unresolved state, and split. Add deterministic validation tests rejecting duplicated IDs, cross-split lineages, contradictory labels for identical claim-and-assumption keys, and a missing adjudicator provenance for observed truth labels. Keep fixture data explicitly synthetic.

This protocol specifies a research design, not experimental evidence. Maintain publication and venue-specific AI-assistance disclosure.
