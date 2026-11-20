# Selective-risk prior-art collision and revised claim gate (2026-11-20)

## Evidence and scope
This note is a literature-screening and preregistration amendment, **not** an experimental result, theorem, or proof of novelty. Latest inspected repository HEAD before writing: `5a703b173e751e459261ac24376d80f4a1d2b1c5`.

### Closest prior art requiring direct comparison
1. Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, https://arxiv.org/abs/1705.08500 — high-probability risk guarantees under abstention.
2. Geifman and El-Yaniv (2019), *SelectiveNet*, https://arxiv.org/abs/1901.09192 — jointly learned prediction/rejection and risk–coverage tradeoffs.
3. Xu, Guo and Wei (2025/2026), *Selective Conformal Risk Control*, https://arxiv.org/abs/2512.12844 — finite-sample selective risk control, including exchangeability after selection.
4. Bai and Jin (2026), *Conformal Selective Prediction with General Risk Control*, https://arxiv.org/abs/2603.24704 — e-value selective risk control, distribution shift and applications to LLMs. **High-priority collision:** do not claim novelty for selective finite-sample risk control in LLMs.
These citations and abstract-level comparisons are verified as discoverable; full-text theorem-by-theorem comparison is outstanding.

## Narrowed research hypothesis
At fixed inference/verifier cost and fixed selection coverage, a *paired, independently adjudicated dual-pool audit* with explicit temporal-consistency evidence may reveal operational error differences missed by shared-acceptance-only evaluation, especially under leave-one-domain-out transfer between NLP, mathematics and physics. This is an **empirical hypothesis**, not a guaranteed improvement or novel estimator.

## Primary estimands and exclusions
For each frozen verifier policy p and domain d, measure:
- accepted-error risk: incorrect accepted / accepted (undefined when accepted=0);
- rejected-correct fraction: correct rejected / rejected (undefined when rejected=0);
- coverage: accepted / all evaluated;
- total operational cost: generation + verification + audit/adjudication, with separately reported human-label effort.
Use paired examples and audit accepted and rejected pools independently. Do not compare policies only on their intersection of accepted items. For any statistical bound, specify finite-population vs future-population target and the assumptions that permit each. A finite-population audit bound **does not imply** out-of-distribution transfer guarantees.

## Predeclared falsification gates
1. If the proposed approach does not improve any prespecified utility/risk metric over confidence-only, conformal/selective risk-control and simple consistency baselines at matched cost and coverage, report null results.
2. If the effect disappears under source-family disjoint splits or leave-one-domain-out transfer, reject cross-domain generalization.
3. If independent labels are missing or disagreements are unresolved, do not certify a risk bound for that pool.
4. If thresholds, prompts, or domains are selected after inspecting the held-out outcomes, label results exploratory and collect new holdout data.
5. If zero-error audit intervals fail to exclude the prespecified unacceptable rate, no certification.
6. If temporal-consistency features add no incremental value after controlling for answer confidence and verification budget, remove mechanistic claims.

## Reproducibility and resource policy
Run only on standard GitHub-hosted Linux runners in this public repository, without paid larger runners, GPU, external model APIs, large downloads, or local laptop workloads. Pure Python standard-library tests and tiny synthetic fixtures first. No real-model inference is authorized until a genuinely free cloud service and account eligibility are verified. GitHub billing docs (checked 2026-11-20): https://docs.github.com/en/billing/concepts/product-billing/github-actions — standard hosted runners in public repos are free; larger runners and excess artifact storage can be billable. Avoid artifact uploads and caches.

## Publication gate (2026-11-22 checkpoint)
A methods/preregistration release may accurately report reproducibility tests and untested hypotheses. An empirical discovery paper requires independent held-out results, validated labels, uncertainty intervals, ablations, verified novelty relative to the four papers above, and AI-assistance disclosure. Do not claim an original theorem from known hypergeometric or survey-sampling identities.
