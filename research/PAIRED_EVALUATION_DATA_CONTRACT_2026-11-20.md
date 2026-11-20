# Paired evaluation dataset contract and leakage-safe analysis (2026-11-20)

Status: **preregistered design only**. No held-out model results are asserted. This contract connects the existing temporal-evidence ablation, dual-pool audit, and cross-domain transfer protocols.

## Unit of analysis and provenance

One row is a frozen (question, candidate answer, verifier policy, evaluation split) decision. The canonical `item_id` identifies a question-answer pair across all policies; `problem_family_id` groups near-duplicates, translations, templated variants, and shared-source derivations. Required fields:

- `item_id`, `problem_family_id`, `source_id`, `source_license`, `domain` in {NLP, mathematics, physics}, `split` in {train, calibration, heldout}, `candidate_answer_hash`, `generator_id`, `generator_version`, `generation_seed` (nullable with reason)
- `policy_id`, `policy_version`, `policy_frozen_at`, `accept` (Boolean), `confidence_score` (nullable), `temporal_feature` (nullable), `feature_provenance`, `feature_available_at_decision`
- `correctness` in {correct, incorrect, unresolved}, `adjudicator_ids`, `adjudication_protocol_version`, `disagreement_flag`, `adjudication_blinded_to_policy`
- `input_tokens`, `output_tokens`, `verifier_calls`, `wall_time_ms`, `compute_platform`, `cost_usd` (must equal 0 for approved experiments), `run_id`, `artifact_digest`

Preserve unresolved adjudications; never silently code them as correct. For temporal features, require evidence that timestamps precede the decision and do not encode labels or future corrections. Do not expose held-out labels to calibration or threshold selection.

## Comparison design

Evaluate the same frozen candidate-answer pool with confidence-only (C), temporal feature (T), shuffled-temporal negative control (S), and strong conventional feature baseline (B). Predefine the shuffle strata using calibration data; shuffle within domain and source-family-compatible strata only if the resulting null is meaningful. If strata are too small, mark the control invalid rather than silently changing its design.

Hold out entire problem families, source families, and generated template clusters, not merely individual answer rows. Run three leave-one-domain-out folds: calibrate on two domains and evaluate the third without changing thresholds. Do not reuse a held-out domain for hyperparameter tuning. Match policy comparisons by accepted count within each held-out domain or report an explicit coverage-risk curve; match verifier calls and tokens with an a priori tolerance. If both constraints cannot be met, report the tradeoff instead of claiming a matched-budget improvement.

## Estimands

For policy p and domain d, define acceptance A_p and independently adjudicated correctness Y, where Y=1 denotes correct. Report coverage P(A_p=1), selective error P(Y=0 | A_p=1) when coverage >0, false rejection P(A_p=0 | Y=1) when identifiable, and total accepted incorrect answers per fixed evaluation pool. Report unresolved-label counts separately.

At exactly matched accepted count k on a common pool of N, the selective-error difference is:

`[sum_i 1(A_Ti=1,Y_i=0) - sum_i 1(A_Ci=1,Y_i=0)] / k`.

Shared accepted items cancel; only policy-discordant accepted items contribute. If k=0, selective error is undefined, not zero. The primary comparison is T versus C; T versus B and T versus S are mandatory robustness and mechanism checks, not substitutes for the primary result.

## Uncertainty and falsification

Cluster resampling at `problem_family_id`, preserving paired policy decisions, with fixed resampling seeds and reported confidence intervals. When clusters are too few, explicitly decline inferential claims. Independently audit both accepted and rejected pools with prespecified sampling probabilities; use design-aware estimators for pool-wide claims. Exact hypergeometric bounds apply only under their specified finite-population simple-random-sampling assumptions; do not substitute them for unequal-probability sampling or optional stopping. Correct simultaneous domain claims for multiplicity.

Predeclare failure if: (1) T does not improve over C at comparable coverage and cost; (2) S performs comparably to T, undermining temporal-specific attribution; (3) B explains the gain; (4) leave-one-domain-out transfer fails; (5) source-family leakage, temporal look-ahead, label exposure, or unresolved adjudication compromises validity; or (6) the experiment cannot be run under verified zero-cost cloud eligibility. A null result is publishable as a null result, not an improvement.

## Reproducibility and zero-cost gate

Before any execution, archive a versioned manifest with dataset digests, source permissions, policy definitions, split assignment, adjudication rubric, random seeds, runner type, dependency lockfile, and exact commands. Prefer lightweight standard GitHub-hosted public-repository CI only after confirming current billing eligibility and runner settings for the account. Never enable larger paid runners, paid APIs, GPU rentals, or automatic billing; no local laptop inference, downloads, or training. Synthetic tests cannot substitute for held-out empirical evidence.

## Claim boundary

This protocol combines established ideas in selective prediction, paired policy evaluation, auditing, temporal-feature ablations, and grouped cross-domain validation. Its combination is a *hypothesis to test*, not established novelty. A paper must explicitly compare with selective classification, conformal risk control, active/anytime-valid risk control, and recent LLM selective-risk methods before any originality claim. Publication requires truthful AI-assistance and compute disclosures.
