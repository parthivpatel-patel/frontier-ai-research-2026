# Source-deletion equivalence and independent validation protocol
Date: 2026-11-23
Status: theoretical derivation and preregistered test specification; no new experimental result.

## Exact equivalence

Let H be hard-label restrictions, E a finite multiset of binary parity assertions, and S the finite set of source IDs. For a candidate completion z, define V(z) = {s in S: at least one assertion attributed to s is false under z}. For integer k between 0 and |S|, define F_k = {z: z satisfies H and |V(z)| <= k}.

For any D subset S, let G(D) = {z: z satisfies H and all assertions whose sources are outside D}. Then:

**F_k = union over D subset S, |D| <= k, of G(D).**

Proof (forward): For z in F_k, choose D=V(z). Every assertion outside D holds, hence z in G(D). Reverse: If z in G(D), every violated assertion has source in D, so V(z) subset D and |V(z)| <= k.

This identity holds with inconsistent constraints, duplicate records, and multiple assertions per source. It does not depend on XOR specifically; it holds for any finite source-attributed Boolean predicates. Therefore the equivalence is not claimed as a novel theorem.

## Independent oracle

For each source subset D of cardinality <=k: delete all assertions attributed to D, enumerate assignments respecting hard labels, retain assignments satisfying remaining assertions, and union them. Compare the resulting assignment set, not merely extrema, to the violated-source counting oracle. Exhaustive reference complexity is O(sum_{j=0}^k C(|S|,j) * 2^m * |E|) without pruning. Restrict CI tests to tiny m and |S|. A scalable solver is a separate engineering problem, not evidence of novelty.

## Further falsification cases

1. Inconsistent hard labels: if H itself is contradictory, every G(D) and F_k must be empty, including k=|S|.
2. Contradictory assertions from one source: k=0 may be empty; k=1 may restore feasibility; duplicate assertions do not change the set.
3. Multiple contradictory sources: relaxing only one may remain infeasible. Check minimal deletion certificates.
4. Source IDs with zero assertions: deleting them must not alter assignments; avoid silently treating the number of distinct IDs as scientific evidence of independent provenance.
5. Source partition sensitivity: reassigning records to one shared source can change F_k; report provenance partitions and do not select them based on held-out outcomes.
6. Undefined estimands: if a completion yields a zero denominator, report the undefined subset and the policy for identification; do not silently discard it.
7. Finite-frame truth exclusion: if independently adjudicated truth is outside F_k, the assumptions are falsified for that frame; interval width alone cannot rescue the method.
8. Cross-domain evidence: NLP labels, mathematical proof correctness, and physical measurements require domain-specific adjudication; parity consistency alone does not validate any of them.

## Research-design consequence

Source deletion is an exact alternative characterization, not an independent *scientific* baseline. Its implementation can serve as an independently coded correctness oracle, but scientific comparisons must additionally include unrestricted missing-label bounds, provenance perturbations, and authenticated ground truth. Report width, truth inclusion, and failure rate together, never just interval narrowing.

## Publication boundary

The mathematics above overlaps general constraint relaxation, grouped constraint deletion and partial identification. Do not claim algorithmic originality or improved AI reliability. A defensible empirical contribution would require preregistered independently authenticated evaluations, leakage controls, transparent negative findings, and direct comparison to closest prior work.

## Compute and reproducibility boundary

This note requires no model inference, GPU, laptop computation or downloads. Any future automated tests should use bounded, standard free GitHub-hosted public-repository runners only after checking account and workflow billing settings. Do not run larger runners or paid APIs.