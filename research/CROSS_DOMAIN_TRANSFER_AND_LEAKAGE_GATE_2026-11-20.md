# Cross-domain transfer and leakage gate (20 November 2026)

Status: prospective experimental protocol, **not an empirical result or novelty claim**.

## Research question

Does a verification policy trained or threshold-calibrated on one domain retain its selective-risk properties on a genuinely unseen domain (NLP, mathematics, or physics), under matched inference and adjudication budgets? A stronger claim than within-domain calibration requires evidence that a common verifier policy transfers without exploiting answer-format or dataset-source cues.

## Precommitted evaluation design

1. Freeze benchmark item identifiers, model outputs, verifier prompts, parsing rules, confidence scores, random seeds, model versions and any costs **before** viewing held-out correctness labels. Split at source/problem-family level, not by randomly shuffling near-duplicate questions. Keep paraphrases, translated versions, shared solutions and generated variants in the same group.
2. Define three leave-one-domain-out (LODO) trials: train/calibrate on NLP+math, evaluate physics; NLP+physics, evaluate math; math+physics, evaluate NLP. Report within-domain calibration separately. Never tune the threshold on the held-out domain.
3. Use the same frozen base answers for all verifier policies. Compare: no verifier, confidence-only selective baseline, domain-specific threshold, common threshold, and proposed structured verification. Equalize *total* inference calls/tokens or report a Pareto frontier; do not silently give one policy extra compute.
4. For each domain and policy report coverage, accepted-answer error rate, correct-answer rejection rate, audit-label availability, total cost, and exact denominators. For paired policies, separately report exclusive-acceptance sets and paired differences. Independently audit both accepted and rejected pools using documented sampling probabilities.
5. Primary endpoint: worst held-out-domain upper confidence bound for accepted-answer error at a prespecified minimum coverage and fixed budget. Choose risk ceiling, minimum coverage, confidence level and multiple-comparison correction before seeing results. A domain with zero accepted answers is **not** a reliability success.
6. Estimate uncertainty at problem-family/source level where dependence is plausible; an answer-level bootstrap is not justified if multiple questions share templates or proofs. Exact finite-population audit bounds apply only to their stated sampling design and target population.
7. Preserve a locked final test set after all ablations and prompt changes. Public test-set contamination and external pretrained-model exposure remain limitations even with a local split.

## Leakage and construct-validity checks

- Check exact and approximate duplicates, benchmark/source metadata, response length, domain vocabulary, and format-only features as potential shortcuts. Include a metadata-only / format-only negative-control classifier where feasible.
- Have correctness judged by an independent rubric or qualified adjudicator blind to policy identity. Mathematical or physics answers may have multiple equivalent valid forms; automatic string matching alone is inadequate.
- Physics problems must distinguish symbolic derivation, dimensional consistency, physical assumptions and numerical accuracy. Dimensional consistency alone does not prove physical correctness.
- NLP evaluation must distinguish entailment, factual support, and stylistic preference. Mathematics must distinguish correct final answer from valid reasoning. Report separately rather than pooling incomparable labels.
- Randomly permute irrelevant answer presentation where possible; large changes in verifier scores indicate sensitivity to nuisance features.
- Record abstention caused by parsing failures as an operational outcome, not a silently dropped observation.

## Falsification gates

Reject any cross-domain-transfer claim if: (a) worst-domain performance fails the preregistered risk/coverage gate; (b) gains vanish under matched compute; (c) duplicate/source-family isolation fails; (d) a format-only control explains the improvement; (e) independent label adjudication is too incomplete to identify the effect; or (f) a paired confidence interval cannot exclude a practically negligible advantage. Report negative results.

## Prior-art collision map (to be verified against full texts)

Selective classification and risk-coverage curves; conformal risk control and risk-controlling prediction sets; distribution-free selective prediction under shift; calibration under domain shift; LLM self-verification, process reward models, and verifier-guided reasoning; benchmark contamination and near-duplicate leakage; survey-sampling audits and finite-population inference. These fields already contain extensive methods. The mere combination of abstention, auditing and three subject areas is **not** presumed novel. Novelty would require a distinctive, reproducible cross-domain mechanism or a rigorously established empirical finding not explained by existing baselines.

## $0-only execution plan

Use only a verified zero-charge standard GitHub-hosted public-repository workflow for lightweight Python unit tests and small public fixtures. Before scheduling model inference, independently verify current per-account free compute limits, hosted-runner eligibility, model weight licenses, storage limits, any card/billing requirements and whether a truly free CPU-sized inference budget is sufficient. No paid APIs, large runners, GPU reservations, local laptop inference or model downloads are authorized. If no eligible free inference exists, publish only code, fixtures, and preregistration with no model-performance claims.

## Publication gate

As of this note: no held-out cross-domain model evidence has been produced; no original theorem has been established. A November 22 methods/pre-registration release is permissible with transparent limitations, but a discovery claim is blocked until the tests and prior-art comparison are complete. Disclose AI assistance as required by venue policy.
