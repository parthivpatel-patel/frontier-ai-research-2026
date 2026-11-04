# Protocol 059 — Reproducibility inventory and benchmark admission gate

Date: 2026-11-04. Status: research protocol, **not** an experimental result.

## Why this gate exists

A commit or an authored test is not evidence that a test passed. A mathematical bound is not a statistical confidence interval. An internally generated physics example is not independent validation. Prior protocol summaries have described pending cloud runs; until job URLs, commit SHAs, exact commands, and raw outputs are attached, no execution claim should be made.

## Required evidence manifest for every experiment

Record: immutable source commit; data provenance and license; source-document cluster identifier; train/validation/test split hashes; exact command; Python/dependency versions; runner and job URL; UTC start/end; exit code; raw stdout/stderr; generated artifact hashes; cost and billing safeguards; and whether ground truth was independently adjudicated. Missing fields are explicitly `unverified`, never inferred.

## First source-disjoint physics benchmark: admission rules

Use public-domain or appropriately licensed physical problem statements. Group every paraphrase, numerical variant, and derivative of the same source problem in the same source cluster **before** splitting. Hold out entire source clusters, not only rows. Maintain an immutable challenge set that cannot influence thresholds, prompts, or model selection.

Each item must include (1) the original text and provenance, (2) a machine-readable claim and units, (3) explicit physical assumptions and domain of validity, (4) an independently derived adjudication with references or a reproducible symbolic/numerical check, (5) an `unknown` truth option, and (6) a documented reason when translation from natural language is ambiguous. Blind the adjudicator to the candidate system's decision.

Begin with controlled problems in dimensional consistency, conservation laws, and elementary mechanics. These are **sanity checks**, not evidence of frontier-level novelty. Add out-of-distribution cases involving boundary conditions, underspecified assumptions, nonidentifiable parameters, and physically invalid but algebraically consistent claims. Preserve negative and ambiguous cases, not only successful certificates.

## Mandatory baselines and ablations

Compare on exactly the same held-out sources: direct answer without abstention; confidence-thresholded answer; language-to-symbolic translation plus a standard solver; and proposed certificate-based acceptance. Where feasible include a strong model with tool use and matched inference budgets. Ablate the certificate, translation checks, and uncertainty calibration separately. Pre-register prompt selection and threshold choice on validation only.

## Primary estimands and falsification

Report acceptance coverage, unsafe accepted claims per all eligible claims, and error among accepted *adjudicated* claims. For unresolved truth, publish sharp identification bounds for unsafe acceptance and paired method differences. A claim of lower risk requires a paired bound excluding zero in the favorable direction, together with an uncertainty procedure accounting for source clustering. An interval touching zero, failure at matched coverage, loss of effect under source-disjoint splitting, or superiority explained by abstention alone **falsifies the strong improvement claim**. Report all such outcomes.

## Prior art to evaluate before a novelty claim

- Geifman & El-Yaniv (2017), *Selective Classification for Deep Neural Networks* — risk-coverage framework.
- Angelopoulos & Bates (2023), *Conformal Prediction: A Gentle Introduction* — distribution-free uncertainty, with its assumptions.
- Cobbe et al. (2021), *Training Verifiers to Solve Math Word Problems* — learned verification.
- Lightman et al. (2023), *Let's Verify Step by Step* — process supervision.
- Yang et al. (2023), *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models* — formal theorem proving infrastructure.
- Trinh et al. (2024), *Solving Olympiad Geometry without Human Demonstrations* — neuro-symbolic formal geometry.

These are initial anchors, **not an exhaustive novelty audit**. Compare problem setting, proof/certificate semantics, distribution, baselines, and evaluation protocol directly before asserting a gap.

## Cloud-only, zero-spend release gate

Do not run jobs until the repository's visibility, GitHub Actions eligibility, available minutes, billing controls, and actual account-specific safeguards are confirmed. Public-repository hosted runner pricing is not sufficient evidence of this account's safe configuration. No self-hosted runner on the user's laptop. No paid model API, credit-card signup, or trial that can silently become chargeable. If any condition is unknown, remain in design/review mode.

## Publication rule

Target November 22 only if an independent source-disjoint benchmark, competitive baselines, raw evidence, uncertainty audit, and substantive novelty review are complete. Otherwise publish a clearly labeled technical report or defer. Disclose assistance and computational provenance according to venue requirements.
