# Audit-label sensitivity and partial identification (2026-11-19)

Status: theoretical protocol / no model results. This note does not claim a new theorem.

## Problem

For each scientific domain d (NLP, mathematics, physics), let A=1 mean that a frozen verifier accepts a fixed model answer, and E=1 mean an independently adjudicated error. The target selective risk is R_d=P(E=1|A=1,d), defined only if P(A=1|d)>0. If correctness is unavailable for some accepted answers, observed accepted-answer accuracy is not an unbiased estimate of R_d without assumptions on label availability.

## Exact finite-sample identification interval

Among N accepted answers in domain d, suppose m have independently adjudicated labels, e of which are errors, and u=N-m are unadjudicated. With no assumptions on missingness, the finite-set error fraction is bounded sharply by

    e/N <= R_d,finite <= (e+u)/N.

Proof: each of the u unknown binary error indicators can contribute either zero or one; both extremes are attainable. This is a finite-dataset identification statement, not a population confidence interval, and does not assume missing-at-random.

If an audit selects accepted answers uniformly at random with known inclusion probabilities, use a design-based estimate and confidence interval, with uncertainty reflecting the sampling design. If audits oversample difficult cases, use the known inclusion probabilities and appropriate design-based variance; do not treat the labeled subset as representative. If labels are missing for unknown reasons, retain the identification interval and report sensitivity analyses rather than declaring the observed subset representative.

## Paired verifier comparison

For verifiers V and W, fix the answer set and domain-specific coverage targets before evaluation. Report the error indicators and acceptance decisions for the same task IDs, and account for overlap of accepted sets. A difference in risk among different accepted subsets is not a per-question causal effect. If acceptance rates differ, report both risks and coverage; do not claim matched-coverage superiority.

For each domain, report: total tasks, accepted tasks, adjudicated accepted tasks, observed errors, unresolved labels, label-selection mechanism, verifier cost, and risk identification bounds. The unweighted macro average of domain risks must be clearly distinguished from a prespecified weighted average. If any domain has zero acceptance, its selective risk is undefined; do not silently substitute zero.

## Prespecified falsification and release gates

1. Reject any empirical superiority claim if the worst-case identification bounds overlap too widely to establish the claimed sign without additional justified assumptions.
2. Reject generalization claims when improvement disappears on held-out source families or under domain-balanced aggregation.
3. Treat label disagreement, unverifiable scientific claims, and incomplete adjudication as separate measured outcomes, not automatically as correct answers.
4. Freeze prompts, thresholds, cost accounting, audit sampling and adjudication rubric before looking at held-out results.
5. Compare against confidence-threshold rejection, random rejection at matched coverage, and domain-specific calibrated baselines.
6. Publish full task IDs, permissible data provenance, audit inclusion probabilities, and CI evidence before making reproducibility claims.

## Closest established prior art

Selective risk and coverage are standard: Geifman & El-Yaniv, *Selective Classification for Deep Neural Networks*, NeurIPS 2017, https://papers.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html ; and Geifman & El-Yaniv, *SelectiveNet*, ICML 2019, https://proceedings.mlr.press/v97/geifman19a.html . Finite-sample missing-label bounds are elementary partial identification, not novel. The potential publishable contribution must instead survive a detailed literature comparison and demonstrate genuinely new methods or empirical cross-domain evidence.

## Zero-cost execution boundary

Repository is public. GitHub documents that standard GitHub-hosted Actions runners in public repositories are free, but larger runners are charged and storage has separate limits: https://docs.github.com/en/actions/concepts/billing-and-usage and https://docs.github.com/en/billing/concepts/product-billing/github-actions . Do not enable larger runners, paid artifacts, paid APIs or third-party GPU accounts. No user laptop computation. Account-level billing/storage state and eligibility are not independently verified here, so do not start new resource-intensive jobs until checked.

## Evidence status

This note is a prespecified analysis framework. No empirical model results, new cloud run, or original novelty are asserted. The November 22 checkpoint is a conditional decision, not a guaranteed publication date.
