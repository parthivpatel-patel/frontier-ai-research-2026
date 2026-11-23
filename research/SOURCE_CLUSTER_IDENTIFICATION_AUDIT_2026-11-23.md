# Source-cluster identification: formal audit and empirical decision gate

Status: mathematical analysis and falsification plan, **not** an empirical result or originality claim. 2026-11-23.

## Exact estimand and semantics

For a fixed finite evaluation frame with missing binary labels \(y\in\{0,1\}^m\), let record \(r=(i,j,p,s)\) assert \(y_i\oplus y_j=p\) and carry provenance source \(s\). For each assignment define \(B(y)=\{s:\exists r\text{ from }s\text{ violated by }y\}\). With hard adjudicated labels \(H\) and source budget \(k\), the feasible set is
\[
F_k=\{y:y\text{ satisfies }H,\ |B(y)|\le k\}.
\]
For nonzero policy acceptance denominators, report \(\min_{y\in F_k}\Delta(y)\) and \(\max_{y\in F_k}\Delta(y)\), where \(\Delta\) is the *finite-frame* difference in selective error rates. If \(F_k\) is empty, report infeasibility rather than a numeric interval. If either denominator is zero, selective risk is undefined; do not substitute zero.

The budget counts *source identifiers*, not independent evidence events, probability of corruption, or percentage of wrong records. Thus \(k=1\) has no universal statistical interpretation. The method gives conditional identification bounds, **not** a confidence interval.

## Propositions and counterexamples

1. **Nested feasible sets.** \(F_k\subseteq F_{k+1}\). If both are nonempty and selective risk is defined, the lower endpoint cannot increase and the upper endpoint cannot decrease. Proof: the feasible-set inclusion immediately implies both extrema inequalities.
2. **Exact duplicate invariance.** Duplicating any record with the same source ID does not change \(B(y)\), so it cannot change \(F_k\) or its sharp endpoints. This does *not* hold when a duplicate is mistakenly assigned a new source ID.
3. **Source renaming invariance.** A bijective renaming of source identifiers preserves \(|B(y)|\) and all bounds.
4. **Merging is not neutral.** For two contradictory records \((0,1,0,A)\) and \((0,1,1,B)\), no assignment is feasible at \(k=0\). At \(k=1\), either parity is feasible. If A and B are merged into one source C, both parities remain feasible at \(k=1\), but the interpretation changes: one suspect cluster can now cover mutually inconsistent claims. More decisively, for \((0,1,0,A)\) and \((1,2,0,B)\), the assignment \((0,1,0)\) violates both independent sources and is excluded at \(k=1\), but becomes feasible if A and B are merged into C. Thus provenance partition is part of the identification assumption and must be frozen independently of results.
5. **Hard-label contradiction.** If adjudicated \(y_0=0,y_1=0\) and a source asserts \(y_0\oplus y_1=1\), \(F_0\) is empty, while \(F_1\) may be nonempty. Hard labels are never relaxed by the source budget.
6. **All-source relaxation.** When \(k\) is at least the number of distinct sources, every assignment satisfying hard labels is feasible; the result must equal unrestricted bounds conditional on those labels.

## Precommitted falsification gates

- Compare exact source oracle to independently enumerated label assignments on small synthetic frames, including contradictory constraints, repeated records, renaming, source merging, hard labels, zero-acceptance policies and all-source relaxation.
- Freeze a provenance policy before any held-out labels or policy outcomes are examined. Report results under alternative defensible source partitions as sensitivity analysis, not as optimized post-hoc choices.
- Independently adjudicate a held-out sample; check whether its realized finite-frame risk difference falls inside the claimed *conditional* identification interval when the authenticated source budget is satisfied. A miss under satisfied assumptions falsifies implementation or assumptions; a hit alone does not establish calibration.
- Include unrestricted bounds, record-budget bounds, and source-budget bounds with matched explicitly stated assumptions. Do not claim one uniformly dominates the other at the same numeric \(k\): their budgets have different units.
- Report infeasible and undefined cases separately. Disclose exclusions, adjudication disagreement, missingness mechanism, source dependence, and any use of model outputs to propose constraints.
- Require source-by-source comparison to partial identification, robust optimization, Max-2-LIN/group constraint satisfaction, and selective prediction before asserting novelty.

## Cloud execution and release gate

The small exact oracle is exponential in the number of missing labels; limit it to tiny synthetic fixtures on a standard public-repository GitHub-hosted runner. Before expanding tests, confirm the repository is public, the runner is standard/free, current GitHub Actions billing policy and account restrictions, and actual workflow completion. Do not run inference or training on the user's laptop, download models locally, provision paid infrastructure, or claim a passing CI run without logs.

## Interpretation boundary

This formalism applies to verification claims from NLP, mathematical reasoning, and physics only when each relation is independently justified. A paraphrase, mathematical equivalence, and physics equivalence under measurement conditions are **not interchangeable** evidence types. Domain-specific validity must be adjudicated before any parity relation is admitted.

Publication decision: methods/preregistration only until prior-art collisions, independent adjudication, and held-out evaluation have been completed. AI assistance must be disclosed according to venue rules.
