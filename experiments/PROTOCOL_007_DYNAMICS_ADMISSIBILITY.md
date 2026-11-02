# Protocol 007 — Dynamics-admissible witnesses and novelty collision gate

Date: 2026-11-02. Status: **exploratory / preregistered guardrails; no novelty claim**.

## Research question and scope
Do logical counterexamples to an inherited NL-to-LTL annotation survive when propositions are grounded in a declared transition system? The code tests this **only** on a deliberately constructed, three-state, discrete bounded-actuator model. Classical finite-state model checking and reachability are established prior art. The purpose is to prevent a scientific category error, not to introduce a new verifier.

External data: the **same** pinned MIT-licensed 25-row RobustifAI mutation snapshot used in Protocol 006. Only the fixed-offset source grammar is used, yielding **one original instruction**, five mutation rows, **four distinct changed offsets** (1,2,4,6). Neither five nor four is a sample size of independent human instructions. Source formula: G(a -> X^3 b). Strict changed English: G(a -> X^n b), with n in {1,2,4,6}. Exact syntax recognition and upstream blob checks are inherited from `src/independent_source_audit.py`.

## Fully declared physical abstractions
State x is an integer in {0,1,2}, initially x(0)=0. Proposition a means x=0; b means x=2; state x=1 satisfies neither.

- **Flexible bounded actuator:** x(t+1) in {0,1,2}, |x(t+1)-x(t)| <= 1. This is a nondeterministic control model, not a sampled continuous physical system.
- **Fixed positive-step actuator:** x(t+1)=min(2,x(t)+1). The **unique** infinite trajectory from x(0)=0 is x=0,1,2,2,... . This gives a complete exact check of the restricted offset formulas for this model.

For the flexible model, enumerate ultimately periodic paths (lassos) with at most nine encoded states and a loop length at most three. Check **every edge, including loop closure**, against the transition relation. Evaluate each G/next-step predicate on the infinite lasso. Report both directions of disagreement: inherited true/changed false and inherited false/changed true.

**Interpretation rule:** A found witness proves non-equivalence on the specified dynamics. No witness in a **bounded** nondeterministic search proves nothing about equivalence. The fixed deterministic model is different: its unique infinite trace is exhaustive, so no witness there establishes equivalence **only on that one fixed model**.

## Predefined negative controls
1. Reject a logically valid lasso containing a jump x=0 to x=2; it violates the bounded actuator even if it separates formulas.
2. Reject a lasso whose final state cannot transition to the start of its repeating loop.
3. Test the fixed model against offsets 1,2,4,6. The inherited formula is true; the changed formula is false at offset 1 and true at offsets 2,4,6. These are elementary consequences of x=0,1,2,2,...
4. For the flexible model, an offset-1 requirement cannot hold because a is true at t=0 but b is unreachable at t=1; this is a simple one-step reachability fact, not an inference from bounded search.
5. Reject unsupported offsets, changes to pinned upstream data, and claims of statistical independence or measured AI performance.

## Threats to validity and falsification
- These models are constructed, not estimated from hardware, sensors, or physical experiments. Finding witnesses is **not** evidence that real robots behave this way.
- Lasso enumeration is incomplete for the flexible system. If a report treats bounded non-detection as equivalence, reject it.
- The data are one source family; if a paper generalizes from four mutation offsets to population error rates, reject it.
- The inherited annotation is a benchmark artifact, not an AI-generated prediction; if the analysis labels its discrepancies as LLM errors, reject it.
- Existing work already evaluates grounded LTL and system-state constraints. A proposed paper claiming novelty merely for dynamics-constrained LTL counterexamples **fails** the novelty gate.
- No new theorem or provider-specific performance claim can be made from this experiment.

## Closest prior art / collision register (links checked 2026-11-02)
- English et al. (2025-07-01), *Verifiable Natural Language to Linear Temporal Logic Translation: A Benchmark Dataset and Evaluation Suite* (VLTL-Bench), https://arxiv.org/abs/2507.00877 — four state spaces, sample traces, and grounding/verification evaluation. **Directly blocks a generic claim that state-space-grounded NL-to-LTL evaluation is new.**
- English et al. (2025-12-18), *GinSign*, https://arxiv.org/abs/2512.16770 — grounded propositions into system signatures, explicitly studies semantic non-equivalence from incorrect grounding.
- Quansah & Bonnah (2026-05-20), *NeuroNL2LTL*, https://arxiv.org/abs/2605.22874 — verifier-in-the-loop learning and satisfiability checks; the reported 28% semantic-equivalence score is an author claim, not independently reproduced here.
- Hou et al. (2026-08-28), *Linear Temporal Logic Translation via Human-Inspired Self-Constrained Reasoning*, https://arxiv.org/abs/2608.28435 — domain constraints integrated into robot task translation.
- De Giacomo et al. (AAAI 2014), *Reasoning on LTL on Finite Traces: Insensitivity to Infiniteness*, https://doi.org/10.1609/aaai.v28i1.8872 — warns that finite/infinite trace interpretation cannot be interchanged without conditions.
- See Protocol 006 for *Beyond Type-checking*, *Quizzing the Translation*, *ReasonSTL*, and the source dataset.

## Next publication gate (not met)
Obtain **lawfully available** real model outputs and at least 30 independently authored, independently adjudicated source requirements. Evaluate source- and template-disjoint held-out cases. Compare against VLTL-Bench-style grounded verification, semantic probing, and clarification methods at matched oracle/query budgets. Predefine source-level precision, accepted-error, coverage, and failure to find a physically admissible counterexample; report uncertainty at the source level. A credible new contribution must survive these direct comparisons. Otherwise pivot.

## Zero-cost reproducibility
Public GitHub repository, standard `ubuntu-latest` GitHub-hosted runner, Python standard library, five-minute job timeout, no paid model API, no GPU, no large dataset download, no local laptop compute, no caches/artifact uploads. GitHub documentation (checked 2026-11-02): https://docs.github.com/en/billing/concepts/product-billing/github-actions states standard hosted runners in public repos are free; larger runners are billed. No new payment card or paid service is required for this GitHub Actions route. Job success must be checked before claiming test results.

## Integrity
Treat code and calculations as AI-assisted research requiring independent scientific review; disclose AI assistance according to the eventual venue. This work is independent of all other user projects. November 22, 2026 is a **conditional internal target**, not a publication guarantee.
