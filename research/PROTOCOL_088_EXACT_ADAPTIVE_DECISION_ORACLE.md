# Protocol 088 — Exact adaptive decision oracle and leakage-resistant benchmark

Date: 2026-11-14. Status: prospective mathematical and experimental specification; no tests run, no model results, no novelty claim.

## Purpose

Protocol 087 correctly requires an adaptive Bayesian oracle, but does not yet give a fully executable state definition. This protocol supplies one for small finite cases, and adds a falsification gate for spurious adaptive improvements from leaked latent variables, improperly counted costs, or comparing against a weak static baseline.

## Formal finite model

Let claims i=1,...,n have positive integer attempt costs c_i, fixed budget B, and binary success X_i indicating whether an attempted adjudication resolves its truth. A claim may be attempted once. A shared latent provenance-family state Z takes values in a finite set with prior pi(z). Conditional on Z, the X_i are independent Bernoulli with specified probabilities p_i(z). The policy observes success/failure after each attempt, but never Z or any unattempted X_i. The objective is expected number of successfully resolved claims, divided by fixed census K if reporting unrestricted interval-width reduction. Truth/falsity of the claim is distinct from adjudication success.

For remaining set R, budget b, and posterior distribution q over Z, define V(R,b,q)=0 if no remaining claim fits. Otherwise

V(R,b,q) = max over i in R with c_i <= b of [ s_i(q) (1 + V(R\\{i},b-c_i,q_i^1)) + (1-s_i(q)) V(R\\{i},b-c_i,q_i^0) ],

where s_i(q)=sum_z q(z)p_i(z), and q_i^x(z) is proportional to q(z) p_i(z)^x (1-p_i(z))^(1-x). If an observation has zero predictive probability, its branch contributes zero and no posterior update is needed. A stop action with value zero is always allowed. Exact rational arithmetic is preferred for tiny enumerated instances.

This recursion is an optimal adaptive oracle only **under the specified latent model and known parameters**. It is not a deployable learned policy and must never receive the realized Z as an input.

## Independence negative control

If p_i(z)=p_i is constant in z for every i, posterior updates cannot change any future success probability. The adaptive optimum must equal max_{S:sum c_i<=B} sum_{i in S} p_i, the exact 0/1 knapsack objective. Test this equality for all small integer-cost instances under exhaustive enumeration. This is a benchmark property, not a novel theorem.

## Correlated-outcome stress case

Construct a synthetic two-state latent family Z in {A,B} with equal prior probabilities, three claims and budget two, unit costs. Claim 1 is a diagnostic with p_1(A)=1 and p_1(B)=0; claim 2 has p_2(A)=1,p_2(B)=0; claim 3 has p_3(A)=0,p_3(B)=1. A static two-claim subset has expected yield at most 1.0 (claim 1+2 or 1+3), while an adaptive policy attempts claim 1 and then chooses claim 2 after success or claim 3 after failure, yielding expected 1.5. This example uses perfect dependence and a fully specified synthetic latent state; it demonstrates adaptivity can matter under correlation but is **not** a scientific-claim result or novelty evidence.

## Implementation and test contract

1. Use deterministic exact fractions and a finite posterior representation. Memoize states using canonical rational tuples; assert each recursive transition decreases budget and remaining claim count.
2. Exhaustively enumerate deterministic policies for n<=4 and B<=3 to cross-check the Bellman solution, including zero-probability observations and nonuniform costs.
3. Confirm the independent-success equality to exact knapsack; include ratio-greedy as a weaker diagnostic baseline only.
4. Verify the correlated stress case: adaptive optimum 3/2, static optimum 1, with no hidden-state access.
5. Reject nonpositive costs, negative budget, probabilities outside [0,1], prior not summing to one, duplicate IDs, and missing domain/provenance metadata where required.
6. Test invariance to claim permutations and latent-state renaming; test separate provenance families and held-out-family transfer.
7. Keep outcome X_i, truth label T_i, and model prediction distinct. Record failures/abstentions and all attempted costs; do not condition evaluation only on successful attempts.
8. Report the gap to the **correct model-aware adaptive oracle**, not merely random or static greedy. Under model misspecification, compare to independently calibrated and held-out baselines; never present an oracle-parameter advantage as a learned-policy result.

## Scientific interpretation and falsification

The candidate contribution would have to show robust provenance-aware, cost-calibrated performance on real independently adjudicated NLP, mathematical and physics claims, against strong adaptive and nonadaptive baselines. If the only improvement occurs in the toy latent example, or disappears when using family/time holdouts, calibrated probabilities, and equal budgets, reject the novelty claim. Report sharp missing-truth identification bounds separately from statistical uncertainty; a wider interval is not automatically a failed model, and a narrower interval may merely reflect more successful adjudications.

## Execution and integrity gate

No cloud compute is authorized by this document. Before running, verify account-specific zero-cost GitHub Actions or other cloud eligibility, quota, billing/card requirements and spending exposure. Do not run compute on the user's laptop, download large models, use paid APIs, or infer empirical results from theoretical examples. Maintain dated source citations and disclose AI assistance under publication rules. Nov 22 is a conditional internal target.
