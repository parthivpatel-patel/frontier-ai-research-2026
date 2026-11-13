# Protocol 054 — Least-favorable truth probability and exact randomized-policy certificates

Status: analytical derivation and reproducibility specification, **not** an original minimax theorem, executed experiment, or demonstrated AI improvement. 2026-11-13.

## Objective

Protocol 053 correctly distinguishes deterministic from randomized minimax decisions. This protocol adds a *dual certificate* and a finite exact-arithmetic solution method, so an independent implementation can challenge the randomized optimization without relying on an external LP solver.

For truth probability p in [L,U], actions A (accept), R (reject), X (abstain), and costs a>0, b>0, c>=0, define the action loss vector

    ell(p) = (a(1-p), bp, c).

The randomized decision q belongs to the three-action simplex. Its robust value is

    V = min_q max_{p in [L,U]} q · ell(p).

Because the objective is bilinear in q and p and both strategy sets are compact and convex, the finite-dimensional minimax theorem gives

    V = max_{p in [L,U]} min{a(1-p), bp, c}.

The maximizer p* is a **least-favorable truth probability**, not a calibrated estimate of real-world truth and not an identified posterior. It is an adversarial witness for the robust policy objective.

## Exact finite candidate set

The lower envelope g(p)=min{a(1-p), bp, c} is continuous, concave, and piecewise affine. Its maximum over [L,U] occurs at an endpoint or an intersection of two action-loss lines. Therefore evaluate g at the following candidates that lie in [L,U]:

- L and U;
- p_AR = a/(a+b), where accept and reject losses meet;
- p_AX = 1-c/a, where accept and abstain losses meet;
- p_RX = c/b, where reject and abstain losses meet.

All values can be represented by Python fractions.Fraction; no floating-point tolerance or numerical optimizer is required. If c=0, the dual value is zero. If L=U, the problem reduces to choosing the least costly action at that p.

This candidate enumeration is a proof of the *value* V. To certify a proposed primal randomized policy q, independently verify (i) nonnegative weights summing to one and (ii) both endpoint risks at most V. Then weak duality and the matching dual candidate establish global optimality. An algorithm that outputs only V without a feasible q is not a complete policy implementation.

## Analytical certificates

Protocol 053 example: L=3/4, U=1, a=4, b=1, c=2. The dual candidate p_AR=4/5 gives g(4/5)=4/5; q=(1/5,4/5,0) gives endpoint risks (4/5,4/5). Hence V=4/5 exactly.

With the same interval and a,b but c=1/5, p_AR gives g(4/5)=1/5; pure abstention q=(0,0,1) has risk 1/5 at both endpoints. Hence V=1/5 exactly.

A further negative control: L=0, U=1, a=b=1, c=1. The dual p_AR=1/2 yields V=1/2, and q=(1/2,1/2,0) attains it. Pure acceptance or rejection has robust loss 1. A point interval L=U=1 has V=0, attained by pure acceptance. These are constructed arithmetic cases, not model results.

## Independent validation specification

Implement two separate pure-standard-library components:

1. A dual oracle enumerating the finite rational candidate set and returning V and all maximizing candidates.
2. A primal certificate checker that takes externally supplied rational weights, checks simplex constraints, computes both endpoint risks, and accepts an optimality claim only when max endpoint risk equals the independently computed dual V.

Use adversarial tests for invalid costs, reversed intervals, zero abstention cost, point intervals, ties, boundary intersections, and non-optimal feasible q. A grid can test *certificates* for candidate policies, but grid search alone cannot prove primal optimality. Never claim a passing suite until executed on verified free cloud infrastructure.

## Relevance, falsification, and limits

This derivation improves the *auditability* of a proposed dependence-aware AI abstention method. It does not establish a new mathematical algorithm, and it does not resolve the identification failure documented in Protocols 050–051. In particular, a least-favorable p* is not evidence that an AI claim has probability p* of being true.

Any future empirical paper must compare against established robust Bayes/minimax and reject-option baselines, test claim-disjoint generalization and dependence shift, and measure false-accept frequency separately from expected loss. A physics contribution must be based on a testable physical mechanism or domain-specific evaluation, not borrowed terminology.

**Stop condition for novelty:** If the only contribution is applying this standard duality to existing verifier bounds, do not describe it as a novel frontier-AI method. Seek a distinct, reproducibly demonstrated algorithmic or empirical contribution before publication.

## Infrastructure and integrity gate

No tests or models are reported as run here. Use only account-verified zero-cost standard GitHub-hosted runners, after verifying repository permissions, billing safeguards, quota and actual runner eligibility. Do not trigger workflows before that gate is satisfied. No local laptop execution, paid services, credit-card requirement, large downloads, or GPU assumptions. November 22 remains a conditional internal target.
