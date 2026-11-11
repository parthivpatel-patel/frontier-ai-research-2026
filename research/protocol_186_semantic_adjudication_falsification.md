# Protocol 186 — Semantic provenance adjudication and falsification plan

Status: proposed protocol; **not** experimental evidence. Prepared 2026-11-11 UTC. No cloud job or model inference executed.

## The causal contrast

For physics verification item i, hold the problem statement, derivation text, constraints, token budget, output schema, model version, decoding settings, and evidence inventory fixed. Randomize only the mapping between registered derivation steps and registered evidence targets. The structural validator (Protocol 183) establishes syntactic pairing, **not** that the correct graph is scientifically correct or that the shuffled graph is scientifically false.

Define Y_i(z) as a preregistered, independently scored binary correctness outcome under provenance assignment z in {correct, shuffled}. The paired contrast is Δ = n^{-1} Σ_i [Y_i(correct) − Y_i(shuffled)] for the eligible item population. This is an experimental contrast conditional on a fixed benchmark and model, not a general claim about model reasoning.

## Independent physics ground truth

Before any model outputs are inspected, create a locked item registry with:
- an unambiguous dimensional or mathematical physics claim, explicit assumptions, derivation steps, and a worked reference solution;
- a source-to-target admissibility matrix A_i(s,t) ∈ {valid, invalid, ambiguous} justified by a human-checkable derivation or exact source span;
- a minimum of two independently admissible target edges in the correct arm and a *degree-preserving* nontrivial permutation in the shuffled arm;
- at least one shuffled edge independently classified **invalid**, with no newly valid compensating edge that makes the whole shuffled graph acceptable;
- frozen scoring rubric, abstention treatment, exclusions, item family, difficulty stratum, and item hash.

Two adjudicators should label each edge independently, blinded to arm names and model outputs. Disagreements are resolved with a third adjudicator before unblinding. Report agreement, ambiguous cases, and every exclusion. If independent adjudicators cannot be obtained at zero cost, mark the pilot **unadjudicated** and do not make semantic-validity claims.

## Hard negative controls

1. **Order-only placebo:** reorder edge serialization without changing the graph. A large effect indicates presentation-order sensitivity, not provenance truth.
2. **Both-valid swap:** swap edges where the admissibility matrix accepts both mappings. A large effect falsifies a clean provenance-correctness interpretation.
3. **No-link baseline:** remove provenance entirely while preserving the physics problem; interpret separately because token counts and input format differ.
4. **Answer leakage probe:** independently review free-text problem statements for labels, solution cues, and intervention identifiers. Syntactic key screening is insufficient.
5. **Cross-family holdout:** preregister a held-out physics family; do not tune prompts or exclusions on it.

## Falsification and reporting

Primary claim fails if the adjudicated shuffled arm is not demonstrably invalid, if structural gate acceptance differs by outcome, if assignment/exclusions are edited after outcomes, or if a preregistered paired confidence interval does not support the prespecified positive effect. Report all estimates including null and adverse results. Control familywise error for multiple models, item families, and endpoints; distinguish exploratory analyses. Do not interpret significance as novelty.

Use a paired randomization/permutation test at the item level only when the randomization mechanism supports it; otherwise use an explicitly justified paired uncertainty interval. Record the number of unique physics templates to avoid pseudo-replication from paraphrases.

## Prior-art audit required before novelty language

Compare full texts and code of work on chain-of-thought faithfulness (Turpin et al., 2023), causal mediation/faithfulness of explanations, retrieval attribution and citation faithfulness, fact verification, and process supervision (Lightman et al., 2023). These are **candidate closest-prior-art families, not verified exhaustive coverage**. Record exact claims, interventions, metrics, datasets, and overlap in a dated evidence table with URLs/DOIs. Novelty must be scoped to a demonstrated difference, never inferred from a new protocol number.

## Free-compute gate

Run standard-library unit tests and any later experiments only on an independently confirmed no-charge hosted runner with current published quotas, account eligibility, and billing/card requirements checked immediately before execution. GitHub Actions hosted-runner allowances depend on repository visibility and plan; do not equate a nominal allowance with verified account availability. Disable paid overage or fail closed if limits cannot be confirmed. No local laptop execution, large downloads, or model inference is authorized by this document.

## Release criteria

Release a methodological preprint only if it explicitly distinguishes proposed protocols from observed results. An empirical paper additionally requires passing adversarial tests, independently anchored preregistration, blinded semantic labels, real cloud-run logs, reproducible scripts, and an honest closest-prior-art matrix. The November 22 target is not grounds for relaxing these criteria.
