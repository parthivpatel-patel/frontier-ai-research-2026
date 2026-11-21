# Paired archival bounds: joint feasibility gate (2026-11-21)

## Status
Mathematical design audit, **not** an empirical finding, a proven novel result, or a verified CI run. Existing `research/archival_bounds.py` reports marginal identification intervals and obtains a conservative paired interval by subtracting endpoints. That difference can be non-sharp because the two policies' missing-case errors share the same unknown ground-truth label.

## Exact finite-population setup
For each unresolved example i, let its unknown binary truth be y_i in {0,1}; policy A and policy B have fixed predictions p_Ai and p_Bi and fixed accept indicators a_Ai and a_Bi, all established **without** using unavailable future evidence. Their error indicators are a_Ai 1[p_Ai != y_i] and a_Bi 1[p_Bi != y_i]. Verified-case counts are E_A,E_B and accepted counts K_A,K_B.

For a candidate truth vector y, define R_A(y)=(E_A + sum_i a_Ai 1[p_Ai != y_i])/(K_A+sum_i a_Ai) and analogously R_B(y). If either denominator is zero, that candidate's risk difference is undefined and MUST be separately counted; it is not zero.

With known predictions and accept decisions, exact sharp extrema for the risk difference are obtained by minimizing and maximizing R_A(y)-R_B(y) over all admissible joint truth assignments y, rather than combining marginal extrema. For small synthetic m, exhaustive enumeration of 2^m assignments can serve as a **cloud-only** reference oracle. For larger m, use a mathematically validated optimizer or report conservative intervals rather than pretending exhaustive enumeration is feasible. Never run this enumeration on the user's laptop.

## Important distinctions and limitations
1. If unresolved cases' policy predictions or acceptance decisions are *also* unknown, the joint feasible set must include those possibilities; the fixed-decision sharp bound above does not apply.
2. If the missing population is not completely enumerated, no finite-population coverage guarantee follows from the counts alone.
3. If missingness depends on evidence availability, historical archive selection can differ across NLP, mathematics and physics. Report family-stratified bounds and weights specified before evaluation.
4. A shared truth label induces dependence across policies. Marginal difference bounds remain conservative but may exaggerate uncertainty.
5. Even a sharp identification interval is **not** a confidence interval. Sampling uncertainty and source-family clustering require separate treatment.
6. Temporal metadata leakage, label adjudication error, and correlated source revisions remain distinct threats not repaired by sharp bounds.

## Required falsification tests before claiming an advantage
- Construct a synthetic unresolved example where both policies make the same prediction and accept the same case: its unknown truth must affect both error counts together, not independently.
- Construct opposite predictions with both accepting: their missing-case errors must be complementary.
- Test one-sided abstention, zero denominators, m=0, duplicate source families and inconsistent frame sizes.
- Verify that any reported sharp interval is contained in the existing conservative interval; if not, halt and debug.
- Verify that chronology-shuffled evidence or matched-compute baselines do not reproduce a claimed temporal benefit.
- Withhold directional superiority claims whenever the uncertainty interval includes zero or family-level results reverse the aggregate conclusion.

## Next engineering gate
Implement a dependency-free *small-m* joint-assignment reference implementation with explicit fixed-policy predictions and acceptance decisions, deterministic regression tests, and a CI job only after checking GitHub Actions free-minute and billing eligibility in the actual account. No paid runners, GPUs, model downloads or local inference are authorized.

## Publication boundary
This is a methodological refinement drawing on established partial-identification and selective-prediction concepts. No originality, novel theorem, cross-domain performance, or model result is asserted. A November 22 methods/preregistration release must disclose the absence of independently validated model experiments and document all AI assistance as required by the venue.
