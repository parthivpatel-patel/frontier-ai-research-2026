# Protocol 145 — Preregistered coverage and failure-semantics experiment

Date: 2026-11-08. Status: experimental design only; no runs or results.

## Question and estimands

The production sampler draws lineage indices independently within each positive-weight physics family (Protocol 142). Protocols 135 and 143 concern the probability that at least one resampled family has no accepted lineages. This is a *definedness* probability, not the coverage probability of a confidence interval.

For family j with n_j lineages and a_j accepted lineages, let q_j=((n_j-a_j)/n_j)^{n_j}. Under independent draws between families, P(any undefined family)=1-product_j(1-q_j). Exclude zero-weight families exactly as production does. This identity applies only to uniform, with-replacement, n_j-draw family bootstrap. Verify those assumptions directly against the code and reject the oracle if they differ.

Separately, for a data-generating mechanism D and interval algorithm I, define unconditional coverage C(D)=P_D(theta(D) in I(X)), counting undefined intervals as failures. Also report conditional coverage C_defined(D)=P_D(theta(D) in I(X) | I(X) defined) and definedness rate P_D(I(X) defined). These must not be conflated: unconditional coverage equals conditional coverage times definedness only if the interval is always either defined or undefined and undefined is counted as noncoverage.

## Prespecified design

1. First fix CI dependency collection and obtain an immutable green run for the full suite, including Protocol 143. Do not run experiments if the suite is red.
2. Use a deterministic exact-enumeration oracle for small n (2, 3, 4) and compare production preflight and sampled undefined counts against it. Include all-accepted, none-accepted, zero-weight, and mixed-family cases.
3. For repeated-sampling coverage, specify a bounded synthetic DGP with known parameter: independent Bernoulli accepted indicators, p in {0.1,0.5,0.9}, family count in {1,2,4}, and n in {4,12,32}. Preserve family and lineage dependence as separate experimental factors rather than pooling them. Record the exact interval definition and estimand before running.
4. Predeclare 2,000 outer replications per cell, fixed publicly recorded integer seeds, and 1,000 bootstrap replicates per outer draw **only after** runtime and free-tier verification. These are targets, not completed runs. Start with a cloud-only tiny smoke test under a verified no-charge allowance, then cap the job duration and stop on failure.
5. For each cell report numerator/denominator of unconditional and conditional coverage, undefined count, mean interval width on defined cases, Monte Carlo standard error, and a binomial confidence interval for measured coverage. Include a negative control with deliberately mismatched resampling dependence to demonstrate sensitivity.
6. Treat intervals below nominal 95% coverage by more than their preregistered Monte Carlo uncertainty as a falsification of the coverage claim; never reclassify undefined draws as successes or silently drop them.
7. Preserve code SHA, dependency lock, runner image, seeds, generated machine-readable results, stdout/stderr, and GitHub Actions URL. Do not claim physical or language reasoning improvement from these synthetic statistics.

## Novelty and publication boundary

The closed-form identity, inclusion-exclusion, and bootstrap resampling are established methods. The candidate contribution, if any, must be a separately evaluated system for verifiable natural-language-to-physics reasoning with calibrated abstention, provenance, and controlled counterexamples. Compare against direct prompting, self-consistency, conformal/selective prediction, and programmatic verification baselines on held-out physics tasks. Report abstention, selective risk, calibration, verification accuracy, and compute budget. A purely statistical oracle is not sufficient for a frontier-AI paper.

## Execution and cost gate

No experiment may execute until the repository's GitHub Actions settings, public-repository billing eligibility, included runner-minute policy, account spending limit, and remaining quota are verified for this account. No payment card, paid runner, local training, local inference, or laptop compute is authorized. This protocol does not itself establish eligibility or perform a run.

## Falsification and decision

If exact oracles disagree with production, repair correctness before inference. If unconditional coverage fails, retract coverage claims and publish the failure transparently. If the candidate system does not beat credible baselines under matched budgets or overlaps prior art, reframe as replication/negative result rather than claim novelty. November 22 is a target, not a justification for unverified publication.
