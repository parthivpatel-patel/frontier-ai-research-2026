# Protocol 010 — Licensed model-output schema gate and task-validity audit

Date: 2026-11-02. **Status: exploratory feasibility, not a result on AI accuracy.**

## Why this protocol exists

Sessions 001–013 established classical exact-checking toy cases, but did not establish a paper-level novelty claim or a statistically defensible real-model evaluation. Session 013's nine regression tests were not included in the old workflow's path filter. The filter has been repaired to watch all `src/**` and `tests/**` files and to run the dynamics audit explicitly. A successful old workflow run must not be used to claim that these tests ran.

A new external benchmark, Cohn and Blackwell (2026), *QSTRBench*, publishes model answers for qualitative spatial and temporal reasoning. **QSTRBench is not an NL-to-LTL translation benchmark.** We will not combine its scores with NL-to-LTL correctness or treat its authors' model labels as independently verified model provenance.

## Pinned external source and licensing

- Upstream repository: https://github.com/RobBlackwell/QSTRBench
- Inspected upstream commit: `7da82bae3b1300e8f7fba8f448adca551e0a1f9a` (2026-10-26).
- Repository `LICENSE` and `README.md`: the University of Leeds licenses its dataset under CC BY 4.0. Third-party SparQ, GQR, Hunspell and Project Gutenberg text have separate terms; exclude them.
- Source claims: 1,806 questions and results from 32 models in the main benchmark, and 14,372 in the extended benchmark. These are **upstream claims** until checked by our schema audit.
- Dataset's academic paper citation is marked TBD upstream; cite repository, authors, commit and license accurately. No assertion that its manuscript is peer reviewed.
- The audit uses **only** the small compressed main-question file and recorded-answer files attributed upstream to `openai-gpt-5` and `claude-sonnet-4-20250514`. Their model identities and generation procedures have not been independently authenticated.
- Compressed source sizes and Git blob SHA-1 values are pinned in `src/qstr_schema_audit.py`. All external bytes are fetched by the GitHub-hosted cloud runner, decompressed with Python's standard library under strict size limits, checked against Git object hashes, and **not copied into our repository or CI artifacts**.
- The script reports field names, types, and row counts only, not prompts, answers, per-model scores, or user text. This is a schema audit, not a model benchmark.

## Go/no-go decision gates

1. Confirm source license and separate third-party material. Fail closed on missing/changed blob hash, size, or upstream file.
2. Confirm question and answer schemas, including whether there is a stable record-level join key, a ground-truth answer, model response, and explicit correctness field. Do not assume a field's meaning from its name alone.
3. Confirm row counts and whether any model results are missing or duplicated. A count match does **not** prove correct alignment.
4. Read the upstream evaluation code and a tiny sample of records only after schema identification, without redistributing records. Verify scoring definitions before reporting accuracy.
5. Separate qualitative relation reasoning from natural-language-to-temporal-logic translation. Any QSTR results belong in a distinct experiment, with task-specific baselines and independent question clusters.
6. Establish an actually novel, falsifiable hypothesis beyond known trace sensitivity, vacuity, and semantics ambiguity. If none survives, reject the topic as a novel methods paper.
7. For a confirmatory NL-to-LTL claim: at least 30 independent source requirements, rights-cleared model predictions, independent semantic adjudication, held-out source/template splits, and source-clustered uncertainty. A few perturbations of one requirement do not satisfy the gate.

## Closest prior art / claims explicitly ruled out

- Beer et al. (2001), *Efficient Detection of Vacuity in Temporal Model Checking*, https://doi.org/10.1023/A:1008779610539
- Kupferman and Vardi (2003), *Vacuity Detection in Temporal Model Checking*, https://doi.org/10.1007/s100090100062
- English et al. (2025), *VLTL-Bench*, https://arxiv.org/abs/2507.00877
- ConformalNL2LTL: https://github.com/kantaroslab/ConformalNL2LTL
- Cohn and Blackwell (2026), *QSTRBench*, https://github.com/RobBlackwell/QSTRBench

These prior works preclude novelty claims based merely on semantic ambiguity, trace selection, physical constraints, vacuity, or benchmarking qualitative spatial reasoning. A future contribution must demonstrate a **specific incremental capability** with appropriate matched baselines.

## Compute and publication integrity

Only standard `ubuntu-latest` GitHub-hosted runners in this **public** repository; job timeout 5 minutes; no GPU, API key, model inference, paid runners, caching, artifacts, or local laptop computation. GitHub documents standard hosted runners in public repositories as free: https://docs.github.com/en/billing/concepts/product-billing/github-actions . Larger runners and some storage incur charges and are forbidden. Availability is checked from actual workflow execution, not assumed.

AI assistance is documented; authorship, originality and any venue disclosure must be represented truthfully. Internal target November 22, 2026 is conditional and does not justify overstating evidence.
