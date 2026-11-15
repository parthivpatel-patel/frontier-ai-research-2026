# Protocol 104 — Correlated verification violates adaptive diminishing returns

Date: 2026-11-15. Status: analytical counterexample and literature boundary; **not an executed experiment**.

## Claim and exact counterexample

Consider two binary claim-truth variables X1 and X2 with P(0,0)=P(1,1)=1/2, and zero probability on mixed outcomes. Verifying claim i reveals Xi perfectly, costs one unit, and earns reward Xi if it is verified. Define f(S,phi)=sum of Xi over verified claims i in S, for a full realization phi. A policy can stop or choose the next claim conditional on previous observations.

The conditional expected marginal gain of selecting claim 2 with no observations is E[X2]=1/2. After selecting claim 1 and observing X1=1, the conditional expected marginal gain of claim 2 is E[X2 | X1=1]=1. Thus Delta(2 | empty)=1/2 < Delta(2 | X1=1)=1. This **violates adaptive submodularity's diminishing-returns condition** for this reward model, even though the realized reward is modular in the selected set for each fixed world. No general adaptive-greedy approximation guarantee may be imported from adaptive-submodular theory without proving its assumptions for the particular objective and observation model.

This counterexample is elementary and **not claimed as a novel theorem**. It also clarifies Protocol 102's correlated-claims example: the correctly contingent policy verifies claim 2 after X1=1 and yields 3/2 expected total reward; the swapped contingent policy yields 1/2. A noncontingent policy verifying both claims always has expected reward 1 and uses both units of budget. The 3/2 result is not proof that the optimizer is correct on general instances.

## Closest prior art and non-novelty boundary

1. Golovin and Krause, *Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization*, JAIR 42 (2011), 427–486, DOI 10.1613/JAIR.3278. Establishes adaptive submodularity and conditional greedy guarantees, subject to assumptions. https://mlanthology.org/jair/2011/golovin2011jair-adaptive/
2. Golovin, Krause and Ray, *Near-Optimal Bayesian Active Learning with Noisy Observations* (2010), https://arxiv.org/abs/1010.3091 . Treats noisy, costly, potentially correlated tests and near-optimal active learning. Our generic sequential test selection is **not novel** relative to this literature.
3. Finite-horizon partially observed decision processes and Bayesian value-of-information planning are broader established frameworks; the present exact tree enumerator is an implementation of a small finite decision problem, not a new class of optimization.

The potentially publishable question is narrower: does **provenance-separated, calibrated dependency-aware scientific claim verification** yield improved *correct adjudications per unit verification cost* across NLP, mathematics, and physics, against strong adaptive Bayesian and fixed-budget baselines, without leakage? This is a hypothesis, not a result.

## Falsification and independent validation gates

- The counterexample fails if an independently checked conditional marginal calculation does not reproduce 1/2 then 1 under the stated world table and reward definition.
- Do not extrapolate the counterexample to all verification objectives; alternative rewards (e.g. entropy reduction or hypothesis identification) require their own analysis.
- Require independent dynamic-programming upper bounds and complete enumeration agreement on tiny exact-rational instances, including the 2-claim example; witness scoring alone is insufficient.
- Before real-domain tests, freeze domain datasets, independent ground truth, verifier budgets, calibration splits, primary cost-normalized accuracy metric, error penalties, and paired uncertainty analysis. Compare static selection, adaptive myopic VOI, and a properly implemented adaptive Bayesian planner. Include calibration ablations and dependency-model misspecification.
- Null or negative improvement versus the strongest adaptive baseline, severe calibration error, provenance leakage, irreproducible results, or lack of meaningful physics and mathematics adjudication are explicit grounds to reject the claimed empirical contribution.
- Record null outcomes; do not backfill novel claims after observing results.

## Zero-cost execution decision

GitHub's billing documentation states standard GitHub-hosted runners are free for **public repositories**, while larger runners can be charged even for public repositories. See https://docs.github.com/en/billing/concepts/product-billing/github-actions . This is a documented service-level rule, **not verification of this account's billing state, Actions permissions, quota, or runner availability**. Only a standard hosted runner in this public repository should be considered, with explicit short job timeout and resource bounds, no paid marketplace actions or external paid APIs, no large artifacts, and no local computation. Before launching, verify repository Actions settings, account billing/spending configuration, and current runner availability; if any are inaccessible or ambiguous, do not launch.

No cloud job was launched for this protocol; no tests have been executed, no laptop compute was used, and no costs were incurred. November 22 remains a conditional research decision checkpoint.
