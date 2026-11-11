# Protocol 201 — Adjudicator independence, evidence sufficiency, and identification limits

Date: 2026-11-11. Status: design and risk audit; not an empirical finding.

## Newly isolated failure mode

Protocol 200 asks reviewers whether cited evidence entails a physics claim. However, if reviewers can infer which graph edit is designated “corruption,” they can unintentionally reproduce the investigator's intended label. Agreement then measures common exposure to the experimental design rather than independent physics validation. Moreover, a cited passage can be true yet insufficient to entail a stronger claim. This protocol treats **evidence sufficiency**, **claim truth**, and **edit integrity** as distinct targets.

## Three separate questions

1. Is the claim physically true in the stated regime, with the given assumptions? A true claim may still lack adequate cited support.
2. Does the supplied evidence, *without relying on uncited background facts beyond explicitly allowed axioms*, support that claim? A false claim cannot be entailed by sound evidence, but a true claim need not be entailed by the displayed evidence.
3. Does the edit preserve the non-provenance content and change only the intended dependency? This is an intervention-integrity audit, not a physics-truth vote.

Store all three answers separately. Never equate graph feasibility, physical truth, and evidential entailment.

## Blinding and independence

- Reviewers receive randomized opaque bundle IDs, neutral instructions, and no arm labels, expected answers, graph-certificate decisions, model outputs, or other reviewers' judgments.
- The person constructing the counterfactual must not be the sole adjudicator. Reviewers must independently cite the relevant equations, assumptions, and page/section locations.
- Mix original, sham, valid-reassignment, and corruption examples with independently sourced distractors; balance obvious textual cues. Reviewers may legitimately infer an invalid edge from physics; the blinding goal is to hide investigator intention, not physics information.
- Record reviewer expertise and conflicts, whether they saw related variants, and the chronology of all judgments. To limit memory contamination, assign all variants of a problem to a reviewer in separated randomized blocks or, preferably, disjoint reviewers where feasible.
- Preserve original individual votes, rationales, disagreement, third-party adjudication, and the exact pre-adjudication dataset. Consensus is not evidence of independence when all reviewers shared the same construction notes.

## Label taxonomy and admissibility

For physical truth: true / false / assumption-dependent / unresolved. For evidence sufficiency: entails / contradicts / insufficient / ambiguous. For edit integrity: passes / fails / uncertain. Only independently supported entails-versus-insufficient/contradicts pairs with passing integrity checks enter the primary discrimination analysis. “Insufficient” is not synonymous with “false”; never score a model as wrong merely for identifying a true but unsupported statement. Disputed cases remain in the exclusion ledger with original votes and source locations.

## Falsification and negative controls

A reviewer-blind audit must check whether arm identity can be recovered from identifier format, passage length, source count, edge count, or answer-position artifacts. Train-free deterministic heuristics are sufficient for this *design check*; they are not evidence of model performance. If an arm is mechanically identifiable, repair or stratify before evaluation. If sham and valid-reassignment conditions cause rejection at rates comparable to corruptions, the provenance-discrimination interpretation fails. If reviewer disagreement is concentrated in the corruption arm, report selection and sensitivity analyses rather than removing hard cases.

## Statistical target and unit

The primary outcome remains a paired *observed natural-response acceptance contrast* across valid original and corrupted variants; report the joint response categories including abstention. Do not reinterpret it as latent forced-choice accuracy or internal causal reasoning. Cluster by independent physics problem, not prompt or variant. Freeze the unit, exclusion policy, contrasts, and multiplicity correction before the first model run. With a small corpus, report exact counts and uncertainty intervals, not unsupported asymptotic precision. A power calculation requires plausible effect sizes and problem-level variance; absent those, publish a precision table over hypothetical values explicitly labeled as scenarios, not achieved power.

## Literature collision checklist

Before any novelty statement, compare full text of explanation faithfulness interventions, process-supervision and verifier work, attribution/citation-grounding benchmarks, evidence graph and claim verification methods, and causal intervention studies. For each nearest paper record its DOI/arXiv, date, intervention unit, physical domain, response estimand, independent annotation procedure, controls, and whether it already studies the same identifiable contrast. Merely combining existing ingredients is not proof of novelty. If a direct predecessor matches all central elements, narrow the contribution to a transparent replication or benchmark.

## Cloud and integrity gate

No jobs are authorized by this document. Before cloud execution, verify the actual account's available free quota, card/billing conditions, workflow limits, and fail-closed budget protections. Do not use the user's laptop for model execution or simulations. Human adjudication is not automatically solved by free compute; if qualified independent reviewers are unavailable, describe the dataset as exploratory and unadjudicated.

## Release decision

A methods-only manuscript is permissible if it transparently reports no model experiment and no validated physics labels. A claim of physics-grounded model discrimination requires independent labels, completed controls, executed regression checks, and reproducible model outputs. November 22 is a conditional target, not evidence.
