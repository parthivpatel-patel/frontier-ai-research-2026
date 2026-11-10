# Protocol 181 — Paired randomization inference and minimum viable pilot gate

Date: 2026-11-10. Status: prospective mathematical analysis; no experimental data or performance claims. Extends Protocols 177–180.

## Why this gate exists

The crossed provenance experiment produces multiple dependent records per source problem. An ordinary row-wise bootstrap, a binomial confidence interval on all paraphrases, or a significance test on all crossed cells would overstate independent evidence. This protocol specifies what is identifiable and testable *before* a pilot begins.

## Locked units and outcomes

The source problem is the primary sampling unit. Each source has a frozen candidate step, independently adjudicated labels for each valid edit, and both correct-link and matched-shuffle verifier outputs. For source s, compute the average paired yield difference d_s across its pre-registered eligible edit instances: indicator(correct verdict with correct links) minus indicator(correct verdict with matched-shuffle links). Wrong verdict and abstention each score zero in this primary yield; report coverage and accuracy among answered cases separately. Never count repeated paraphrases as new independent sources.

The target estimand is the equally source-weighted average d_s among the *eligible, observed pilot sources*, not necessarily a population effect. If inclusion depends on finding a feasible same-type/scope shuffled link, describe that restricted target population and report attrition. Fix edit-stratum weights in advance; if a source lacks a stratum, do not silently reweight the surviving strata. Either restrict to complete sources under a pre-registered rule or report stratum-specific estimands with denominators.

## Exact paired assignment test: conditions and limitations

If correct-versus-shuffled provenance assignments are genuinely randomized within source, with no interference, no carryover, and a frozen evaluation pipeline, a randomization test can assess the *sharp null* that assignment changes no source's potential outcome. Enumerate or Monte Carlo sample assignment vectors consistent with the actual randomization scheme, recompute the pre-specified source-weighted statistic for each, and compare with the observed statistic. The assignment space must preserve blocking and any paired presentation constraints; do not assume arbitrary independent sign flips if that was not the design.

A simple sign-flip test on observed d_s is **not automatically exact** merely because observations are paired. Exactness requires a justified exchangeability or randomized assignment mechanism under the null. If there was no assignment randomization, present descriptive paired effects and sensitivity analysis rather than label the p-value design-based. Randomization inference for the sharp null does not by itself yield a confidence interval for the average effect or establish transfer to unseen physics families.

## Uncertainty and multiplicity

Publish every d_s and source count. If enough independent sources are available, use a source-level resampling interval as a descriptive uncertainty analysis, stating assumptions and small-cluster limitations. With very few sources, report exact counts, paired effects, and a cautious uncertainty discussion rather than a nominal 95% guarantee. If physics families are few, leave-one-family-out results are a stress test, not a substitute for independent family replication.

Primary endpoint: source-weighted correct-verdict yield, correct minus matched-shuffle, with abstentions counted as zero. Secondary endpoints: coverage, selective accuracy, matched-coverage risk, correct two-verdict transitions, false flips on equivalence/placebo edits, and family sensitivity. Lock one primary contrast before evaluating held-out cases; label all other comparisons exploratory and report all attempted analyses. Set the minimum worthwhile improvement independently of observed pilot performance.

## Minimal auditable data contract

Required fields per record: source_id, physics_family, original_problem_id, edit_id, edit_stratum, candidate_step_id, provenance_condition, assignment_seed, rule_inventory_hash, prompt_hash, model_or_verifier_version, label_original, label_edited, label_adjudication_status, verifier_output, abstained, eligible, eligibility_reason, token_budget, compute_budget, and run_manifest_hash.

Reject duplicate primary keys (source_id, edit_id, candidate_step_id, provenance_condition, run_manifest_hash), unknown labels, missing adjudication, and mismatched budgets before scoring. Preserve rejected rows and reasons in a separate attrition manifest. A deterministic reference scorer must be unit-tested with toy examples, including all-abstain, no eligible source, one source with many paraphrases, missing paired condition, and both-direction label transitions. Synthetic test fixtures must never be described as experimental results.

## Decision gate

1. Verify rights to redistribute or reference each pilot problem and any generated annotations.
2. Independently adjudicate a small source-diverse pilot while blind to link assignment; record disagreements and exclusions.
3. Freeze a matched baseline that has identical rules, numerical tolerances, token/compute budget, and answer visibility.
4. Confirm a valid same-type/scope shuffled-link candidate for each eligible intervention before seeing outputs.
5. Verify account-specific no-charge cloud entitlement, remaining quota, any payment-card requirement, billing safeguards, and that the planned job cannot trigger a charge. If not verifiable, do not execute.
6. Freeze scoring code and the assignment mechanism; only then evaluate held-out cases.

## Falsification and reporting

A null or negative primary difference, matched-shuffle performance indistinguishable from correct-link performance, widespread placebo false flips, substantial label disagreement, or systematic eligibility attrition undermines the proposed mechanism. Even a positive pilot contrast is not proof of general physics reasoning, causal understanding, or novelty. Compare full methods against 2025–2026 physics process verification and provenance/formal-premise prior art before submitting a manuscript.

No cloud job, model inference, or laptop-heavy computation is authorized by this document. Nov 22 remains conditional on independent evidence and research integrity.
