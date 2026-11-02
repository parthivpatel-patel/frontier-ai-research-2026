# Protocol 017 — Independent-source precision and selective-risk feasibility gate

Date: 2026-11-02. **Locked design before implementation.** This protocol contains exact mathematical planning calculations, **not observed model errors, improved reliability, or new theory**.

## Question and independent unit

Can a proposed assumption-aware verifier reduce the *source-clustered false-accept probability* at matched coverage against fixed-physics, may/must, grounded verification and calibrated abstention baselines? A source is one independently authored original requirement/document cluster; all repeated outputs belong to it. The intended meaning and the physical admissibility set require blinded independent adjudication before evaluation. No semantic claims from the four-source NL2MTL collection.

## Pre-specified conservative safety endpoint

For each held-out source, the locked method either abstains on all its evaluated predictions or accepts at least one. An **accepted source is a failure if ANY accepted formula is independently adjudicated incorrect**; otherwise it is a success. The denominator is the number of independently authored held-out sources with at least one accepted prediction, not total outputs, formulas or prompts. Report coverage separately as accepted sources divided by all eligible held-out sources. This source-level ANY-error endpoint is deliberately conservative and distinct from prediction-level false-accept risk.

For a single **pre-specified** method/threshold and iid independent-source Bernoulli outcomes with common risk p, if zero failures occur among n accepted sources, the exact one-sided (1-alpha) binomial upper confidence bound is

    U(n, alpha) = 1 - alpha ** (1 / n).

The minimum n to make this bound <= target risk r is ceil(log(alpha)/log(1-r)), subject to floating-point boundary verification. For alpha=.05: n=30 -> U=9.50339%; n=59 -> 4.95076%; n=299 -> 0.99691%. If coverage is 50%, obtaining 59 *accepted* sources would require at least 118 eligible sources in the idealized exactly-half-accepted scenario. With only 15 accepted sources the upper bound is 18.10363%, even with zero observed errors. The 30-source gate from Protocol 016 is **only a pilot eligibility minimum**, not enough to certify a <5% error risk.

## Validity and stopping rules

1. All labels, accept/abstain thresholds, physical-model assumptions, source groupings, baselines and evaluation exclusions must be frozen before accessing held-out outcomes. Source provenance, rights and blinded human adjudication must pass Protocol 016.
2. The zero-failure calculation is a *best-case feasibility bound*, not a power analysis for detecting improvement between methods. Any observed failures require a full exact binomial upper bound or a separately pre-registered clustered procedure; do **not** use the zero-failure formula for k>0.
3. The iid/common-risk assumption is substantial: heterogeneous domains, selection bias, dependent source authorship, and distribution shift can invalidate the simple confidence interpretation. Report per-domain results and selection mechanisms; do not claim distribution-free guarantees.
4. Do not use this single-test confidence level after searching multiple thresholds, models, domains, or stopping times. Any selection, multiple comparison or sequential peeking needs a separately pre-registered multiplicity/sequential correction.
5. If accepted-source sample size is below the target, mark the claim **not statistically certified**, even if zero failures are observed. If there are no accepted sources, risk is undefined, not zero.
6. Compare coverage and source-level risk at matched acceptance budgets against strongest reproducible prior baselines; do not claim improvement based solely on an upper confidence bound. Pre-register pairwise comparison and precision requirements after obtaining realistic pilot error/coverage estimates, before confirmatory evaluation.

## Research and resource constraints

The code implementing the arithmetic must be standard-library only and run exclusively on the existing **public GitHub repository standard hosted ubuntu-latest runner**; no laptop computation, paid inference, new account, larger runner, artifact upload, cache, or paid service. GitHub's official documentation confirms standard runners in public repositories are free, but larger runners and over-quota storage can incur charges: https://docs.github.com/en/billing/concepts/product-billing/github-actions .

## Relevant prior art and claim exclusions

Exact binomial limits are classical (Clopper and Pearson, 1934), not novel. LTLGuard (Andresel et al., March 2026, https://arxiv.org/abs/2603.05728) already combines compact language models, constrained generation, and lightweight formal consistency checks; this is a direct baseline candidate. Fahim, Lagoa and Meira-Góes (July 2026, https://arxiv.org/abs/2607.10918) already address LTL learning from uncertain demonstrations, albeit a different input setting. SCP-NL2TL (https://arxiv.org/abs/2608.05439) already studies calibrated selective translation and must be compared directly. No novelty is asserted for uncertainty handling, checking, abstention, or this sample-size formula.

## Falsification

Abandon a claimed improvement if it fails on independent adjudications, if source-disjoint evaluation cannot be assembled lawfully, if the method fails to outperform a relevant baseline at matched coverage, if the observed risk exceeds the predeclared threshold, or if the confidence bound is too wide to support the claim. Publish negative/limited results transparently. AI assistance must be disclosed as required by the publication venue.
