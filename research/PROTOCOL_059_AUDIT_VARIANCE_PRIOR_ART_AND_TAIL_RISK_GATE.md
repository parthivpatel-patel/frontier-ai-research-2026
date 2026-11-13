# Protocol 059 — Audit-variance prior-art collision and tail-risk gate

Date: 2026-11-13. Status: literature-grounded methodological audit; no experiments executed; no original theorem claimed.

## Why this checkpoint matters

Protocol 058 correctly derives design variance from first- and second-order inclusion probabilities. It does **not** follow that these probabilities determine the entire sampling distribution, the validity of normal confidence intervals, or reliable tail-risk control. This protocol separates (a) unbiased point estimation, (b) variance identification, (c) variance estimation from observed labels, and (d) confidence coverage. These are different guarantees.

The existing fixture `research/fixtures/test_joint_inclusion_variance.py` uses full synthetic population truth labels in its `plug_in_variance` guard to detect a zero-probability pair. That is legitimate in a constructed oracle test but **not implementable as a real audit diagnostic**: labels of unaudited units are unknown. The operational gate must inspect the sampling design's full pairwise inclusion matrix independently of truth labels. In particular, if any pair of eligible units has pi_ij=0, do not advertise a general design-unbiased pairwise plug-in variance estimator. This is a specification correction; no claim that the existing fixture was executed or failed.

## Closest verified prior art

1. Peter M. Aronow and Cyrus Samii, *Conservative variance estimation for sampling designs with zero pairwise inclusion probabilities*, Survey Methodology (2013), Statistics Canada: https://www150.statcan.gc.ca/n1/pub/12-001-x/2013001/article/11831/section1-eng.htm . This directly addresses the non-measurable sampling designs highlighted in Protocol 058 and develops conservative bias correction. Any claim that our zero-pair handling is novel would collide with this work.
2. Aronow and Samii, variance decomposition: https://www150.statcan.gc.ca/n1/pub/12-001-x/2013001/article/11831/section2-eng.htm . This establishes that first-order positivity permits HT total unbiasedness but is insufficient for general unbiased design variance estimation if joint inclusion is zero.
3. Justin T. Greene and Tirthankar Dasgupta, *Variance Estimation Under Local Pivotal Methods*, arXiv:2610.05464 (2026): https://arxiv.org/abs/2610.05464 . Contemporary approaches use estimated pair inclusion and model-assisted bootstrap when pair probabilities are difficult to obtain. Not equivalent to AI auditing, but a strong method comparator.
4. Jiahua Chen, *Low-Order Inclusion Probabilities Do Not Determine Asymptotic Normality*, arXiv:2610.09168 (2026): https://arxiv.org/abs/2610.09168 . The reported counterexample shows matching first- and second-order inclusion probabilities need not yield matching asymptotic laws. Treat as a preprint requiring independent scrutiny, not as independently reproduced proof.

This is a targeted collision audit, not a comprehensive systematic review of AI selective prediction, conformal risk control, physics verification, or verifier-dependence modeling.

## Conservative finite-sample bound, with limitations

For a fixed finite population and an HT estimator with *known exact* design variance V, Chebyshev yields P(|T_hat-T| >= sqrt(V/alpha)) <= alpha for alpha in (0,1), with probability taken over the sampling design. This is a classical inequality, not a novel method. It does not produce an implementable interval when V is unknown. Replacing V with an arbitrary plug-in estimate **does not** preserve this finite-sample coverage guarantee. A rigorously proven deterministic upper bound V_upper >= V would suffice, but may be too loose for practical use.

For a known stratum size M, divide the total and radius by M to target the stratum mean. If M=0, the conditional reliability estimand is undefined and must not be reported as zero or perfect. If audit probabilities depend on unrecorded verifier decisions, even the HT unbiasedness claim may fail.

## Required new tests and falsification

- Implement a design-only `validate_joint_inclusion(pi, pi_ij)` check before seeing truth labels; reject zero off-diagonal pairs for generic unbiased plug-in variance claims, while allowing point estimation when all pi_i>0.
- Enumerate small complete sampling designs using exact fractions and check direct moments against the pairwise identity, including heterogeneous labels and negative cross-covariances.
- Distinguish *known variance* oracle Chebyshev intervals from estimated-variance intervals; prohibit unconditional coverage assertions for the latter.
- Compare against Aronow–Samii conservative correction and suitable cluster-robust/design-aware alternatives; preregister sample sizes, audit budgets, dependence regimes and evaluation units.
- For mathematical and physics claims, adjudicate truth under explicitly stated axioms, physical model, parameter range, and units; do not treat two paraphrases as independent ground-truth labels.
- For NLP claims, use held-out source and claim families; compare calibrated selective prediction, duplicate-aware aggregation and audit-design-aware baselines at equal independent-labeling cost.
- Report failure if the proposed method does not improve prespecified family-level risk–coverage or audit efficiency over strong baselines, or if coverage falls below the declared target in shift stress tests. No post-hoc novelty rescue.

## Zero-cost cloud gate

GitHub's published Actions billing documentation says **standard GitHub-hosted runners on public repositories are free**, while larger runners and storage have different rules: https://github.com/github/docs/blob/main/content/billing/concepts/product-billing/github-actions.md . This establishes a platform-level candidate, **not** this account's enabled Actions status, available runner capacity, spending limits, payment-method state, or storage position. Do not launch a workflow until account/repository settings and the exact workflow configuration are checked. If approved, use a standard Linux runner, a minimal standard-library job, short timeout, no artifacts or caches, no GPU, no external inference, no third-party hosted models, and no laptop computation. Do not claim $0 eligibility merely because a repository is public.

## Publication and disclosure

The target date 2026-11-22 is conditional. No tests were executed, no cloud jobs were started, and no empirical performance or novel theorem is claimed here. Disclose AI assistance as required by the eventual venue; retain code, provenance, negative results, and the distinction between synthetic proofs and measured results.
