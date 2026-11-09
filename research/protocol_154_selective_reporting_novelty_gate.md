# Protocol 154 — Selective reporting and novelty gate (9 November 2026)

Status: preregistered methodological audit, **not an executed experiment or novelty claim**.

## Research question

Does a physics-family-aware verification and abstention mechanism improve *unconditional* reliability of language-model scientific claims, compared with matched baselines, at fixed coverage and compute? This question is distinct from proving correctness of the existing bootstrap implementation.

## Critical selection problem

Let S indicate that a system returns a numeric interval, C indicate that this interval covers the known parameter, and A denote the analytic eligibility decision. Then

P(S and C) = P(S) P(C | S).

Reporting only P(C | S) can hide failure through abstention. Conditioning on A as well can change the evaluated population and create selection bias. Preflight must be evaluated as part of the **entire deployed procedure**; post-selection intervals must not be called nominal 95% intervals without a valid coverage argument. Record P(A), P(S | A), P(S), P(C | S), and P(S and C), with independent outer-dataset uncertainty. Treat undefined intervals as failures for unconditional coverage; report their rate separately.

An empirical coverage estimate across N independently generated outer datasets has Monte Carlo standard error sqrt(p(1-p)/N), not a standard error based on the number of inner bootstrap draws. For a 95% target, 2,000 outer datasets give an approximate standard error of 0.0049 if the true probability is 0.95; this is a design calculation, not observed coverage.

## Baselines and falsification

Compare (i) always-answer baseline; (ii) matched random abstention at the same return rate; (iii) score-threshold selective prediction; (iv) analytic preflight without bootstrap; (v) full preflight plus bootstrap. Fix splits, family weights, budgets, scoring, and test datasets before comparison. Include deliberately shifted physics families and paraphrased NLP instructions. Measure selective risk versus coverage, unconditional correctness, calibration, latency, and compute per useful verified answer.

**Falsify the claimed contribution** if the method does not beat matched abstention baselines under paired uncertainty, if gains disappear under held-out physics families or linguistic paraphrases, if interval coverage falls below the prespecified tolerance, if improvement is attributable solely to higher abstention, or if a substantially equivalent method already exists in prior work.

## Closest prior art to investigate (bibliographic leads, not an exhaustive or newly verified search)

- Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*: risk–coverage tradeoffs and abstention.
- Angelopoulos and Bates (2023), *Conformal Prediction: A Gentle Introduction*: finite-sample calibration under exchangeability.
- Efron and Tibshirani (1993), *An Introduction to the Bootstrap*: resampling intervals and limitations.
- Yao et al. (2023), *ReAct*: language-model reasoning coupled with actions.
- Lightman et al. (2023), *Let's Verify Step by Step*: process versus outcome verification.
- Cobbe et al. (2021), *Training Verifiers to Solve Math Word Problems*: verifier-guided mathematical reasoning.
- Hendrycks et al. (2021), *Measuring Mathematical Problem Solving With the MATH Dataset*: evaluation precedent.

Before asserting novelty, retrieve and check primary versions, relevant subsequent work (including scientific reasoning, physics benchmarks, verifier calibration, abstention, selective inference and conformal risk control), dates, exact methods, and overlapping claims. A novelty claim requires a documented claim-by-claim comparison, not simply a different application area.

## Reproducible execution plan

1. Fix CI dependency declaration and validate all tests in an eligible, verified zero-cost hosted environment.
2. Run tiny deterministic analytic checks before any large experiment.
3. Freeze independent outer datasets, test split, prompts, intervention families, random seeds, failure policy, and stopping rules.
4. Run matched baselines and paired uncertainty analysis only after cloud eligibility and zero-billing exposure are verified.
5. Publish code, configurations, logs, negative results, licenses, and AI-assistance disclosures. Never imply human-only authorship if disclosure is required.

## Resource and integrity gate

No cloud jobs were dispatched for this protocol. GitHub Actions account-specific remaining quota, spending limits, billing/card status and actual availability are **unverified**; a public repository alone is not proof of zero-cost eligibility. No paid infrastructure, local model inference, local training, large downloads or laptop-heavy computation is authorized. The 22 November target is conditional on reproducible results and a defensible novelty audit.
