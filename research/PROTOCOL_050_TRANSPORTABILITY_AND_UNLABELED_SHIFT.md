# Protocol 050 — Transportability stress test and non-identification under unlabeled shift

Date: 2026-11-12. Status: mathematical audit and preregistered design only. No experiment run, no novelty or performance claim.

## Research question
Can the observed joint-positive rate of two scientific-claim verifiers support reliable abstention when deployment prevalence or their shared failure modes change? Protocol 049 derives sharp *within-population* bounds given known prevalence, class-conditional marginals and joint-positive frequency. This protocol specifies when that information cannot be transported.

## Exact transport equation
For a population e, define prevalence pi_e=P_e(Y=1), class-conditional joint-positive probabilities a_e=P_e(V1=V2=1|Y=1), b_e=P_e(V1=V2=1|Y=0), and observable unlabeled q_e=P_e(V1=V2=1). Then

q_e = pi_e a_e + (1-pi_e)b_e.

A source-population measurement q_s does **not** constrain q_t unless assumptions connect (pi_s,a_s,b_s) to (pi_t,a_t,b_t). Even if q_t is observed exactly, it is one equation in three unknowns. A point posterior pi_t a_t/q_t cannot be identified without additional constraints.

### Constructive counterexample (mathematical only)
Fix pi_t=1/2 and q_t=0.34, and verifier marginals s1=s2=0.8, f1=f2=0.2. Both of the following class-conditional joint tables satisfy the same observed q and the same verifier marginals:

- World A: a=0.60, b=0.08. Posterior P(Y=1|++) = 0.30/0.34 = 0.88235294.
- World B: a=0.68, b=0.00. Posterior P(Y=1|++) = 0.34/0.34 = 1.00.

In each world, the remaining class-conditional cells are P(+-|Y=1)=P(-+|Y=1)=0.8-a, P(--|Y=1)=a-0.6; for Y=0, P(+-)=P(-+)=0.2-b and P(--)=0.6+b. All entries are nonnegative and sum to one. Thus even exact q, known prevalence and known verifier marginal rates cannot identify the posterior. These are constructed probability tables, **not model observations**.

### Shift taxonomy and audit
1. **Prior/label shift only**: assume a_t=a_s, b_t=b_s and all class-conditional verifier distributions fixed. Then q_t changes with pi_t; if a_s != b_s and q_t is reliably measured, pi_t=(q_t-b_s)/(a_s-b_s), subject to [0,1] feasibility. If a_s=b_s, q_t gives no prevalence information. This is an assumption-dependent identification result, not a universal estimator.
2. **Shared-error/correlation shift**: a_t or b_t changes even when single-verifier sensitivities and false-positive rates are stable. A source q_s is invalid for target inference. Require new labeled evidence or explicit worst-case bounds.
3. **Semantic and evidence shift**: changes in claim topic, paraphrase families, retrieval sources or model versions can change all parameters. Report coverage failure and abstain from transport claims.
4. **Selection shift**: a sample enriched for verifier disagreements is not representative of production q. Require sampling weights or a population-representative calibration design.

## Planned falsification tests (no cloud execution authorized yet)
- Generate tiny *synthetic* 2x2 class-conditional tables from fixed rational probabilities; enumerate all 16 joint truth/verdict combinations with exact rational arithmetic, no pretrained model or GPU.
- Compare (A) naive independence, (B) duplicate collapse, (C) source-domain point-calibration, (D) within-domain Fréchet partial-identification bounds, (E) q-constrained bounds, (F) transport-aware worst-case bounds.
- Evaluate exact coverage of the true posterior by each reported interval; width; selective-risk/coverage tradeoff at preregistered thresholds; and infeasible-assumption detection. Synthetic outcomes establish only software and mathematical correctness, **not** AI effectiveness.
- Stress test label shift separately from class-conditional dependence shift. Never claim that a method robust to one is robust to both.
- On real data, freeze claim-equivalence and evidence-lineage connected-component splits before fitting. Calibrate on labeled source families only; measure q_t from a genuinely representative unlabeled target sample; do not use target labels for tuning.
- Reject the proposed method if it fails nominal coverage under its stated assumptions, has no practical gain over simple baselines, or its useful gain disappears under source-family and claim-disjoint testing.
- Report false equivalence merges, undetected shared evidence, and shifts where the correct action is to abstain.

## Literature and originality boundary
Dependent diagnostic-test accuracy is established literature, including Walter et al. (2012), *Statistics in Medicine*, DOI: 10.1002/sim.4444, and Hudak et al. (2026), arXiv:2606.28033 (Bayesian hierarchical joint-test models with conditional dependence). These directly challenge any claim that modelling correlated verifier errors is new. Our elementary transport equation and counterexample are **not novel theorems**. Any defensible contribution must instead be a reproducible, empirically useful claim-lineage-aware selective calibration protocol under explicitly audited shift, with convincing advantages over dependent-test and calibration baselines.

References:
- https://doi.org/10.1002/sim.4444
- https://arxiv.org/abs/2606.28033
- https://docs.github.com/en/billing/concepts/product-billing/github-actions

## Strict zero-cost execution gate
GitHub documentation states standard GitHub-hosted runners are free for public repositories; larger runners may be charged, and storage is separately constrained. This does not verify this account's Actions permissions, billing settings, or current runner availability. Do not launch any workflow until those checks pass. If approved, use only a standard `ubuntu-latest` public-repository runner, short timeout, no artifacts/caches, no paid API, no downloaded models, no self-hosted laptop runner. The user's laptop is browser-only.

## Integrity and publication gate
Do not convert synthetic validation into empirical evidence. Do not claim physics relevance beyond a carefully stated analogy to correlated measurements and inverse problems. Disclose AI assistance according to the publication venue's rules. November 22 is a conditional internal target, not a commitment to publish an unsupported claim.
