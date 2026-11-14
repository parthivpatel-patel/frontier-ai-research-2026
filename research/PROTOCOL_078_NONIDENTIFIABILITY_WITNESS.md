# Protocol 078 — Nonidentifiability witness for selectively unresolved scientific claims

Date: 2026-11-14. Status: analytic counterexample and preregistration; not empirical AI evidence, a novel theorem, or a cloud execution record.

## Claim and precise boundary

A known probability-sampling design, even a census, cannot point-identify the false-release fraction when some released claims have unresolved truth labels and no identifying assumptions constrain those missing labels. This is a standard missing-data identification limitation. It must be made explicit before any active-verification performance claim.

Freeze a finite population of K=4 released claims. All four are selected for adjudication (sampling inclusion probability 1). Observed adjudication outcomes are: claim A false (Y=1); claim B true (Y=0); claims C and D unresolved (D=0). Selection, provenance IDs, policy release decisions, evidence snapshots, and observed adjudication status are identical in both worlds below.

- World W0: latent truths for C,D are (0,0). False-release fraction = 1/4.
- World W1: latent truths for C,D are (1,1). False-release fraction = 3/4.

No statistic of the observed record can distinguish W0 from W1. The sharp finite-frame logical identification set is [1/4,3/4] when each unresolved binary label may take either value. This is **not** a 95% confidence interval. The endpoints are attainable. Replacing unresolved with true gives the lower endpoint, not an unbiased estimate of truth.

If the two unresolved claims are known to be exact duplicates of the same underlying proposition, their latent labels may be constrained to agree, but the endpoints above remain attainable. If C and D are mutually contradictory propositions under a consistent formalization, additional logical constraints may narrow the set; those constraints must be explicitly adjudicated, not inferred from language similarity.

## Additional sampling limitation

When only a probability sample is labeled, the realized sampled number of false and unresolved claims cannot be inserted into the census interval formula as if it represented the whole population. HT estimators may estimate totals under valid selection probabilities, but uncertainty from sample selection and nonidentification from missing outcomes are distinct. No nominal coverage guarantee follows from naively applying the census bounds to sampled observations.

## Preregistered negative-control fixture

Implement a dependency-free fixture that:
1. Enumerates all binary completions of the two unresolved released labels, yielding risks 0.25, 0.50, 0.50, 0.75.
2. Verifies both extremal worlds produce exactly the same observed (release, selection, resolution, resolved-label) record.
3. Verifies that the interval collapses to a point when all released labels resolve.
4. Rejects K=0 as undefined risk (coverage is zero), and rejects treating an unresolved label as observed true.
5. Verifies a sampled-only record does not claim a deterministic whole-frame census interval.
6. Keeps provenance families as sampling units in any subsequent design-based inference.

This is an exact logical check, not a stochastic simulation or model benchmark.

## Comparison with prior work and novelty gate

The witness is a textbook-style partial-identification argument, not original mathematical theory. It complements rather than supersedes the prior-art ledger in Protocols 076–077. Next source-level audit should examine Manski-style partial identification, missing-not-at-random sensitivity analysis, verification bias in selective labels, and active testing with incomplete oracle responses. A genuine research contribution would require a new, defensible operational result or held-out discriminating experiment against strong corrected baselines; merely applying these established principles to AI-generated scientific claims is insufficient.

## Publication and execution safeguards

Do not describe this witness as proof of improved scientific verification, model safety, or cross-domain generalization. No NLP, mathematics, or physics model outputs were evaluated here. Execute the proposed fixture only after verifying standard public-repository GitHub Actions eligibility and account-specific restrictions. No local compute, paid cloud, credit card, API billing, or large downloads are authorized. Preserve source URLs, commit SHA, run logs, and AI-assistance disclosure for any subsequent publication. The November 22 target remains conditional.
