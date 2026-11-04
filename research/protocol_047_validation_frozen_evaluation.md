# Protocol 047: Validation-frozen selective risk evaluation

Status: preregistered design; no empirical results. Date: 2026-11-04.

## Question
At a fixed target coverage, does independent physics-certificate checking lower the rate of *unsafe accepted claims* compared with competitive language-only and logic-grounding baselines? Do not equate a valid mathematical certificate with a faithful physical model.

## Dataset contract
Each record has immutable example_id, source_group, physical_model_family, split, adjudicated_truth (supported/contradicted/indeterminate), baseline_prediction, certificate_prediction, baseline_confidence, certificate_confidence, and provenance. A separate auditor must validate physical assumptions and truth labels. No source_group or near-duplicate problem template may cross validation/test. Indeterminate examples are excluded from the primary binary-risk estimand and reported separately, including their rejection/acceptance rates.

## Frozen operating point
For each method and predeclared target coverage c in {0.25, 0.50, 0.75}, fit a score cutoff on validation only. Sort distinct confidence values in descending order; select the cutoff whose empirical validation acceptance fraction is closest to c, with ties resolved toward the *lower* acceptance fraction. Define acceptance as score >= cutoff. Do not rank or select the top k test cases. Freeze all cutoffs and model versions before examining test labels. Record realized test coverage separately; never describe it as exactly matched when drift or score ties prevent matching.

To compare at strictly equal *realized* test coverage, report an additional descriptive paired risk-coverage curve, clearly labeled post hoc, rather than treating it as the preregistered primary test. An optional validation-only deterministic tie-breaker based on a fixed hash of example_id and prespecified seed can improve granularity; do not choose a seed using test outcomes.

## Outcomes and uncertainty
Primary: unsafe accepted count / accepted count, with zero-denominator cases marked undefined. Also report unsafe accepted count / eligible total, coverage, abstention, error by physics family, and false rejection of supported claims. Use cluster bootstrap resampling by source_group (not individual examples) with a fixed seed and >= 2,000 resamples when cloud quota permits; publish intervals and the complete bootstrap procedure. If insufficient independent groups, state that inference is not reliable. Report paired group-level differences with uncertainty and multiplicity adjustment across coverage targets.

## Mandatory baselines and ablations
(1) confidence-only selective language baseline; (2) language-to-logic with standard model checker; (3) grounded predicate verification; (4) proposed independent physical certificate audit; (5) proposed method without physical-model audit; (6) oracle-grounded diagnostic upper bound, clearly not deployable. Hold dataset, model budget, acceptance decision definition, and eligible labels fixed.

## Falsification
Reject the improvement hypothesis if: confidence intervals fail to exclude zero for the preregistered primary contrast; improvements vanish against strongest grounded baseline; realized coverage differs materially without defensible matched comparison; physical-model errors dominate; source-group leakage is detected; or performance does not generalize to a held-out physics family. Publish negative outcomes.

## Implementation and audit gates
1. Inspect existing Protocol 046 evaluator before changing it.
2. Add validation-frozen threshold routine and tests for score ties, empty acceptance, test score distribution shift, label leakage, and duplicate IDs.
3. Run standard-library-only unit tests in a verified zero-cost public-repository GitHub Actions standard runner, after checking account billing/runner restrictions. Never use paid runners or require a card.
4. Archive commit SHA, environment, test command, logs, dataset hashes, and exact evaluation config.
5. Only then proceed to actual language-derived physics benchmarks.

## Novelty boundary
Selective classification, calibration, forward simulation, formal model checking, and language-to-temporal-logic translation are established. Any contribution must be evidenced by independently reproducible gains over the strongest prior methods. Relevant comparisons include CEGAR, grounded NL-to-temporal-logic methods, and physical trajectory verification. This protocol does not assert novelty, experimental superiority, or any completed execution.

## Research ethics
Disclose AI assistance and provenance according to venue rules. Never fabricate citations, experiments, dataset sources, or model access. No spending and no laptop compute.
