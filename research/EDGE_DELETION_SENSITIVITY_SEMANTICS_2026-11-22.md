# Edge-deletion sensitivity: exact semantics and adversarial specification (2026-11-22)

Status: mathematical specification and proposed tests, not an executed experiment or novelty claim.

## A precise feasible set

Let V be the unresolved binary-label indices and E a **multiset of separately asserted evidence records** e=(i,j,d), with d in {0,1}. Each record asserts y_i XOR y_j=d. For D subset of record IDs, let F(E\D)={y in {0,1}^V: every retained record is satisfied}. Given a fixed paired-risk contrast g(y), define

S_k = union over D subset E, |D|<=k, F(E\D).
B_k = [min_{y in S_k} g(y), max_{y in S_k} g(y)] when S_k is nonempty.

The cardinality counts *evidence records*, not unique endpoint pairs or graph edges after deduplication. This matters when two independently sourced records assert the same relationship.

## Derived mathematical properties (conditional on fixed g and finite V)

1. S_k subset S_(k+1), so nonempty B_k are nested. This is immediate because deletion sets allowed at k are allowed at k+1.
2. S_|E| = {0,1}^V because deleting every record is permitted. Thus B_|E| equals the unrestricted finite-frame bound. This is a useful oracle identity, not a computational novelty claim.
3. A contradictory full graph gives S_0 empty; **B_0 is undefined**, not [0,0]. A higher deletion budget can restore feasibility. Report the minimum repair budget k_min explicitly and never present B_k for k<k_min as a valid identification interval.
4. The optimization can be rewritten as min/max g(y) over assignments y violating at most k *records*: S_k={y: number of unsatisfied assertions <=k}. Proof: delete all records violated by y; conversely every y feasible after <=k deletions violates only deleted records. This yields a simple independent exhaustive oracle for small frames and avoids enumerating deletion subsets.
5. If a constraint record is duplicated, its violation consumes two units of the record-level budget. Consequently, duplicating an assertion can change B_k even though the zero-deletion feasible set is unchanged. Never silently deduplicate without defining whether the sensitivity budget is per record, per independent source, or per unique logical claim.

## Explicit falsification fixtures

- **Contradiction:** V={0}, E={(0,0,1)}. S_0 is empty, S_1 includes both assignments. Any returned numeric interval at k=0 is a defect.
- **Conflicting pair:** V={0,1}, E={(0,1,0),(0,1,1)}. k_min=1; a zero-budget interval is invalid.
- **Duplicate penalty:** V={0,1}, E contains two distinct records asserting (0,1,0). At k=1, assignments with y_0 XOR y_1=1 remain infeasible; at k=2 they are feasible. Deduplicating the two records changes the estimand.
- **Full relaxation:** For every small graph, B_|E| must equal the unrestricted exhaustive contrast bound.
- **Nestedness:** For all k>=k_min, lower(B_(k+1)) <= lower(B_k) and upper(B_(k+1)) >= upper(B_k).
- **Oracle equivalence:** For n<=8 and m<=12, compare (a) enumeration of all 2^n assignments with <=k violated records and (b) enumeration of deletion sets with parity-consistency checks. Use exact rational g(y), no floating-point tolerance.

## Identification and statistical limits

These are *finite-frame* sharp ranges conditional on the observed acceptance/prediction pattern and chosen evidence assertions. They are not sampling confidence intervals. If acceptance depends on unresolved truth, g(y) may have label-dependent denominators and the fixed-denominator linear objective cannot be reused. If a policy has zero accepted cases, its selective risk is undefined and the contrast needs a prespecified alternative estimand; do not coerce the denominator to one.

An asserted edge is not automatically authentic merely because it is temporally admissible. In particular, a physics claim under different boundary conditions or a mathematical equivalence with missing hypotheses may be false. Provenance review and held-out label adjudication remain separate gates.

## Research positioning and next actions

The feasibility rewrite resembles a binary constraint-satisfaction problem with a bounded number of violated parity assertions (a Max-2-LIN / nearest-codeword style objective). Parity union-find handles the zero-violation feasibility case but does not establish an efficient algorithm for bounded violations. This is a **prior-art search direction**, not a claim that the method is novel or that these problems are equivalent in every computational formulation.

Implement the independent violation-count oracle in hosted CI only after confirming the actual zero-cost runner entitlement and available minutes. Compare against the existing parity solver at k=0 for consistent graphs and against the unrestricted paired solver at k=m. Record exact commit SHA, CI run ID, test counts, and failures. No AI model-performance conclusions follow from these mathematical fixtures.
