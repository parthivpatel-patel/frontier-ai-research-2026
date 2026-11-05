# Protocol 087 — Four-way scientific claim semantics and falsification contract

Status: research specification, not empirical evidence. Date: 2026-11-05.

## Scope and relation to prior protocols
This protocol follows the assumption-admission and evaluation specifications in Protocols 084–086. It does not assert that a production classifier, independently adjudicated benchmark, or frontier-model comparison exists. It separates **claim truth** from **applicability of a proposed physical model**.

## Claim and evidence objects
For each item record (a) the exact natural-language claim, (b) a formal proposition P, (c) quantities and SI units, (d) domain D, (e) assumptions A, (f) cited evidence E with source identity and timestamp, (g) a proposed model M, (h) evidence-access budget, and (i) independent adjudication status. Never expose hidden reference labels to the evaluated verifier.

Let W(E) be the set of physically possible worlds compatible with admitted evidence E and explicit background constraints. Define:

* **SUPPORTED** iff W(E) is nonempty and P holds in every world in W(E).
* **REFUTED** iff W(E) is nonempty and not-P holds in every world in W(E).
* **UNDERDETERMINED** iff W(E) contains at least one P-world and one not-P-world.
* **OUTSIDE_SCOPE** iff the evaluator cannot legitimately apply the declared model M to D under A, or the required proposition/units/domain cannot be parsed sufficiently for this model-specific evaluation.

OUTSIDE_SCOPE is a *model-applicability disposition*, not an ontological truth value. A separate model-independent adjudicator may still determine P. Inconsistent evidence (W(E) empty) is an **ERROR / CONFLICT** requiring quarantine, never vacuous support and refutation. Unsupported sources, missing assumptions, and numerical uncertainty must be recorded explicitly.

## Two-axis adjudication to prevent category errors
Store `model_applicability` in {applicable, inapplicable, unknown} separately from `claim_status` in {supported, refuted, underdetermined, not_adjudicated}. The four-way operational output is derived only for a *specified model*. If inapplicable, output OUTSIDE_SCOPE regardless of an independent claim truth label; retain the latter separately for scoring. If applicability is unknown, do not silently treat it as inapplicable: record unresolved applicability and abstain or output UNDERDETERMINED with a reason code. This priority rule is preregistered and must not be changed after inspecting test results.

## Illustrative counterfactuals (constructed, not independently adjudicated)
1. Ideal resistor: R=10 ohm and V=20 volt, with explicitly stated ohmic, steady-state conditions. The model predicts I=2 ampere. Changing the *claim* to I=3 ampere under the same conditions is REFUTED.
2. Non-ohmic component: V=20 volt and an observed differential resistance of 10 ohm does not license I=2 ampere from V=IR. Mark the Ohm-law **model** OUTSIDE_SCOPE; do not assert the current is not 2 ampere.
3. Newtonian point mass: m=2 kg and net F=6 N in an inertial frame imply a=3 m/s². If net force is unspecified, the acceleration is UNDERDETERMINED rather than REFUTED.
4. Contradictory evidence: an exact same-time, same-frame acceleration independently fixed to both 3 and 4 m/s² triggers ERROR / CONFLICT, not a supported claim through an empty feasible-world set.

## Validator acceptance criteria
* Required fields: record_id, proposition, model_id, assumptions, units, evidence_sources, evidence_budget, adjudication_status, split_id, and source_family.
* Reject NaN/Infinity, negative physical masses where prohibited by the stated model, zero resistance for an I=V/R calculation, duplicate IDs, malformed units, missing provenance, and hashes that do not match canonicalized record bytes.
* Enforce source-family-disjoint train/development/test partitions and immutable held-out test hashes.
* Require a reason code for every abstention, conflict, or OUTSIDE_SCOPE decision.
* Do not permit a synthetic expected label to be marked independently adjudicated.

## Preregistered falsification
Primary endpoint: unsafe acceptance among answered claims at matched coverage, with the same evidence and compute budgets. Report per-domain and per-source-family breakdowns, uncertainty intervals, and selective-label partial-identification bounds. A reduction in unsafe acceptance at materially lower coverage is **not** a positive finding. Evaluate calibration, abstention, and error on scope perturbations separately. Include equation-only, retrieval-backed, symbolic/units, and independent-verifier baselines; choose baseline implementations and thresholds on development data only.

The contribution fails its primary claim if (i) strong baselines match or outperform it under the matched protocol, (ii) apparent improvements disappear after source-family separation, (iii) withheld physical assumptions are leaked into the evaluator, (iv) independent adjudicators cannot reach acceptable agreement under a preregistered rubric, or (v) selective-label bounds do not identify the claimed advantage.

## Publication and infrastructure gates
No claim of novelty or frontier-model improvement without a documented closest-prior-art matrix, a frozen benchmark, independent adjudication, reproducible cloud logs, and honest negative results. Run only on cloud resources whose account-specific free eligibility, billing controls, quotas, and actual availability have been checked. No laptop workloads. Do not incur charges or require a payment card. Preserve assistance and disclosure records as required by the eventual venue.

## Next implementation slice
Implement a pure standard-library validator and table-driven tests for the four outcomes and conflict quarantine, then obtain cloud-run evidence after eligibility verification. No results are claimed by this document.
