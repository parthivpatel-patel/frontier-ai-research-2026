# Protocol 082 — Deterministic physics seed records and falsification gates

Status: **constructed examples only; not independently adjudicated; no model evaluations run**. 2026-11-05.

## Why this protocol exists

Protocols 079–081 define a benchmark schema but do not yet provide independently validated physical truth labels. This document locks a small set of numerical *candidate* records, explains the assumptions and arithmetic, and separates an algebraic oracle from the later blinded physical adjudication. It must not be cited as empirical evidence of verifier performance.

## Candidate records (SI units)

Each pair contains a positive control and a counterfactual or negative control. Numerical tolerance is an explicit part of the claim; exact decimal equality is not assumed.

| Pair | Claim and declared premises | Candidate expected status | Independent calculation or counterexample |
|---|---|---|---|
| N1a | A 2 kg point mass with net force 6 N in a Newtonian inertial frame accelerates at 3 m/s² | Supported under stated premises | a=F/m=6/2=3 |
| N1b | Same mass with net force 6 N accelerates at 4 m/s² | Contradicted under stated premises | F=ma would require 8 N |
| K1a | Constant acceleration 2 m/s², initial speed 1 m/s, elapsed time 3 s; final speed 7 m/s | Supported | v=u+at=1+2·3=7 |
| K1b | Same initial speed and elapsed time, acceleration changed to 0 m/s²; final speed still 7 m/s | Contradicted | v=1 |
| E1a | A 4 kg body moving at 3 m/s has translational kinetic energy 18 J (nonrelativistic) | Supported | E=mv²/2=4·9/2=18 |
| E1b | Same body at 6 m/s has translational kinetic energy 18 J | Contradicted | E=72 J |
| C1a | Ideal ohmic 4 Ω resistor with 12 V across it carries 3 A | Supported | I=V/R=12/4=3 |
| C1b | Same resistor with 8 V across it carries 3 A | Contradicted | I=2 A |

These are deliberately elementary: they test whether the pipeline can represent premises, counterfactual changes, dimensions and known numerical contradictions. They are **not** evidence of scientific reasoning beyond equation substitution.

## Immutable candidate data contract

For each record store: record_id, pair_id, domain, claim_text, premise_text, constants with SI units, derivation, expected_candidate_label, source_reference, source_license, provenance_timestamp, authoring_method, adjudicator_id (null until adjudicated), adjudication_timestamp (null), adjudicated_label (null), uncertainty_reason, SHA-256 over a canonical UTF-8 JSON representation. A hash detects changes; it does not authenticate truth or authorship. Source references and licensing must be checked before release as an adjudicated benchmark.

## Evaluation gates

1. **Before model runs:** freeze benchmark and source-family split, register the hashes, evaluation code revision, prompt templates, evidence budget and stopping rule. Keep source references unavailable to a model if they would leak the answer.
2. **Blind independent adjudication:** two adjudicators assess premise applicability, numerical derivation, ambiguity and the candidate truth label without seeing verifier decisions. Resolve disagreements by documented third review; do not overwrite initial labels.
3. **Counterfactual scoring:** report both per-record correctness and pairwise premise sensitivity. A pair is passed only if both claims are judged correctly. Report abstentions separately.
4. **Matched-coverage comparisons:** compare unsafe accepted claims at equal acceptance coverage and equal evidence budget; stratify by physics family and source cluster. Report uncertainty bounds for unresolved labels; never silently drop them.
5. **Negative controls:** check leakage by permuting labels within matched strata and by replacing meaningful premises with contradictory premises. If gains persist when premises are irrelevant or labels are permuted, treat the claimed mechanism as unsupported.
6. **Failure conditions:** no improvement over competitive baselines, a confidence interval including zero under the preregistered estimand, source-disjoint degradation, inability to replicate, or gains driven only by selective adjudication preclude a superiority claim.

## Key conceptual caveat

A violated modeling assumption does **not** logically imply the negation of every conclusion derived under that assumption. The counterfactuals above use new numerical values with explicit countercalculations; they do not infer falsity merely from changing an assumption. Claims about real apparatus require additional empirical validation.

## Cloud execution and integrity

No execution is authorized by this document. Use only standard free eligible cloud runners after checking the actual repository's Actions permissions, billing/spending settings, remaining quota, and runner availability. Do not use larger paid runners, self-hosted laptop runners, paid APIs or card-required services. The laptop remains browser-only. If eligibility cannot be verified, leave experiments pending.

## Publication status

This protocol contributes **candidate test fixtures and a falsification design**, not a novel theorem, validated benchmark, model result or independent adjudication. Literature comparison must explicitly address selective prediction, conformal risk control, scientific claim verification, uncertainty-aware abstention and physics consistency checking before any novelty claim. Disclose AI assistance as required by the eventual venue.
