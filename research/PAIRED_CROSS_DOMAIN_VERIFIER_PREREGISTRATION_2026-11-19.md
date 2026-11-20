# Cross-domain verifier audit: paired estimands, negative controls, and release gates
Date: 2026-11-19
Status: preregistration/methodology only; no empirical results or novelty claim.

## Primary question
At fixed, prespecified **within-family acceptance coverage** and comparable verification compute, does a candidate verifier lower accepted-answer error relative to a baseline on source-held-out NLP, mathematics, and physics tasks?

This question is not itself novel. Selective classification and risk–coverage methods predate this project; a cross-domain evaluation alone does not establish methodological novelty.

## Units and frozen protocol
An evaluation unit is (task_id, source_id, family, base_answer_id, verifier_id, verifier_score, acceptance, adjudicated_correctness, verifier_compute). All verifiers must assess the **same frozen base answer** per task. Split by source and task *before* fitting thresholds; prevent near-duplicate contamination across splits. Record ambiguous and unadjudicable labels separately; no silent exclusion. Freeze prompt templates, task selection, adjudication rubrics, thresholds, costs, and aggregation weights before held-out scoring.

For family f, define coverage C_vf = sum_i A_vi / n_f, and accepted error R_vf = sum_i A_vi(1-Y_i) / sum_i A_vi, only if the denominator is nonzero. Define D_f = R_candidate,f - R_baseline,f at a prespecified comparable coverage. Negative D_f favors candidate. Report coverage and error **together**, including raw numerators/denominators; undefined risk is not zero. If exact coverage is impossible because of score ties, do not claim exact matching: report attainable thresholds and their mismatch, or preregister randomized tie-breaking with a fixed seed and repeated-seed sensitivity analysis.

Primary summary D = (D_NLP + D_math + D_physics)/3 only when all three family-specific estimands are defined and meet the coverage tolerance. Otherwise primary summary is not estimable. The equal weights are a normative evaluation choice, not a claim about deployment frequency. Report pooled, macro, and per-family outcomes separately to expose aggregation reversals.

## Statistical discipline
Paired inference must preserve common task/answer outcomes. Bootstrap by source cluster (not independently by verifier), stratified by family, with cluster count and interval construction reported. When too few independent source clusters exist, bootstrap confidence intervals are unreliable; label results exploratory and use transparent sensitivity analyses. Report simultaneous or multiplicity-adjusted uncertainty for three family outcomes, plus a prespecified overall endpoint. Do not turn a non-significant result into an equivalence claim.

## Essential baselines and controls
1. Baseline score threshold and random acceptance at matched within-family coverage.
2. Simple confidence/length heuristics, where available; compare at matched verifier cost.
3. Score permutation within source/family as a negative control: any apparent improvement should disappear in expectation; report realized variation.
4. Label-shuffle sanity check only in a sandboxed *evaluation copy*: should destroy genuine score–correctness association. Never use shuffled labels for model selection.
5. Answer-only and verifier-only ablations to test whether improvements are caused by answer quality or metadata leakage rather than verification.
6. Adversarial source-held-out splits and an explicit abstention-rate stress test.

## Falsification and stop criteria
Reject the proposed empirical superiority claim if (a) gains vanish after within-family coverage matching; (b) gains vanish after source-held-out evaluation; (c) adjudication disagreements or source leakage explain the effect; (d) gains require unmatched compute; (e) a simple baseline matches performance within uncertainty; or (f) negative controls exhibit comparable gains. An unobserved target correctness rate is **not** identified from unlabeled acceptance/confidence data alone under arbitrary shift. Do not claim distribution-free conditional risk guarantees without stated assumptions and proof.

## Physics and mathematics are domains, not metaphors
Physics questions must have independently checkable numerical/analytical answers with units, assumptions and tolerance rules. Mathematics must have proof or solution adjudication independent of the tested verifier. NLP must include factual/evidence-backed questions with source-grounded labels. Domain labels alone do not demonstrate a new AI–physics theoretical connection.

## Closest established literature, first-pass primary-source anchors
- Geifman & El-Yaniv, *Selective Classification for Deep Neural Networks*, NeurIPS 2017: https://papers.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html (selective risk/coverage and rejection).
- Geifman & El-Yaniv, *SelectiveNet: A Deep Neural Network with an Integrated Reject Option*, 2019: https://arxiv.org/abs/1901.09192 (joint prediction/rejection).
- Jones et al., *Selective Classification Can Magnify Disparities Across Groups*, 2020: https://arxiv.org/abs/2010.14134 (group disparity under abstention).

These are **prior-art constraints**, not proof that the proposed design is novel. Continue full-text comparison to conditional/conformal risk control, distribution-shift calibration and recent cross-domain selective prediction before any novelty claim.

## Zero-dollar cloud execution guard
Public repository confirmed. GitHub documentation (accessed 2026-11-19) says standard GitHub-hosted runners in public repositories are free, while larger runners are billed: https://docs.github.com/en/actions/concepts/billing-and-usage and https://docs.github.com/en/billing/concepts/product-billing/github-actions . Account-specific Actions permission, quotas, billing configuration and workflow eligibility remain unverified. Restrict future CI to ordinary public-repository standard hosted runners; no larger/self-hosted/paid runner, no paid API, no artifacts/caches or heavy dependencies without independent checks. Do not require user laptop compute. Do not equate successful synthetic CI with real-world verifier efficacy.

## Publication gate for 2026-11-22
If held-out labels, independent CI, matched-compute baselines and literature comparisons are not ready, publish an explicitly labeled methods/preregistration report only; do not publish a claimed positive empirical finding. Disclose AI assistance as required by venue and maintain provenance of code, data and labels.
