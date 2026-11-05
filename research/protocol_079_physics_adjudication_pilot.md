# Protocol 079: Physics-grounded claim adjudication pilot (preregistered design)

Status: DESIGN ONLY. No model outputs, experiments, independent expert adjudications, or novel empirical findings are claimed. Date: 2026-11-05.

## Purpose and scientific boundary

The proposed study asks whether assumption-explicit, independently checkable certificates reduce unsafe acceptance of scientific claims relative to strong verification baselines at matched acceptance coverage and evidence budget. Mathematical validity of a certificate is distinct from empirical validity of its assumptions. A correct equation cannot rescue a physically inapplicable model.

The pilot below contains **constructed canonical textbook claims** with exact analytic or dimensional checks. They are not independent expert-adjudicated benchmark records, and should never be counted as empirical evaluation evidence. Do not claim these examples are novel physics.

## Pilot record contract

Each record must store:
- `claim_id`, `source_family_id`, `physics_domain`, `claim_text`, `assumptions_explicit`, `assumption_scope`
- `symbols_units`, `expected_relation`, `reference_derivation`, `reference_source_url_or_doi`
- `truth_label` in {supported_under_assumptions, contradicted_under_assumptions, unresolved}
- `adjudicator_ids`, `adjudication_protocol_version`, `adjudication_disagreement`, `evidence_provenance`
- `verifier_decision` in {accept, reject, abstain}; `certificate`, `certificate_check_result`, `time_or_token_budget`
- `split` in {development, sealed_test}; `claim_family_hash`; `model_version`; `prompt_hash`; `timestamp`

Missing adjudication must be encoded as `unresolved`, never as safe. Model-generated reasoning is not a reference derivation. A verifier cannot adjudicate its own claim. Any non-independent label must be flagged.

## Constructed pilot cards (NOT evaluation results)

| ID | Claim and declared conditions | Exact oracle | Counterfactual failure mode |
| --- | --- | --- | --- |
| P079-01 | A constant net force F acts on mass m > 0 in Newtonian mechanics | a = F/m, with dimensions L/T² | Assert a = Fm |
| P079-02 | A particle starts at rest under constant acceleration a over time t >= 0 | x - x0 = at²/2 | Assert x - x0 = at |
| P079-03 | A nonrelativistic body of mass m has speed v | K = mv²/2 | Assert K = mv/2 |
| P079-04 | An ideal gas with fixed amount n is in equilibrium at absolute temperature T | PV = nRT | Assert PV = nR/T |
| P079-05 | A resistor is ohmic at fixed temperature | V = IR | Assert V = I/R |
| P079-06 | A small-angle simple pendulum of length L in uniform g > 0, negligible damping | T = 2π sqrt(L/g) | Assert T = 2π sqrt(g/L) |
| P079-07 | Light in vacuum propagates over distance d in an inertial frame | travel time = d/c | Assert travel time = dc |
| P079-08 | A closed system exchanges no energy or matter and is governed by conservation of energy | total energy change = 0 | Assert energy increases spontaneously without external transfer |

Each oracle is conditional. For example, P079-06 is not an exact large-amplitude pendulum law; P079-05 fails for non-ohmic devices; P079-02 assumes constant acceleration. For P079-08, clarify energy accounting and boundaries before adjudication. Dimensional agreement is necessary but not sufficient for correctness. The counterfactuals are deliberate synthetic errors, not observed model hallucinations.

## Independent verification pipeline

1. Freeze pilot examples and source families before prompts are selected. Use textbooks or primary physical references with exact page/section citations; do not cite a generated derivation as independent evidence.
2. Assign two independent human or otherwise genuinely external subject-matter adjudicators per test item; document conflicts and escalation. Until then, use the pilot only for engineering and label all results provisional.
3. Create paired valid/invalid claims and assumption-removal variants; keep every variant from the same source family in one split.
4. Compare (a) direct LLM judge, (b) claim decomposition + retrieval, (c) uncertainty-calibrated selective judge, (d) symbolic/unit checker, and (e) proposed assumption-explicit certificate verifier. Specify actual implementations before testing; a weak strawman does not count.
5. Freeze acceptance coverage and compute/evidence budgets before comparing unsafe acceptance. Report abstention, coverage, calibration, per-domain error and adjudication cost.
6. Use the existing paired missing-truth bounds with shared item truth. Report bounds and the fraction unresolved. Do not turn non-identification into a positive claim.
7. Cluster bootstrap by source family; include paired uncertainty intervals and family-held-out results. Report sensitivity to adjudication missingness and assumption mis-specification.

## Falsification and stop rules

- If the certificate verifier does not outperform the strongest baseline at matched coverage and budget, do not claim improvement.
- If improvement vanishes under source-family separation, report leakage sensitivity.
- If a certificate is mathematically valid but assumptions fail, score the scientific claim as unsafe for its asserted scope.
- If paired bounds include no improvement, do not assert superiority.
- If independent adjudication is unavailable, restrict publication claims to methodology, software validation, and clearly labeled synthetic demonstrations.
- If strongest prior art already implements the proposed mechanism, narrow or abandon novelty claim; audit DeepSciVerify, CURE, selective prediction, scientific fact-checking, formal verification and physics-informed evaluation with primary links and publication dates.

## Zero-cost cloud execution gate

Preferred *candidate*, not yet authorized to run: standard GitHub-hosted runner for a public repository, subject to current GitHub policy and the account's billing/Actions settings. Before starting: verify repo visibility, Actions enabled, standard runner availability, applicable free public-repo allowance, no larger runner, no paid services, no self-hosted laptop runner, no external paid inference API, no paid artifact/storage upgrade. Fail closed if any condition is unverified. Use only Python standard library for deterministic checks. Never launch heavy local computation on the user's laptop.

## Evidence ledger for manuscript

Every claim in a manuscript must link to one of: (1) an executable source commit, (2) an actual cloud-run log with commit SHA and exit status, (3) independently adjudicated evidence with provenance, or (4) a dated primary literature citation. Design specifications and authored tests are not passing tests. Synthetic examples are not independent physics experiments. Report AI assistance according to the chosen venue's disclosure requirements.

## Immediate next steps

- Obtain a source citation and independent adjudication for each canonical item, then create a machine-readable sealed pilot dataset.
- Run Protocols 072, 073, 077 and 078 on an eligible verified free runner; capture immutable logs and exact failures.
- Audit the strongest 2025–2026 prior-art implementations and preregister a genuine head-to-head evaluation.
- Keep the 2026-11-22 target conditional on evidence, not on the number of protocols.
