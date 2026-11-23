# Evaluation leakage and source-provenance audit (2026-11-23)

Status: preregistration supplement; no empirical result, novelty claim, or confirmed CI result.

## Unit of analysis and truth

Define a unit as (model checkpoint, prompt, decoding configuration, proposition, evaluation time). The binary error label is whether the **specific model response** violates an independently adjudicated answer key. A proposition's logical truth is not itself a model-error label. An implication between propositions does not generally imply any relationship between errors made by a model on separate prompts.

For NLP, adjudicators should use an answer key and documented ambiguity policy. For mathematics, require an independently checked derivation or formal verifier where possible; a model-generated proof is not a ground-truth certificate. For physics, distinguish symbolic identities, idealized-model predictions, and empirical measurements, including units, measurement uncertainty and the regime of validity.

## Leakage and pseudo-replication threats

1. **Shared upstream source:** Two nominally separate web pages, papers or benchmarks may reproduce the same original assertion. Cluster at the earliest verifiable common origin; freeze a source lineage table before inspecting held-out labels.
2. **Benchmark contamination:** Public test questions may appear in model training data. Record publication dates, available contamination evidence, model version and prompt overlap; do not call a benchmark clean merely because contamination cannot be proved.
3. **Repeated prompts and paraphrases:** Treat paraphrases and multiple stochastic samples of one underlying question as dependent observations. Split and bootstrap by underlying problem/source, not individual response.
4. **Model-assisted adjudication:** If an LLM proposes labels, a separately documented independent validation step is required. The model under evaluation cannot certify its own correctness.
5. **Post hoc partition selection:** Selecting the grouping, violation budget or task exclusions after examining held-out performance invalidates confirmatory interpretation. Report a frozen primary analysis plus labeled exploratory sensitivity analyses.
6. **Correlated source failures:** A budget on number of erroneous clusters is a deterministic sensitivity assumption, not a probabilistic guarantee that at most k sources are wrong. Do not describe resulting intervals as confidence intervals without a separately justified sampling procedure.

## Falsification and reporting gates

- Verify that independently authenticated hard labels are never relaxed by source deletion.
- Compare the complete feasible sets of direct violation counting and independent source deletion on tractable cases, not just their endpoints.
- Predefine coverage: for each held-out case, whether the authenticated truth lies in the identification set; report exclusions and empty sets.
- Compare against no-constraint missing-label bounds, hard-label-only bounds and at least one prior-art-compatible robust constraint baseline. Report when the proposed constraints provide no tightening.
- Vary provenance grouping, violation budget, contamination exclusions and dependence-aware resampling. If the substantive conclusion changes, report instability, not robust improvement.
- Track compute cost, cloud provider, public-runner type, job duration and any billing prerequisite before launching. Do not start paid or card-gated infrastructure.
- For any apparent cross-domain advantage, require independently established truth in all three domains and report domain-specific results rather than pooling incompatible label semantics.

## Decision rule for a publishable claim

The work may support a **methodological evaluation claim** only if (i) the constraints have valid task semantics, (ii) implementation and independent reference agree, (iii) frozen held-out evaluations support a clearly specified benefit against meaningful baselines, and (iv) the literature review rules out a materially equivalent earlier method. Otherwise publish negative findings, a reproducibility note, or a scoped theoretical exposition rather than claiming novel frontier-model reliability.

## Evidence ledger

- Mathematical implementation and prior CI evidence are tracked in existing repository files; this supplement does not rerun or verify them.
- No new model inference, dataset collection, held-out score, or free-cloud quota check was performed for this supplement.
- Literature review still needs direct comparison with partial identification, clustered measurement error, robust optimization, selective prediction, benchmark contamination and dependent-data evaluation.

