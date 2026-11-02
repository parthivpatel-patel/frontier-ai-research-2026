# Protocol 020 — Equal-exposure gate for paired unsafe-acceptance

Date: 2026-11-02. **Specified before running the new implementation or cloud tests.** This is a methodological correction to Protocol 019, not a new statistical theorem or a claim about measured frontier models.

## Problem and estimand

Protocol 019 collapses repeated model outputs into `any(accepted and incorrect)` per original source. That endpoint depends on the number of generated attempts. If each independent attempt has failure probability `p`, the probability of at least one failure in `k` attempts is `1-(1-p)^k`. For the *illustrative assumption* p=0.1, k=1 gives 0.10 and k=5 gives 0.40951. Independence and equal p are not warranted for real correlated model generations. The monotonic exposure effect is nevertheless a genuine design confound: comparing different attempt budgets can change the any-failure endpoint even when the underlying per-attempt behavior is identical.

The any-error source endpoint is appropriate if deployment actually emits k outputs and any accepted error can cause harm. But for a **method comparison** that attributes differences to a verification algorithm, freeze and balance the intended trial budget before collecting outputs. Do not silently discard surplus attempts post hoc. Report both source-level any-error and descriptive attempt-level failure; their denominators differ.

## Predeclared strict schema and test cases

Input rows contain exactly `method_id, source_id, trial_id, accepted, incorrect`. The caller supplies immutable rosters of exactly two method IDs, at most 10,000 original eligible source IDs, and 1–32 trial IDs per source. Require the **complete Cartesian product**: one and only one row for each method × source × trial. Reject missing slots, duplicate slots, extra slots, unknown identifiers, malformed rosters, non-boolean acceptance, accepted output without an independently adjudicated boolean correctness label, and non-null correctness labels on abstentions. Require exactly the same source and trial roster for both methods. Run Protocol 019's paired source-level audit only after this gate passes. All accepted labels remain **caller-supplied and unauthenticated**.

Predeclared synthetic checks: k=1 and k=5 mathematical illustration; p=0 and p=1 boundaries; invalid p/k; complete 2-source/2-trial roster; attempt-versus-source denominators; missing B trial rejected; duplicate trial rejected; unknown IDs; invalid rosters; missing adjudication; abstention handling; coverage collapse; method-swap symmetry; malformed schema. No real model performance inference.

## Falsification and remaining limitations

The gate prevents *unequal recorded attempt counts* from masquerading as a verifier effect. It does **not** establish equal generation policies, equal compute/token budgets, identical prompts, model provenance, independent trial draws, unbiased source selection, source-author independence, physical admissibility, or correct human meaning labels. A full confirmatory design must freeze the same prompt families and decoding policy (where appropriate), stop conditions, repeat budget, model/version provenance, and independent annotation plan on source-disjoint development data; perform source-level paired inference on a held-out eligible population; and test sensitivity to k without selecting a favorable k after looking at test labels.

Reject any claimed improvement if it appears only under unequal attempt budgets, is driven by abstention/coverage loss, disappears under frozen k, or requires invalid physical constraints. Source clusters, not repeated generations, are the independent sampling units. Exact McNemar and the k-attempt identity are classical. Neither constitutes a novel contribution.

## Prior art and cost

- Chen et al. (2021), *Evaluating Large Language Models Trained on Code*, demonstrates material effects of repeated sampling and formalizes pass@k evaluation: https://arxiv.org/abs/2107.03374
- McNemar's exact paired comparison (NIST): https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/mcnemar.htm
- Geifman and El-Yaniv (2017), selective classification: https://mlanthology.org/neurips/2017/geifman2017neurips-selective/
- Project Protocol 019: paired unsafe-acceptance and coverage, not independent proof of equal exposure.

Use the existing **public** repository's standard GitHub-hosted `ubuntu-latest` runner, Python standard library only, five-minute job timeout, no GPU, downloads, model calls, caches, artifacts, laptop compute or paid services. GitHub's current public-runner policy: https://github.com/resources/insights/2026-pricing-changes-for-github-actions . Nov 22 target remains conditional on lawful independent adjudication and defensible novelty. Disclose AI assistance per venue requirements.
