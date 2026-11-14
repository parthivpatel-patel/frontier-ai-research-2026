# Protocol 076 — Prior-art collision audit and discriminating experiment

Date: 2026-11-14. Status: literature-screening note and preregistration; no empirical runs or novelty claim.

## Direct prior art (publisher / author records)

1. Geifman & El-Yaniv (NeurIPS 2017), *Selective Classification for Deep Neural Networks*: https://papers.nips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html . Selective release, risk–coverage tradeoffs, and risk guarantees predate this project. **Collision:** abstention and calibration are not novel.
2. Kossen, Farquhar, Gal & Rainforth (ICML 2021), *Active Testing: Sample-Efficient Model Evaluation*: https://proceedings.mlr.press/v139/kossen21a.html . Cost-aware active acquisition of evaluation labels with bias correction and variance reduction. **Strong collision:** adaptive selection of test labels plus corrected estimation cannot be claimed as invented here.
3. Angelopoulos, Bates, Fisch, Lei & Schuster (ICLR 2024), *Conformal Risk Control*: https://research.google/pubs/conformal-risk-control/ . Expected-loss control using conformal methods, including NLP examples. **Collision:** risk-controlled selective release is an existing research family; its assumptions and guarantees must be compared exactly rather than treated as equivalent to finite-frame design-based auditing.

These sources establish substantial prior work, not a comprehensive novelty clearance. Follow-up must examine provenance-aware auditing, clustered active testing, partial identification for missing labels, and cross-domain scientific verification in primary papers.

## Candidate distinction, explicitly unproven

Potential contribution is a **jointly specified evaluation protocol** for provenance-family-correlated claims, heterogeneous domain-specific adjudication, selectively missing truth labels, and cost-matched verification policies. Combining known tools is not itself novelty. To warrant a methods claim, demonstrate an operational gap in nearest baselines and a reproducible improvement or an identifiable failure mode not already covered by prior work.

## Discriminating experiments (preregister before observing results)

* Frozen finite claim frame; fixed claims, provenance IDs, evidence versions, label status, policy decisions, and budgets. Keep a separate held-out test frame.
* Compare random family sampling, standard active testing with inclusion-probability correction, selective release/calibration, and proposed provenance-aware policy. Do not assert conformal guarantees when exchangeability or monotone-loss assumptions fail.
* Synthetic negative controls: perfect within-family duplication; zero inter-family correlation; adversarial missing labels concentrated in disagreements; fixed-size versus independent family sampling; census; all-abstain policy; unequal costs. Exact enumeration on small designs can test identities but is **not** empirical AI evidence.
* Held-out domain cases: NLP evidence entailment with 'unsupported' separate from 'false'; mathematics proof/counterexample/unresolved; physics dimension/units, tolerance, and measurement/model distinction. Avoid conflating the three labels.
* Primary outcomes: false-acceptance risk and coverage together, label cost, unresolved-label identification interval, provenance-family uncertainty, and worst-domain outcomes. Report confidence intervals only with a justified sampling design and sufficient independent families.
* Falsification: no difference from corrected active testing under matched costs; gains vanish when duplicate provenance is removed; advantage depends on unresolved labels being coded favorable; conclusions reverse under plausible adjudication tolerances; held-out gains do not replicate.

## Important estimand caveat

Protocol 075 defines false-release rate as F/K with a **fixed full-frame release count K**. A sampled numerator can be design-unbiased if sampling probabilities are known and positive, but if K is estimated from the same sample, the ratio need not be unbiased. If released truth labels are unresolved, logical bounds [F/K,(F+M)/K] are only fully observed finite-frame bounds; applying them to a probability sample requires additional sampling uncertainty treatment. Do not call the resulting interval a confidence interval.

## Execution and disclosure gate

No cloud execution until provider free-tier eligibility, remaining account-specific quota, payment/card conditions, and stop-before-billing behavior are verified. Do not use the user's laptop for compute. Record GitHub Actions job URLs, code SHA, dependencies, runtime and logs for any authorized free-cloud test. AI-assisted research and drafting must be disclosed wherever required; never invent findings, significance, or novelty.

## November 22 decision

Publish a results paper only with genuine held-out empirical evidence and a defensible distinction from the above work. Otherwise release a clearly labeled protocol/negative-result methods note or defer.
