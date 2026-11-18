# Cross-domain verifier evaluation: falsifiable execution gate (2026-11-18)

Status: **protocol proposal only**. No new model, benchmark, or statistical result is claimed here. This file does not replace a previously frozen preregistration.

## Research question

At a fixed verification cost, does a proposed reliability score improve *selective prediction* on independently sourced NLP, mathematics, and physics questions relative to simpler baselines, and does any improvement survive source-family shift?

This is not a claim that combining three domains is novel. The candidate contribution, if any, must be a *specific* calibrated cross-domain decision rule with demonstrated transfer and honest uncertainty.

## Related work that must be distinguished

- Geifman and El-Yaniv (2017), **Selective Classification for Deep Neural Networks**: selective risk and coverage.
- Angelopoulos and Bates (2023), **Conformal Prediction: A Gentle Introduction**: coverage calibration; distinguish marginal coverage from conditional guarantees.
- Angelopoulos et al. (2024), **Conformal Risk Control**: risk-controlling calibration, not a novel idea by itself.
- Kadavath et al. (2022), **Language Models (Mostly) Know What They Know**: model confidence and correctness.
- Lin, Hilton and Evans (2022), **Teaching Models to Express Their Uncertainty in Words**: verbalized uncertainty.
- Cobbe et al. (2021), **Training Verifiers to Solve Math Word Problems**: learned math verification.
- Lightman et al. (2023), **Let's Verify Step by Step**: process supervision and verification.
- Hendrycks et al. (2021), **Measuring Mathematical Problem Solving With the MATH Dataset**: math evaluation.
- Rein et al. (2023), **GPQA: A Graduate-Level Google-Proof Q&A Benchmark**: difficult science QA.
- Schick et al. (2023), **Toolformer**: tool-augmented language modeling.

Before claiming novelty, verify bibliographic details, inspect full texts, and extend the audit to 2025–2026 literature and closest code releases. These entries are *candidate prior art*, not a completed exhaustive search.

## Pre-outcome design

1. Fix exact model outputs, source identifiers, licenses, split definitions, label adjudication rules, and verifier budget **before** accessing held-out outcomes. Do not train or download models on the user's laptop.
2. Use three independently sourced domain families: NLP factual/entailment tasks with evidence-grounded labels; mathematical problems with independently checked final answers; physics questions with dimension/unit and numerical-consistency checks. Avoid treating answer-string agreement as proof of correctness.
3. Group splits by original source, author/template, problem generator, and near-duplicate cluster. Never split variants of the same source across train and test.
4. Compare: (a) always answer, (b) confidence-only abstention, (c) length/format heuristics, (d) matched-budget domain-specific verification, (e) calibrated selective/conformal risk baseline, and (f) the proposed combined score. Use identical candidate answers and information access where feasible.
5. Primary estimand: held-out **error among answered items** at prespecified coverage levels (e.g. 50%, 70%, 90%), separately by domain and macro-averaged over domains. Also report coverage at a fixed risk ceiling. Predefine treatment of empty answer sets.
6. Secondary measures: calibration error, AUROC for error detection, compute/call cost, error by source family, and subgroup/domain failure modes. Report all prespecified coverage points, not just the favorable one.
7. Statistical unit: source-family cluster. Use paired comparisons and cluster bootstrap confidence intervals; report raw counts and avoid item-level independence assumptions. Include a negative-control verifier signal and a label-permutation sanity check.
8. Freeze the full analysis plan, code version, baseline definitions, exclusion criteria, and a SHA-256 manifest. Verify the manifest's Git object identity; **do not** claim Git commit timestamps prove pre-outcome registration. Preserve an externally auditable timestamp if available.
9. All compute must use an independently verified $0 cloud allocation with confirmed quotas, card/billing conditions and availability. Do not launch any job without that verification. A public repository alone does not establish a free execution entitlement.

## Falsification and stop conditions

- **No performance contribution:** the proposed score fails to outperform the strongest matched-budget baseline on macro-averaged source-family held-out risk, or confidence intervals include meaningful degradation.
- **No cross-domain transfer:** gains are confined to one domain or disappear under held-out source families.
- **Leakage:** source/template overlap or contaminated labels invalidate the affected split; do not silently substitute a new test set.
- **Calibration failure:** risk-control assumptions do not hold under observed shift; report empirical violations rather than claiming distribution-free conditional guarantees.
- **Cost infeasibility:** verified free-cloud quotas cannot support the frozen plan; stop, shrink and explicitly re-preregister a pilot, or report no experiment.
- **No novel mechanism:** the approach reduces to an existing selective prediction or verifier ensemble under an equivalent budget. Reframe as replication or negative-result study.
- **Unreliable evidence:** missing provenance, contradictory labels, inaccessible artifacts, or post-outcome protocol changes preclude confirmatory claims.

## Execution gate

**GO** only after (i) prior-art matrix and dated literature audit, (ii) independent labels and deduplication, (iii) frozen estimand and baselines, (iv) verified free-cloud execution budget, and (v) runnable tests of the full evaluation pipeline. Until then: **NO-GO for superiority or novelty claims**.

A paper for OpenAI, Anthropic, or Google DeepMind audiences should emphasize failure analysis, generalization limits, calibration assumptions, reproducibility, and negative results. Relevance to these labs does not imply endorsement.
