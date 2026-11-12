# Protocol 046 — Identifiability limits of provenance-aware evidence aggregation

Date: 2026-11-12. Status: mathematical design and counterexample; not an executed empirical study.

## Scope and relationship to existing protocols

This protocol stress-tests the provenance-evidence conservation hypothesis in `research/2026-11-12-prior-art-falsification.md`. It does not replace the physically grounded matched-coverage study in Protocol 045. They are distinct hypotheses; combining their results would require a new preregistration. No frontier-model claim is authorized by this note.

## An identifiability counterexample

Let binary truth be Y in {0,1}; let two verifiers return V1,V2 in {0,1}. Suppose each verifier has accuracy q (1/2 < q < 1), errors symmetric conditional on Y, and equal class priors.

World I: conditional on Y, the verifier errors are independent. For agreeing positive votes, posterior odds for Y=1 are (q/(1-q))^2.

World D: V2=V1 almost surely, with the same marginal accuracy q. For agreeing positive votes, posterior odds are only q/(1-q).

Both worlds can produce the *same observed pair* (V1,V2)=(1,1), the same marginal calibration q, and identical surface-level agreement. The observation alone cannot identify whether two pieces of evidence are independent. For q=0.8, posterior probabilities are 16/17 (~0.9412) versus 4/5 (0.8). These are analytic illustrative values, **not experimental results**.

A shared URL or source ID is evidence of potential dependence, not proof of perfect correlation. Distinct URLs do not prove independence. A provenance graph alone cannot identify latent dependence without additional assumptions or labeled joint observations. Thus a universal claim that counting provenance clusters produces calibrated probabilities is false without a calibrated dependence model.

## Candidate method, bounded claim

Define a claim-level evidence record with source lineage, verifier lineage, original observation IDs, timestamps, and transformation parents. Duplicate detection may collapse *known exact copies* into one observation; for uncertain dependence, learn a conditional joint calibration function on held-out labeled calibration groups. Compare with (i) strongest single verifier, (ii) independent naive Bayes fusion, (iii) logistic stacking on vote vectors, (iv) calibrated stacking with lineage features, and (v) a duplicate-collapse heuristic. Use identical labels, inference budgets, and access to verification outputs. The lineage-feature approach is **not asserted novel**.

For binary predictions, report log loss, Brier score, calibration reliability, and selective risk at prespecified supported-claim coverage. Crucially report both in-distribution and source-family-shifted holdouts. Avoid claiming conformal coverage when exchangeability or calibration-set independence is absent.

## Diagnostic matrix

1. Exact copies, where lineage is observable: independent fusion should become overconfident; duplicate-collapse should avoid double-counting.
2. Correlated errors with different apparent sources: lineage-only collapse can fail.
3. Shared source but conditionally independent transformations: indiscriminate collapse can discard information.
4. Latent common failure mode: test whether learned calibration generalizes to held-out failure families.
5. Adversarial paraphrases and copied citations: split by original source and transformation family, never by output row.
6. Label noise and uncertain scientific truth: retain indeterminate adjudication; do not force binary labels.

## Decision and falsification

If ordinary calibrated stacking equals or exceeds lineage-aware stacking on source-disjoint held-out data, abandon a performance novelty claim. If gains only appear on known duplicates, describe the result as duplicate-handling engineering rather than a new scientific principle. If lineage features worsen under shift, report the failure prominently. A strong mathematical contribution would need a theorem with explicit assumptions and a proof beyond the elementary counterexample above, plus a demonstrated distinction from prior literature.

## Feasibility gate

No cloud execution is authorized by this document. A small standard-library-only deterministic fixture is sufficient to test the algebra, but even this must run only on an eligible **free standard GitHub-hosted runner** after checking Actions permissions, account billing safeguards, and runner availability. Never use the user's laptop for computation. No model downloads, paid APIs, or card-dependent resources.

## Literature collision checks (not an exhaustive review)

- Dawid and Skene (1979), maximum-likelihood estimation of observer error rates: https://doi.org/10.2307/2346806
- Karger, Oh and Shah (2011), iterative learning for reliable crowdsourcing: https://arxiv.org/abs/1110.3564
- Mohri and Hashimoto (2024), language models with conformal factuality guarantees: https://proceedings.mlr.press/v235/mohri24a.html
- Existing ensemble calibration, dependent classifiers, data provenance, and selective prediction literature must be reviewed at full-text level before any originality claim.

## Next executable artifact

Create a minimal versioned JSON manifest and pure-standard-library validation script that rejects repeated source-family identifiers across train/calibration/test, missing verifier lineage, and unknown truth labels. Keep fixture data tiny and label all generated cases synthetic. Do not report passing tests until a cloud run log exists.
