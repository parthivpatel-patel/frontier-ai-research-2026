# Protocol 047 — Source-family split integrity and calibrated evidence evaluation

Date: 2026-11-12. Status: preregistered design, **not an executed experiment**. Extends Protocol 046; no empirical claim.

## Research question
Does an explicit verifier/source-lineage representation improve *out-of-family* probabilistic calibration relative to calibrated vote-only stacking at fixed label and verification budgets? The null is that any apparent benefit vanishes under source-family-disjoint evaluation or is attributable only to exact duplicate removal.

## Minimal data contract (v0.1)
Each JSONL row MUST have: `case_id` (unique nonempty string), `claim_id`, `split` (train/calibration/test), `source_family_id` (nonempty stable identifier for the **originating observation**, not the URL), `verifier_family_id` (nonempty model/prompt lineage), `truth` (0, 1, or null for adjudication unresolved), `vote` (0 or 1), `synthetic` (boolean), and `origin_ids` (nonempty array of source observation IDs). Distinct case rows may share claim IDs but must not leak a source family between splits. Never encode identifying user data or copyrighted full text in fixtures.

Validation is a hard gate: reject malformed records, duplicated case IDs, absent verifier/source family, empty origin IDs, inconsistent labels for the same claim, and ANY source-family overlap between train, calibration, and test. Reject unknown truth values; null is permitted only when explicitly flagged as indeterminate and must be excluded from scored binary metrics with counts reported. If a source observation spans multiple source-family IDs, collapse to a connected component before assigning splits. Also group paraphrases, citations, and transformation descendants by the original observation lineage.

## Experimental order
1. Create a tiny hand-authored **synthetic** fixture with exact-copy, latent-common-cause, independent, and mixed-lineage cases; publish fixture generator seed and hash.
2. Validate schema and split-disjointness with pure Python standard library. Include negative fixtures that MUST fail for each prohibited leakage pattern. Record GitHub Actions run URL, commit SHA, Python version, and raw logs before describing tests as passed.
3. Evaluate strongest-single-verifier, naive independent Bayes, vote-only logistic stacking, lineage-aware stacking, and known-duplicate collapse. Fit all calibration parameters using training/calibration only; test labels must remain sealed until scoring.
4. Compare log loss and Brier score (primary), ECE with prespecified binning (descriptive), and selective risk at 50%, 70%, and 90% supported-claim coverage. Report paired source-family bootstrap uncertainty and counts of independent source families, not merely row counts.
5. Perform a leave-one-source-family-out stress test, then a held-out failure-mechanism test. Report both failures and improvements; never relabel synthetic results as observations from frontier models.

## A critical failure mode
Even perfect observed lineage cannot reveal latent dependence from distinct originating sources. A lineage-aware model may overfit source identifiers and deteriorate on unseen families. Therefore *source-family generalization*, not in-sample duplicate detection, is the decisive benchmark. If calibrated vote-only stacking matches or outperforms lineage-aware stacking, the proposed predictive contribution fails. A mathematical theorem would require additional assumptions about latent common causes and must be compared with dependent-classifier fusion and crowdsourcing identifiability literature.

## Literature audit still required
Dawid–Skene (1979), Karger–Oh–Shah (2011), Mohri–Hashimoto (2024), dependent-classifier fusion, correlated ensemble calibration, provenance graphs, and conformal risk control. These establish significant prior art; no broad novelty claim is warranted.

## Strict $0 cloud gate (checked against GitHub Docs 2026-11-12)
GitHub documents that **standard GitHub-hosted runners for public repositories** are free; larger runners are charged, even for public repositories. References:
- https://docs.github.com/en/actions/concepts/billing-and-usage
- https://docs.github.com/en/billing/concepts/product-billing/github-actions
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository

Do NOT launch until this exact repository's public visibility, Actions enabled status, standard runner eligibility/availability, account spending controls and any payment-method requirement are confirmed. The public GitHub documentation is **not** evidence that this account's configuration has been verified. Do not use Codespaces, larger runners, paid APIs, hosted GPU services, or local laptop compute. No card should be added and no cost incurred. Any approved workflow must use only `ubuntu-latest` standard runner, read-only token permissions, no third-party downloads, short timeout, no artifacts/caches, and no secrets.

## Publication integrity
Separate proofs, synthetic sanity checks, and empirical model results in manuscript tables. Preserve null findings. Nov 22 is an internal target, not a publication commitment. Disclose AI assistance in accordance with venue policy.
