# Prior-art and falsification audit — 2026-11-19

Status: **research protocol, not a novelty claim or empirical result**. Bibliographic identifiers below are candidate anchors; full-text and version-specific verification is required before citing them in a submitted paper.

## Research question and unit of analysis

Can a frozen, budget-accounted verifier improve *selective risk at operationally meaningful coverage* on a fixed roster of candidate answers from NLP, mathematics, and physics, including previously unseen source families? The intervention is verification/abstention, **not** training a foundation model or proving that a common physical mechanism exists in all three disciplines.

Candidate answer, reference label, source-family identity, and split membership must be fixed before verifier comparison. The same candidate answer must be shown to each verifier; otherwise the estimand is end-to-end generation-plus-verification.

## Closest conceptual prior art (must compare experimentally)

1. **Selective classification / risk–coverage**: Geifman and El-Yaniv, *Selective Classification for Deep Neural Networks* (NeurIPS 2017); Geifman and El-Yaniv, *SelectiveNet: A Deep Neural Network with an Integrated Reject Option* (ICML 2019). Risk–coverage curves and abstention are established; implementing them is not novel.
2. **Distribution-free calibration and shift limitations**: Angelopoulos and Bates, *A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification* (2023); Barber et al., *Conformal Prediction Beyond Exchangeability* (2023). Exchangeability assumptions and shifted distributions must be explicit. Do not claim arbitrary-shift guarantees.
3. **Self-evaluation / verbalized uncertainty**: Kadavath et al., *Language Models (Mostly) Know What They Know* (2022). Compare with confidence-based selective prediction and a no-verification abstention baseline.
4. **Process and outcome supervision for mathematical reasoning**: Lightman et al., *Let's Verify Step by Step* (2023). Distinguish answer correctness, step correctness, and external-tool verification.
5. **LLM-as-a-judge biases**: Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (2023). Evaluate judge dependence and shared-model error correlation.
6. **Cross-domain scientific QA**: Hendrycks et al., *Measuring Massive Multitask Language Understanding* (2020); Rein et al., *GPQA: A Graduate-Level Google-Proof Q&A Benchmark* (2023). Domain mixtures alone do not establish cross-domain generalization or a novel benchmark.

This is a **screening list**, not a completed exhaustive literature search. Check exact bibliographic versions, newer work, benchmark licenses, contamination, and available public baselines before any novelty statement.

## Minimum falsification matrix

| Claim to test | Primary contrast | Failure criterion |
| --- | --- | --- |
| Verification helps beyond confidence alone | Frozen verifier vs frozen confidence-only rejector on identical candidates | No improvement at matched achieved coverage and measured full-roster budget |
| Cross-family transfer | Train/calibrate on disjoint families; evaluate on entirely held-out families | Gains disappear or reverse on held-out families |
| Not merely more abstention | Report full risk–coverage curve and fixed-threshold operational coverage | Apparent improvement exists only at materially lower achieved coverage |
| Not merely more resources | Count costs for accepted, rejected, and failed attempts | Prospective 5% measured-cost gate fails or units are incomparable |
| Robust to label uncertainty | Independently adjudicate a preregistered ambiguous-label subset | Conclusion changes under plausible adjudication |
| Not benchmark leakage | Audit overlap, near duplicates, and prompt/template families | Leakage or split contamination is found |
| Not pooled-domain masking | Report each source-family's coverage and selective risk, with undefined risk when no items accepted | Any claimed universal improvement is contradicted by a held-out family |
| Not a ranking/deployment confusion | Separate held-out top-k ranking from frozen calibration threshold | Claimed deployment coverage is supported only by transductive top-k selection |

## Statistical and operational guardrails

Use a single prespecified primary comparison and a coverage region chosen without inspecting held-out labels. Pair methods on the same questions. Cluster uncertainty by source family where there are enough independent families; with very few families, report descriptive estimates and avoid asymptotic confidence claims. Predefine treatment of ties, invalid/unknown labels, failed verification, zero acceptance, and partial execution. Preserve a machine-readable roster and hashes of prompts, answers, labels, splits, model versions, and execution environment. Record free-tier eligibility and actual cloud-run billing exposure before dispatching workloads.

## Physics and mathematics specificity

A physics item needs dimensional consistency and stated physical assumptions, but dimensional correctness alone is insufficient. A mathematics item needs a valid derivation or independently checked proof step, not merely matching a numeric final answer. NLP factual claims need source-grounded evidence and temporal validity. These are **different verification oracles**; any proposed shared method must be evaluated against domain-specialist oracles, not silently replace them.

## Publication gate

By 2026-11-22, publish a defensible empirical paper **only if** independent held-out evidence, baseline parity, free-cloud provenance, CI execution, and prior-art audit are verified. Otherwise publish an accurately labeled preregistration/methods note with no novelty or performance claims. No fabricated experiments or unverified CI status.
