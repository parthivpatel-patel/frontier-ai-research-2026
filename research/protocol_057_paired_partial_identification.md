# Protocol 057 — Paired partial-identification bounds for unresolved physical truth

Status: methodological specification, **not** experimental evidence. Date: 2026-11-04.

## Research question

Does a certificate-gated scientific-claim acceptance system reduce unsafe acceptance relative to a baseline, when some physical claims cannot be adjudicated? The analysis must not silently discard unresolved claims or assume they are correct.

## Definitions and exact finite-sample identification

For each held-out claim i, let B_i and C_i be binary baseline and certificate-system acceptance decisions, frozen before examining test labels. Let Y_i=1 denote a physically false claim and Y_i=0 a true claim. Y_i is observed only for independently adjudicated cases O; unresolved cases form U. Let N=|O|+|U|. Define the *paired unconditional unsafe-acceptance difference* (certificate minus baseline):

D = (1/N) sum_i (C_i-B_i) Y_i.

A negative value favors the certificate system. For observed truth, set S = sum_{i in O}(C_i-B_i)Y_i. For unresolved i, the coefficient d_i=C_i-B_i belongs to {-1,0,1}. Without assumptions about their unknown binary labels, the **sharp bounds** are

L = [S + sum_{i in U} min(0,d_i)] / N,

H = [S + sum_{i in U} max(0,d_i)] / N.

Sharpness follows because each unresolved Y_i can independently be set to 0 or 1 to attain each extreme. A paired comparison is essential: if both systems accept the same unresolved claim, d_i=0 and it cannot affect the difference, although it affects each method's absolute unsafe acceptance.

For each method M in {B,C}, absolute unconditional unsafe acceptance has bounds

[sum_{i in O} M_i Y_i / N, (sum_{i in O} M_i Y_i + sum_{i in U} M_i) / N].

Report all three intervals, unresolved-label rate, number of distinct source clusters, coverage of each method, and observed-only conditional error with its denominator. Never present observed-only conditional error as population risk without a missingness assumption.

## Worked algebraic falsification control (illustrative, NOT observed data)

Take N=4. On two adjudicated cases, the paired unsafe-acceptance difference sums to S=-1. On two unresolved cases, one has d=+1 and the other d=-1. Then L=(-1-1)/4=-0.5 and H=(-1+1)/4=0. A claim of strictly lower unsafe acceptance is **not identified**, despite the negative observed contribution. This is a hand-constructed unit-test target, not an experiment.

## Deployment and inference gates

1. Thresholds are chosen only on validation data, then frozen on the source-disjoint test split. Report actual test coverage; do not force matched test coverage using test labels or confidence rankings.
2. Source-disjointness applies to documents, physical systems, generation templates, and near duplicates. Disclose any unavoidable overlaps.
3. Report finite-sample identification intervals separately from uncertainty intervals. A cluster bootstrap of the lower and upper bound estimators may quantify sampling uncertainty, but must not be called a confidence interval for a point-identified effect.
4. Resample independent source clusters, preserving all within-cluster examples and paired system outputs. Recompute S, L, H, and denominators on each replicate. Report the number of clusters and bootstrap failure/sparsity diagnostics; no inferential claims with too few independent clusters.
5. If H >= 0, the data do not establish that certificates reduce unsafe acceptance under arbitrary unresolved labels. Even if H < 0, also evaluate acceptance coverage and accepted-claim error; a trivial reject-all system must not be counted as a scientific advance.
6. Independently adjudicate physical claims using explicit assumptions, units, boundary conditions, equations, and source provenance. Unknown, disputed, or model-dependent claims remain unresolved; a language model's self-rating is not ground truth.
7. Compare with at least: ungated baseline, confidence-only abstention, symbolic/unit checks without certificates, and certificate verification with matched budgets. Preregister primary endpoint, coverage floor, and falsification criteria before held-out evaluation.

## Prior-art positioning and novelty gate

Partial identification under missing outcomes is established statistical methodology, not novel. Selective prediction, conformal risk control, formal methods, and scientific claim verification are also established areas. Potential novelty would require an independently demonstrated, generalizable improvement from *physically meaningful certificates* over strong controls, not simply a new bootstrap or thresholding scheme.

Prior-art starting points (verify exact scope and citations before manuscript):
- Manski (1990), Nonparametric Bounds on Treatment Effects, American Economic Review. https://www.jstor.org/stable/2006592
- Geifman & El-Yaniv (2017), Selective Classification for Deep Neural Networks. https://arxiv.org/abs/1705.08500
- Angelopoulos et al. (2024), Conformal Risk Control. https://arxiv.org/abs/2208.02814
- Cobbe et al. (2021), Training Verifiers to Solve Math Word Problems. https://arxiv.org/abs/2110.14168

These are starting points, not a completed novelty audit. Closest work in physics-language formalization and proof-carrying reasoning still needs targeted review.

## Execution and resource policy

Implement the bounds as pure standard-library Python with deterministic tests for all-unknown truth, identical decisions, opposing decisions, empty acceptance, and known-label recovery. Execute only after verifying an actually available zero-cost hosted runner, account billing limits, and card requirements. Do not use the user's laptop for computation. Do not report tests as passing until actual cloud logs are retained. No model inference or paid resource is authorized.

## Publication decision

The November 22, 2026 target is conditional. No claim of novelty, safety improvement, or publication readiness is justified by this protocol alone. Document AI assistance and experimental provenance according to venue policy.
