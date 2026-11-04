# Protocol 045 — Matched-coverage evaluation and independent adjudication

Status: preregistered experimental design; **not an empirical result**. Date: 2026-11-04.

## Question
Does requiring independently checked physical-model evidence reduce unsafe acceptance of language-derived scientific claims compared with a strong existing language-to-logic/verification baseline **at the same acceptance coverage**, on source-disjoint examples?

## Unit, data, and separation
An evaluation unit is a tuple (natural-language claim, physical model, property, independent ground-truth adjudication, source family, model family, perturbation family). Freeze the benchmark and labels before selecting decision thresholds. Deduplicate semantic near-duplicates and perturbation siblings across splits; grouping by source identifier alone is insufficient. Keep all examples derived from the same source/model/perturbation parent in a single split. Record licenses and provenance. Synthetic examples must be identified as synthetic.

## Three-way adjudication
Ground truth is (supported, contradicted, indeterminate) **relative to explicit assumptions, finite horizon, numerical tolerance, and model scope**. Independent adjudicators must not inspect the system's verdict. Disagreements remain indeterminate pending a documented resolution; do not force binary labels. Distinguish formal certificate validity from physical fidelity of the underlying model. Neither a model checker nor a language model establishes physical truth when assumptions are wrong.

## Predeclared endpoints
Primary endpoint: unsafe acceptance rate = accepted contradicted claims / all contradicted claims, with the denominator and confidence interval shown. Report a second conditional endpoint = accepted contradicted / all accepted determinate claims. Report supported-claim coverage, overall abstention, unsupported rejection, invalid certificate rate, and cost/latency separately. Exclude indeterminate labels from primary denominator but report their frequency and how systems handle them. Never use accuracy alone.

For matched coverage, choose each system's decision threshold on **validation only** to target the same supported-claim coverage c (prespecified grid c = 0.25, 0.50, 0.75). Freeze thresholds and evaluate once on held-out source-disjoint test. If exact matching is impossible due to discrete scores, report attainable coverage and interpolate only as a clearly labeled sensitivity analysis; do not tune on test. Include full risk–coverage curves, not a single favorable operating point.

## Comparators and ablations
B0: language-to-logic system without physics certificate.
B1: same translator plus established model checking.
B2: same translator plus established verification and a calibrated abstention rule.
P: identical translator and abstention budget, plus independently audited physical-model certificate.
Ablate certificate validation, independent model adjudication, and abstention separately. Equalize model access, prompts, evidence, runtime budget and test examples; document unavoidable differences. Compare against CEGAR, timed-automata and recent grounded NL-to-logic/verification work; these ingredients are not claimed novel.

## Uncertainty and falsification
Report raw confusion matrices per domain, source family, and physical system. Bootstrap at the **source/model family cluster** level, not individual paraphrases; present 95% confidence intervals and paired differences. No significance claim if too few independent clusters. Predeclare failure: no material reduction in unsafe acceptance at matched supported-claim coverage; improvement disappears against B2; advantage depends on incorrect physical assumptions; or results reverse on source-disjoint holdout. Also report false abstention on supported claims and computational burden. A null or negative result remains publishable as an evaluation finding but does not establish a new algorithm.

## Physical domains and counterexamples
Start with small independently specified finite dynamical systems, bounded motion with explicit units, and timed transition systems. For each, include (i) a valid invariant, (ii) a genuine reachable counterexample, (iii) a misleading linguistic paraphrase, (iv) an invalid physical assumption, (v) an out-of-domain claim, and (vi) an inconclusive case. Keep exact trajectories and independently generated certificates as audit artifacts. Do not extrapolate finite graph results to arbitrary continuous dynamics.

## Reproducibility and safety
Publish manifest version/hash, random seeds, immutable test IDs, exact dependencies, evaluation code, threshold-selection log, environment, raw predictions, abstentions, checker outcomes, adjudication decisions and full failures. Mark any AI assistance and follow venue-specific disclosure requirements. Do not describe authored tests as executed or report benchmark performance before cloud logs exist.

## Zero-cost execution gate
Only standard GitHub-hosted public-repository runners may be considered after verifying repository visibility, current GitHub pricing, enabled Actions, account billing safeguards, and storage usage. No larger runners, paid APIs, credit-card-dependent services, local training/inference, or large downloads. If the safeguards cannot be checked, **do not launch**. Use CPU-only, standard-library checks first, capped runtime, no uploaded artifacts until retention/storage limits are confirmed.

## Prior-art review queue (verify full texts before claims)
- Clarke et al., 2000: counterexample-guided abstraction refinement.
- Alur and Dill, 1994: timed automata.
- VLTL-Bench (arXiv:2507.00877): grounded language-to-logic evaluation.
- SCP-NL2TL (arXiv:2608.05439): selective prediction and semantic verification.
- SENTINEL (arXiv:2510.12985): physically grounded trajectory verification.
- GinSign (arXiv:2512.16770): typed grounding.
These references are *collision checks*, not evidence that Protocol 045 is novel. Confirm titles, methods, versions and licensing from primary sources before manuscript submission.

## Decision rule
Proceed to a novelty claim only after (1) a full-text closest-work matrix, (2) independent reproducible cloud runs, (3) source-disjoint benchmark results, (4) competitive matched-coverage comparisons, and (5) a concrete methodological distinction not already in prior art. Otherwise frame the output as a negative/replication study or defer submission.
