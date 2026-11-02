# Protocol 013 — Three-domain robustness of temporal disagreement (registered before execution)

Date: 2026-11-02. Status at registration: **planned; no three-domain results inspected**. This is an exact, constructed **finite-state methodological stress test**, not a frontier-model experiment, an original model checker, or a claim about human intent.

## Research question and frozen scope

For the *same* pair of formulas `G(a -> X^3 b)` and `G(a -> X^k b)`, where `k in {1,2,4,6}`, can adding or removing physically allowed transitions change whether a separating infinite trace exists? Analyze both directional differences (source true / changed false, and changed true / source false), eight comparisons total. **One original requirement** underlies all eight comparisons. Do not treat the four mutations or eight directions as independent human-authored examples.

Three nested three-state transition systems share initial state 0 and labels `a iff x=0`, `b iff x=2`:

1. **Broad bounded-step:** `0->{0,1}`, `1->{0,1,2}`, `2->{1,2}` (existing FLEXIBLE).
2. **Intermediate monotone with waiting:** `0->{0,1}`, `1->{1,2}`, `2->{2}`. This is a strict transition-subset of the broad system.
3. **Fixed forward:** `0->{1}`, `1->{2}`, `2->{2}` (existing FIXED), a strict subset of the intermediate system.

Use the existing exhaustive `exact_witness` product-state cycle check and `satisfiable_on_model`, with explicit search-budget failure rather than treating a timeout as equivalence. All models are synthetic; no physical-world measurements.

## Pre-specified outputs and hypotheses

For each of eight comparisons report (a) witness existence on all three systems, (b) satisfiability of the formula required to hold in each system, (c) number of **domain transitions** from witness present to absent (broad->intermediate and intermediate->fixed), (d) classification:

- `all_domains`: witness on all three models;
- `assumption_sensitive`: witness on some but not all models;
- `no_domain_witness`: no witness on any model.

For any absent witness with an unrealizable required formula, explicitly flag `required_unrealizable` as a *different* reason for absence; no human-intent conclusion follows from any category. Assert the monotonicity implication `witness(fixed) => witness(intermediate) => witness(broad)` and independently validate every emitted witness against the transition system.

Primary hypothesis **H1**: at least one comparison is `assumption_sensitive` across the three domains. Null outcome H1 unsupported if all comparisons are `all_domains` or `no_domain_witness`. Report the null honestly. **H2**: at least one disagreement is detectable on the intermediate model but not the fixed model. Null H2 unsupported if none. Do not adjust the models or hypothesis after seeing results. No p-values or statistical inference for this one-source deterministic toy.

## Prior art and originality exclusion

- Classical vacuity and model-checking: Beer et al. (2001), https://doi.org/10.1023/A:1008779610539 ; Kupferman and Vardi (2003), https://doi.org/10.1007/s100090100062 .
- English et al. (2025), VLTL-Bench, https://arxiv.org/abs/2507.00877 : grounded state spaces and trace-based translation verification.
- Wang et al. (2026-08-05), SCP-NL2TL, https://arxiv.org/abs/2608.05439 : semantic agreement, calibrated abstention, formal-translation reliability. **Abstention and semantic consistency are not available novelty claims.**
- Newcomb and Ochoa (2026-08-06), https://arxiv.org/abs/2608.06287 : repeated NL-to-LTL model outputs, manual semantic adjudication.
- Quansah et al., ICLR 2026 VERIFY, https://proceedings.iclr.cc/paper_files/paper/2026/hash/8b078da44614b6e249dc9e9474dc8d11-Abstract-Conference.html : large NL/LTL dataset with intermediate logic and validation.

These results, if confirmed, illustrate classical domain dependence and **must not be called novel**. They only inform the experimental design for a possible paper on independent semantic adjudication under uncertain physical assumptions.

## Real-data go/no-go and ethics

The main research remains blocked from a novelty claim without legally usable recorded NL-to-formal predictions and at least 30 independent, human-adjudicated source requirements. Compare matched trace, vacuity, multi-reference, and selective/abstention baselines, with source-disjoint evaluation, declared admissible dynamics, confidence intervals clustered at source requirement and a genuine negative-control domain. If unavailable, downgrade to a transparent replication/limitations report rather than inventing model results.

Run Python standard library on the **public repository's standard GitHub-hosted ubuntu-latest** only, <=5 minutes, read-only permissions, no artifacts, caches, paid APIs, GPU, credit card or user-laptop compute. GitHub's 2026 billing documentation says standard hosted runners in public repositories remain free, while larger runners are billed: https://docs.github.com/en/billing/concepts/product-billing/github-actions . No new spending authorized. Preserve AI-assistance disclosure, third-party citations and all negative results.
