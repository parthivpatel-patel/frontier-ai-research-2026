# Primary-source overlap audit and claim boundary — 2026-11-22

Status: research audit, **not** a novelty certification or empirical result. Sources were checked at their primary publication pages on 2026-11-22. This note is independent of all other projects.

## What the current code actually establishes

The repository's `research/paired_archival_linear.py` computes an exact finite-sample *identification interval* for the difference between two fixed binary selective-verification policies when unknown binary ground-truth labels are shared between policies. The acceptance denominators are fixed before truth assignment. The endpoint optimization separates across missing examples, conditional on no cross-example constraints. It does **not** provide sampling confidence intervals, model accuracy improvements, an original general partial-identification theorem, or a validated time-travel dataset.

Complexity: linear *number of case contributions*, not unconditional bit-operation O(m) or constant space: `Fraction` arithmetic, input materialization and exponential-size assignment counts affect costs.

## Closest documented prior art: direct overlap and distinction

1. **Manski (2005), Partial identification with missing data: concepts and findings.** https://doi.org/10.1016/j.ijar.2004.10.006 . Missing-outcome identification regions and conservative assumption-free bounds are established work. **Consequent restriction:** do not claim invention of missing-label bounds or sharp partial identification.
2. **Zhang & Choi (2021), SituatedQA.** https://arxiv.org/abs/2109.06157 . Explicit temporal/geographical context and changing answers are established QA problems. **Restriction:** cutoff-sensitive QA is not new by itself.
3. **Jia, Christmann & Weikum (2024), Faithful Temporal Question Answering over Heterogeneous Sources.** https://arxiv.org/abs/2402.15400 . Enforced temporal constraints and evidence-grounded QA already exist. **Restriction:** temporal evidence filtering is not inherently novel.
4. **Zhang et al. (2024), MRAG / TempRAGEval.** https://arxiv.org/abs/2412.15540 . Temporal perturbations, evidence annotations, temporal retrieval/ranking and trainless evaluation already exist. **Restriction:** merely combining retrieval and time constraints is not novel.
5. **Uddin et al. (ACL 2025), UnSeenTimeQA.** https://aclanthology.org/2025.acl-long.94/ . Synthetic time-sensitive questions to mitigate memorization/leakage already exist. **Restriction:** synthetic temporal falsification is not novel alone.
6. **Tan et al. (ACL Findings 2023), TimelineQA.** https://aclanthology.org/2023.findings-acl.6/ . Structured timeline reasoning and QA benchmarks predate this project.

This is a *targeted*, non-exhaustive literature audit. Search must continue for selective prediction with missing labels, paired evaluation under MNAR, bitemporal databases, and time-indexed proof verification before any novelty claim.

## Narrow potential contribution, still unproven

An **auditable evaluation protocol** joining (a) immutable evidence availability at decision cutoff, (b) two policies assessed on the same unresolved ground-truth labels, (c) sharp finite-sample selective-error *difference* bounds under explicitly stated acceptance rules, and (d) provenance-verified timestamp and missingness audits. The contribution, if any, is in the specific protocol and its empirical usefulness, not the individual ingredients. Compare against independent missing-label bounds and cutoff-aware retrieval with matched abstention.

## Falsification and go/no-go

- **Theorem/implementation:** exhaustive enumeration and linear endpoints must match on every feasible small binary frame. Reject exactness on any mismatch; test nonbinary and cross-example constraints as out-of-scope counterexamples.
- **Evidence integrity:** reject point-in-time claims if first-publication timestamp, source revision, cutoff or historical snapshot cannot be independently authenticated. A page's current content is not proof it existed at cutoff.
- **Practical value:** preregister the same accepted coverage, label audit budget, and evidence budget for both policies. Report sharp intervals and paired uncertainty separately. If intervals include zero, do not claim an ordering of true selective risks. If a simpler conservative procedure yields the same actionable conclusions, do not claim distinctive practical advantage.
- **Generalization:** NLP is the initial domain. Mathematics requires versioned proof statements and verifiable checker outcomes; physics requires versioned empirical claims, measurement uncertainty, units and provenance. No cross-domain performance claim until each domain has held-out authenticated data.
- **Scientific novelty:** if prior art already jointly provides this protocol, recast as replication, engineering synthesis, or benchmark rather than original method.

## Zero-cost execution and disclosure

Only use standard GitHub-hosted public-repository CI after verifying its current free eligibility, workflow permissions and quota/billing status. Do not provision GPUs or invoke paid model APIs. Keep experiments CPU-small and cloud-only; laptop is browser-only. Publish dataset inclusion/exclusion rules, model/prompt versions, cutoff source records, scripts, test logs, negative findings, and AI-assistance disclosure as required by venue. No experiment, model gain, physics result, or literature completeness is asserted by this note.
