# Protocol 188 — Intervention feasibility, positivity and non-identifiability audit

Date: 2026-11-11 UTC. Status: mathematical design note; no experiments or novelty claims.

## Core issue

Protocol 187 defines a paired contrast between a correct provenance graph and a semantically invalid graph while holding the evidence inventory, source degrees, target multiset, link type and scope fixed. These constraints can make an intervention mathematically impossible. A benchmark that silently drops such templates may select unusually ambiguous or densely connected derivations, biasing the population to which results generalize.

## Formalization

Within a fixed link-type/scope stratum, let registered sources be S, targets T, and edges E be a **simple bipartite graph** (no repeated ordered source-target pairs). Define source degrees d_s and target degrees d_t. Let A subset S x T denote independently adjudicated semantically admissible edges, fixed before model responses. The observed correct graph E0 must be a subset of A.

Define the degree-preserving feasible set F(E0) = { E subset S x T : E is simple, |E|=|E0|, deg_E(s)=d_s for all s, deg_E(t)=d_t for all t }. This is the fixed-margin graph fiber. An eligible invalid intervention E1 belongs to F(E0), differs from E0, and has at least one edge outside A. Preserve any additional preregistered constraints, including link scope and no answer-label leakage.

**Existence condition:** eligibility requires F(E0) to contain at least one graph with an inadmissible edge. Nonidentity of edge serialization, or even nonidentity of edge sets, is insufficient.

**Constructive sufficient condition:** if (s1,t1) and (s2,t2) are edges of E0, s1 != s2, t1 != t2, and crossed edges (s1,t2), (s2,t1) are absent, replacing the original pair by the crossed pair preserves all source and target degrees. It qualifies as a semantic corruption only if at least one crossed edge is independently inadmissible. This is sufficient, not necessary for every possible feasible transformation.

**Counterexample:** S={s1,s2}, T={t1,t2}, E0={(s1,t1),(s2,t2)} and A=S x T. The crossed swap is structurally valid but no invalid edge exists; this item is ineligible for the primary contrast. If |S|=1 and all target degrees are fixed, the fiber is a singleton: no structural intervention exists.

## Selection and estimands

Define eligibility I_i=1 if template i has at least one independently verified feasible semantic corruption. The estimand among eligible templates, E[Y_i(E0)-Y_i(E1) | I_i=1], does **not** automatically generalize to all physics-verification templates. Report a flow table of all proposed templates, structural infeasibility, semantic infeasibility, adjudication disagreement, and other exclusions. Do not choose E1 based on model outputs.

A uniform draw from F(E0) is not uniform over *semantically invalid* graphs. A single two-edge swap also induces a local-intervention estimand, not the effect of arbitrary provenance corruption. Specify the intervention distribution q_i(E1) before evaluation and publish its algorithm, random seed commitment and acceptance rules. If no feasible invalid intervention exists, record the template as ineligible; do not weaken constraints after seeing responses.

## Testable implementation properties (not executed)

1. For each proposed E1, verify both source and target degree vectors, link-type/scope partitions, edge uniqueness, source/target universes, and unchanged evidence text.
2. Require a separately signed or independently preserved admissibility matrix and at least one E1 edge outside it; a self-attested matrix embedded in the same mutable payload is not independent evidence.
3. Reject the identical graph, an order-only shuffle, and any graph whose semantic invalidity is unadjudicated.
4. Include a both-valid placebo where a distinct graph in F(E0) lies entirely inside A; report it separately.
5. Detect singleton fibers and zero qualifying swaps with an explicit reason code, not a runtime failure.
6. Test whether identifier aliases or source descriptions reveal arm assignment; blind graders to arm and randomization seed.
7. Report the selection fraction and compare eligible versus ineligible templates on preregistered, outcome-independent characteristics.

## Interpretation limits

Random assignment identifies the effect of the **delivered graph intervention** under consistency and no interference. It does not isolate internal attention, mechanistic reasoning faithfulness, or truth recognition. A large both-valid placebo response undermines a provenance-specific interpretation. A null result does not prove that the model ignores provenance if the intervention was weak or the outcome insensitive.

## Research integrity and execution gate

This note is mathematical reasoning, not a claim of a newly discovered theorem; fixed-margin bipartite graph switches and positivity are established concepts. A full-text literature audit must examine graph rewiring, citation perturbation, evidence attribution and counterfactual faithfulness before any novelty claim. No model inference, training, cloud jobs, laptop compute or paid resources were used. Cloud quota, payment-card and overage verification remains a prerequisite to execution.
