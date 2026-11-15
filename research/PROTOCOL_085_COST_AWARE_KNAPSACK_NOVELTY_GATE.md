# Protocol 085 — Cost-aware verification: exact decision-theoretic baseline and novelty gate

Date: 2026-11-14. Status: mathematical protocol only; not executed, not empirical evidence, and not a novelty claim.

## Scope and estimand
For a fixed census of K>0 released claims, let each unresolved claim i have a *predeclared* deterministic attempt cost c_i>0 and independent, known one-attempt adjudication success probability p_i in [0,1]. A successful attempt permanently resolves one label; failure leaves it unresolved. No repeat attempts in the baseline. Assume success probability is not updated by observing other attempts and does not depend on hidden truth for the purposes of the expected-width calculation. The total attempt budget is B. The unrestricted sharp false-release-rate width is U/K.

For a nonadaptive chosen subset S with sum(c_i)<=B, the expected final width is (U - sum_{i in S} p_i)/K. This is an additive 0–1 knapsack objective. It is **not** a novel ML formulation. When costs are equal and the number of attempts is fixed, selecting the largest p_i is optimal. With unequal costs, sorting by p_i/c_i is only a heuristic and need not be optimal.

## Exact counterexample to naive greedy ratio
Let B=10, K=3, three unresolved claims, costs (6,5,5), probabilities (1, 4/5, 4/5). Ratio ordering selects cost 6 with p=1, leaving budget 4 and expected resolutions 1. The feasible pair of cost-5 claims yields expected resolutions 8/5 and a larger expected width reduction (8/5)/3. Therefore a learned policy should never be evaluated only against a ratio-greedy baseline. An exact dynamic-programming knapsack optimum is a stronger small-instance comparator. Probabilities are synthetic and known by assumption, not measured.

## Scope of adaptive policies
Under fixed p_i, one attempt per claim, deterministic costs, and no information spillovers, observing a success or failure does not change the expected marginal benefit p_j/K of any remaining claim. Adaptation to outcomes cannot improve the optimal expected total gain beyond the best feasible selection; any policy can be compared with a mixture over feasible attempted subsets. This claim ceases to hold when costs are stochastic, attempts can be repeated, outcomes update shared latent difficulty, or adjudication success has family dependence. Those extensions require a clearly specified generative model and a strong adaptive baseline.

## Experimental design and falsification
1. Implement a dependency-free Fraction-based exhaustive subset oracle for n<=12 with exact budget constraints, alongside greedy ratio, highest-p, random feasible, and a predeclared policy.
2. Verify the B=10 counterexample exactly; assert greedy gain=1, oracle gain=8/5, and corresponding expected width reductions 1/3 and 8/15.
3. Include equal-cost and equal-p negative controls, zero-success and certain-success cases, and permutation invariance. Invalid probabilities, nonpositive costs, bool-as-int, and budget violations must fail closed.
4. In stochastic simulation, distinguish *realized* adjudication yield from *expected* yield; report confidence intervals only with justified independent units or provenance-family clustered resampling.
5. Include a selective-label adversary where false claims have lower resolution probability. Do not present the resolved-only error fraction as an unbiased estimate of overall false-release rate.
6. For unknown p_i, separate train, calibration, and held-out test sets by provenance family and source time; include calibration error, model training cost, and a simple logistic or frequency-based baseline. A learned policy must beat the exact oracle only if the oracle uses **estimated**, not true, probabilities; the true-p oracle is an unattainable ceiling, never a fair operational comparator.
7. Test transfer across NLP, mathematics, and physics with frozen definitions of claim, source provenance, adjudication outcome, attempt cost, and abstention. Report domain-specific failure and incomplete adjudication, not just pooled averages.
8. Reject positive novelty claims if improvements disappear against exact cost-aware baselines, depend on outcome leakage, fail family-held-out transfer, or do not survive realistic abstention and budget accounting.

## Prior-art collision checklist
Review and cite source-level work on budgeted active learning, optimal experimental design, adaptive stochastic knapsack, active testing, selective classification, selective labels/verification bias, and partial identification. The additive objective, knapsack formulation, and missing-label bounds are existing ideas. A possible contribution would require a demonstrably distinct scientific-claim adjudication problem, a reproducible benchmark with meaningful physics/mathematics/NLP tasks, or a rigorously validated method beyond these baselines.

## Compute, cost, and integrity gate
This document requires no compute. Do not launch GitHub Actions, hosted notebooks, APIs, or paid runners until public-runner eligibility, repository settings, quotas, storage, and any billing/card prerequisites have been checked for the actual account. Standard public GitHub-hosted runners may be free under GitHub policy, but account-specific availability is not verified here. No user laptop computation, downloads, model inference, or training. Publish synthetic fixtures as synthetic; publish negative findings. November 22 remains a conditional internal target.
