# Protocol 081 — Auditable physics certificates and premise perturbations

Status: preregistered design, **not experimental evidence**. Date: 2026-11-05. Scope: independent frontier-AI research only.

## Research question

Does requiring a machine-checkable physical certificate, with explicitly enumerated assumptions, reduce unsafe acceptance of scientific claims relative to strong evidence-retrieval and abstention baselines **at the same acceptance coverage and evidence budget**, on source-disjoint physics tasks?

A certificate can be algebraically valid while scientifically invalid: validity of the derivation is conditional on the premises. Therefore measure *derivation validity*, *premise applicability*, and *claim truth* separately. Do not score an algebraically correct derivation as a physically correct claim when its premises fail.

## Immutable benchmark record contract

Each record must include:
- `claim_id`, `family_id`, `source_cluster_id`, `version`, `created_utc`;
- `claim_text`, `variables` (quantities with SI units), `assumptions` (explicit predicates), `domain`;
- `expected_relation`, `derivation_steps`, `reference_source` (stable URL and section), `source_license`;
- `perturbation_of` (nullable), `perturbation_kind`, `changed_premise`;
- `truth_label` in {true, false, unresolved}, `adjudicator_ids`, `adjudication_rationale`, `adjudication_status`;
- `split` in {development, locked_test}, `sha256` of canonical serialized content.

An `unresolved` truth label is not silently treated as false. Keep adjudication metadata outside model-visible prompts. Keep all paired perturbations and near-duplicates in the same split, including any records sharing a source cluster.

## Pilot cards (constructed, not observed results)

| Family | Conditional statement | Premise perturbation that must be separately adjudicated |
|---|---|---|
| Mechanics | F = ma in an inertial frame for constant mass | Accelerating frame without fictitious-force correction |
| Kinematics | x = x0 + v0 t + (1/2) a t² for constant acceleration | Time-varying acceleration |
| Energy | K = (1/2) m v² in nonrelativistic regime | Relativistic speed |
| Gas | PV = nRT for ideal gas at equilibrium | Strongly nonideal high-density state |
| Circuits | V = IR for ohmic element at fixed conditions | Non-ohmic diode |
| Pendulum | T ≈ 2π sqrt(L/g) for small angle, negligible damping | Large amplitude |
| Optics | c = λf for vacuum electromagnetic wave | Confusing vacuum speed with material phase speed |
| Conservation | Mechanical energy conserved for isolated conservative system | Dissipative friction |

The right-hand column does **not** automatically imply the original numerical conclusion is false; adjudicators must assess the actual changed claim and parameters. Generate numeric examples only after specifying units, boundary conditions, tolerances, and authoritative references.

## Independent adjudication

Two reviewers independently annotate each locked-test record before seeing model outputs, using written physical derivations and references. Disagreements are retained; a third adjudicator resolves them or the record stays unresolved. Record whether reviewers had access to the original prompt. Reviewers must not see system identity or confidence. If qualified independent reviewers cannot be obtained at $0, label the benchmark *author-constructed / not independently adjudicated* and prohibit empirical superiority claims.

## Leakage and counterfactual safeguards

1. Freeze test prompts and hashes before baseline evaluation.
2. Partition by physical family and source cluster, not random individual claim.
3. Hold perturbation pairs together; report pairwise premise sensitivity.
4. Keep labels, references, and rationales out of model-visible context unless explicitly budgeted equally for every method.
5. Include invalid-units, missing-boundary-condition, and contradictory-premise controls.
6. Log prompt version, model identifier, access date, response, latency, evidence tokens and cost. Never present unrun baselines as evaluated.
7. Report safety bounds when truth is unresolved and both adjudicated-only and full-cohort sensitivity analyses.

## Primary endpoints and falsification

Primary endpoint: unsafe-acceptance rate among accepted claims at prespecified matched acceptance coverage; separately report unresolved-truth partial-identification intervals. Secondary endpoints: premise-swap sensitivity, correct abstention, certificate checkability, evidence consumption, calibration and adjudicator agreement. Bootstrap by source family or source cluster; avoid treating perturbation pairs as independent.

The central hypothesis fails if the proposed method cannot demonstrate a robust safety improvement over the strongest eligible baseline at matched coverage, if the effect disappears under source-disjoint evaluation, if certificate validity does not predict physical correctness, or if bounds include both benefit and harm. An uninformative or negative result is publishable only with transparent limitations, not as an invented breakthrough.

## Cloud execution gate

No run is authorized until the specific account and repository are verified to have a standard **free** hosted runner, zero billable exposure, sufficient remaining quota and storage, and no required card or paid upgrade. Never use larger paid runners, paid APIs, or local laptop computation. If the gate cannot be verified, preserve executable plans and report execution pending.

## Prior-art and integrity boundaries

Partial identification, selective prediction, abstention, scientific claim verification, symbolic checking and premise-sensitive reasoning are established areas. Audit contemporary closest prior art before asserting any novelty; compare actual implemented baselines, not only their descriptions. Cite original primary sources with dates and versions in the eventual paper. Disclose AI assistance and data provenance as required by the target venue. No empirical outcomes, qualified reviewer participation, cloud eligibility, or novel method are asserted by this document.
