# Protocol 018 — Nonzero-failure selective-risk bounds and multiplicity gate

Date: 2026-11-02. **Pre-implementation specification; methodological planning only.** This protocol extends Protocol 017, not a claim of new statistics, AI performance, or a valid safety certificate.

## Question and estimand

When accepted AI-generated formal specifications contain one or more independently adjudicated errors, how should a held-out study report source-level error uncertainty without silently treating repeated generations as independent? Can the same reporting remain conservative when several **pre-specified** methods are inspected?

For each independently authored original source, each locked method accepts zero or more outputs or abstains. A source counts as accepted if at least one output is accepted, and counts as failed if **any** accepted output is adjudicated incorrect. The estimand is the probability of a source-level failure **conditional on that method accepting the source** under the target source distribution. Coverage is the fraction of eligible sources accepted; it is a separate endpoint. A method that accepts none has undefined selective risk.

## Exact one-sided binomial bound for any observed failure count

For a fixed, independently evaluated method with k failed accepted sources among n accepted independent sources, define U as the solution of

    sum_{j=0}^k choose(n,j) U^j (1-U)^(n-j) = alpha

for 0 <= k < n. For k=0, this reduces to U=1-alpha^(1/n). For k=n, U=1. The resulting one-sided Clopper–Pearson upper bound is a classical conservative frequentist interval, not a novel result. Use a monotone binary search and numerically stable log-binomial summation; no SciPy dependency or paid compute. If n=0, return undefined, not zero. Reject malformed counts, missing adjudications, and non-boolean acceptance labels.

For M **pre-specified** methods evaluated on the same held-out eligible source set, report Bonferroni-adjusted bounds using alpha/M per method, as well as raw observed failure fractions and coverage. This provides simultaneous conservative upper-bound coverage under the individual binomial assumptions even with dependence across methods; it **does not** establish superiority or compensate for undisclosed exploration of thresholds, source subsets, domains, or stopping times. Never use M inferred after examining outcomes to justify a confirmatory guarantee. Require an explicit fixed method roster and identical eligible-source identifiers for each method.

## Assumptions and validity gates

- Independently sampled, exchangeable or iid source clusters from the declared target population; conditional-on-acceptance Bernoulli outcomes have a stable common probability. Author/template overlap, domain shift, and adaptive source selection can invalidate the interpretation.
- Fixed prompts, models, adjudication rules, physics assumptions, thresholds, eligibility, method roster and sample size before accessing held-out labels. Human semantic labels must be independent and blinded.
- Separate calibration/development sources from final evaluation sources. If test labels influence threshold or model selection, the nominal intervals are not automatically valid. A Bonferroni adjustment for fixed candidate methods does not fix arbitrary post-hoc tuning.
- Report accepted-source counts, eligible-source counts, source-level failures, abstention, confidence levels and exact assumptions. Do not present these intervals as deployment safety guarantees.
- A matched-coverage comparison needs a separately pre-registered **paired** statistical test and power calculation; differences between marginal upper bounds are not a valid significance test. A method with trivial coverage is not a success.
- Missing independent semantic labels, inadequate source count, licensing restrictions, or an unverified physical model block confirmatory claims. Use a negative or feasibility report if the gate cannot be passed.

## Pre-specified implementation checks

Tests must verify: k=0 identity against Protocol 017; k=n boundary; k=n-1 closed form U=(1-alpha)^(1/n); CDF(U)=alpha for interior k; monotonicity in failures and sample size where applicable; invalid inputs; source deduplication; any-error aggregation; zero-coverage undefined risk; fixed method roster; identical source sets; and Bonferroni conservatism. All tests use synthetic examples only.

## Closest statistical prior art

- Clopper and Pearson (1934), *The use of confidence or fiducial limits illustrated in the case of the binomial*; modern reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html
- Geifman and El-Yaniv (NeurIPS 2017), *Selective Classification for Deep Neural Networks*: https://mlanthology.org/neurips/2017/geifman2017neurips-selective/
- Angelopoulos, Bates, Candès, Jordan and Lei, *Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control* (2021 preprint; Annals of Applied Statistics 2025): https://arxiv.org/abs/2110.01052
- SCP-NL2TL (2026), calibrated selective NL-to-temporal-logic translation: https://arxiv.org/abs/2608.05439

These references already establish exact confidence bounds, selective prediction, risk control and domain-specific selective formalization. The present work is **an evaluation-integrity safeguard**, not a novelty claim.

## Compute and spending

Implement and test on the existing public GitHub repository's **standard** `ubuntu-latest` hosted runner only, with the existing five-minute job limit. No laptop compute, GPU, new cloud accounts, cards, model inference, external data downloads, large artifacts, caches, paid runners or services. GitHub official public-runner policy: https://docs.github.com/en/billing/concepts/product-billing/github-actions .

## Falsification and next stage

If the model comparison fails at matched coverage, if the source-level risk bound exceeds the pre-registered threshold, if confidence assumptions are not defensible, or if lawful source-disjoint adjudicated data cannot be obtained, do not claim improved AI reliability. After realistic pilot data, freeze a paired matched-coverage analysis before touching confirmatory labels. Target November 22 only if evidence permits; disclose AI assistance per venue rules.
