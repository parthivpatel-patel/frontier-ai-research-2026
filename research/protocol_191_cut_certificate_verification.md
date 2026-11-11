# Protocol 191 — Independently checkable forced-edge infeasibility certificates

Date: 2026-11-11 UTC. Status: mathematical specification, not an executed implementation or empirical result.

## Motivation and correction

Protocol 190 permits a PROVEN_INELIGIBLE conclusion only after **every** structurally permitted but semantically inadmissible edge has been ruled out. A maximum-flow library returning "infeasible" is not, by itself, a portable proof. This protocol specifies a short, independently checkable cut witness for each failed forced-edge instance, and a complete proof manifest. The construction is standard max-flow/min-cut duality, not a new theorem.

## Preconditions and audit boundary

For one stratum, define disjoint registered S and T, permitted edge set U ⊆ S×T, independently adjudicated admissible set A ⊆ U, observed original E0 ⊆ A, and integer degree margins d_s, e_t from E0. Check uniqueness, registration, total M=Σd=Σe, and E0 ⊆ U. If semantic labels are absent, return UNADJUDICATED; if E0 is semantically invalid, return INVALID_ORIGINAL. Extra constraints such as connectivity, time order, or coupled strata are UNSUPPORTED by this flow oracle.

For each f=(a,b) in U\\A, first rule out d_a=0 or e_b=0 by a zero-degree certificate. Otherwise construct residual degrees d'_a=d_a−1, e'_b=e_b−1, all other degrees unchanged, and residual permitted edges U'=U\\{f}. The required flow value is N=M−1.

## Negative certificate: explicit cut inequality

For any subsets X ⊆ S and Y ⊆ T, consider the source side of a flow-network cut containing the super-source, precisely the source vertices in X, and precisely the target vertices in Y. Its capacity is

C(X,Y) = Σ_{s∉X} d'_s + |{(s,t)∈U':s∈X,t∉Y}| + Σ_{t∈Y} e'_t.

All S→T capacities are one. If C(X,Y) < N, max-flow/min-cut proves that no residual feasible flow of value N exists and hence f cannot occur in a fixed-margin graph. A negative certificate must supply X, Y, f, the registered universe and degree digests, and the computed integer C; the independent checker must recompute C from immutable inputs rather than trust the reported value. There is no requirement to trust the solver's reported optimum.

For f with positive endpoint degrees, a full infeasibility certificate consists of such a strictly deficient cut. If a solver returns infeasible without a checkable deficient cut, classify that edge as UNKNOWN_SOLVER, never ruled out.

## Positive certificate

Supply a canonical edge set E1 ⊆ U with f∈E1, no duplicates, and exact original source/target degrees. Check E1\\A ≠ ∅ and E1 ≠ E0. Do not infer physical semantic correctness from a checksum or the graph alone. E1 may be returned as ELIGIBLE_GLOBAL; label ELIGIBLE_LOCAL only after a separate exhaustive legal one-switch check from E0.

## Complete global negative proof manifest

A PROVEN_INELIGIBLE result requires one entry for **every** f∈U\\A, with either a checked zero-degree reason or a checked deficient cut. Require canonical sorted enumeration of U\\A, no duplicate or omitted entries, fixed digests of S,T,U,A,E0, and deterministic checker version. If U\\A is empty, the manifest is vacuously complete and the result is PROVEN_INELIGIBLE conditional on the adjudicated A. Any unverified edge gives UNKNOWN, not a negative conclusion.

## Adversarial verification cases to implement on verified free cloud

1. Reject a cut whose claimed capacity is less than N but whose recomputed capacity is not.
2. Reject omitted or duplicated forbidden-edge manifest entries.
3. Reject cuts containing unregistered vertices or wrong-stratum vertices.
4. Reject a positive certificate with a duplicate edge or altered margins.
5. Reject E0 not contained in A; do not silently reclassify it as a corruption experiment.
6. Accept a valid zero-degree exclusion only for the corresponding forced-edge endpoint.
7. Accept a genuine deficient cut and cross-check tiny instances against exact enumeration.
8. Reject an unqualified PROVEN_INELIGIBLE claim if any edge has UNKNOWN_SOLVER.
9. Handle M=0 and an empty forbidden-edge set without underflow.
10. Require immutable independent semantic adjudication before interpreting an inadmissible edge as physically wrong.

## Scientific interpretation

These certificates establish combinatorial feasibility **conditional on the supplied semantic relation A**. They do not establish A's correctness, whether model-visible text is controlled, intervention sampling quality, causal effects, or scientific novelty. The prior-art audit should compare standard b-matching feasibility and Hall-type capacity inequalities; do not present cut duality as an original discovery.

## Resource and publication gate

This note was prepared without model inference, training, simulations, cloud jobs, laptop compute, or spending. Before any execution, verify GitHub Actions or other cloud service account-specific remaining free minutes, billing/card conditions, job configuration, and hard failure controls. Never launch jobs that could bill. No tests or experimental results are claimed. November 22 remains conditional on independent evidence and complete literature review.
