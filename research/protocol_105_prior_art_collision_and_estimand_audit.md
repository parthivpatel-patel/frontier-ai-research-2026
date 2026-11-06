# Protocol 105 — Prior-art collision and estimand correction audit

Date: 2026-11-06. Status: literature triage and mathematical correction; **no experiments, theorem of novelty, or empirical superiority established**.

## Important novelty collision found

Protocol 104 correctly acknowledged classic selective classification but did not include several directly relevant **2025–2026 selective/conformal risk-control papers**. This materially narrows what the project may claim.

| Work | Date / source | Direct overlap | Required differentiation |
| --- | --- | --- | --- |
| Xu, Guo and Wei, *Selective Conformal Risk Control* | 2025-12-14, https://arxiv.org/abs/2512.12844 | Joint abstention and risk-controlled prediction sets; finite-sample and PAC-style variants | Do **not** claim selective risk control or abstention with guarantees is novel. |
| Wang, Fan and Wang, *SAFER: Risk-Constrained Sample-then-Filter in Large Language Models* | 2025-10-11, https://arxiv.org/abs/2510.10193 | Open-ended LLM QA, abstention-aware sampling, conformalized filtering | Compare against a risk-constrained LLM baseline where feasible. |
| Salem et al., *Hierarchical Group-Conditional Conformal Risk Control for Selective Prediction in Language Models* | 2026-07-27, https://arxiv.org/abs/2607.24562 | **Especially close**: group-specific risk budgets under domain/difficulty shift; reports groupwise violations and abstention costs | Family-specific risk and protection against pooling reversals **alone are not novel**. Compare to group-conditional risk control; inspect assumptions and limitations in full text. |
| Basu, *Cross-Domain Uncertainty Quantification for Selective Prediction* | 2026-03-09, https://arxiv.org/abs/2603.08907 | Domain transfer and finite-sample risk bounds for selective prediction | Do not claim domain-transfer or family-conditional guarantees without distinguishing these methods. |
| Deutschmann et al., *Conformal Autoregressive Generation* | AAAI 2024, https://doi.org/10.1609/aaai.v38i10.29062 | Conformal guarantees in NLP generation | Clarify why the research concerns verification of physics claims, not novel sequence-set coverage. |

These are bibliographic leads confirmed from publicly available abstracts/metadata, **not** a completed full-text or citation-forward systematic review. Search additional physics verification, scientific hallucination, mechanistic consistency and theorem-proving work before submission. No frontier-lab endorsement implied.

## Critical mathematical correction to Protocol 104

Protocol 104 defines family-specific unsafe-acceptance risk R_vf(c) at matched coverage c and then averages over a deployment mixture. This is interpretable only where **both methods have attainable and nonzero acceptance within each family at the same preregistered target coverage**. Pooled matched coverage does not imply familywise matched coverage (Protocol 095's reversal illustrates this). A common familywise c may be infeasible, especially with discrete score ties or abstention.

Pre-register the following:
1. Let A_v(i,t) be acceptance at threshold t; Y_i=1 if the frozen label definition calls claim i unsafe; F_i the physics family; L_i the independent scenario lineage.
2. For each family f, report C_vf(t)=P(A_v=1|F=f) and R_vf(t)=E[Y A_v|F=f]/E[A_v|F=f] when the denominator is positive. An empty accepted cell is **undefined**, never zero.
3. Select thresholds **using calibration data only**, with deterministic tie-breaking or prespecified randomization. Do not tune on held-out test outcomes or retroactively force identical empirical test coverage.
4. Declare a feasible common calibration coverage grid and tolerance epsilon. If a method cannot attain the grid point in a family, label the contrast non-identifiable and report its achieved coverage, rather than extrapolating.
5. For fixed nonnegative weights w_f summing to 1, compute standardized conditional risk sum_f w_f R_vf only when all positively weighted family risks are defined. Also report pooled unsafe accepted count / accepted count separately; the two estimands are different.
6. Quantify uncertainty at the **source-family or scenario-lineage cluster level**, depending on the sampling design. If too few independent clusters exist, do not report a misleading narrow bootstrap CI or distribution-free guarantee.
7. A model's *calibration-sample* conformal guarantee does not automatically survive source-family holdout, adversarial paraphrases or distribution shift; report assumptions explicitly. A per-group marginal guarantee is not a guarantee for every individual claim.

## Refined falsifiable research hypothesis

The defensible **candidate** contribution is an empirically tested, physics-assumption-intervention benchmark of *evidence dependence* and selective safety under unseen source lineages, with blinded adjudication and matched-budget baselines. Even that benchmark may overlap existing work. A useful negative result would show where apparently reliable scientific verifiers fail when the physical model or assumptions change.

**Disconfirming outcomes:** performance indistinguishable from matched retrieval and deterministic physics checks; no degradation when evidence is removed/shuffled; high cross-source variance; contradictory independent adjudications; poor transfer to held-out physics families; or full-text prior art demonstrating the same intervention protocol.

## Execution and billing gate

GitHub's official 2026 documentation states that **standard GitHub-hosted runners in public repositories are free** (https://docs.github.com/en/billing/concepts/product-billing/github-actions and https://github.blog/changelog/2026-01-01-reduced-pricing-for-github-hosted-runners-usage/). **Larger runners are charged**, even for public repositories; storage limits apply. This repository's public visibility was confirmed through the connected GitHub account on 2026-11-06. However, **account-specific Actions permissions, billing state, runner availability and card requirements have not been confirmed**. Accordingly, no workflow is launched or billed. Only standard hosted runners may be considered after account-specific checks. Do not run laptop workloads or paid inference.

## Publication integrity

Treat all protocols and fixtures as methodological artifacts, not empirical model evaluations. Require dated model versions, permitted dataset licenses, real independently adjudicated claims, full baseline logs, and disclosure of AI-assisted drafting/coding according to venue policy. The 2026-11-22 date is a conditional internal target.
