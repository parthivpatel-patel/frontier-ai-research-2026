# Protocol 104 — Pre-registered evaluation gate and closest-prior-art map

Date: 2026-11-06. Status: research protocol only; no empirical model result or novelty claim.

## Research question

Does physics-grounded evidence verification improve *unsafe accepted claim risk* at matched coverage under source-family holdout, compared with equally budgeted language-only and retrieval-based verifiers? This is an empirical hypothesis, not an established result. A negative or inconclusive result is publishable only as such.

## Closest prior art requiring explicit comparison

1. **Selective classification and risk–coverage**: El-Yaniv (2010), *On the Foundations of Noise-free Selective Classification*; Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*. Abstention and coverage-controlled risk are not new here.
2. **Language-model factuality and calibration**: Lin, Hilton and Evans (2022), *TruthfulQA*; Kadavath et al. (2022), *Language Models (Mostly) Know What They Know*. Self-evaluation and factuality benchmarks are not novel.
3. **Scientific reasoning and physics question answering**: Hendrycks et al. (2021), *Measuring Massive Multitask Language Understanding* (MMLU); Rein et al. (2023), *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. A physics question set alone is not novel.
4. **Evidence-grounded factuality**: Min et al. (2023), *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation*; Es et al. (2023), *RAGAS: Automated Evaluation of Retrieval Augmented Generation*. Claim decomposition and evidence-grounding are not novel.
5. **Dataset contamination and robust evaluation**: consider paraphrase contamination, source overlap, and shared derivations; perform a dated literature search and check exact bibliographic details before submission.

This is a *starting map*, not a completed systematic literature review. Search and compare subsequent work through the manuscript cutoff, especially physics-specific verification, uncertainty quantification, and conformal risk control. Do not imply frontier-lab endorsement.

## Units, labels and split contract

- Unit of randomization/evaluation: **scenario lineage**, not paraphrased claim.
- Hold out entire source families; never distribute one source family across train, development and test.
- Each scenario specifies a physical model, assumptions, claim, intervention, reference derivation, and adjudicator provenance.
- Truth labels: supported, refuted, underdetermined, outside_model. Missing adjudication is explicitly unresolved, never coded as safe.
- At least two independent reviewers should adjudicate test claims without model outputs; conflicts go to a recorded resolution process. A reviewer identifier alone is not evidence of independence.
- Freeze dataset, split assignments, primary metric, coverage grid, baseline prompts, model versions and cost budgets before inspecting test outcomes.
- Group bootstrap or randomization inference by scenario/source family, not by correlated paraphrases.

## Comparators and controls

A. Claim-only verifier with abstention.
B. Equal-budget evidence-retrieval verifier.
C. Physics-assumption-aware verifier (candidate).
D. Candidate with physical evidence removed or shuffled (ablation).
E. Oracle-style deterministic unit/dimensional consistency checks where applicable; report applicability rather than pretending universal coverage.

Use the same candidate claims and truth labels across verifiers. Match coverage within physics families and report the full risk–coverage curves. Count missing, timeouts and abstentions explicitly. Never select a favorable coverage threshold on the held-out test set.

## Primary estimand

For family f and verifier v at preselected coverage c, define R_vf(c) = P(unsafe truth | accepted by v, family f) with unsafe defined before evaluation. Standardize over a fixed, declared deployment mixture w_f: R_v^std(c) = sum_f w_f R_vf(c). The primary contrast is R_candidate^std(c) - R_baseline^std(c), with confidence intervals clustered by independent scenario lineage. Empty accepted cells are non-identifiable, not zero-risk. Report absolute coverage and per-family risk alongside the standardized contrast.

A possible operational unsafe definition is accepted labels in {refuted, underdetermined, outside_model}; report sensitivity to treating underdetermined separately. The definition must be frozen before tests.

## Falsification and stopping rules

- No gain if the confidence interval includes no improvement at the preregistered primary coverage, or if improvement vanishes on source-family holdouts.
- No physical-grounding claim if removing or shuffling physical evidence leaves performance materially unchanged.
- No generalization claim if gains are confined to one family or vanish under paraphrase/assumption interventions.
- No valid primary result if independent adjudication, lineage integrity, model-version provenance or matched-coverage positivity fails.
- No novelty claim until the dated prior-art audit identifies a specific distinction not already covered by existing work.

## Zero-cost execution gate

Do not launch GitHub Actions or any hosted model until **account-specific** free-minute balance, repository visibility, workflow permissions, runner eligibility, billing configuration and possible overage behavior have been verified. Public-repository hosted-runner policies and billing terms may change. Do not assume unlimited free execution or that a credit card is unnecessary. Use browser-only access from the user's laptop. Standard-library validator tests can be scheduled for a verified free GitHub-hosted runner; model evaluations must wait for separately verified card-free, zero-cost inference access. No local training, downloads or GPU workloads.

## Publication and disclosure

Publish code, hashes, frozen protocol, licensed dataset metadata, negative results, uncertainty, and limitations. Disclose AI assistance according to venue requirements; do not misrepresent authorship or adjudication. Target date 2026-11-22 is conditional, not a justification to skip validation.
