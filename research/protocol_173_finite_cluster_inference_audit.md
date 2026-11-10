# Protocol 173: Finite-cluster inference and selective-risk audit

Date: 2026-11-09
Status: prospective analysis plan, not experimental evidence. Supersedes no earlier preregistration.

## The inferential unit

An original physics problem is a source cluster. Its paraphrases, generated perturbations, and repeated model calls are correlated measurements, not independent physics problems. Split by source ID before calibration, tuning, prompt selection, or evaluation. If a common textbook, template, or derivation connects sources, record a parent provenance group and rerun sensitivity analyses splitting and resampling at that higher level.

For a frozen method m and threshold t_m, define source-level coverage c_g(m) as the fraction of eligible paraphrases accepted, and source-level correct yield z_g(m) as the fraction accepted AND correct. The primary estimand is the mean of z_g over held-out source clusters. Conditional accuracy is the ratio of aggregated correct yield to aggregated coverage, not the mean of per-source conditional accuracies (undefined when c_g=0). Report both yield and coverage with their numerators and denominators.

For paired methods A and B, define d_g=z_g(A)-z_g(B), and e_g=c_g(A)-c_g(B). Report means of both and source-level distributions. The coverage gate must be defined before test inspection and must not be repaired by post-hoc test threshold tuning.

## Inference decision tree

1. **Validity first:** missing labels, overlapping provenance, unregistered filtering, inconsistent family IDs, or post-test tuning invalidate the confirmatory comparison. Report descriptive diagnostics only.
2. **Coverage comparability:** if the frozen coverage gate fails, label the matched-coverage claim inconclusive. Report both methods' raw coverage/yield and avoid selecting a favorable alternative coverage target after inspection.
3. **Small number of independent sources:** do not use normal-theory intervals or naive row-level bootstrap. Show every source-level paired difference, the number of independent clusters, and an exact paired sign-flip/randomization *sensitivity* distribution when exchangeability and a sharp null can be justified. Sign flips are not automatically valid when methods have asymmetric error distributions or the null concerns only mean effects.
4. **Sufficient independent clusters:** a paired cluster bootstrap resamples source IDs with replacement, preserving all paraphrases and both methods together. Report resampling seed, draws, percentile method, and a cluster count sensitivity grid. A bootstrap interval is not proof of validity under strong heterogeneity, rare families, or few clusters.
5. **Few physics families:** show per-family effects and equal-family aggregate. Resampling source clusters alone does not establish generalization to unseen physics families. Leave-one-family-out analysis is descriptive; do not treat its folds as independent p-values.
6. **Multiple outcomes and ablations:** preregister one primary contrast. Treat other comparisons as exploratory unless an explicit familywise error or false-discovery procedure is frozen before testing.

## Selection and uncertainty

Correct yield and coverage share decisions and are statistically dependent. Never calculate a matched-coverage p-value while treating the selected threshold as if estimated on the held-out set. Calibration randomness remains relevant to repeatability; report results across separately predeclared calibration splits when feasible, without choosing the best split. A single held-out test supports conditional performance for that frozen training/calibration procedure, not universal model superiority.

## Required falsification and negative controls

- Permute physical constraint assignments across source problems within physics family while preserving acceptance budgets; a comparable improvement undermines the proposed physics-grounding mechanism.
- Compare against a constraint-blind verifier with matched compute, prompt budget, and answer coverage; otherwise compute or abstention may explain the gain.
- Evaluate dimensionally valid but physically wrong answers and physically correct answers expressed in unusual units; dimensional checking alone must not masquerade as full physical verification.
- Report valid-answer false rejection and erroneous-answer false acceptance separately, including by family and paraphrase type.
- Track problem provenance and contamination risks; a reused derivation or generated paraphrase cannot count as independent evidence.

## Reproducibility contract

Record immutable commit SHA, input hashes, source/provenance split manifest, thresholds, exact metric definitions, random seeds, dependency lock, CI runner image, and executed test counts. Distinguish specified, committed, executed, and independently replicated checks. A green workflow is insufficient if test discovery omitted modules. Do not claim tests passed without the actual job logs.

## Novelty and publication gate

The equal-source estimator, cluster bootstrap, selective prediction metrics, and calibration-only thresholding are established methodology, not new contributions. The only candidate empirical claim is incremental detection of physically invalid reasoning against strong prior-art baselines at defensibly matched coverage. If the result vanishes under a strong baseline, physics-family sensitivity, contamination audit, or independent-source resampling, report a negative or inconclusive finding. Compare methods and evaluation settings explicitly against PhysReason (ACL 2025), UGPhysics (ICML 2025), and PhysicsEval (2025); do not claim comprehensive novelty from a targeted review.

No inference, tests, cloud jobs, model calls, or local compute were run to produce this protocol. Cloud quota and billing eligibility must be verified before any cloud execution. Laptop remains browser-only. Budget remains strictly $0.
