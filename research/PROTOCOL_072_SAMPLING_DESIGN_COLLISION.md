# Protocol 072 — Sampling-design collision and falsification gate

Date: 2026-11-14. Status: analytical specification only; no executed tests, empirical claims, or novelty assertion.

## Why this gate is necessary

Protocols 069–070 use **independent Bernoulli inclusion of provenance families**. Their variance expression is not automatically valid for a fixed-size sample, sampling without replacement with dependence, adaptive selection, or a deterministic audit quota. A reproducible paper must record the actual design rather than apply an independent-inclusion variance formula to arbitrary evaluation logs.

## General paired estimator

For a finite set of provenance families g=1,...,G, let Z_g denote the family-summed difference between candidate and baseline false-release contributions, using denominators fixed from the full policy-release universe, not from the sampled labels. Let I_g indicate evaluation inclusion, pi_g=P(I_g=1)>0, and pi_gh=P(I_g=1,I_h=1)>0 for distinct g,h. Then

Dhat = sum_g I_g Z_g / pi_g

is design-unbiased for D=sum_g Z_g if Z_g is fixed before evaluation sampling and truth labels are resolved without selective missingness. For dependent inclusion, the design variance is

Var(Dhat) = sum_g sum_h (pi_gh - pi_g*pi_h) Z_g Z_h / (pi_g*pi_h),

where pi_gg=pi_g. An unbiased estimated variance uses sampled pairs and divides each summand by pi_gh. This estimator **cannot** be used where relevant joint inclusion probabilities are zero; alternative bounds or design-specific variance methods are needed. A negative numerical variance estimate due to finite precision or unstable pairwise weights must not be silently clipped without an audit record.

## Exact fixed-size counterexample

Consider G=2, sample exactly one family uniformly, and Z=(0.2,-0.1). Then pi_1=pi_2=0.5 but pi_12=0. Dhat is 0.4 or -0.2 with equal probability; its expectation is 0.1 and design variance is 0.09. Incorrectly applying the independent-Bernoulli formula gives 0.05. The difference, 0.04, is the omitted covariance contribution. The single realized sample cannot identify an unbiased pairwise variance estimate because the two families are never observed together. This is an *analytic counterexample*, not an executed test.

## Required reproducibility checks

1. Store sampling unit, full eligible family frame, design type, inclusion and joint-inclusion probabilities, seed (when random), realized sample, and any adaptive sampling history.
2. Reject an independent-Bernoulli variance implementation if the design selects a fixed number of families or if empirical pair inclusion contradicts factorization.
3. Add an exact-enumeration negative control for the two-family fixed-size example: expectation 0.1, variance 0.09; verify that the Bernoulli variance 0.05 is rejected for this design.
4. Require independent truth adjudication for every sampled family; report missing-label bounds separately and never substitute zero for unknown truth.
5. Keep release denominators and operational verification budgets fixed across paired comparisons, and distinguish released-claim coverage from evaluation-family inclusion.
6. Report family count, effective sample size, and uncertainty limitations; do not infer normal confidence-interval coverage from an unbiased variance identity.
7. Pre-register per-domain effects and failure thresholds for NLP, mathematics and physics; label ambiguous physical truth conditions explicitly.

## Prior-art collision and novelty boundary

The Horvitz–Thompson estimator, unequal-probability sampling, joint-inclusion variance, and design-based inference are established survey-sampling tools, **not novel contributions**. Relevant primary sources for manual verification include Horvitz and Thompson (1952), *A Generalization of Sampling Without Replacement From a Finite Universe* (JASA, DOI: 10.1080/01621459.1952.10483446), and Särndal, Swensson and Wretman (1992), *Model Assisted Survey Sampling*. Any candidate originality must instead survive direct comparison with selective prediction, active auditing, off-policy evaluation, conformal risk control, and provenance-aware evaluation, using verified source texts and experimentally matched budgets. These citations are starting points, not evidence that a comprehensive 2026 literature audit has been completed.

## Execution and publication gates

No workload is authorized here. Before cloud execution, verify current provider-specific free tier, account eligibility, card/billing requirements, quota headroom, availability, and an enforceable zero-cost stop mechanism. Never use the user's laptop for computation. No result should be represented as observed until a cloud run is independently documented with exact commit, environment, invocation, exit status and logs. If these gates cannot be satisfied by November 22, publish a transparent methods/pre-registration note or defer a results paper; never invent results.
