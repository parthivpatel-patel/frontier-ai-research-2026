# Protocol 190 — Polynomial-time global eligibility via forced-edge bipartite flow

Date: 2026-11-11 UTC. Status: mathematical design and proposed verification, not executed experiment or novel algorithm.

## Correction to Protocol 189

Protocol 189 proposes exhaustive enumeration of the degree-constrained fiber to establish global semantic eligibility. Enumeration is sufficient but **not necessary** when the only structural constraints are a simple bipartite graph, fixed source and target degrees, and a fixed universe of permitted source-target pairs. In that setting, global eligibility can be decided using standard bipartite b-matching / integral maximum flow, in polynomial time. This reduces the need for exponential enumeration and can make zero-cost validation much more feasible. This is an application of established combinatorial optimization, **not a new theorem**.

## Exact decision algorithm

Let S and T be disjoint finite registered vertex sets, U subset S x T be the permitted structural edge universe for one stratum, d_s and e_t the nonnegative integer degree margins of the original simple graph E0 subset U, and A subset U the independently adjudicated semantically admissible pairs. The original must satisfy E0 subset A, or label INVALID_ORIGINAL rather than analyze interventions.

An invalid graph exists in the fixed-margin fiber if and only if at least one inadmissible pair f=(s,t) in U minus A belongs to some graph satisfying the margins.

For each such f:
1. Reject f as impossible if d_s=0 or e_t=0.
2. Force f to be present, reduce its endpoint degrees by one, and remove f from the residual edge universe (simple-graph rule).
3. Build a flow network with source-to-S capacities d'_s, S-to-T capacities 1 for all edges in U minus {f}, and T-to-sink capacities e'_t.
4. Check whether maximum integral flow equals M-1, where M=sum_s d_s=sum_t e_t. If so, the selected unit-flow edges together with f form a positive witness E1.
5. If no f in U minus A succeeds, the fiber contains no semantically invalid graph; return PROVEN_INELIGIBLE with a checkable sequence of residual infeasibility certificates (e.g. min-cut witnesses), not merely a search timeout.

Because all capacities are integral, standard max-flow integrality yields a simple graph. The argument assumes there are **no extra non-flow-expressible restrictions** such as graph connectivity, forbidden motifs, temporal causality, or multi-stratum coupled constraints. If such restrictions exist, the above test is not sufficient for the restricted fiber; mark unsupported or use a separately justified exact solver.

## Proof sketch

Necessity: Any invalid E contains at least one f in E minus A. Remove f; its remaining edges satisfy all residual margins and the residual structural universe, so they define a flow of value M-1.

Sufficiency: A residual integral flow of value M-1 gives a set of distinct permitted edges excluding f with the reduced margins. Reinsert f; the result has the original margins and contains an inadmissible edge.

The search over |U minus A| forced edges and polynomial-time flow instances is polynomial in the explicit input size. The algorithm does **not** claim that an invalid graph is reachable in one two-switch from E0; local eligibility L remains a separate question. Nor does it prove an intervention sampler is uniform or establish a provenance-specific causal effect.

## Proposed executable checks, not yet run

- Cross-check the forced-edge oracle against exhaustive enumeration for tiny registered simple bipartite graphs.
- Singleton fiber: prove ineligible.
- All pairs admissible: prove ineligible without flow calls.
- A valid forbidden-edge witness: verify margins, edge uniqueness, registration and semantic invalidity.
- Forbidden edge incident to a zero-degree vertex: reject.
- Infeasible forced-edge instance: independently validate max-flow/min-cut certificate.
- Restrict U to exclude a tempting inadmissible edge: never claim eligibility using that edge.
- Reject nonintegral, negative, mismatched or unregistered degree inputs.
- Compare L and G on enumerated small examples without assuming a counterexample exists.
- Reject cross-stratum reassignments and model-visible text changes.

## Consequences for the research

A global eligibility oracle should no longer be described as necessarily requiring exponential enumeration in the basic fixed-margin model. Enumeration remains valuable as an independent small-instance oracle and for counting or uniform sampling; deciding existence is different from counting, sampling, and estimating effects.

If an independent adjudicator has not supplied A, the mathematical oracle can only test conditional eligibility given hypothetical labels, not scientific validity. Preserve adjudication provenance and preregistration separately.

## Prior art and publication integrity

This is the standard integral max-flow reduction for bipartite degree-constrained graph realization with a forced edge. Relevant background includes the max-flow integrality theorem, bipartite b-matching, and transportation feasibility. A full-text literature audit is still required for any claim about the *experimental research contribution*. Do not claim that this reduction, the proof, or graph switching is novel.

No tests, model evaluations, physics adjudication, cloud jobs, or laptop workloads were executed to prepare this note. Additional spending: $0. Free-cloud quotas, account/card requirements and availability remain unverified. The November 22 publication target remains conditional on evidence.
