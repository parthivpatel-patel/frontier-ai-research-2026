# Protocol 091 — Independent-oracle audit and empirical readiness gate

Date: 2026-11-15. Status: source inspection only; no execution, no empirical results, no novelty claim.

## Scope and provenance
Inspected `research/fixtures/test_protocol_090_possible_world_policy_enumeration.py` and `research/PROTOCOL_088_EXACT_ADAPTIVE_DECISION_ORACLE.md` from the repository default branch. This is a static code review, not a claim that any test passed.

## What Protocol 090 actually validates
The alternate solver constructs an exact joint distribution over binary adjudication-success outcomes by mixing conditionally independent Bernoulli vectors over a latent state. It recursively conditions that distribution on observed attempt outcomes and maximizes expected future successful adjudications. This is a valuable independently parameterized *possible-world dynamic program*, but is **not a literal enumeration of every complete policy tree**: it still uses Bellman recursion and memoization. Consequently, agreement with Protocol 089 can expose posterior-update bugs but is not independent exhaustive-policy enumeration as required by Protocol 088 item 2.

The grid covers 3 claims, 2 latent states, probabilities in {0, 1/2, 1}, one fixed prior (1/3, 2/3), and two cost/budget settings; 3^6 = 729 conditional tables. It does not cover n=4, B=3, arbitrary rational priors, or broad integer costs. A separate permutation test covers a particular three-claim instance. The independence control tests one instance rather than exhaustive small integer-cost cases. The zero-mass-world test confirms unreachable joint outcomes are excluded, but does not independently certify every unreachable observation-history branch. These are coverage limitations, not confirmed defects.

## Additional model assumptions requiring explicit treatment
1. The success event X_i means *successful truth adjudication*, not truth, correctness, or scientific validity. A policy optimizing successful adjudications can be scientifically unhelpful if adjudication standards are weak.
2. The latent mixture implies conditional independence given Z. Real verification outcomes may share tools, sources, annotators and hidden failure modes that invalidate this assumption.
3. The oracle knows costs, priors, and conditional success probabilities. A real policy must estimate these without using test-family outcomes or unattempted outcomes. Comparing a learned method against an oracle with privileged parameters must be labeled accordingly.
4. Verification attempts can themselves change evidence availability or downstream costs. The current fixed-cost, single-attempt model does not represent these effects.
5. Expected successful adjudications and unrestricted interval-width reduction are equivalent only for a fixed census with identical claim weights and correctly recorded resolutions. Neither measures scientific importance or calibrated truth risk.

## Required independent validation before claiming the oracle verified
Implement a genuinely different finite policy-tree enumerator for n <= 4 and B <= 3. Enumerate each first action and both observation-conditioned continuation mappings without reusing either oracle's Bellman solver. Score complete deterministic policies against precomputed joint possible worlds using exact fractions. Compare the maximum score to both existing solvers. Add tests with asymmetric priors, nonuniform costs, degenerate probabilities, arbitrary claim permutations, latent-state relabelings, and separate provenance families. Include a deliberate perturbation/mutation check demonstrating that the cross-check catches a corrupted posterior or reward term.

This may be combinatorially expensive. Before running even small tests, verify an actual zero-cost cloud execution path, account eligibility, remaining quota, billing/card requirements and spending exposure. Never execute on the user's laptop.

## Held-out empirical falsification design
Freeze data and adjudication rubric before model selection. Create three independently sourced domain strata: NLP factual/evidence-grounding claims, mathematical proof/solution claims, and physics reasoning/quantitative claims. For each, record source and provenance family, timestamp, generator/version, candidate claim, predicted truth, adjudication success/failure, verification cost, adjudicator independence, and unresolved truth status. Avoid copyrighted dataset redistribution and leakage of answer keys into policy features.

Split by provenance family and time before estimating success probabilities; reserve at least one cross-domain transfer evaluation. Count all attempted costs and failures. Pre-register primary metric as expected independently confirmed resolutions per fixed budget, with uncertainty clustered by provenance family. Secondary metrics: false-release partial-identification bounds, calibration, coverage/abstention, and worst-domain performance. Compare to exact static knapsack with oracle probabilities (upper-bound diagnostic), realistic calibrated static knapsack, random, cost-aware greedy, and a calibrated adaptive baseline. The model-aware adaptive oracle is an upper bound under its assumed generative model, not an attainable baseline with leaked test labels.

**Falsify the proposed contribution** if gains disappear against calibrated adaptive baselines, depend on test-family leakage, rely on assumed oracle parameters, fail domain/time holdouts, or do not survive cost and adjudication-quality sensitivity analysis. A negative result should be reported rather than relabeled as novelty.

## Literature collision checklist (verify primary sources before manuscript citations)
- Adaptive submodularity and adaptive stochastic optimization: Golovin & Krause (2011).
- Selective labels / selective observation bias: Lakkaraju et al. (2017).
- Budgeted active learning, Bayesian experimental design, value of information, partially observable Markov decision processes, and correlated bandits: search and compare precise objectives, assumptions and baselines.
- Scientific claim verification, fact-checking, theorem verification, and physics reasoning benchmarks: inspect contemporary methods and dataset licenses, with source dates.

Do not assert novelty from combining domains or from implementing a known dynamic program. A contribution is conditional on a distinct problem formulation or rigorously demonstrated, reproducible held-out improvement.

## Publication and compute gate
No empirical AI results were produced in this protocol. No test execution, cloud job, paid API or laptop workload was performed. The November 22, 2026 internal target is conditional; publication without independently executed validation should be framed as a prospective methods note, not a validated frontier-AI breakthrough. Disclose AI assistance as required by venue rules.
