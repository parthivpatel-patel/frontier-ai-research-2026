# Protocol 094 — Certificate audit, scope limits, and pre-execution acceptance gate

Date: 2026-11-15. Status: source-level audit only; **no code executed** and no empirical AI results.

## Source inspected

Read `research/fixtures/test_protocol_093_complete_policy_trees.py` and Protocol 092 from the public default branch. Protocol 093 does enumerate structural pairs of continuation trees and scores each complete tree across the full joint possible-world distribution; it does not use a Bellman maximum. This meets the *algorithmic-independence design criterion*, but does not yet constitute an executed certificate.

## New audit finding: the cap is not a reproducible policy-count limit

In `certify`, `count[0]` increments once at every recursive `trees` invocation and once for every emitted non-STOP root tree. It does **not** increment for emitted STOP trees. Moreover, the same subproblem's continuation sets are rebuilt independently for left and right outcomes. Thus `cap` is a **mixed generator-work counter**, not a maximum number of complete policies scored, and its value depends on traversal and duplicated subtree construction. The returned `ntrees` counts scored top-level policies, a different quantity. The exception message, “tree generation cap exceeded,” is directionally accurate, but a reader must not interpret the cap as a bound on total CPU time, memory, or policies.

Required correction before cloud execution: report separately (a) complete policies scored, (b) generated subtree nodes / invocations, and (c) maximum materialized continuation size. Impose an explicit upper bound on materialized continuation size *before* constructing the Cartesian product. A counter incremented during generation is not a hard memory bound because the continuation tuples are fully materialized.

## Input-contract and witness checks

1. `worlds` is required to contain every binary world; verify that tuple keys are of length `n` and bits are precisely integers 0 or 1 (the current equality against `itertools.product` enforces this indirectly).
2. The code accepts integer masses and `Fraction` masses and rejects floats; add tests for booleans (Python's `bool` is a subclass of `int`, but `type` checks currently reject them), negative masses, missing/extra worlds, malformed costs, and zero/negative caps.
3. Witness trees should be validated by a *separate* checker: each index appears at most once along a path, each action is affordable on its path, both outcomes are represented, and scoring the witness directly reproduces the reported maximum.
4. Add permutation invariance for the full-policy enumerator itself, not only for prior oracle implementations.
5. Compare Protocol 093 to Protocols 089 and 090 for a frozen grid of exact joint tables, including asymmetric costs, nontrivial correlations, and independent distributions; record disagreements as failures, not select only passing cases.
6. A mutated reward function must be run as a negative control and detected by an asymmetric example; the present `test_asymmetric_mutation_guard` only checks the unmutated function, so it does **not** yet demonstrate mutation detection.

## Mathematical cross-check and identifiability

For the synthetic latent state Z with equally likely states 0 and 1 and success vectors (1,1,0) and (0,0,1), a two-attempt policy that first tests claim 1, then chooses claim 2 after success or claim 3 after failure, obtains 2 successes in state 0 and 1 in state 1, hence expected reward (2+1)/2 = 3/2. Any fixed pair has expected reward 1. These are exact consequences of an *assumed* distribution, not observations. The example illustrates the value of information under dependence, not novelty in AI.

For independent outcomes, adaptive observations cannot update untested marginals; the expected reward of any budget-feasible adaptive strategy is bounded by the optimal static knapsack objective. This independence control must pass even when outcomes have asymmetric probabilities and costs.

Crucially, adjudication-success indicators are not claim-truth indicators. A verification attempt can fail to resolve a true or false claim, and any claimed scientific benefit must account for adjudication reliability and uncertainty rather than counting only successful attempts.

## Empirical falsification and prior-art gate

A future method fails its proposed contribution if its held-out gains disappear against calibrated static knapsack and strong adaptive Bayesian baselines, vanish under provenance-family or temporal holdouts, rely on privileged joint-distribution access, or reflect unequal verification budgets. Report zero and negative findings. Closest conceptual prior art includes adaptive submodularity (Golovin & Krause, 2011), Bayesian experimental design, finite-horizon POMDP planning, budgeted active learning, and selective-label evaluation (Lakkaraju et al., 2017). These categories are **collision warnings**, not a claim of an exhaustive or newly verified literature search. The full bibliographic novelty audit remains open.

A valid cross-domain test must preregister family-disjoint splits and explicit task definitions in NLP, mathematics, and physics; use licensed data; prevent near-duplicate leakage; estimate costs and outcome probabilities without test-label access; and include confidence intervals clustered by provenance family. No dataset, model result, or novelty is asserted here.

## Cloud and spending gate

Do not run this fixture on the user's laptop. Do not launch a cloud job until the specific provider's current account eligibility, free compute quota, card/billing requirements, public/private repository treatment, and runner availability are verified. Even on a free runner, use a strict execution timeout and small enumeration caps. **No cloud execution or spend occurred in this session.**

## Acceptance decision

**Not yet certified.** Protocol 093 is a credible independent *implementation approach*, but it has not been executed; its cap is not a strict memory safeguard, its witness lacks an independent validator, and its mutation test does not exercise a mutant. Resolve these issues and execute under verified zero-cost cloud conditions before describing the result as a computational certificate. The 2026-11-22 publication target remains conditional.
