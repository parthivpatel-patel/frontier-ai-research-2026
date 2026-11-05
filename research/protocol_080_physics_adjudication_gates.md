# Protocol 080 — Physics pilot: adjudication-ready records and leakage-resistant evaluation
Date: 2026-11-05
Status: preregistered design; **not executed**, **not independently adjudicated**, **no empirical novelty claim**.

## Objective and scope
Test whether an assumption-explicit verifier reduces unsafe acceptance of physics claims versus evidence-retrieval, calibrated-abstention, and direct-answer baselines **at identical acceptance coverage and evidence budgets**. Mathematical proof of a conditional implication is distinct from empirical validation of the premise. A valid equation under false assumptions is not a safe physical conclusion.

## Record contract
Every immutable record must contain: `claim_id`, `source_family_id`, `domain`, `claim_text`, `symbols_and_units`, `assumptions`, `proposed_derivation`, `testable_prediction`, `counterexample_or_failure_mode`, `source_reference`, `source_license`, `adjudicator_ids`, `adjudication_rationale`, `truth_status` (supported/refuted/unresolved), `truth_visibility`, and `split`. Record provenance and a SHA-256 digest of the original text before running any verifier. No model-produced adjudication may silently become gold truth.

## Eight seed families (illustrative constructions, not verified data)
| Family | Conditional statement | Premise or counterexample to probe |
|---|---|---|
| Newtonian motion | F=ma for a fixed-mass body in an inertial frame | Changing-mass rocket or non-inertial frame |
| Constant acceleration | x=x0+v0t+at²/2 | Time-varying acceleration |
| Kinetic energy | K=mv²/2 in nonrelativistic mechanics | Relativistic regime |
| Ideal gas | PV=nRT | Condensation or nonideal high-pressure regime |
| Ohm's law | V=IR for an ohmic component at fixed conditions | Diode or temperature-dependent resistor |
| Simple pendulum | T≈2π√(L/g) for small angles | Large-amplitude pendulum |
| Light propagation | d=ct in vacuum in an inertial frame | Material medium and group velocity |
| Mechanical energy | K+U constant in conservative isolated dynamics | Friction or external work |

Each family must include at least one premise-satisfied and one premise-violated instance, with numerical parameters and dimensional analysis supplied **before** evaluation. These rows are templates only, not independent adjudications.

## Preregistered pilot gates
1. Two independent qualified adjudicators must judge each physics instance blind to verifier identity; disagreements remain unresolved until documented reconciliation. Disclose qualifications and conflicts.
2. Partition by source family, not individual claim. Never place a derived variant or near-duplicate across train/dev/test.
3. Freeze claims, reference solutions, baselines, prompts, budgets, coverage grid, and analysis code before the held-out run. Log model/version, sampling, date, latency, token counts, and abstention.
4. Compare unsafe-acceptance rates at matched coverage, including all unresolved truth labels via sharp paired partial-identification bounds; no complete-case-only superiority claim.
5. Use a source-family clustered paired uncertainty analysis; report both per-domain and aggregate estimates, plus negative controls for missingness and source leakage.
6. Require an identified advantage (worst-case bound favors the proposed verifier) and a prespecified meaningful effect threshold. Otherwise report inconclusive or negative result.
7. If baseline evidence access differs, label the comparison non-equivalent; no claim of verifier superiority.
8. Evaluate counterfactual assumption swaps: changing only a premise should alter the certificate appropriately. This is an essential falsification test for premise sensitivity.

## Failure and publication gates
The hypothesis fails if the method performs no better at matched coverage, gains vanish after source-family separation, fails premise swaps, or depends on unavailable gold truth. A mathematical bound is not a new theorem merely because implemented in software. Publish a negative result or methods note if the empirical hypothesis fails; do not market a pilot as a validated physics benchmark.

## Prior-art audit tasks (not yet completed)
Compare against selective prediction and risk-coverage literature, conformal risk control, scientific claim verification, automated theorem proving, physics benchmark suites, and retrieval-grounded fact checking. For each closest work record exact title, authors, year, stable URL/DOI, task, assumptions, evidence budget, benchmark, and what—if anything—remains distinguishable. Do not claim that assumption checking, abstention, or evidence escalation is independently novel.

## Execution and cost safeguards
Only GitHub public-repository standard hosted runners are a **candidate** for small CPU-only, standard-library validation tests. Before any workflow dispatch, verify current GitHub billing policy, repository visibility, account-specific Actions allowance, workflow runner label, artifact retention, and no paid services or larger runners. A generic published free-tier statement is not account-specific verification. Do not run inference, training, or physics simulations on the user's laptop. No cloud jobs are authorized by this document.

## Integrity ledger
Authored protocol: yes. Independently adjudicated records: 0 confirmed. Executed cloud tests: 0 in this protocol. Measured effect size: none. Established novelty: none. New expenditure: none.
