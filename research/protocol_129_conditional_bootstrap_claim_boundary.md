# Protocol 129 — Conditional bootstrap precision and scientific claim boundary

Date: 2026-11-08. Status: theoretical audit only; no experiment executed.

## Question

Can the DKW diagnostic in Protocols 127–128 justify reporting a 95% confidence interval for the difference in unsafe-response rates between two systems on their jointly accepted physics interventions?

**No.** Three separate probability statements must not be conflated:

1. **Conditional Monte Carlo error.** Given a fixed observed dataset and a fixed resampling law, if bootstrap replicates are independent and identically distributed, retaining only draws with defined denominators produces iid draws from the *conditional* distribution given a defined denominator. DKW controls the supremum difference between the empirical CDF of these retained draws and that conditional CDF. It does not control coverage of a population parameter.
2. **Bootstrap statistical validity.** Coverage requires a separate argument about the sampling distribution of the statistic, dependence structure, and whether the resampling procedure mimics that distribution. DKW cannot establish this.
3. **Selection estimand.** The common-acceptance difference conditions on both systems accepting. It does not identify the marginal all-intervention difference in unsafe response rates; acceptance can be associated with difficulty and safety.

## Exact conditional-draw argument

Let B_1,...,B_R be independent draws from a fixed bootstrap resampling law Q. Let D(B) indicate a defined denominator, with p=Q(D=1)>0, and let T(B) be a real statistic when D=1. Conditional on any fixed pattern of D indicators, the retained T values are independent with common CDF F_D(t)=Q(T<=t | D=1). Therefore conditional on the observed number M=m>0, the DKW-Massart inequality gives

P(sup_t |F_m(t)-F_D(t)| > epsilon | M=m) <= 2 exp(-2m epsilon^2).

This is a conditional statement about a **random M**. It is valid only if draws are independent, the bootstrap law is fixed across draws, and all defined draws are retained without outcome-dependent post-selection beyond D. If the algorithm adapts its resampling distribution, stops according to observed statistic values, or discards extreme defined draws, this derivation no longer applies without additional proof.

If p=0, M=0 almost surely and no conditional statistic distribution exists. If M=0 in a finite run, report no DKW bound.

## Quantile warning

A CDF-rank error bound of epsilon does not yield an absolute numerical error bound on a percentile endpoint without distributional regularity (for example a positive lower density near the target quantile). In particular, discrete or highly concentrated conditional bootstrap distributions can have arbitrarily large endpoint jumps under small rank changes.

The existing field `dkw_informative_for_two_sided_95pct_tails` only checks epsilon<0.025. That condition means the bound is narrower than the nominal lower-tail probability, **not** that the resulting interval has 95% frequentist coverage or that endpoints are numerically stable.

## Prior art and novelty guardrail

These mathematical ingredients are established, not novel:

- Dvoretzky, Kiefer and Wolfowitz (1956), *Asymptotic minimax character of the sample distribution function and of the classical multinomial estimator*, Annals of Mathematical Statistics.
- Massart (1990), *The tight constant in the Dvoretzky-Kiefer-Wolfowitz inequality*, Annals of Probability.
- Efron (1979), *Bootstrap methods: Another look at the jackknife*, Annals of Statistics.
- Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, NeurIPS workshop / arXiv:1705.08500.
- Angelopoulos and Bates (2023), *Conformal Prediction: A Gentle Introduction*, Foundations and Trends in Machine Learning.

These references establish conceptual overlap, not an exhaustive or verified 2026 novelty search. A paper must separately establish any new contribution in the physics/NLP intervention design, paired evaluation estimand, or validated measurement protocol. Do not claim the DKW diagnostic or conditional bootstrap as a novel algorithm.

## Falsification plan, preregister before evaluation

1. Construct a synthetic two-family paired dataset with a known exact finite resampling distribution; enumerate it analytically for a small case and compare the conditional CDF to empirical cloud-run bootstrap draws.
2. Repeat over frozen seeds, recording M, undefined fraction, epsilon(M), and lower/upper endpoint movement. Verify the diagnostic changes with M while the deterministic preflight eligibility does not change with seed.
3. Introduce a discrete bimodal statistic with a large gap: demonstrate that a small CDF-rank bound does not imply a small endpoint-value error.
4. Generate independent synthetic datasets under prespecified clustered data-generating processes, both with acceptance independent of difficulty and with informative acceptance. Compute empirical 95% interval coverage separately from within-dataset DKW precision.
5. Compare to an all-intervention safety estimand and report the accepted-population fraction. Do not extrapolate conditional results to all interventions.
6. Run a negative-control experiment where physics labels are permuted within preregistered strata; reject claimed semantic or physics improvements if the effect survives permutation without a justified mechanism.

## Cloud-only implementation plan and cost gate

Use a minimal CPU-only Python standard-library test job on GitHub Actions **only after** confirming the repository/account's current free included minutes, billing/spending cap, runner eligibility, and workflow permissions. Public repository status alone is not sufficient proof of no cost. Do not dispatch a workflow if eligibility cannot be confirmed. No local execution, model downloads, GPU use, or paid service.

Record workflow URL, exact commit, Python version, dependency lock, seed manifest, job duration, raw output, and failures. If account-specific billing eligibility is inaccessible, leave experiments pending rather than claiming tests passed.

## Decision for November 22

The manuscript may present a *methods/limitations study* only if novelty relative to closest prior art and independent evidence support it. Otherwise publish a transparent technical report with negative or inconclusive findings, not a claimed novel physics-reasoning breakthrough. AI assistance and experiment provenance must be disclosed according to venue rules.
