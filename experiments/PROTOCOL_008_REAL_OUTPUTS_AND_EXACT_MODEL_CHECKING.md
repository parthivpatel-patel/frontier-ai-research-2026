# Protocol 008 — Exact toy-model verification and real-output feasibility gate

Date: 2026-11-02. **Exploratory, no publication-grade claim.** Do not promote the toy results to a model benchmark.

## Scope and prespecified checks

### A. Complete finite-state verification (implemented)

System: three physical states `{0,1,2}`, initial state 0, proposition `a` iff 0, proposition `b` iff 2. Models:
- Flexible: `0 -> {0,1}`, `1 -> {0,1,2}`, `2 -> {1,2}`.
- Fixed: `0 -> 1 -> 2 -> 2 -> ...`.

Compare `G(a -> X^3 b)` with `G(a -> X^n b)`, `n in {1,2,4,6}`, in **both** separation directions. Exact product states retain at most `max(3,n)+1` recent physical states and a monotone flag recording the desired formula's first violation. Transitions violating the formula required to hold are removed. An admissible infinite separating trace exists iff the reachable safe product graph contains a cycle after the desired violation. Construct a physical-state lasso and independently verify its temporal truth values and loop edge.

A `SearchBudgetExceeded` exception is an **incomplete result**, never a proof of equivalence. On this finite system, an exhaustive search without a cycle establishes absence of that directional witness **on the specified dynamics only**. Validate with independent negative controls (all formulas false, all true, impossible reverse offset 1, invalid parameters, resource exhaustion, and both directions of known witnesses).

The four mutations belong to **one original human requirement**; no confidence interval or source-level generalization is permitted.

### B. Upstream-attributed model-output records (discovered, NOT imported)

Primary candidate: English et al., VLTL-Bench, https://arxiv.org/abs/2507.00877 and https://github.com/Dubascudes/VLTL-Bench . Inspected `main` commit `383baea8210b93fe9fa7d14edd4757e5b3464e82` on 2026-11-02.

Exact inspected file paths:
- `translation_eval/direct/gpt-5/search_and_rescue.jsonl` (direct translation, model label from upstream folder)
- `translation_eval/direct/llama-3_1-8b/search_and_rescue.jsonl` (direct translation, different upstream model)
- `grounding_eval/claude-sonnet/search_and_rescue_scenario.jsonl` (grounding only, response metadata `claude-sonnet-4-20250514`)
- `VLTL-Bench/benchmark/search_and_rescue.jsonl` (source annotations and traces)
- `evaluation/trace_sensitivity.py` and `evaluation/trace_sensitivity_results.json` (published trace-choice sensitivity baseline)
- `evaluation/compute_direct_metrics.py` (existing exact-match and trace evaluation)

**Licensing stop gate:** upstream GitHub metadata has `license: null` and its tracked tree contains no LICENSE; linked Kaggle page did not expose verifiable terms. No dataset or model-response contents may be copied into this repo or republished until license or explicit authorization is established. If rights remain unclear, use another explicitly licensed source or ask upstream authors for clarification; never infer a license from public visibility.

**Task-comparability stop gate:** Claude grounding outputs cannot be treated as direct NL-to-LTL predictions. GPT-5 and Llama direct outputs are stored as prior model-response records with unverified generation provenance, **not fresh model calls**. Do not claim we ran or paid for either model.

**Temporal-semantics stop gate:** provided `good_trace`/`bad_trace` arrays are finite; do not silently interpret them as infinite traces or assume a last-state loop. Specify LTLf or a justified infinite extension, and check any declared physical transition relation before a physical witness claim.

### C. Confirmatory research plan (NOT started)

1. Obtain rights-cleared, independently authored requirements with actual NL-to-LTL predictions, including a minimum of 30 **distinct source requirements**, multiple domains and template families. Freeze source revisions and file hashes.
2. Independently adjudicate the intended meaning of each instruction; label ambiguous cases as unresolved rather than invent a gold interpretation. Separate annotation adjudicators from the algorithm and from inherited reference labels.
3. Define physically admissible transition systems from documented specifications. Distinguish toy graphs, synthetic models, and measured physical systems.
4. Pre-register source- and template-disjoint splits, model/task strata, oracle/query budgets, trace-generation budgets, and failure handling. Do not select cases after seeing which method wins.
5. Compare against (i) inherited reference formula match, (ii) VLTL-Bench trace-based verification, (iii) published trace sensitivity with multiple variants, (iv) independent semantic adjudication, and (v) physically admissible verification. Add semantic probing/clarification baselines if their implementations and rights permit.
6. Report source-clustered confusion counts, accepted-error rate, abstention/coverage, invalid-witness rate, unresolved-intent rate, and per-source confidence intervals. Distinguish source sample size from mutations and traces. Report all models and all attempted examples, including parsing failures.
7. Run negative controls: intentionally wrong labels, deliberately impossible physical traces, misleading but logically satisfying formulas, prompt/template overlap, and adversarial ambiguity. Require that an improved method detects meaningful additional errors at a matched cost and false-positive budget.

### Falsification and pivot criteria

- **No independent, lawful data:** stop the confirmatory experiment; publish no model scores.
- **No meaningful increment beyond VLTL-Bench and prior semantic probing:** reject the novelty claim.
- **New errors disappear after independent intent adjudication:** reject the hypothesis.
- **Physical admissibility offers no benefit over a matched trace-variation baseline:** reject the physics-specific contribution.
- **Method increases false positives or relies on post-hoc label selection:** reject the proposed advantage.
- **Fewer than 30 independent sources:** treat as a feasibility case study only, not a population-level AI result.
- **No reliable source-clustered effect:** report null/negative findings without inflating significance.

### Free-cloud execution

Only standard GitHub-hosted Linux runners on the public repository, with a 5-minute job timeout, standard-library tests, no secrets, no paid model calls, no external model downloads, no large runners, no stored artifacts/caches, and no laptop execution. GitHub billing docs checked 2026-11-02: https://docs.github.com/en/billing/concepts/product-billing/github-actions . Public standard runner usage is free; larger runners are not. Confirm job status before claiming CI verification.

### Integrity

Do not equate mathematical counterexamples with human-intent errors, source labels with model outputs, or finite traces with infinite-trace LTL. All research code/text is AI-assisted and subject to independent audit and venue disclosure. The November 22, 2026 deadline is a conditional internal goal.
