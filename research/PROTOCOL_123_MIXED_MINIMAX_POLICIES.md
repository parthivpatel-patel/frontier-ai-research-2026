# Protocol 123 — Mixed minimax policies, adversarial dependence, and publication gates (2026-11-16)

**Status:** Mathematical specification, not an executed experiment. No novel theorem, cloud execution, or empirical improvement is claimed.

## Why the deterministic 81-policy calculation is not the complete minimax benchmark

Protocol 122 correctly identifies four extreme conditional joint distributions for any *fixed* policy, but enumerating 3^4 deterministic policies only solves **deterministic** minimax. An agent permitted to randomize its action after observing a signal can potentially obtain strictly smaller worst-case expected loss. Thus a deterministic minimax result must not be described as globally minimax without either solving the mixed problem or proving a pure optimum exists.

Let truth t∈{0,1}, observation o∈{++, +−, −+, −−}, action a∈{accept,reject,abstain}, prior π, and nonnegative prespecified loss ℓ(t,a). For each truth state t, write the joint likelihoods as

p_t(++;q_t)=q_t; p_t(+−;q_t)=a_t−q_t; p_t(−+;q_t)=b_t−q_t; p_t(−−;q_t)=1−a_t−b_t+q_t,

where q_t∈[max(0,a_t+b_t−1),min(a_t,b_t)]. For each observation o choose probabilities x[o,a]≥0 summing to 1. The four adversarial corners c=(q_0,q_1)∈{L_0,U_0}×{L_1,U_1} give unconditional risk

R_c(x)=Σ_o Σ_a x[o,a] { π p_1(o;q_1) ℓ(1,a) + (1−π) p_0(o;q_0) ℓ(0,a) } + k,

with fixed verification cost k≥0. Minimize z subject to R_c(x)≤z for all four corners, Σ_a x[o,a]=1, x[o,a]≥0. This is a **finite linear program** (12 policy variables and one epigraph variable; 4 corner inequalities and 4 simplex equalities). For any fixed x, R is affine in q_0,q_1, so corners suffice. This proves the LP represents the ex-ante mixed minimax problem under the specified rectangular uncertainty set. It does not imply that randomization is always necessary.

## Independent validation and failure modes

1. Implement an exact-rational evaluator of R_c(x) separate from the existing posterior and risk helpers. Validate every conditional row sums to one and reproduces the two margins.
2. For each of the 81 deterministic policies, compute all four corner risks directly and recover the deterministic minimax value D. A mixed optimum M must satisfy M≤D. If M>D beyond solver tolerance, the implementation fails.
3. Validate the LP using an independently implemented small-case oracle or a second solver; record solver name, version, tolerances, primal residuals and duality gap. Never label a floating-point optimum exact without a rational certificate.
4. Check zero-cost/no-verification baseline B=min_a [πℓ(1,a)+(1−π)ℓ(0,a)]. If verification is optional and no-verification is an admissible choice, the optimal *overall* strategy must have risk ≤B. The verification-only optimum can exceed B when k>0; keep these quantities distinct.
5. Check that a second perfectly duplicated verifier offers no incremental information relative to the first under identical observation and action costs; do not confuse that result with zero value for the first verifier.
6. Stress-test prior 0 and 1, impossible observations, asymmetric losses, zero-width Fréchet intervals, verifier exchangeability, and nonzero verification costs. A posterior conditional on a zero-probability event is undefined, but ex-ante risk remains well-defined.
7. Record a counterexample with M<D if one is found; do not assert such a counterexample exists for the specific three-action loss family without construction and verification.
8. Evaluate plug-in independence, duplicate-assumption, deterministic minimax, mixed minimax, and no-verification policies on **held-out** truth-adjudicated examples. Report proper scoring rules and realized decision loss with source-cluster uncertainty, not synthetic worst-case guarantees as empirical gains.

## Important identification qualification

The rectangular set assumes each truth-conditional dependence parameter may vary independently while individual conditional margins and the prior are known exactly. Real estimated margins, label errors, dataset shift, and source dependence enlarge or alter the uncertainty set. A rectangular conditional model is a sensitivity analysis, not a confidence region. For deployment, distinguish sampling uncertainty from structural non-identification and prespecify how both enter the ambiguity set.

## Prior art and novelty constraints

This formulation belongs to established finite zero-sum games, robust Bayesian decision theory, imprecise probability, Fréchet bounds, and distributionally robust optimization. Relevant anchors to check include Fréchet (1951) bounds; Wald (1950), *Statistical Decision Functions*; Gilboa and Schmeidler (1989), *Maxmin Expected Utility with Non-Unique Prior*; and modern distributionally robust optimization surveys. Bibliographic details and closest experimental AI-verifier papers require source verification before citation in a manuscript. Neither the LP nor its corner reduction is claimed to be novel.

A possible **empirical** contribution would be demonstrated, reproducible improvements in decision risk under correlated verifier failures across independently adjudicated NLP, mathematics, and physics tasks, relative to strong calibrated baselines. It is falsified by absent held-out gains, sensitivity to truth adjudication or source leakage, poor calibration, or costs that eliminate the benefit. Cross-domain generalization must be measured, not inferred from a shared mathematical formulation.

## Zero-cost execution and Nov 22 decision

Do not run on the user's laptop. No GPU is needed for the small standard-library fixtures; a GitHub-hosted workflow may be considered **only after** verifying the account/repository's actual free Actions allowance, current usage, billing/card exposure, and job-level controls. Public repository status alone is not a guarantee against charges or policy changes. No cloud job is authorized by this protocol.

Publication gate: if executed tests, independent replication, rigorous closest-prior-art review and real held-out evidence remain absent by November 22, label the output as an analytical protocol or preliminary methods manuscript; do not advertise a validated empirical AI discovery. Disclose AI assistance where required and preserve full provenance.
