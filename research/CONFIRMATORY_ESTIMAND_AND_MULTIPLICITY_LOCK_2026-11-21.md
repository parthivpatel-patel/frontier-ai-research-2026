# Confirmatory estimand and multiplicity lock — 2026-11-21

**Status:** proposed preregistration amendment; NOT evidence of performance, novelty, cloud eligibility, or publication readiness.

## Primary question and unit of inference
Does a temporally grounded verifier reduce **selective error** relative to a non-temporal verifier on independently adjudicated, held-out examples at the same predeclared coverage and matched total resource budget? The source-family cluster, not the individual question, is the primary unit of independent sampling. Domain-specific conclusions for NLP, mathematics, and physics require genuinely time-dependent evidence; arbitrary dates attached to timeless statements do not qualify.

For verifier v, let a_vi be a binary acceptance indicator and e_vi a binary error indicator for item i. The operational target is

R_v(c) = sum_i a_vi e_vi / sum_i a_vi,

evaluated at prespecified coverage c, with a zero-denominator result recorded as undefined. The primary contrast is Δ(c) = R_temporal(c) − R_control(c). A negative Δ favors temporal verification. Acceptance sets may differ, so this contrast is an operational selective-risk comparison, **not** proof of improved predictions on the same items or causal mediation by temporal reasoning.

## Freeze before final-test access
Record the exact eligible data snapshot, source-family assignment, license and contamination checks, calibration and test manifests, cryptographic hashes, code SHA, model/prompt revisions, verifier versions, costs and resource measurement method, threshold selection and tie-breaking rule, acceptance target c, adjudicator independence, and any exclusions. No numeric c or superiority margin is silently chosen here: these are unresolved preregistration fields, not permission to optimize on the final test. If exact equal coverage is impossible under frozen thresholds, report non-comparability and the observed coverage gap; do not refit on the final test.

## Primary analysis
1. Compare temporal and non-temporal verifiers at matched resource accounting including model calls, input/output tokens, evidence retrieval and preprocessing, with transparent treatment of unavailable cost components.
2. Report coverage and numerator/denominator for each verifier; Δ(c); source-family counts; confidence interval from prespecified **cluster-level** resampling, resampling whole source families and retaining paired items. Do not interpret item-level bootstrap intervals as independent-family inference.
3. Include a prespecified paired permutation/sensitivity analysis only where its exchangeability assumptions are defensible; otherwise label it descriptive. Do not equate a McNemar test on different acceptance sets with a valid primary test.
4. Report acceptance-set intersection, temporal-only and control-only accepted items, error differences on the shared accepted subset, and full-coverage prediction error. These diagnostics cannot replace the primary estimand.
5. Leave-one-source-family-out estimates must show changes in coverage and whether the comparison becomes undefined. If there are too few independent families for reliable inference, report descriptive estimates and withhold statistical superiority claims.

## Multiplicity and failure gates
The single primary contrast is the prespecified pooled, domain-stratified estimate at one coverage target; the weighting scheme must be locked without viewing test outcomes. Domain-specific NLP, mathematics, and physics effects, alternative coverages, and subgroup analyses are **secondary/exploratory** unless a multiplicity correction and family of tests are explicitly locked in advance. Do not select the most favorable domain or coverage post hoc. Record all attempted comparisons and null results.

Required mechanism challenges: timestamp permutation (with OOD caveat), evidence removal, chronology-preserving placebo, and matched non-temporal evidence controls. If chronology-insensitive controls perform similarly, do not attribute any improvement to temporal ordering. If effects disappear after matched resource accounting, do not claim a compute-efficient advantage. If independent labels, source separation, or provenance fail, no confirmatory empirical conclusion is permitted.

## Feasibility and publication
The November 22 checkpoint is a **go/no-go decision**, not a promise of a discovery paper. A methods/preregistration manuscript must prominently state that it is unvalidated and must cite closest prior art in temporal verification, selective prediction, conformal risk control, adaptive data analysis and benchmark contamination. Similarity to those fields is a collision risk; novelty is unproven until a structured comparison and experimental falsification are completed.

This document requires no laptop workload and authorizes no paid resources, GPU deployment, inference, or billing enrollment. Any proposed free cloud provider must be checked separately for current quotas, access, card requirements and actual availability.
