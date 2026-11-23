# Source partition refinement: a monotonicity result and a falsification fixture

Status: theoretical consequence of the existing finite-frame definition, not a new theorem or an empirical result. 2026-11-23.

## Proposition: coarsening sources weakly expands feasibility at fixed k

Fix the same binary-label frame, hard adjudicated labels, and multiset of parity records. Let P be a partition of records into provenance clusters and let Q be a **coarsening** of P: every P-cluster lies inside exactly one Q-cluster. For an assignment y, let V_P(y) be the set of P-clusters containing at least one violated record; define V_Q similarly. There is a surjection from V_P(y) onto V_Q(y), hence |V_Q(y)| <= |V_P(y)|. Therefore

    F_k(P) subseteq F_k(Q)

for every nonnegative integer k, provided the budget is valid for both partitions. When sharp selective-risk endpoints exist, the Q interval contains the P interval. Splitting clusters reverses this inclusion. A strict expansion need not occur.

This is a combinatorial property of counting violated groups, **not** a statement that merging sources improves evidence quality or produces calibrated uncertainty. In particular, grouping all evidence under one source and allowing k=1 makes every parity record optional. Provenance grouping must be independently fixed, and the paper must report sensitivity to plausible alternative partitions.

## Minimal strict witness

Records: (0,1,0,A), (1,2,0,B). Assignment y=(0,1,0) violates both. With k=1, it is excluded under the two-source partition but admitted when both records share source C. Hard labels, if any, remain binding in both cases.

## Additional adversarial CI checks

1. For small exhaustive frames, verify that every assignment admitted under a refined partition is admitted under its coarsening at the same k, whenever both budgets are valid.
2. Verify strict inclusion for the witness above.
3. Verify equality at k=0 for every partition (all records must hold).
4. Verify equality to unrestricted hard-label bounds at k equal to the number of sources in each partition.
5. Verify that an assignment contradicting hard labels never enters the feasible set, even under full source relaxation.

## Publication and domain guardrails

This monotonicity is not a novel optimization algorithm. It provides a necessary integrity test for source-cluster evaluation. Domain-specific evidence remains essential: NLP entailment, mathematical equivalence and physics claims conditional on measurement regimes must not be converted to parity constraints merely because a model says they are equivalent. Report empty feasible sets and undefined acceptance denominators separately; these are conditional identification sets, not statistical confidence intervals.

## Cost and reproducibility

The checks require only tiny synthetic fixtures. GitHub documents that standard hosted runners in public repositories are free, while larger runners and excess artifact/cache storage can incur charges. Use the existing standard public-repository CI workflow only; do not schedule GPU jobs, install large models, or use the user's laptop for computation. Check actual run logs before reporting passes.

References:
- GitHub Actions billing (checked 2026-11-23): https://docs.github.com/en/billing/concepts/product-billing/github-actions
- Existing project definition: research/SOURCE_CLUSTER_IDENTIFICATION_AUDIT_2026-11-23.md
