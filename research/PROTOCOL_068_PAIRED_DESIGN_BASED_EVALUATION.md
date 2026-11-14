# Protocol 068 — Paired policy evaluation with sampled truth labels

Date: 2026-11-14 UTC. Status: pre-experimental mathematical specification; no empirical result or novelty claim.

## Design correction

Protocol 067 defines a Horvitz–Thompson (HT) numerator with a known release denominator. A comparison of policies must also account for *covariance* when the same independently sampled evaluation claims are used for both policies. Treating two estimates as independent discards pairing and can give incorrect uncertainty. This protocol fixes a finite-population, design-based comparison and its failure conditions.

## Frozen finite population

For each claim i, prespecify a nonnegative weight w_i, binary false-truth Y_i, provenance-family identifier g(i), domain d(i), and policy-specific release R_i^p. A policy's operational audit and release decisions must be finalized **before** evaluation-audit labels are revealed. Define W_p = sum_i w_i R_i^p > 0 and FAR_p = sum_i w_i R_i^p Y_i / W_p. Define the contrast Delta = FAR_candidate - FAR_baseline. Negative Delta favors the candidate, but only when policy verification cost and release coverage are comparable under preregistered tolerances.

## Paired HT estimator

An independent evaluation sample includes claim i with probability q_i > 0 and jointly includes i,j with probability q_ij (q_ii=q_i). With A_i as inclusion indicator, define

z_i = w_i (R_i^candidate/W_candidate - R_i^baseline/W_baseline) Y_i.

Then Delta = sum_i z_i and Delta_hat = sum_i A_i z_i/q_i. Conditional on fixed policies, the finite population and truthful complete labels for sampled units, E_design[Delta_hat] = Delta. This is standard HT estimation, **not a novel result**.

If all q_ij > 0 for pairs with potentially nonzero contributions, an unbiased design variance estimator is

V_hat = sum_{i,j sampled} [(q_ij - q_i q_j)/q_ij] (z_i/q_i)(z_j/q_j).

This includes diagonal terms and within-family dependence through the actual joint sampling design. The variance formula requires known inclusion probabilities and cannot be replaced by an IID claim bootstrap merely because labels span NLP, mathematics and physics. Some valid fixed-size designs have zero q_ij for certain pairs: in that case this unbiased estimator is unavailable as written; use a design-specific alternative and disclose the limitation.

## Preferred evaluation design

Freeze domain and provenance-family strata before test outcomes. Prefer selecting entire provenance families with known positive family inclusion probabilities and independently adjudicating all eligible claims in sampled families, if feasible. Record all q_i and q_ij induced by the actual design, including certainty strata. If sampling claims within selected families, derive joint probabilities from both stages. Use the *same* independent evaluation sample to score every candidate and baseline policy. Keep the independent evaluation-adjudication budget B_eval separate from the policy's operational verification budget B_policy and compute budget B_compute.

## Missing or contested truth

If a sampled label is unresolved, ordinary HT weighting by q_i is not sufficient. Do not silently drop unresolved labels. Report adjudication completion rates by domain and provenance family. Present worst-case bounds or a prespecified sensitivity analysis; inverse-response weighting is only valid with defensible response assumptions and positivity. If truth is a contestable scientific judgment rather than a binary observable, prespecify adjudication rubrics, blinded reviewers, disagreement reporting, and a third outcome 'unresolved' rather than forcing certainty.

## Preregistered comparisons

Evaluate at a common target release coverage and a matched operational audit budget. Record achieved coverage, the absolute budget deviation, per-domain FAR and family-level outcomes. Compare candidate against at least random audit, calibrated selective release, and family-stratified audit, with strong adaptive-audit baselines added after direct prior-art review. No claim of superiority if a comparator fails admissibility, if intervals are inconclusive, or if any prespecified critical domain worsens beyond its tolerance. Multiple candidate-policy or hyperparameter searches require multiplicity control or a separate untouched confirmation sample.

## Falsification checks

1. **Policy leakage:** evaluation labels alter release decisions, thresholds, or candidate selection. Invalidate design-unbiased claim.
2. **Zero positivity:** any relevant claim has q_i=0. Population FAR is not fully identified by HT.
3. **Pairwise nonpositivity:** a needed q_ij=0. Reject the generic unbiased variance formula.
4. **False independence:** two policy estimators are evaluated as independent despite shared audit labels. Reject.
5. **Family pseudo-replication:** uncertainty resamples individual claims despite joint family sampling. Reject.
6. **Missing-label optimism:** unresolved adjudications disappear from the numerator. Reject.
7. **Coverage mismatch:** candidate releases fewer claims to manufacture a lower FAR. Reject unmatched comparison.
8. **Budget mismatch:** candidate receives more operational verifier actions than baseline. Reject.
9. **Physics ambiguity:** adjudication depends on unverifiable assumptions or inconsistent physical units. Mark unresolved and report sensitivity.
10. **Novelty collision:** method reduces to known HT, stratified audit or existing active-learning policy under matched information. Withdraw novelty claim.

## Cross-domain scientific integrity

NLP claims need source provenance and semantic-duplicate grouping; mathematical claims need checkable proof obligations and explicit treatment of conjectures; physics claims need stated model assumptions, units, regimes, and whether ground truth is empirical, simulated, or derived. These are *different adjudication regimes*, not interchangeable labels. Do not claim a unified scientific-verification breakthrough solely from pooling domain scores.

## Literature and cloud execution gates

Direct source-level audit still needed for survey-sampling variance, two-phase sampling, active learning, off-policy evaluation, positive-unlabeled evaluation, and benchmark contamination. Starting references for verification: Horvitz & Thompson (1952), https://doi.org/10.1080/01621459.1952.10483446; Särndal, Swensson & Wretman (1992), *Model Assisted Survey Sampling*; Dudík, Langford & Li (2011), *Doubly Robust Policy Evaluation and Learning*, https://arxiv.org/abs/1103.4601. These are prior-art leads, not proof of novelty or a completed literature search.

No experiment is authorized until free cloud quota, billing/card requirements, and account-specific eligibility are verified. No local laptop training, inference, downloads or simulations. Evaluation manifest remains draft. November 22 is a conditional internal target. Disclose AI assistance as required by venue.
