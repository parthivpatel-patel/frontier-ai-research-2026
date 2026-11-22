# Equality-constrained missing labels: exact extension and falsification plan (2026-11-22)

**Status:** mathematical design note; not an implemented or benchmarked algorithm. This extends the independent-label boundary identified in the estimand audit. No model inference, empirical performance, or novel theorem is claimed.

## Scope and estimand

For fixed paired binary predictions and acceptance decisions, write the selective-error difference as

\[
D(y)=B+\sum_{i=1}^m c_i(y_i),\qquad
B=E_A/K_A-E_B/K_B,
\]

where \(K_A,K_B>0\) are fixed accepted counts, \(E_A,E_B\) are verified accepted errors, and

\[
c_i(t)=a_i[\hat y_{Ai}\ne t]/K_A-b_i[\hat y_{Bi}\ne t]/K_B.
\]

Here \(a_i,b_i\in\{0,1\}\) are fixed acceptance flags. Unknown truths \(y_i\) are **shared** across the policies. The existing linear method optimizes each \(c_i\) separately; that is sharp only when the feasible label set is the full Cartesian product (or when separability otherwise holds).

## Exact equality-group extension

Suppose a verified constraint source establishes that all labels in each group \(G_g\) are equal, with no constraints between groups. The sharp endpoints are

\[
L=B+\sum_g\min_{t\in\{0,1\}}\sum_{i\in G_g}c_i(t),\qquad
U=B+\sum_g\max_{t\in\{0,1\}}\sum_{i\in G_g}c_i(t).
\]

**Proof:** Each group's common binary truth is a single free variable. The objective is additive over groups, so independently choosing the minimizing or maximizing group truth attains each endpoint. This proves sharpness, not merely outer bounds. The independent-label formula is recovered when every group is a singleton.

A union-find data structure can construct equality components from a list of pairwise equality constraints. Accumulating two exact-rational contributions per component then requires a linear number of case visits plus near-linear union-find operations, **not** guaranteed linear bit complexity. Outputting \(2^g\) as a count of admissible assignments requires integer storage proportional to \(g\) bits. Arithmetic complexity must be qualified accordingly.

## Parity extension

If independently authenticated constraints are of the form \(y_i\oplus y_j=d_{ij}\), with \(d_{ij}\in\{0,1\}\), a parity union-find or graph traversal assigns \(y_i=z_g\oplus p_i\) within each connected component. Contradictory cycles make the feasible set empty; they must be reported as **infeasible**, not as a zero-width interval. Otherwise evaluate the two possibilities \(z_g=0,1\) and apply the same componentwise optimization. The result is sharp under these parity-only constraints. Arbitrary global cardinality, logical, or model-dependent constraints are outside this claim.

## Mandatory adversarial checks before implementation is accepted

1. Two missing labels constrained equal, with opposite per-item contribution preferences: unconstrained bounds \([-1,1]\), constrained bounds \([0,0]\) for the specifically constructed valid fixed-denominator case. Confirm by enumerating only \(00\) and \(11\).
2. Singleton components exactly reproduce the existing independent-label implementation.
3. Equality constraints duplicated or presented in a different order do not change endpoints.
4. A parity cycle with inconsistent XOR requirements returns an explicit infeasibility error.
5. Compare exact-rational component bounds to exhaustive feasible-assignment enumeration for small random **synthetic** instances, including zero acceptance and policies with different acceptance rates.
6. Confirm that constrained intervals are subsets of the unconstrained interval, and that removing constraints cannot shrink the feasible interval.
7. Verify no component is formed merely because two claims concern the same topic; equality/parity must be independently justified by the annotation protocol.

## Scientific interpretation and failure modes

Constraints may be inferred from shared underlying facts, but annotator agreement, document duplication, or model-generated entailment is not automatically a logical equality of ground truths. Wrong constraints can yield falsely narrow bounds. Archive timestamps govern evidence availability, not label truth. If acceptance decisions change with candidate truth assignments, the fixed-denominator decomposition fails. If either accepted count is zero, the selective-risk difference is undefined and must not be assigned numeric endpoints. These are hard stop conditions.

**Falsification:** A single feasible assignment outside the proposed interval, an unattainable claimed endpoint, a missed contradictory constraint, or disagreement with an exhaustive feasible-assignment oracle invalidates the implementation. No publication claim should be made before independent cloud CI verifies these properties.

**Next action:** Implement a small, dependency-free exact-rational parity-component oracle and focused GitHub Actions tests; retain the current independent-label function unchanged and require explicit constraint provenance for the extension.
