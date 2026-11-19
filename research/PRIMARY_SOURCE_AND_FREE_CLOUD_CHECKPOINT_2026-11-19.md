# Primary-source checkpoint: selective prediction and free-cloud feasibility

Date: 2026-11-19. Scope: limited primary-source verification; not a comprehensive literature review, empirical result, or novelty certification.

## Verified closest prior art

**Geifman and El-Yaniv (2017), _Selective Classification for Deep Neural Networks_, NeurIPS.** Primary conference record: https://mlanthology.org/neurips/2017/geifman2017neurips-selective/ ; preprint https://arxiv.org/abs/1705.08500 . The authors construct a selective classifier from a trained network, targeting a user-specified risk level through rejection. Consequently, risk-controlled abstention, a target selective risk, and an observed risk–coverage tradeoff are **not new contributions** of this project.

**Geifman and El-Yaniv (2019), _SelectiveNet: A Deep Neural Network with an Integrated Reject Option_, ICML/PMLR 97.** Primary proceedings: https://proceedings.mlr.press/v97/geifman19a.html . The authors optimize prediction and rejection jointly and evaluate risk–coverage improvements. Consequently, end-to-end learned rejection and generic superiority over confidence-threshold abstention are already established research directions.

These sources were checked against primary conference abstracts/records, **not audited line by line against the full PDFs**. Remaining candidate references in PRIOR_ART_FALSIFICATION_AUDIT_2026-11-19.md require the same scrutiny. No claim of a novel theorem, mechanism, or benchmark follows from this checkpoint.

## Narrowest plausible contribution, pending falsification

An empirical *audit protocol* might contribute evidence about whether pre-calibrated, source-family-shifted verifier comparisons remain valid after enforcing (i) identical candidate-answer rosters, (ii) frozen deployment thresholds, (iii) complete measured cost including abstentions, (iv) explicit achieved-coverage mismatch, and (v) source-family clustered uncertainty across NLP, mathematics, and physics. Each ingredient has precedents; only a rigorous comparison against the closest combinations could support a novel contribution. The three domains are evaluation strata, not a claim that NLP and mathematical physics share a new physical law.

**Null/failure outcomes to publish:** no improvement over confidence-only and random-abstention baselines; a benefit that vanishes at matched achieved coverage; budget mismatch beyond the preregistered 5% relative measured-cost tolerance; failure on held-out source families; uncertain or disputed labels; leakage; no statistically defensible gain after multiple-comparison controls. Frozen-threshold operational results and transductive exact-k rankings must be separately labeled. Do not choose held-out thresholds to repair infeasible coverage matching.

## Free cloud policy checkpoint

GitHub's official billing documentation says standard GitHub-hosted runners in **public repositories** are free, while **larger runners are billed even for public repositories**: https://docs.github.com/en/billing/concepts/product-billing/github-actions . GitHub's 2026 pricing announcement also states public-repository standard runner usage remains free: https://github.com/resources/insights/2026-pricing-changes-for-github-actions .

**Permitted future CI design:** public-repository workflow on a standard GitHub-hosted Ubuntu runner only; bounded, dependency-light Python unit tests; no GPU; no model downloads; no paid APIs; no large artifacts; no paid larger runners. Add a timeout, minimal token permissions, and no secrets. Public-repository eligibility does **not** prove this account has Actions enabled, that jobs are currently schedulable, or that a specific job has passed. Account-specific eligibility and workflow status must be checked before describing any cloud execution as successful. No card or billing enrollment should be requested for this protocol.

## Publication gate (November 22 internal checkpoint)

If CI and genuinely independent held-out evaluations are not completed, publish a clearly labeled methods/preregistration note, not an empirical breakthrough. Disclose assistance in accordance with venue rules, report negative findings, preserve versioned evaluation manifests and provenance, and do not imply endorsement by OpenAI, Anthropic or Google DeepMind.
