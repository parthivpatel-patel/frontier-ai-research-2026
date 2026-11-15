# Protocol 097 — Exact structural policy counts and preflight safety gate

Date: 2026-11-15
Status: mathematical derivation and unexecuted implementation specification; no empirical results
Scope: independent frontier-AI research; zero-cost only; no laptop workloads.

## 1. New source-level finding

Inspection of Protocol 093 confirms that its `cap` is not a process resource bound. In particular, `tuple(trees(...))` creates complete continuation collections, and input validation constructs `set(product((0,1), repeat=n))` before any policy cap is enforced. Both can consume memory before a meaningful limit is applied. This is a potential resource-exhaustion pathway, **not** an observed failure.

## 2. Exact number of complete policy trees

Let `S` be the remaining claims, `b` the remaining integer budget, and `c_i>0` each claim's cost. A policy can stop, or select any affordable `i`, after which it specifies one continuation for each possible binary observation. Consequently the number of syntactically distinct complete policy trees is

```
T(S,b) = 1 + sum_{i in S: c_i <= b} T(S\\{i}, b-c_i)^2
T(empty,b) = 1
```

The square counts ordered (failure, success) continuation pairs, including branches with zero probability; this matches Protocol 093's everywhere-defined-tree convention. The recurrence is **a structural count, not an optimal-value Bellman recursion**, and does not depend on the probability model. It can be computed by integer arithmetic with memoization, but the integer itself can grow very large. For admission control, saturate all additions and multiplications at `L+1` when the allowed maximum is `L`; this proves whether the count exceeds `L` without constructing enormous integers or policy trees.

Example: three unit-cost claims and budget two give `T(3,2)=1+3(1+2)^2=28` complete root policy trees. Three unit-cost claims and budget one give `T(3,1)=4`. These are derived mathematical counts, not executed test results.

## 3. Preflight acceptance contract

Before calling `certify`, require strict bounds on number of claims, number of binary worlds (`2^n`), budget, cost magnitudes, and saturated `T(S,b)`. Refuse the job when any bound is exceeded. Check the number of worlds before materializing a full world-key set; reject oversized `n` even if an attacker supplies a sparse dictionary. Treat a rejected instance as **not certified**, never as a zero-value optimum.

The policy-tree count is a useful upper bound on the number of root candidates to score; it is **not** a bound on intermediate Python object memory, because Protocol 093 materializes continuation tuples and can generate the same subtree repeatedly. A genuinely resource-safe implementation additionally needs streaming or indexed subtree enumeration, cloud-enforced process timeout and memory limits, and logged exit status.

For a bounded cloud CI validation, use deliberately tiny cases and require the process to exit on any preflight refusal rather than silently reducing the test set.

## 4. Proposed falsifiable cross-checks

1. Enumerate root trees for small accepted instances and compare the observed count with the saturated structural recurrence, including unequal costs, zero budget and no affordable actions.
2. Compare Protocol 093's optimum with Protocol 089's Bayesian dynamic program and Protocol 090's possible-world method on exactly identical distributions and budgets; independently score its witness using Protocol 095.
3. Permute claim indices, costs and joint-table bit positions together and verify identical optimal values.
4. Under independent binary outcomes and additive positive-success rewards, compare adaptive optimum with the exact static knapsack optimum; expected advantage must equal zero.
5. Deliberately corrupt a reward evaluator to count failures and require an asymmetric fixture to detect the mutation.
6. Record all exceptions, rejected instances and timeouts; do not report a green result from code inspection alone.

## 5. Empirical and novelty implications

Exact enumeration and Bayesian optimization are established methods, not a new AI algorithm. The research's potential contribution must be tested on held-out scientific claims with independently adjudicated truth, provenance-family separation, calibrated dependency estimates and a predeclared cost/error-sensitive endpoint. Test NLP source-grounding, mathematical proof validity and physics dimensional/reference consistency separately; avoid equating a verifier's success with scientific correctness. Compare against optimal static, independent Bayesian and equally informed adaptive Bayesian baselines.

Stop a positive novelty claim if the advantage vanishes under these comparisons, depends on leaked sources, or fails calibration/cost sensitivity. A negative result may be publishable only with appropriately narrow framing and disclosed limitations.

## 6. Execution, cloud and publication gate

No tests were run for this protocol. No cloud runner, quota, payment-card eligibility, or account-specific free allowance was verified in this session. Do not launch any job or require local execution until these are confirmed and hard spending safeguards exist. The November 22 date is a conditional scientific decision point. Disclose AI assistance and data/compute provenance in any submission.
