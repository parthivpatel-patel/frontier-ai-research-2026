# Protocol 080 — Audit of adversarial record validation and nonidentification boundaries

Date: 2026-11-14. Status: source-level code audit and preregistration only. No cloud execution, AI-model experiment, or novelty claim.

## Concrete implementation issue

In `research/fixtures/test_protocol_079_nonidentifiability.py`, `released_risk_bounds` first evaluates `r[0]` in a comprehension to select released records, *before* validating that each record has exactly three fields and the release flag is a Boolean. Consequently an empty record triggers `IndexError`, a non-sequence may trigger `TypeError`, and a truthy non-Boolean release flag can affect the selected denominator before the later validation rejects it. The current tests do not cover malformed record arity. This is a validation-order weakness, not evidence that the mathematical interval is wrong for well-formed records.

A subsequent patch should validate every record as a length-three tuple/list; require exact Boolean types for release and resolution; require a Boolean false-label if resolved and `None` if unresolved; only then construct the released subset. Explicitly test `[]`, `[()]`, `[(True,)]`, `[(1, True, True)]`, `[(True, 1, True)]`, and a valid nonreleased unresolved record. Define whether malformed nonreleased records are rejected (recommended: yes) so inputs cannot bypass checks.

## Statistical scope: three different targets

1. **Census with missing truth:** if F released claims are confirmed false, U are unresolved, and K>0 are released, the sharp unrestricted binary-label identification interval is [F/K,(F+U)/K]. This is logical, not probabilistic.
2. **Probability sample with all selected labels resolved:** a Horvitz–Thompson estimator targets the finite-frame false total under valid known inclusion probabilities. Design variance requires the actual first- and second-order inclusion probabilities; fixed-size sampling cannot silently use independent Bernoulli variance.
3. **Probability sample with unresolved selected labels:** a design-based estimate of the observed confirmed-false total is not point identification of the latent false total. Design uncertainty and missing-label identification uncertainty must be reported separately. A plug-in interval using only sampled F and U is not automatically a confidence interval or sharp population identification region.

No generic valid 95% confidence interval follows from these three statements without specifying sampling design, missingness assumptions, and a coverage construction. Provenance-cluster dependence is not corrected by relabeling claim-level records as independent.

## Falsification and acceptance criteria

- Exhaustive completions of the four-claim witness must retain the same observable record and yield 0.25, 0.50, 0.50, 0.75.
- Malformed records must raise documented input-validation exceptions before denominator computation.
- A complete census must collapse the logical interval to a point; zero released claims must remain undefined, not silently zero.
- Sampling-only inputs must not be accepted by a census-bounds function.
- Any future uncertainty procedure must demonstrate its claimed coverage by exact enumeration under small finite frames and specified missingness mechanisms, including adversarial unresolved-label selection; report failures, not only successes.
- A claimed cross-domain gain must survive matched-budget comparisons against strong active-testing, abstention, and missing-data baselines with provenance-level resampling.

## Novelty and experiment gate

This is software-hardening and known partial-identification theory, not a new AI method. Compare with Manski partial identification, verification-bias/selective-label work, and active testing before proposing novelty. The empirical hypothesis must be formulated as a measurable improvement beyond these methods on held-out NLP, mathematics, and physics claims, not as novelty of the interval formula.

## Execution and publication

Do not run any model or local simulation on the user's laptop. Before any cloud job, verify standard public-repository GitHub-hosted runner eligibility and repository/account restrictions, confirm no paid runner or billing exposure, and use only explicitly zero-cost capacity. Preserve commit SHA, exact test command, logs, and negative results. The November 22 publication target is conditional; disclose AI assistance and do not claim executed tests or empirical findings until independently observed.
