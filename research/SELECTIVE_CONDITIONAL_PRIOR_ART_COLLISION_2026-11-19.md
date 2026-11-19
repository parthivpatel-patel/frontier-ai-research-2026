# Closest-prior-art collision audit: conditional and selective guarantees (2026-11-19)

Status: literature screening and falsifiable design, **not** a novelty claim or empirical result.

## Additional directly relevant primary sources

1. Gibbs, Cherian & Candès, *Conformal Prediction With Conditional Guarantees* (2023 preprint), https://arxiv.org/abs/2305.12616. This work explicitly relates conditional guarantees to classes of covariate shifts and gives subgroup-oriented guarantees. Therefore group-conditional evaluation and robustness to a specified shift class are not inherently new.
2. Xu, Guo & Wei, *Selective Conformal Risk Control* (December 2025 preprint), https://arxiv.org/abs/2512.12844. It explicitly combines selective classification and conformal risk control; a proposed two-stage accept-then-calibrate architecture would collide with this work unless a substantive distinction is established.
3. Zecchin et al., *Generalization and Informativeness of Weighted Conformal Risk Control Under Covariate Shift* (2025 preprint), https://arxiv.org/abs/2501.11413. It studies weighted risk control under covariate shift, including efficiency; reweighting or shift-sensitive risk calibration alone cannot support novelty.
4. Xu et al., *Robust Conditional Conformal Prediction via Branched Normalizing Flow* (May 2026 preprint), https://arxiv.org/abs/2605.01868. It studies conditional invalidity under shift and transport-based remedies. The present project does **not** propose or claim a new transport guarantee.

These references require full-text theorem/assumption comparison before any novelty claim. Abstract-level screening cannot certify uniqueness.

## Proposed narrow, falsifiable empirical question

On *the same frozen candidate answers*, does an independently scored verifier improve **paired accepted-answer correctness** under held-out source-family shifts in NLP, mathematics and physics, at prespecified family coverage and verifier-only compute budgets, against confidence-only, selective prediction, and feasible conformal/risk-control baselines?

This is an empirical hypothesis, not a new theoretical guarantee. A cross-domain benchmark alone is not novel unless its construction, auditability or experimentally established phenomenon adds something beyond prior work.

## Non-negotiable estimands and audit constraints

For family f and verifier v, record acceptance A_v, correctness Y from independent adjudication, per-answer verifier compute C_v, family coverage q_vf = sum(A_v)/n_f, and selective error e_vf = sum(A_v(1-Y))/sum(A_v) when denominator > 0. Report undefined selective error when no answers are accepted. Use a prespecified fixed family-weight vector for macro aggregation; do not replace family risks with pooled risk. Use paired comparisons on the same answer IDs. Cost must include scoring, calibration amortization and abstention decisions; report inference compute separately from candidate generation. Thresholds are frozen using development/calibration data before evaluating held-out shifts. Do not tune on test labels.

The paired accepted-error identity is only a diagnostic at equal coverage; unequal accepted sets still require explicit accounting of discordant acceptances. Group-specific coverage tolerance and score-tie feasibility must be checked before making matched-coverage claims. Where target labels are absent, arbitrary-shift reliability is not identifiable without additional assumptions; report bounds or abstain from guarantee claims.

## Predeclared failure / falsification gates

- **Novelty failure:** a prior method already establishes the same distinctive method or experimental result; reposition as replication or benchmark, not discovery.
- **No efficacy:** the candidate fails to improve prespecified family-balanced error against strongest feasible baseline, with uncertainty intervals excluding a practically meaningful advantage.
- **Selection confounding:** a claimed advantage disappears at matched family coverage or is explained by changes in the accepted-answer mixture.
- **Cost confounding:** advantage disappears at equal verifier-only compute or requires paid/GPU infrastructure.
- **Shift fragility:** advantage fails in at least one preregistered family or held-out source shift; report heterogeneity instead of universal superiority.
- **Adjudication leakage:** labels, answer keys, near-duplicates, source families or test prompts leak into training/threshold selection.
- **Invalid guarantee:** any claimed finite-sample or distribution-shift guarantee fails its required assumptions or independent check.

## Minimal cloud execution plan and $0 gate

Use only standard GitHub-hosted runners for this public repository (e.g., ubuntu-latest), with standard-library synthetic invariant tests first. GitHub documentation currently says standard hosted runners in public repositories are free, while larger runners are billed: https://docs.github.com/en/billing/concepts/product-billing/github-actions . Avoid larger/GPU runners, paid APIs, artifact uploads and excessive caches. Account-specific billing configuration, permissions and limits are **not verified** by this note; inspect workflow configuration and account eligibility before any new execution. No laptop compute. For genuine held-out experiments, use only verified openly licensed small existing answer/label datasets or no-charge cloud compute; do not infer model results from synthetic tests.

## Release gate (November 22 checkpoint)

Publish an empirical paper only if independently executed experiments, reproducible evaluation data, credible baselines, provenance, uncertainty, disclosure, and defensible distinct contribution all exist. Otherwise publish a clearly labeled protocol / negative-results or methods report, not an invented result.
