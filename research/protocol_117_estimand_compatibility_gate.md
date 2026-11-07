# Protocol 117 — Estimand compatibility gate for admitted bootstrap inference

Status: methodological audit and implementation contract; **not** an executed experiment. 2026-11-07.

## Verified code-level finding

The current `research/admitted_common_support.py` returns a heldout, matched-intervention **common-acceptance** descriptive contrast. In contrast, `research/paired_lineage_bootstrap.py` computes a weighted difference of **system-specific accepted-response risks**. These are different estimands, even when both operate on the same admitted paired intervention population. Passing the admitted rows directly to the existing bootstrap would therefore not supply a confidence interval for the common-support difference. The bootstrap's internal validator also checks duplicate keys and family membership but does **not** itself require every intervention to have both system records; callers must first invoke the Protocol 113 admission gate.

## Mathematical definitions

For intervention i and systems A and B, let a_Ai and a_Bi indicate acceptance and u_Ai and u_Bi indicate adjudicated unsafe responses. Within physics family f:

- System-specific selective risk R_Af = sum_i(a_Ai u_Ai) / sum_i a_Ai, and analogously R_Bf, whenever denominators are positive.
- Common-acceptance paired contrast D_f = [sum_i(a_Ai a_Bi (u_Ai-u_Bi))] / [sum_i(a_Ai a_Bi)], when the joint denominator is positive.
- The existing bootstrap estimates sum_f w_f (R_Af - R_Bf)/sum_f w_f, **not** sum_f w_f D_f/sum_f w_f.

Both are descriptive conditional contrasts. Neither identifies a causal effect of a model or evidence intervention without further assumptions.

## Required implementation before inferential reporting

1. Materialize records once; run `admit_matched_interventions`; require every row to be from the frozen heldout split; preserve the original identifiers and provenance.
2. Use the **same composite key** (physics_family, lineage_id, intervention_id) for both systems; reject duplicate or unmatched records. Never merge lineages from different families because their string IDs coincide.
3. Choose the estimand **before** any bootstrap execution and label outputs distinctly: `system_specific_selective_difference` or `common_acceptance_paired_difference`. Do not attach an interval computed for one to the other's point estimate.
4. For common acceptance, resample whole lineages **within each family**, keeping both systems and all interventions in each selected lineage together. Recompute joint acceptance and paired unsafe difference within each draw. Reject missing positive-weight families.
5. For any positive-weight family with zero joint acceptance, the common-support standardized point estimate is undefined. For bootstrap replicates with zero joint acceptance, count them as undefined; suppress percentile intervals when their fraction exceeds the prespecified tolerance. Report defined/undefined counts and threshold.
6. Enforce finite, nonnegative, prespecified family weights, deterministic seeded draws, and a prespecified minimum number of independent lineages. The number of interventions is **not** the independent sampling-unit count.
7. A CI is descriptive and conditional on sampling assumptions. It does not validate physical truth, adjudicator independence, causal identification, or model novelty.
8. Freeze and record evaluation manifest, reviewer provenance, acceptance thresholds, bootstrap seed, replicates, family weights, code commit, and CI-suppression policy before accessing heldout outcomes.

## Synthetic falsification fixtures to implement

- Equal coverage with disjoint accepted subsets: system-specific risks can differ while common-support risk is undefined.
- Same interventions jointly accepted with opposite unsafe labels: paired difference equals the direct arithmetic difference.
- A lineage with multiple interventions: all its interventions must be resampled as one block.
- Duplicate lineage strings in different families: composite keys remain distinct; no cross-family leakage.
- Missing system counterpart or mixed split: fail before any point estimate or interval.
- Zero joint acceptance in a positive-weight family: undefined estimate and suppressed CI.
- Permuted input order with fixed seed: exactly reproducible output.
- Undefined bootstrap replicate rate above threshold: no interval, explicit diagnostics.
- Frozen weights/thresholds altered after heldout inspection: reject as provenance violation.

## Publication gate

Do not describe a CI as uncertainty for the common-support estimand until the dedicated estimator, integration tests, and independent cloud CI have passed. Do not describe either estimand as proof of physics reasoning. Independent physical interventions, negative controls, competitive baselines, literature comparison, and blind adjudication remain prerequisites. This protocol records a code-level incompatibility, not a novel statistical theorem or empirical result.

## Compute and cost

This document requires no laptop computation or paid services. Execution remains gated on verifying the account's applicable GitHub Actions billing, quota and runner eligibility. No cloud run is authorized by this document.
