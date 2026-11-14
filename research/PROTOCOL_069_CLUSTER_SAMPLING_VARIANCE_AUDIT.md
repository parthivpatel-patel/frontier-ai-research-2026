# Protocol 069 — Cluster-sampling identification and variance audit

Date: 2026-11-14 UTC. Status: mathematical specification only; not executed, not validated experimentally, and not a novelty claim.

## Why this protocol is needed

Protocol 068 gives a general paired Horvitz–Thompson (HT) contrast. A particularly transparent special case is independent Bernoulli sampling of entire provenance families. This protocol derives its estimator and design variance directly, states its limitations, and specifies executable falsification cases. It must not be confused with a demonstrated improvement in AI verification.

## Family-level formulation

Fix the finite population, the two policies' release decisions, weights, labels and denominators before the independent evaluation sample is drawn. Let G denote disjoint provenance families. For each claim i define

z_i = w_i Y_i (R_i^C/W_C - R_i^B/W_B),

where W_C and W_B are strictly positive full-population released weights. Let Z_g = sum_{i in family g} z_i. The target is Delta = sum_g Z_g.

Sample each family independently with known probability p_g in (0,1], and adjudicate every eligible claim in a sampled family. Write S_g in {0,1} for the family inclusion indicator. The paired estimator is

Delta_hat = sum_g S_g Z_g / p_g.

Because E[S_g]=p_g, E[Delta_hat | fixed population, policies and complete truthful labels] = Delta.

Independence across selected families gives the *design variance*

Var(Delta_hat) = sum_g (1-p_g) Z_g^2/p_g.

An unbiased estimator from the sampled families is

V_hat = sum_{g:S_g=1} (1-p_g) Z_g^2/p_g^2.

For certainty families p_g=1, the corresponding term is zero. This variance is conditional on fixed policies and adjudicated truth; it does not quantify adjudicator error, model-training uncertainty, or systematic provenance misclassification. It may equal zero in a particular sample even when true design variance is nonzero. An unbiased variance estimate is not an automatic finite-sample confidence interval, especially with few selected families or very unequal probabilities.

**Pairwise subtlety:** Under all-or-none family sampling, claims within a family have joint inclusion probability p_g, not p_g^2; claims in different families have p_g p_h. Treating claims as independent understates clustering. The formula above aggregates within-family contributions before squaring. It is a special case of the general expression in Protocol 068, not an original theorem.

## Identification and feasibility boundaries

1. All relevant families require p_g>0. If any family has zero inclusion probability, a population-wide design-unbiased estimator is unavailable without additional assumptions.
2. Family membership must be frozen and must represent shared provenance/semantic duplication as credibly as possible. Undetected cross-family duplication can invalidate the intended independence of *adjudication errors*, even though design-based unbiasedness for fixed labels does not require independent outcomes.
3. Full-population denominators W_C and W_B must be computable without independent truth labels. If policy release is altered after evaluation labels are viewed, the fixed-policy proof fails.
4. Sampled-family adjudication must be complete for the stated estimand. Unresolved labels require explicit sensitivity analysis or a separate missingness design. Do not substitute Y=0.
5. The policy's operational verification budget, independent evaluation-label budget, and cloud-compute budget are distinct. Match policy budgets and release coverage before interpreting Delta as comparative effectiveness.
6. Small or rare physics families may be prohibitively expensive to adjudicate. A statistically valid sampling formula does not establish that an evaluation is feasible or that physics ground truth is obtainable.

## Deterministic negative-control examples (analytic, not test results)

- One family, p=1, Z=0.2: Delta_hat=0.2 and V_hat=0.
- One family, p=0.5, Z=0.2: if sampled, Delta_hat=0.4 and V_hat=0.04; if not sampled, Delta_hat=0 and V_hat=0. True design variance is 0.04. This illustrates why a single realized V_hat is not a guarantee.
- Two claims in the same family with contributions +0.3 and -0.3: Z_g=0, so the family's contrast contribution and variance are zero. Squaring claim contributions separately would falsely report positive variance.
- Two families, each p=0.5, Z_1=0.2 and Z_2=-0.1: true Delta=0.1 and true design variance=0.05. Across the four equally likely sample outcomes, Delta_hat is 0, 0.4, -0.2, or 0.2; their mean is 0.1 and population variance is 0.05.
- If a family has p=0, reject rather than silently removing it.
- If a released-weight denominator is zero, the corresponding FAR and paired contrast are undefined; reject.
- If an evaluation label is unresolved, do not treat the example as complete-data HT.

## Proposed dependency-free verification fixture

Implement a standard-library-only unit test using *enumeration* of all possible family inclusion sets for 1–4 synthetic families (not an empirical simulation). Check exact expectation and variance against the analytic formulas; check that average V_hat equals true variance. Add negative controls for p=0, missing labels, zero release denominator, and claim-level pseudo-replication. This is appropriate for an explicitly authorized zero-cost GitHub-hosted workflow after verifying account and Actions eligibility. No local laptop computation or large downloads.

## Closest prior art and novelty boundary

This derivation is established survey sampling, not a novel AI or physics result. Read and compare Horvitz & Thompson (1952), DOI: https://doi.org/10.1080/01621459.1952.10483446; Särndal, Swensson & Wretman (1992), *Model Assisted Survey Sampling*; and the active-auditing / off-policy-evaluation literature cited in Protocols 066–068. Source-level novelty comparison remains incomplete. A defensible research contribution would have to be an independently validated *policy or problem formulation* outperforming strong prior art under equal cost and release coverage, not the estimator itself.

## Release and cost gates

Do not interpret a negative Delta_hat without uncertainty and prespecified domain-level safety criteria. Do not claim validated NLP, mathematics or physics outcomes from synthetic checks. Manifest remains draft. Cloud quotas, card requirements, and account-specific no-cost eligibility are unverified; **no workflow is authorized to run yet**. No paid API, laptop compute, or unapproved billing. November 22, 2026 is an internal conditional target, not a promised publication date. Disclose AI assistance wherever the publication venue requires it.
