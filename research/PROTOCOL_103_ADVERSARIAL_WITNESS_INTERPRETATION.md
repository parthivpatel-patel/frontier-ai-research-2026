# Protocol 103 — Adversarial witness test interpretation and falsification

Date: 2026-11-15. Status: source-level audit; no tests executed.

## Finding

Protocol 102's `test_branch_swap_changes_witness_reward` compares two *legal* observation-contingent policies under a perfectly correlated binary world distribution. The good policy `(0, STOP, (1, STOP, STOP))` has expected reward 3/2, while the swapped policy `(0, (1, STOP, STOP), STOP)` has expected reward 1/2. The latter is suboptimal, **not structurally invalid**. Both policies satisfy the no-repeated-claim and budget constraints.

The current test calls `score_witness` directly on both trees and checks their distinct rewards. It does **not** test that `bounded_certify` rejects an optimizer that returns a suboptimal but accurately scored witness. Nor can the independent witness scorer alone certify optimality: it checks legality and reward consistency, not a global upper bound.

## Concrete acceptance experiment (not yet executed)

1. Keep the two exact-rational correlated worlds `(0,0)` and `(1,1)` with mass 1/2 each, two unit-cost claims and budget two.
2. Confirm both trees pass structural validation and obtain the distinct scores 3/2 and 1/2.
3. Inject a deliberately suboptimal yet self-consistently scored witness into a controlled replacement of the optimization entry point. Verify the current witness scorer accepts its legality and score; this is **expected**, not a failure.
4. Compare the candidate value against a separate complete enumeration or independently implemented dynamic-programming oracle; require a mismatch to fail certification.
5. Mutation-test swapped branch labels, altered world mass, duplicated actions, and incorrectly claimed value as *separate* failure classes. Record which layer detects each.
6. Run under OS-enforced wall-clock and memory ceilings only after confirming a genuinely free cloud environment and account-specific eligibility. Record exact command, interpreter version, commit SHA, exit code, and logs.

## Scientific interpretation

A certificate of witness feasibility and exact expected reward is weaker than a certificate of optimality. The latter requires either exhaustive coverage with verified completeness and resource controls, or a mathematically justified independent upper bound that matches the witness value. Cross-oracle agreement is evidence against shared bugs only to the extent the oracles are genuinely independent.

No results, performance improvements, or novel algorithmic claims follow from this source audit. The proposed adaptive-verification research must still establish closest prior art in sequential experimental design, Bayesian active learning, adaptive submodularity, metareasoning, and value-of-information planning; preregister real adjudication outcomes and falsification thresholds before evaluating NLP, mathematics, and physics tasks.

## Publication gate

Do not claim optimality based on Protocol 102's branch-swap test. Do not claim experimental validation until the exact tests have run and artifacts are retained. Maintain $0 spending, cloud-only compute, no laptop workload, and separate project provenance. November 22 is a conditional decision checkpoint.
