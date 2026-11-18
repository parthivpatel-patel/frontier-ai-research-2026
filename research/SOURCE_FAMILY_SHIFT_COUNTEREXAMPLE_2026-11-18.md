# Source-family shift: why calibration coverage and risk do not transfer (2026-11-18)

**Status:** analytical counterexample and experimental design note. Not a measured result, a theorem of improvement, or a preregistration freeze. Complements the matched-budget selective-risk audit.

## A falsifying construction

Let a verifier score S be binary and let the policy answer only when S=1. Consider calibration families with P(S=1)=0.7, P(error=1 | S=1)=0.01, and P(error=1 | S=0)=0.40. The resulting *population* calibration coverage is 0.7 and selective risk is 0.01. Now consider independent held-out families with P(S=1)=0.2, P(error=1 | S=1)=0.60, and P(error=1 | S=0)=0.10. Applying the **same** policy gives population held-out coverage 0.2 and selective risk 0.60. These values follow directly from the stipulated conditional probabilities; they are synthetic mathematical examples, not observations.

This construction proves that source-family separation alone does **not** guarantee stable coverage, calibrated error risk, or improvement under arbitrary distribution shift. A threshold chosen on calibration families can be evaluated without leakage on held-out families, but its calibration-domain guarantee cannot automatically be transported to the new population.

## Consequences for the planned paper

1. Distinguish **within-population exchangeability** assumptions behind any conformal or risk-control guarantee from empirical robustness on unseen families. Do not advertise distribution-free guarantees under arbitrary family shift.
2. Record two independent endpoints: achieved test coverage and conditional error among answered examples. A method can appear to reduce selective risk merely by abstaining much more. Compare full risk–coverage curves descriptively, but do not select operating points using test labels.
3. Fix a minimum acceptable achieved test coverage floor on validation data, and report held-out floor violations as failures rather than silently removing them. A calibration-selected threshold does not ensure the floor under shift.
4. Separate **source-family-held-out** evaluation from **time-held-out** evaluation. Both can be compromised by shared templates, answer leakage, or benchmark exposure. No single split establishes training-data uncontamination.
5. Do not infer a causal role for the proposed shared score from predictive improvement. Mechanistic claims require distinct interventions and controls.
6. If the proposed score combines physics dimensional consistency, mathematical proof checks, and NLP entailment checks, specify exactly what is shared (e.g., a decision rule) versus domain-specific. Otherwise a cross-domain result may merely aggregate three existing verifiers.

## Statistical correction to the proposed primary contrast

The existing primary contrast subtracts the strongest eligible baseline selected on validation families. This is acceptable as a **predeclared selection algorithm**, but the selected baseline is random and its identity must be frozen before final held-out inspection. Confidence intervals that condition on that selected baseline do not account for uncertainty in the baseline-selection procedure; present the inference as conditional on the frozen choice, and report sensitivity to alternative eligible baselines without claiming post-hoc superiority.

An additional issue: a difference between selective risks at two *different achieved coverages* is not a pure accuracy comparison. Treat matched **calibration** coverage as the policy definition, report achieved held-out coverage separately, and require a prespecified minimum held-out coverage criterion for any practical deployment claim. Do not tune thresholds to equalize held-out coverage using held-out labels or outcomes.

## Concrete pre-experiment gates

- **Data:** independently sourced and licensed question/answer/evidence inventories for each domain; provenance and cluster IDs; source-family separation; leakage audit.
- **Labels:** blinded external adjudication of answer correctness, including reasoning validity and physical consistency, with disagreement handling.
- **Baselines:** confidence-only abstention, domain-specific verification, and applicable calibrated risk-control method; equal evidence access and measured resource usage.
- **Decision:** fixed coverage targets, minimum achieved coverage, practical risk margin, safety margin, and multiplicity policy chosen before observing held-out labels.
- **Compute:** confirm the actual GitHub-hosted public-repository runner eligibility, account restrictions, workflow permissions, and resource limits before any job; no paid runner or self-hosted laptop.

## Publication stop/go

A negative or null outcome remains reportable. A confirmatory improvement claim is **NO-GO** if evaluation data, baselines, provenance, independently established freeze timing, or actual cloud resource eligibility are unresolved. The November 22 date is a review checkpoint, not a reason to relax evidence requirements.

**Originality caveat:** This counterexample is elementary probability reasoning, not claimed as novel theory. The paper's novelty remains unestablished pending full-text comparison with selective classification, conformal risk control, verifier benchmarks including VerifyBench, and recent cross-domain evaluation work.
