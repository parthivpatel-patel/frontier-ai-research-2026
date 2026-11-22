# Constraint provenance and falsification gate (2026-11-22)

## Scope

This note applies to the parity-constrained sharp bounds for paired selective verification. It is a protocol and mathematical validity audit, **not** an empirical result, a claim of a new theorem, or evidence that any model improves.

## What is being identified

For each policy p in {A,B}, define the selective error as (verified accepted errors + missing accepted errors)/(verified accepted count + missing accepted count), provided the denominator is positive. The estimand is selective error(A) minus selective error(B). Missing binary truths are shared across policies. If verified denominators and acceptance flags are fixed independently of the missing truth assignments, the objective is affine in the missing binary truths.

An edge (i,j,d) imposes y_i XOR y_j = d. In a consistent connected component, choose one root bit z; every other label is z XOR a known parity. Therefore each component has exactly two feasible orientations, and the minimum and maximum of the affine objective are obtained by choosing the better of these two orientations separately for each component. This proves sharpness **conditional on the constraint set being correct and exhaustive**. It does not prove that constraints extracted from natural-language documents are correct.

## New threat: constraint contamination

A model or human annotator might infer equality between two historical claims because they sound synonymous, while the claims differ in time, units, scope, measurement convention, or evidential status. Even a single false equality or XOR edge can exclude the true labeling and produce an artificially narrow identification interval. Thus interval contraction is not itself evidence of better verification.

Required provenance for every edge:
- stable IDs and exact text of both claims, with their time and domain scopes;
- logical relation (equal or opposite) and a written justification;
- source documents and immutable snapshots, including timestamps available at the experimental cutoff;
- independent adjudication of the relation, without using the tested model's prediction;
- whether the edge is logically necessary, contingent on scientific assumptions, or merely heuristic.

Only logically necessary and independently adjudicated edges may enter the primary sharp bounds. Heuristic and disputed edges belong in separately labeled sensitivity analyses.

## Falsification gates

1. **Oracle validity:** For small cases enumerate all binary assignments satisfying the edges, evaluate both selective risks directly, and compare exact rational minima/maxima with the component solver.
2. **Contradiction detection:** An inconsistent XOR cycle must be rejected, not silently assigned an empty interval or an arbitrary value.
3. **Constraint monotonicity:** Adding a consistent edge cannot widen the feasible-label identification set; the interval can only stay the same or contract.
4. **Provenance ablation:** Report unconstrained, adjudicated-only, and heuristic-augmented intervals separately. If the claimed advantage depends on heuristic edges, the primary claim fails.
5. **Chronology:** Do not admit an edge justified only by a source first available after the historical cutoff into the historical-evidence arm.
6. **Cross-domain validity:** Mathematical identity, NLP paraphrase, and physics equivalence require distinct adjudication rubrics; equal-looking statements may differ in quantifiers, boundary conditions, uncertainty, or units.
7. **Denominator validity:** If a policy accepts zero cases, selective error is undefined, not zero. Do not report a numerical paired difference in that setting.
8. **Selection stability:** If acceptance changes as missing truth is assigned, the affine objective and two-orientation component optimization need not apply; re-derive the objective before reuse.
9. **Inferential separation:** A sharp finite-sample identification interval is not a confidence interval for a population effect. Sampling uncertainty and uncertainty about edge correctness require separate treatment.
10. **Leakage:** A constraint derived from test-set ground truth, post-cutoff knowledge, or model outputs invalidates its use as an independent primary experimental input.

## Next zero-cost cloud verification

Integrate `research/test_paired_archival_parity_metamorphic.py` into the existing hosted CI test command and workflow path triggers, then inspect the run's actual job conclusion and test-step output. Execute only after confirming the repository/account's applicable free hosted-runner allowance and absence of billable exposure. No local model inference, training, downloads, or heavy computation is needed.

The empirical paper is **not publication-ready** until authenticated held-out cases, independent constraint adjudication, robust baselines, negative controls, and a documented closest-prior-art comparison are available. A methods/preregistration manuscript may accurately describe the protocol without claiming an observed AI effect.
