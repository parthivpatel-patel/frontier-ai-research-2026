# Protocol 052 — Paired source-cluster uncertainty: executable specification

Date: 2026-11-04. Status: design only; no experimental result or execution claimed.

## Estimand and data contract

Each held-out example has immutable `example_id`, `source_cluster_id`, adjudicated `unsafe_truth` (0, 1, or unknown), and for each competing system a validation-frozen `accepted` boolean. Thresholds must be fitted on validation sources only; test labels must never enter threshold selection. Both systems must be evaluated on identical example IDs. The cluster ID must identify the *highest shared provenance* (document, physical model, template family), rather than merely a row ID. Any overlapping validation/test provenance fails admission.

Define unconditional unsafe-acceptance probability U_s = N^{-1} sum_i 1(accepted_{s,i} and unsafe_truth_i=1), and acceptance coverage C_s = N^{-1} sum_i 1(accepted_{s,i}). Primary paired contrast D = U_certificate - U_baseline (negative favors certificate), evaluated at frozen validation-calibrated operating points. Report the paired coverage contrast C_certificate - C_baseline beside D; do not interpret a lower U with materially lower coverage as an unqualified safety improvement. For unknown truth, report count, distribution by system and a conservative identification interval: unknown accepted claims can be either safe or unsafe. Never silently classify unknown as safe.

Conditional selective risk R_s = unsafe accepted / all accepted is a secondary metric; when no claims are accepted it is **undefined**, not zero. An acceptance coverage target selected on validation is not guaranteed to be achieved on test. A retrospective matched-test-coverage curve is descriptive and must be labeled separately.

## Paired cluster bootstrap

1. Construct the source-cluster partition before examining outcomes. Freeze an integer seed, 2,000 replicates and the cluster resampling rule in the run manifest.
2. In each replicate, sample K source clusters with replacement from the K held-out clusters; include *all* examples belonging to each selected cluster, preserving the baseline/certificate pair and its frozen decisions. Repeated clusters contribute repeated rows.
3. Recompute D, coverage contrasts, and identification bounds using replicate sample denominators. Never re-fit thresholds in test bootstrap replicates.
4. Report point estimates, percentile 95% intervals, K, cluster-size distribution, effective example count, and a source-level leave-one-cluster-out sensitivity table. Report Monte Carlo error / stability across additional prespecified seeds if computationally feasible.
5. If K is too small for reliable cluster inference (provisional guardrail K < 20), mark intervals exploratory, report source-level estimates and abstain from strong significance claims. This guardrail is a design choice, not a theorem guaranteeing validity above K=20.
6. For a confidence interval excluding zero, still require no material coverage degradation, independent physical-label audits, and survival of baseline and source-disjoint sensitivity checks before discussing empirical superiority.

## Falsification gates

Reject or substantially weaken the central hypothesis if (a) matched competitive baselines perform equivalently or better, (b) safety gains vanish when accounting for abstention or unknown truth, (c) results reverse across independent physical-system families, (d) source-level sensitivity is dominated by a few clusters, (e) independent adjudication finds incorrect physical assumptions/certificates, or (f) leakage or post-hoc threshold choice is detected. Multiple comparisons across coverage targets and physical families must be explicitly controlled or labeled exploratory.

## Physics / NLP evidence boundary

A formal certificate verifies a claim **relative to an explicitly stated model**. It does not establish that the model accurately captures the physical world. Each example needs a human-auditable physical-system specification, units, boundary/initial conditions, numerical tolerances where relevant, provenance, and a counterexample or independently checkable witness. The language interpretation, formalization, model fidelity, and solver correctness are separate failure modes.

## Novelty and disclosure boundary

Cluster bootstrap, selective classification, temporal-logic grounding, and physics-aware verification are prior art. The paper's possible contribution is a reproducible benchmark and a *demonstrated* comparative result under independent physical adjudication, not the novelty of these statistical methods. Explicitly compare SENTINEL, VLTL-Bench, SCP-NL2TL, GinSign and conventional selective prediction; check publication versions, licenses, and actual experimental setups before asserting distinctions. AI assistance and data/compute provenance must be disclosed according to target venue policy.

## $0 cloud gate

Do not schedule a runner until repository visibility, runner class, current GitHub Actions pricing, account billing controls, artifact retention and current quota are verified. Only standard GitHub-hosted public-repository runners may be considered; no larger runners, paid services, or card-dependent trials. Keep job timeout, permissions, concurrency and artifact retention bounded. A public repo's free standard runner policy is not proof of this account's billing configuration. No laptop compute, training, inference or downloads.

## Next implementation milestone

Implement a pure-standard-library CLI that validates the paired record schema and cluster partition, calculates D/C/R and unknown-truth bounds, performs paired source-cluster resampling with frozen thresholds, and emits a deterministic JSON report. Add fixture-based tests for singleton/imbalanced clusters, duplicate IDs, unknown truth, zero acceptance, perfect dependence, seed reproducibility and non-overlapping splits. Run tests only after zero-cost cloud eligibility is confirmed; archive authentic logs and exact source commit.
