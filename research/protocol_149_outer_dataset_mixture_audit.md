# Protocol 149 — Outer-dataset mixture audit for interval abstention

Date: 2026-11-08. Status: exact mathematical counterexample and preregistered production checks; no experiments executed.

## Why this audit is necessary

Protocol 148 derives a binomial-tail interval failure probability conditional on one observed dataset X. It explicitly warns that replacing the random conditional failure probability q(X) by its average is generally incorrect. This protocol supplies an exact counterexample and a reproducible oracle for that distinction.

Let X be drawn from a fixed outer data-generating process. Given X, let B bootstrap draws be conditionally independent, each invalid with probability q(X). Let K be the number of valid draws and let an interval be returned iff K >= m. Define

g_{B,m}(q) = sum_{k=0}^{m-1} C(B,k)(1-q)^k q^(B-k).

Then P(interval unavailable) = E_X[g_{B,m}(q(X))]. It is generally NOT g_{B,m}(E_X[q(X)]). This is the law of total probability, not a novel result.

## Exact two-stratum counterexample

Consider a preregistered outer process that chooses one of two observed acceptance-mask strata with equal probability. In stratum A, q(X)=0; in stratum B, q(X)=1. For B=2 and m=1, g(q)=q^2. The true outer interval failure probability is (0^2 + 1^2)/2 = 1/2. Substituting the mean q=1/2 into the conditional formula gives (1/2)^2=1/4. The resulting absolute error is 1/4.

This counterexample uses extreme acceptance masks deliberately. It establishes non-commutation, not typical real-world effect size. For m=1 and B>=2, g(q)=q^B is convex on [0,1], so Jensen's inequality gives E[q^B] >= (E[q])^B. For other m, do not assume a universal direction of bias without analyzing the shape of g.

The counterexample is a theoretical reference case, NOT a run result, confidence-interval coverage estimate, or evidence of physics/NLP capability.

## Reproducible reference checks

1. Freeze an outer finite mixture of acceptance masks, probabilities w_s summing to one, and conditional q_s values obtained from independently enumerated production resampling outcomes.
2. Calculate the exact outer interval-abstention oracle sum_s w_s g_{B,m}(q_s) using rational arithmetic for small B; independently enumerate all conditional replicate-validity sequences.
3. Include the two-stratum example above; test B=1 (where g_{1,1}(q)=q), B=2,m=1, B=2,m=2, q=0, q=1, and nondegenerate interior q values.
4. Distinguish the mixture oracle from g(sum_s w_s q_s); report both and their signed difference.
5. Inspect the production interval builder for additional failure conditions (nonfinite values, percentile construction, downstream abstention). If any occur, the binomial-tail oracle is only one component, not a complete failure model.
6. For Monte Carlo outer datasets, independently sample X and bootstrap seeds; log counts of outer datasets, interval returns, covered returned intervals, and abstentions. Outer datasets, not inner bootstrap replicates, determine the effective sample size for uncertainty estimates.
7. For a physics claim, independently freeze a physical estimand, noisy measurement model, extraction contract and direct non-LLM baseline; do not transfer this toy calculation into a performance claim.

## Falsification and publication gates

- Reject the exact mixture formula if conditional bootstrap independence or the iff K>=m return rule fails.
- Reject any published unconditional interval-availability estimate that simply plugs a mean q into a nonlinear tail without a justified approximation and uncertainty bound.
- Do not claim 95% unconditional coverage if the outer abstention probability exceeds 5%, even if selective coverage among returned intervals is high.
- Do not claim novelty for this probability identity, Jensen's inequality, bootstrap, or selective inference. These are established foundations. Originality requires separately verified physics-language experiments and a documented contemporary prior-art comparison.
- Do not promote the November 22 target to a publication commitment without passing code, CI, statistical, and novelty gates.

## Execution and resource boundary

This is a paper-and-code specification only. No model inference, simulation, GitHub Actions dispatch, local computation, or paid service was initiated. The previously identified pytest CI configuration issue remains open. Account-specific GitHub Actions free quota, billing settings, and remaining allowance were not verified; therefore cloud execution is withheld. Laptop remains browser-only. Additional spending: $0.
