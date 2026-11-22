# Constraint credibility and partial-identification sensitivity (2026-11-22)

Status: methodological proposal; no empirical results or novelty claim.

## Core problem

A parity constraint y_i XOR y_j = d_ij is a mathematical restriction on latent binary labels. The exact-rational solver is sharp *conditional on the restriction being true*. An unsupported restriction may exclude the actual label assignment and yield an interval that is too narrow. Passing unit tests does not establish the factual validity of input constraints.

## Three distinct estimands

1. **Unrestricted interval** I_0: optimize the paired selective-risk contrast over all missing-label assignments.
2. **Authenticated-constraint interval** I_A: optimize over assignments satisfying constraints independently verified from admissible pre-cutoff evidence. Require an explicit evidence record per edge and a consistent parity graph.
3. **Sensitivity family** I_k: allow deletion of up to k purported constraints before optimizing. Define I_k as the union of feasible contrast values across all edge subsets obtained by deleting at most k edges, with contradictory subsets discarded. Its reported interval is [min I_k, max I_k]. This construction is nested: I_0^sens (no deletions) is contained in I_1^sens, and so on. **Do not confuse I_0^sens with the unrestricted I_0 above.**

If constraints are independently authenticated, I_A may be reported as the primary conditional bound. Otherwise, report the unrestricted bound as primary and constraint-conditioned bounds as sensitivity analyses. A contradiction in the full edge set invalidates that conditional analysis; do not silently drop edges to manufacture feasibility.

## Falsification and robustness gates

- For every edge, record case identifiers, parity value, provenance URI, archived timestamp, claim-normalization rule, adjudicator, and a documented reason the relationship is logically necessary rather than merely plausible.
- Exclude edges inferred from model predictions, post-cutoff evidence, or the outcome being evaluated.
- Test exact equivalence against exhaustive feasible-label enumeration on small graphs, including deletion budgets k=0,1,2 and conflicting cycles.
- Verify nested sensitivity intervals and that the unrestricted interval contains every feasible constrained interval.
- Test duplicate edges, redundant transitive edges, isolated vertices, and contradictory self-edges.
- Re-run all estimates with all uncertain edges removed. If the direction or substantive interpretation changes, describe the result as constraint-sensitive.
- Cluster uncertainty estimation by shared source/claim family when dependence is present; sharp finite-frame identification bounds are not confidence intervals.

## Complexity and implementation warning

A parity graph can be solved efficiently for a fixed consistent edge set using connected components and two orientations per component. However, optimizing across all subsets of up to k potentially wrong edges is a distinct combinatorial problem. **Do not claim the sensitivity family has the original linear-time complexity.** For small authenticated test frames, exhaustive edge-deletion enumeration is a reference oracle; larger cases require a separately justified algorithm or conservative approximation.

## Cross-domain examples

In NLP, paraphrases are not automatically equivalent factual claims. In mathematics, two statements may be logically equivalent only under explicit hypotheses. In physics, claims may depend on measurement uncertainty, units, regimes, and model assumptions. These differences prohibit unreviewed automatic edge generation across domains.

## Publication gate

The paper must separately establish (a) correctness of optimization conditional on constraints, (b) factual authenticity of constraints, (c) temporally valid labels, and (d) incremental scientific value over prior partial-identification, parity/union-find, and robust optimization literature. No empirical improvement, priority, or novelty is asserted here.
