# Protocol 092 — Exhaustive contingent-policy certificate (design, not execution)

Date: 2026-11-15. Status: mathematical design and reproducibility specification only. No tests run, cloud allocation, or empirical result.

## Why a third implementation is necessary

Protocols 089 and 090 both solve an optimality recursion, although they represent uncertainty differently. A genuinely independent cross-check must score *complete deterministic contingent policies* against a fixed joint distribution, rather than invoke another Bellman recursion. This protocol specifies that certificate and explicitly limits its tractable scope.

## Finite setting and assumptions

There are n claims, one attempt per claim, nonnegative integer costs c_i, integer budget B, and binary adjudication-success vector x in {0,1}^n. A joint probability mass function p(x) is supplied as exact rational numbers, with nonnegative masses summing to one. No independence assumption is needed for the certificate. A policy observes each attempted claim's success/failure before selecting the next affordable unattempted claim, or stopping. Its reward in world x is the number of successfully adjudicated attempted claims. This reward does not assert that the claims are true.

A history h is an ordered sequence of distinct attempted indices and observed binary outcomes. Define remaining budget b(h) = B - sum of attempted costs. Actions A(h) are STOP plus unattempted i with c_i <= b(h). A deterministic policy is a mapping pi(h) in A(h) at every reachable history. Its score is

V(pi) = sum_{x in {0,1}^n} p(x) * sum_{i attempted by pi in world x} x_i.

A history reachable under pi must be simulated from the same policy for each world. The policy must not access x_i before attempting i. Zero-cost actions still consume one previously unattempted claim, guaranteeing termination.

## Independent exhaustive enumeration procedure

1. Precompute all possible worlds and their rational masses; reject invalid probabilities, negative costs, negative budget, duplicate indices, and malformed vectors.
2. Generate the finite set of all legal *complete contingent policies*, represented as rooted binary decision trees. At each node choose STOP or an affordable unattempted claim. For each non-STOP action independently choose one legal continuation tree for outcome 0 and another for outcome 1. Generate subtrees by structural Cartesian products; **do not choose the maximizing continuation separately or memoize optimal values**.
3. Score each complete tree by walking it separately in every possible world and accumulating exact successful-attempt rewards, weighted by p(x).
4. Take the maximum over the scored tree set. Retain the maximizing tree as an independently inspectable witness. If several policies tie, use a fixed canonical ordering only for reproducibility, not to alter the optimum.
5. Compare this maximum against Protocols 089 and 090 on exactly the same p(x), costs and budget. The certificate must also show the value of a fixed nonadaptive subset and ensure adaptive optimum >= static optimum.
6. Introduce a deliberately corrupted reward calculation in a test-only copy (e.g. count failures instead of successes) and require a known asymmetric case to detect disagreement. A mutation test is not evidence that all bugs are caught.

**Implementation caution:** Building all policies may grow super-exponentially in n. Do not claim that exhaustive n=4, B=3 is feasible without measuring resource use on a verified free cloud runner. Start with n=2, B=2; progress to n=3 and restricted budgets, with a hard cap on enumerated trees and explicit SKIP/INTRACTABLE status rather than silent pruning. A generator that replaces the Cartesian product with a maximum is no longer an independent certificate.

## Hand-checkable invariants

- With n=1, c_1 <= B, optimum is P(X_1=1); if unaffordable, optimum is 0.
- With all c_i=1 and B >= n, optimum is sum_i P(X_i=1), regardless of dependence.
- With B=1 and all costs 1, optimum is max_i P(X_i=1); observing a claim cannot improve a second decision.
- If p(x) factors across claims, the optimal expected reward equals the best feasible static subset's sum of marginal success probabilities, even when the policy may adapt to observed outcomes. This follows because previous observations do not change any unattempted claim's success probability; optional stopping and zero-cost cases must be handled explicitly.
- Relabeling claim indices, and relabeling latent states in any representation that induces the same p(x), cannot change the optimum.
- A policy's score cannot exceed sum_i P(X_i=1), and cannot be negative.

## Cross-domain empirical gate

Do not use the exact oracle as a deployable model: it receives a joint distribution unavailable for real held-out scientific claims. Before experiments, freeze a provenance-family/time split and independently adjudicated outcomes for NLP, mathematics and physics. Distinguish claim truth, verification success, cost, and abstention. Estimate success probabilities on training families only; compare realistic calibrated static and adaptive policies on held-out families under equal budgets. Report family-clustered uncertainty and sensitivity to verification cost and adjudication quality. Treat performance collapse, leakage dependence, or no improvement over strong calibrated adaptive baselines as falsification, not as a novelty claim.

## Literature and publication gate

Finite-horizon partially observable decision processes, stochastic adaptive optimization, Bayesian experimental design and budgeted active learning are close prior art. Exhaustive policy-tree scoring is a validation technique, **not a novel algorithmic contribution**. A publishable scientific advance would require an original, well-delineated problem or convincing independently reproducible empirical findings beyond these literatures. Verify precise citations and dataset licenses before manuscript submission.

## Compute and integrity

This protocol was written without running tests or models. No laptop compute, cloud workload, billable service, or expenditure is authorized. Before any future execution, check provider-specific current free-tier quota, card/billing prerequisites, runner availability, and account eligibility; cap the job to fit a confirmed zero-cost allocation. The November 22 target is conditional on successful verification. Disclose AI assistance according to venue requirements.
