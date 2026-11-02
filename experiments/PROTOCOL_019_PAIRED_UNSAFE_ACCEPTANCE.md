# Protocol 019 — Paired source-level unsafe-acceptance audit and coverage gate

Date: 2026-11-02 (US Eastern). **Registered before implementing this audit.** Extension of Protocols 016–018; methodological engineering only. No authentic model comparison is claimed.

## Question, outcomes and scope

For two **frozen** verification methods A and B applied to the **same independently authored eligible sources**, can we quantify whether one method accepts incorrect formal specifications more often without confusing an abstention-only strategy with a reliability improvement?

Each original source is one cluster. For each method and source, collapse all repeated output rows:
- `accepted = any(output.accepted)`;
- `unsafe = any(output.accepted and output.incorrect)`;
- accepted output without independent semantic correctness adjudication is invalid;
- an abstained output's `incorrect` may be null and is not counted as a failure.

The **primary descriptive endpoint** is the fraction of *all eligible sources* with at least one incorrectly accepted output, not the conditional error rate among accepted sources. It is zero for an abstain-all method, so **coverage is a co-primary descriptive guardrail**. Separately report conditional selective failure rates among accepted sources (Protocol 018); never infer superiority from these two different denominators alone.

## Paired exact comparison (classical McNemar)

For the same N eligible sources define paired binary unsafe outcomes and count:
- a: unsafe under both A and B
- b: unsafe under A only
- c: unsafe under B only
- d: unsafe under neither

N=a+b+c+d. The observed unsafe-acceptance rate difference (A minus B) is `(b-c)/N`. The **two-sided exact McNemar p-value** is `min(1, 2 * P[Binomial(b+c, 0.5) <= min(b,c)])`, and is 1 when b+c=0. Compute log tails for numerical stability, and report discordant pairs explicitly. This is a standard paired test, **not a new theorem**, not a test of conditional selective-risk equality, and not a proof of physics-grounded improvement. Do not infer statistical equivalence from a non-significant p-value.

Report per-method coverage and absolute coverage gap on the full eligible source set. A predeclared `min_coverage` for each method and `max_coverage_gap` must be provided by the caller; gate passing is a **descriptive eligibility condition**, not a statistically justified equivalence test. If the gate fails, the paired p-value remains visible but is **ineligible** for a matched-coverage interpretation. Even when it passes, a small observed gap does not establish true population coverage equivalence. For confirmatory matched-coverage inference, lock acceptance thresholds on source-disjoint development/calibration data before touching the test labels and use a separately justified power and multiplicity plan.

## Strict input and reporting contract

Require exactly two distinct fixed method IDs and identical eligible source sets; every row has exactly `method_id, source_id, accepted, incorrect`. Reject malformed IDs, missing labels on accepted outputs, non-boolean flags, incomplete method rosters, duplicate method IDs and mismatched eligible-source sets. Repeated predictions are not independent observations. Keep method direction explicit (positive difference means A worse). Output `data_provenance=caller_supplied_unverified` and `analysis=synthetic_or_descriptive_only` until independent source provenance and adjudication are established.

Pre-specified synthetic regression checks: balanced discordance p=1; zero discordance p=1; 6 vs 0 discordance p=0.03125; method-swap sign inversion and p invariance; source duplicates aggregate with any-error rule; differing coverage can reverse apparent benefit; zero acceptance has undefined selective risk; missing adjudications, missing sources and invalid roster/thresholds fail closed. All tests must be standard-library-only and run in public GitHub Actions, not on the user's laptop.

## Identifiability and falsification

A meaningful positive claim requires: lawful source-disjoint human requirements; independent, blinded semantic labels; authenticated or appropriately qualified real-model predictions; a physically justified and independently checked admissible dynamics model; frozen baseline and proposed methods; matched coverage selected without using final test labels; predeclared primary endpoints, power and multiplicity control. If these gates fail, publish a feasibility or negative finding rather than a model superiority claim.

Potential confounds include source-author overlap, templates, cherry-picked physical assumptions, method-dependent adjudication, correlated outputs, post-hoc thresholds and label leakage. An unsafe-acceptance reduction with materially reduced coverage is **not** evidence of a better verifier. A physics assumption that excludes genuine feasible trajectories falsifies the claimed safety interpretation.

## Closest prior art

- McNemar (1947), paired binary testing; NIST reference: https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/mcnemar.htm
- Geifman and El-Yaniv (2017), selective classification and risk–coverage tradeoffs: https://mlanthology.org/neurips/2017/geifman2017neurips-selective/
- Angelopoulos et al., Learn then Test (2021 preprint, 2025 journal): https://arxiv.org/abs/2110.01052
- SCP-NL2TL (2026), calibrated selective temporal-logic translation: https://arxiv.org/abs/2608.05439
- Existing project Protocols 016–018: source-disjoint evaluation and exact selective-risk bounds.

No novelty claim is made for McNemar, source clustering, selective risk, or coverage matching.

## Cloud and cost

Use only existing public repository standard GitHub-hosted `ubuntu-latest` runner, five-minute job cap, Python standard library, no large downloads, training, model inference, GPUs, caches, artifacts, external accounts, credit cards, or paid services. GitHub official 2026 pricing: https://github.com/resources/insights/2026-pricing-changes-for-github-actions . Public standard hosted runner use remains free; larger runners may be billed. Laptop stays browser-only.

**Target:** November 22, 2026, contingent on evidence, legal rights, and publication integrity. Disclose AI assistance as required by venue.
