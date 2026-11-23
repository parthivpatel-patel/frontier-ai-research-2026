# Source-cluster sensitivity: estimand and falsification gate (2026-11-23)

Status: mathematical design and proposed tests only. No empirical results or novelty assertion.

## Why the record-level budget is insufficient

The current violation oracle counts parity *records*. Two identical edges copied from one webpage can cost two violations, while two genuinely independent sources may each contribute one. Deduplicating exact records helps but does not solve the general problem: a single upstream source can generate several distinct, correlated assertions. Treating those as independent inflates apparent robustness.

## Source-cluster budget

Freeze a finite set of claim labels y in {0,1}^n, observed-label equalities H, and an evidence record set E. Each record e=(i,j,b,s) asserts y_i XOR y_j = b and has a provenance cluster s. Define the set of violated provenance clusters

V(y) = {s : there exists e in E with source(e)=s and (y_i XOR y_j) != b}.

For integer k >= 0, F^source_k = {y : y satisfies H and |V(y)| <= k}.

For a policy pair with nonzero frozen acceptance denominators, the source-budget identified set is the minimum and maximum of the fixed selective-risk contrast over F^source_k. Return infeasible if F is empty, and undefined if either denominator is zero. Do not use [0,0] for either case.

**Interpretation:** a single corrupted source may invalidate any number of its claims. The model assumes at most k source clusters contain at least one wrong assertion; it does not assume that all assertions from a compromised source are wrong. A source cluster is an evidence-dependence unit, not necessarily a domain, URL, or document. Syndicated articles and common upstream citations must be clustered together when dependence is known.

## Basic deductions (not novelty claims)

1. F^source_k is nested in k, hence its feasible objective range cannot shrink as k increases.
2. Duplicating any record with the same source cluster leaves F^source_k unchanged, even if it is not textually deduplicated.
3. For k >= number of source clusters, the constraint system imposes no additional restriction beyond H.
4. Contradictory records inside a single source cluster can be made jointly feasible with k=1, subject to H.
5. The record-level and source-level budgets are **not directly comparable at the same numeric k** in general: one compromised source may contain multiple violated records. In fact, with each record assigned exactly one source, the number of violated sources is <= the number of violated records for every y, so F^record_k is a subset of F^source_k for the same k. The corresponding source-budget interval is at least as wide whenever both are defined.
6. Merging source clusters weakly decreases the number of violated clusters for every y, so a fixed-k feasible set can expand. Splitting a cluster can contract it. Provenance grouping is therefore an identification assumption requiring an audit trail.

## Proposed exact oracle

For n <= 18 small-fixture claims, enumerate all binary y satisfying H. For each assignment, compute the set of source IDs on violated records; admit iff its cardinality <= k. Use exact rational selective-risk contrasts and return the sharp extrema. Do not use this exponential algorithm for full experiments. A future optimized solver may introduce one Boolean bad-source variable per cluster with implications (violated edge => bad source) and cardinality sum <= k; compare its answers to the exhaustive oracle.

## Adversarial fixtures required before publication

- Two identical records from the same source: duplicating must not change bounds.
- Two distinct records from the same source: a single k=1 relaxation can permit both to be wrong.
- Same assertions with two independent source IDs: compare to the one-source case and verify the direction of the change.
- Contradictory edges with one shared source versus two independent sources: test k=0 and k=1.
- Known observed labels contradicting a source assertion: k=0 infeasible, k=1 potentially feasible.
- Exhaustive monotonicity for k from 0 to the number of sources.
- No edges, all labels observed, zero accepted claims, and infeasible observed-label constraints.
- Randomly permute record order and consistently rename source IDs; endpoints must be invariant.
- Explicitly test nontrivial record-level vs source-level differences with the same k.

## Empirical provenance and inference

Prespecify two plausible source-clustering policies (strict shared upstream evidence and conservative merged-dependence groups) before seeing held-out errors. Report both. A source budget k is a sensitivity parameter, not a statistical confidence level or probability of truth. An observed interval that excludes the independently adjudicated truth invalidates at least one of the assumed labels, constraints, clustering, or budget. Do not claim population coverage from finite-frame sharp bounds.

## Closest mathematical connections to check

This formulation overlaps group-sparse constraint violation, group-robust optimization, Max-2-LIN/weighted constraint satisfaction, and partial identification under contaminated assumptions. The group-budget construction should be treated as a straightforward adaptation unless a source-by-source literature audit establishes a specific new theorem or application. A potential empirical contribution is *measuring* how provenance dependence changes AI-verification conclusions on independently adjudicated, frozen data.

## Cross-domain limits

In NLP, paraphrase or shared quotation is not automatically an independent source. In mathematics, equivalence needs a proof under explicitly frozen assumptions. In physics, evidence claims require units, uncertainty, calibration, and operating regime; a shared experiment or measurement instrument can induce common-source dependence. Keep domain-specific results separate.

## Execution and integrity gate

No tests were executed by creating this document. Before running hosted tests, confirm public-repository standard-runner eligibility and account spending safeguards. Never run laptop inference/training, paid GPUs, large model downloads, or unapproved services. Preserve AI-assistance disclosures and label all synthetic tests as synthetic.
