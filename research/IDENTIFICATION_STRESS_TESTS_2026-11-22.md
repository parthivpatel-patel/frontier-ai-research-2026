# Identification stress tests and failure taxonomy (2026-11-22)

**Status:** analytical design note, not empirical results, novelty proof, or a claim of model improvement. Complements the evidence-admission protocol and held-out preregistration. No model execution was performed.

## Estimands and denominators

For a frozen claim frame of size n and policy p, let A_ip in {0,1} denote its fixed accept/abstain decision, Y_i in {0,1} the shared (possibly unknown) truth, and H_ip in {0,1} the frozen binary prediction. Define D_p = sum_i A_ip. When D_p > 0, the selective error is R_p(Y) = (sum_i A_ip 1[H_ip != Y_i])/D_p. The paired difference is Delta(Y) = R_p(Y)-R_q(Y), with *one common Y_i* across policies. When either denominator is zero, Delta is undefined; never replace it with zero.

Let K be independently adjudicated labels and U the unresolved labels. Holding acceptance, predictions, and denominators fixed, Delta(Y) = C + sum_{i in U} g_i(Y_i), where C is the known-label contribution and g_i(y) = A_ip 1[H_ip != y]/D_p - A_iq 1[H_iq != y]/D_q. For unconstrained binary unknown labels, the sharp endpoints are C + sum min(g_i(0),g_i(1)) and C + sum max(g_i(0),g_i(1)). The endpoints are attainable by choosing each unresolved Y_i independently. This is a separability result under *explicit* assumptions, not a claim of mathematical novelty or bit-complexity O(n).

## Counterexamples that must be retained

**Shared-label dependence.** One unknown item, both policies accept, p predicts 0, q predicts 1. If Y=0 then Delta=-1; if Y=1 then Delta=+1. Thus the paired sharp interval is [-1,+1]. Independent marginal error intervals are both [0,1], but combining their independently chosen endpoints without respecting common truth can imply unattainable pairs, such as both policies having zero error simultaneously.

**Cross-item label constraints.** Two unknown items with a trusted external constraint Y_1=Y_2. Policy p accepts only item 1 and predicts 0; policy q accepts only item 2 and predicts 1. The unconstrained separable construction yields [-1,+1] for Delta, whereas the actual constrained Delta is exactly -1 when both labels are 0 and +1 when both are 1 (same endpoints here, but a disconnected feasible set). More starkly, set p to accept both items with predictions (0,1), and q to accept both with predictions (1,0). With Y_1=Y_2, Delta is always 0, whereas unconstrained labels allow Delta in [-1,+1]. Do not apply the separable formula when labels have verified coupling constraints.

**Endogenous acceptance.** If a policy changes its acceptance decisions after a missing label is revealed, D_p is not fixed. The linear decomposition no longer follows. The correct analysis must freeze the decision policy or explicitly optimize over the resulting joint decision rule.

**Archive chronology.** A webpage with a claimed publication date before cutoff but first authenticated capture after cutoff is not sufficient evidence that its *captured content* existed before cutoff. Treat it as unavailable absent independent contemporaneous proof. A post-cutoff correction to a previously available document is a distinct version.

**Truth versus evidence.** A pre-cutoff source may be wrong; a post-cutoff source may correctly describe historical truth. Use separately audited time-indexed truth and availability labels.

## Locked cloud validation plan

1. Construct tiny enumerated cases covering each counterexample above and assert the exact rational endpoints, including an explicit undefined-denominator outcome.
2. Compare the linear implementation against exhaustive shared-label enumeration for every small fixed-policy case within the selected finite grid; publish grid specification and count, not an invented coverage percentage.
3. Add permutation, policy-swap, prediction-complement and duplicate-case tests. Duplication invariance requires *all* case weights and both accepted denominators to scale together; do not apply it to partial duplication.
4. For coupled-label cases, implement a separate constrained exhaustive oracle on tiny instances. It must be treated as an out-of-scope detector for the linear formula, not silently used to validate the unconstrained theorem.
5. Record exact commit, Python version, runner label, test counts, and Actions job URL. Run only after checking current GitHub public-repository free-runner eligibility and repository settings; do not use larger or paid runners.
6. Do not claim successful execution until the relevant job steps are observed passing.

## Scientific decision rules

**Reject mathematical correctness** if a fixed-policy unconstrained case disagrees with exhaustive enumeration, or if zero denominators produce numeric results. **Reject temporal-integrity claims** if a future-evidence trap is admitted or if a post-cutoff snapshot is treated as proof of pre-cutoff availability. **Reject generalized AI performance claims** without independently authenticated held-out evaluation, model/version provenance, and explicit source/model leakage caveats. **Reject novelty claims** until nearest prior work in selective classification, partial identification, and temporal evidence auditing is compared at the level of assumptions and estimands.

The current deliverable remains a methods/preregistration candidate, not an empirical discovery paper. No physics-model results, NLP model gains, or new theorem are asserted.
