# Protocol 108 — Cross-oracle coverage accounting and independence audit

Date: 2026-11-15. Status: static source audit; no tests executed.

## Finding: Protocol 107 has 58, not 88, optimization comparisons

Direct inspection of `research/fixtures/test_protocol_107_cross_oracle.py` gives:

- One-claim: 4 weight vectors × 3 budgets = **12**.
- Two-claim: 5 weight vectors × 3 cost vectors × 3 budgets = **45**.
- Three-claim: 1 sparse correlated instance = **1**.
- Total: **58 calls to `compare`**. The separate legal-STOP witness test is **one additional assertion scenario**, not an optimization cross-comparison.

The previously reported count of 88 is incorrect. This document corrects the public record without implying tests were executed. A Python `unittest` method count is not the same as the number of `subTest` cases.

## What the three checks establish

1. `optimal_value` (Protocol 106) computes a Bellman optimum over exact rational posteriors, independent of Protocol 093's policy-tree generator.
2. `certify` (Protocol 093) enumerates candidate policies and returns a purported optimum and witness.
3. `score_witness` (Protocol 099) checks the returned policy's legal structure and its unconditional expected reward.

Agreement on a finite test case is evidence of implementation consistency, **not** a general optimality theorem, a formal certificate independent of shared assumptions, or empirical scientific-verification benefit. All three implementations assume noiseless binary tests, finite fully specified world tables, known exact probabilities, positive integer costs, and reward equal to the number of true claims verified.

## Specific blind spots and falsifiers

- **Common-model error:** all oracles could agree on an incorrectly specified prior, reward definition, or scientific truth label. Falsifier: independent domain ground truth and calibration tests.
- **Distribution coverage:** five hand-chosen two-claim distributions do not exhaust all rational priors. Falsifier: reproducible seeded rational-table generation, bounded to a documented small instance space.
- **Tie behavior:** equal optimal values can have different legal witnesses. Compare values and witness scores, not serialized tree identity.
- **Counter limits:** enumerator generator-event caps differ from complete-policy counts. Refusals must be reported as resource refusals, not optimization disagreements.
- **Unreachable branches:** Bellman excludes zero-mass branches; policy enumeration may still represent them. Verify agreement on values, not the number of reachable decision paths.
- **Independent witness score:** the scorer is not an independent upper bound. A legal suboptimal STOP witness has score zero on a nontrivial one-claim problem.
- **Runtime safety:** in-process state caps cannot replace external memory and wall-clock enforcement.

## Cloud-only execution gate

Do not run on the user's laptop. Before dispatch, verify the repository is public, the standard GitHub-hosted runner is available, the workflow uses no paid larger runner, account/repository Actions permissions permit execution, and the current GitHub billing documentation still treats standard public-repository runners as free. Use `ubuntu-latest`, minimal permissions (`contents: read`), no third-party actions beyond vetted checkout/setup, no paid API calls, no model downloads, and explicit job timeout. The exact cloud execution status, workflow run URL, runner type, test counts, and failures must be recorded before claiming tests passed.

## Publication gate

This validation is infrastructure, not a novel AI/ML/NLP/mathematics/physics result. The scientific contribution must survive strong baselines from Bayesian experimental design, active learning, adaptive test selection, value-of-information planning, and adaptive submodularity. Report preregistered accuracy-versus-cost, calibration, uncertainty, and failure modes on provenance-separated NLP, mathematical and physical claim sets. No novelty claim should be made until those comparisons exist.

## Next action

Add an executable coverage-accounting assertion and execute Protocols 101–107 on a verified free public GitHub Actions runner, with resource limits. Archive logs and exact commit SHA. Do not equate authored tests with passed tests.
