# Protocol 096 — Witness certification boundaries and empirical stop/go gate
Date: 2026-11-15
Status: source-level audit and preregistration; no execution or empirical result
Scope: independent frontier-AI research only. No local computation, paid service, or account-dependent free-cloud claim.

## 1. Source inspected
- `research/fixtures/test_protocol_093_complete_policy_trees.py`
- `research/fixtures/test_protocol_095_independent_witness_validator.py`

## 2. What the independent validator proves — and does not
For a supplied finite binary joint distribution, a proposed policy tree, positive integer costs and a budget, Protocol 095 checks structural legality on **both** branches of each action and recomputes expected successful-verification count by summing over possible worlds. If its function returns successfully, the witness is legal under those input conventions and its reported expected reward matches the specified joint distribution. This is a conditional correctness statement about the witness *score*, not about truth, calibration, or optimality.

It **does not prove that the witness is optimal**. That requires a separate upper bound or exhaustive comparison. Nor does it prove that the joint distribution represents real verifier outcomes, that observed success means the underlying scientific claim is true, or that adaptive verification is novel.

The source contains no observed CI run or test result. The existence of unittest methods must not be represented as passed tests.

## 3. Specific source-level risks to resolve before certification
1. Protocol 093's `cap` counts generator entry and emitted non-stop trees, not peak materialized continuation tuples, memory, elapsed time, or total Cartesian-product work. `tuple(trees(...))` materializes both continuation sets before scoring, so the cap is **not** a hard resource ceiling. This is a design limitation; no resource-exhaustion incident has been observed.
2. Protocol 093 enumerates legal policy trees, but the returned `tree_count` counts only root trees evaluated, whereas the internal cap counts a different quantity. Report these as different counters, not as interchangeable policy totals.
3. Protocol 095 validates all structural branches, including zero-probability branches. This is conservative and appropriate for an everywhere-defined policy, but the paper must state this convention; otherwise a policy that is valid almost surely could be rejected.
4. The reward is the number of successful verification attempts. No claim-level correctness, error costs, adjudication ambiguity, correlated verifier mistakes, or abstention penalty is modeled.
5. Tests in Protocol 095 verify rejection of a wrong claimed score, but do not provide a deliberate mutation test that alters the reward formula while preserving the nominal expected value on a selected fixture.

## 4. Acceptance tests before any empirical claims
A. Run Protocols 089, 090, 093 and 095 on a verified no-cost cloud runner with logged runtime, exit codes, Python version, runner identity, repository commit and test counts. Never execute on the user's laptop.
B. Construct small enumerated joint distributions and compare: independent policy-tree enumeration (093), Bayesian DP (089), possible-world recursion (090), and independent witness rescoring (095). Distinguish algorithmic independence from shared problem assumptions.
C. Independently replay the returned tree and check `value_093 == value_095`; compare against `value_089` and `value_090` on identical costs, budgets and distributions. Preserve exact rational arithmetic.
D. Add negative controls: independent Bernoulli outcomes (no adaptive advantage over exact static optimum under additive rewards), zero budget, no affordable action, impossible observations, claim permutations, unequal costs, deterministic outcomes and correlated outcomes.
E. Add a mutation test that substitutes an intentionally incorrect reward function (e.g., counts failed attempts rather than successful attempts) and verifies that at least one asymmetric fixture fails.
F. Put hard bounds on *problem size before enumeration*, including maximum number of claims, maximum world count, maximum budget and a conservative maximum structural-tree bound. A process-level timeout and memory cap should be enforced by the cloud runner. A Python generator counter alone is insufficient.
G. Publish actual run logs and failure details. A nonzero exit or timeout is not a scientific success.

## 5. Empirical design and provenance firewall
Define an item as a scientific claim with source provenance, date, domain, independently adjudicated outcome and verification cost. Train a calibrated probabilistic dependency model on training families only; freeze the model and threshold-selection rules before evaluation. Hold out entire source/provenance families, and separately hold out time and domains. Do not permit duplicate claims, shared derivations, answer keys or model-generated paraphrases to cross train/test partitions.

Domain-specific outcomes must be defined *before* testing:
- NLP: source-grounded factual claims; human or deterministic evidence adjudication; citations and answer-key leakage audited.
- Mathematics: theorem/proof steps with independently checked validity where feasible; do not treat a language model's confidence as ground truth.
- Physics: dimensionally and physically testable claims or reference-data consistency, with units and uncertainty; distinguish source agreement from physical truth.

Primary endpoint: held-out **correct adjudications per unit verification cost**, including false-positive and false-negative penalties. Secondary endpoints: calibration (Brier/log loss), abstention coverage, latency, sensitivity to assumed costs and performance by provenance family. A raw count of positive verification outcomes is insufficient.

Predeclare comparisons against (i) optimal static selection with the same cost budget, (ii) calibrated independent Bayesian selection, (iii) adaptive Bayesian policy using the same information and budget, (iv) simple cost-aware heuristics, and (v) an oracle with true synthetic probabilities as a diagnostic upper bound, **not** a deployable baseline. Use paired family-cluster bootstrap intervals and report all domains, including failures.

## 6. Novelty and falsification gate
Closest methodological foundations include adaptive stochastic optimization/adaptive submodularity (Golovin & Krause, 2011), Bayesian experimental design, value of information, budgeted active learning and selective-label/selection-bias work. These are research leads for a documented bibliography audit, not claims of an exhaustive literature search.

Reject a claimed new algorithm if the contribution reduces to standard exact finite-state dynamic programming or exhaustive tree enumeration. Reject the central empirical claim if improvements vanish against a calibrated adaptive Bayesian comparator, vanish on provenance-family holdouts, depend on leaked labels or inflated verification-success proxies, or are not robust to plausible costs and adjudication error.

A valid negative result may still support a carefully framed methods/replication report, but not a paper advertising demonstrated frontier-model improvements.

## 7. Cloud and publication restrictions
No cloud execution is authorized solely because a provider advertises a free tier. Before running, verify current free compute allowance, runner availability, usage/billing status, payment-card requirement, repository eligibility and safe execution limits. Prefer a short, standard-library-only CI job *only after* confirming the specific account's eligibility and zero-charge safeguards. If verification is unavailable, keep execution pending. No GPU or local laptop work.

The November 22, 2026 target is an internal decision checkpoint, not a promise of a publishable positive result. Disclose AI assistance and any actual compute/data provenance as required by the chosen venue. Do not fabricate execution, novelty, performance, or independent human authorship.
