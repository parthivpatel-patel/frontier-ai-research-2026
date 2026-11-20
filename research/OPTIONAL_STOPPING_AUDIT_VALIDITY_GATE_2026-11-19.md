# Optional stopping and audit selection: preregistered validity gate (2026-11-19)

## Scope and status
This note supplements the finite-population audit gate. It is a methodological safeguard, **not** an original theorem, empirical finding, or evidence that any AI verifier works. No model execution is reported.

## Fixed-size audit
Freeze a finite accepted-answer population of size N and draw n distinct items uniformly without replacement, before observing correctness. Let K be its unknown total errors and X the errors in the sample. Then
P_K(X=0) = C(N-K,n)/C(N,n) for n <= N-K, and zero otherwise.
For a one-sided confidence level 1-alpha, a zero-error observation excludes any candidate K with P_K(X=0) < alpha. In particular, to reject a prespecified unacceptable error count K0 at level alpha, require C(N-K0,n)/C(N,n) <= alpha (with the boundary convention specified in advance). Because this probability decreases with K, this also rejects every K >= K0. This is a **fixed-n** statement. It does not license a claim that the true risk is zero.

For family-wise inference over NLP, mathematics and physics, prespecify family-specific alpha_f with sum alpha_f <= alpha, or use a valid simultaneous procedure. Denominators must be the frozen accepted populations within each family, not only audited subsets.

## Failure under repeated peeking
Suppose investigators inspect an audit after each additional label and stop as soon as a nominal fixed-n confidence test looks favorable. The stopping time depends on the observed labels, so the fixed-n coverage argument no longer automatically applies. A post hoc choice among thresholds, families, or accepted populations creates further selection. Even if each individual test is valid at a fixed sample size, the union of many opportunities to declare success can inflate the probability of a false reliability claim.

## Allowed designs
1. **Fixed n:** Freeze population, sampling seed, sample size, alpha allocation, and decision rule before any audit labels are exposed; evaluate once.
2. **Sequential:** Use an independently justified time-uniform confidence sequence or an anytime-valid test for sampling without replacement, with its assumptions and proof/reference specified before inspecting outcomes. Do not substitute repeated fixed-n hypergeometric tests.
3. **Multiple looks with spending:** If only a finite set of planned looks is used, allocate alpha across all looks and families (e.g., Bonferroni). At each look, apply a valid fixed-sample test at its allocated level. This is conservative but controls the chance of any false rejection by the union bound, regardless of dependence, provided the sampling design is valid at each look.

## Operational preregistration
- Freeze model outputs, task IDs, correctness rubric, source-shift splits, accepted populations, and thresholds before audit sampling.
- Record the sampling frame, randomization algorithm, seeds, audit selection probabilities, and exclusions. Audit adjudicators should not know which verifier accepted an answer where feasible.
- Separate confirmatory from exploratory tests; all exploratory re-thresholding must use fresh held-out tasks and a new frozen audit.
- Declare any missing audit label as missing, not correct. Report sharp worst-case bounds alongside design-based estimates.
- Report per-family accepted counts, audited counts, observed errors, confidence bounds, and compute costs. Do not infer performance for unobserved target shifts without assumptions.
- Test code must cover n=0, n=N, K=0, K=N, ties, infeasible coverage targets, and the exact hypergeometric tail with integer arithmetic.

## Falsification and release
A reliability claim fails its preregistered gate if the upper error bound exceeds the risk target, the sample was selected after viewing correctness, a sequential stop used only fixed-n inference, a family is underpowered, labels are unresolved, or a baseline is not compared at matched family-specific coverage and compute. If no no-charge cloud execution and held-out labels are available, release a methods/preregistration report rather than an empirical discovery paper.

## Prior-art and novelty boundary
Finite-population hypergeometric inference, family-wise error control, optional-stopping pitfalls, and confidence sequences are established statistical ideas. This note claims no new theory. Any contribution to AI/ML/NLP/mathematics/physics must be independently established through a new method or reproducible, leakage-resistant cross-domain findings. Full-text novelty audit and actual held-out model experiments remain pending.

## Infrastructure guardrails
Only standard no-charge public-repository GitHub Actions runners may be considered after checking current terms and account eligibility. No paid runner, card registration, GPU service, laptop inference, large download, or cost-bearing operation is authorized.