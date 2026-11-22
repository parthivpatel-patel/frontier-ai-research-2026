# Held-out evaluation preregistration: temporal evidence and paired selective verification

Status: **proposed protocol, not executed**. 2026-11-22. No model results, novelty determination, or publication acceptance are claimed.

## Research question and estimand

Does enforcing *historically available* evidence (rather than present-day evidence) change selective verification error and coverage for an AI verifier evaluated at a past decision cutoff? The primary paired estimand is the difference in selective error among **fixed accepted decisions** for cutoff-aware and cutoff-blind policies on a common evaluation set. Because acceptance sets can differ, report each policy's coverage and risk alongside the difference. The sharp shared-label interval identifies this difference conditional on observed verified labels, unresolved labels, and fixed policies; it is **not** a sampling confidence interval.

## Evidence and leakage contract

Every item must include: (i) claim and domain, (ii) decision cutoff in UTC, (iii) evidence publication/availability timestamp and timestamp source, (iv) retrieved evidence snapshot hash, (v) source URL and archive identifier where possible, (vi) verification label and provenance or explicit missingness, and (vii) precommitted split identifier. A webpage's current modification date does **not** prove its content was available at the historical cutoff. Exclude or separately flag any item whose availability cannot be authenticated. Record failures of archival retrieval, not just successful examples.

## Experimental arms and controls

- **B0:** closed-book verification, with no retrieval.
- **B1:** retrieval without cutoff enforcement, exposing potential hindsight leakage.
- **T:** retrieval filtered to evidence demonstrably available by cutoff.
- **T+A:** the same filtered retrieval plus a preregistered abstention rule.

Use identical underlying claims, model versions, prompt budgets, decoding settings, and retrieval corpora where possible. Freeze predictions and acceptance flags before inspecting held-out labels. A cutoff-blind arm is a diagnostic for leakage, not necessarily a deployable competitor. Include negative controls with deliberately post-cutoff evidence and with timestamps shuffled among documents; neither is admissible in the primary treatment.

## Identification and inference

Let n be the common frame size, m unresolved labels, and k_p the fixed accepted count for policy p. For each unresolved example i, the shared binary truth y_i contributes e_{Ai}(y_i)/k_A - e_{Bi}(y_i)/k_B. The sharp identification endpoints are the verified contribution plus the sum of the per-item minima/maxima, **only if** labels are unconstrained and binary, the same truth applies to both policies, and acceptance is fixed independently of the unresolved truths. If either accepted denominator is zero, the difference is undefined. If labels obey cross-example constraints, this separability may fail; use constrained optimization rather than the linear formula.

For population inference, cluster-resample at the original claim/source grouping (and time block when applicable), recomputing the entire evaluation statistic and identification endpoints; distinguish confidence sets for identified regions from identification regions themselves. Report sensitivity to missing-label mechanisms; absent assumptions, do not replace bounds with point estimates.

## Domain-specific falsification

**NLP:** If cutoff enforcement does not measurably reduce documented post-cutoff evidence use, the claimed temporal-integrity benefit fails.

**Mathematics:** A mathematical statement is not time-varying merely because a proof was published later. Restrict temporal claims to *knowledge availability* (proof, counterexample, conjecture status) and use mechanically checkable propositions or independent expert adjudication where available. If theorem/proof provenance cannot be dated, exclude from temporal evaluation.

**Physics:** Separate timeless physical laws from historically changing measurements, estimates, instrument calibrations, and scientific consensus. Record units, uncertainty, dataset versions, and measurement dates. A claim of physical accuracy requires domain-specific validation; temporal source matching alone is insufficient.

**Cross-domain:** Require each domain to clear its own preregistered validity checks and report disaggregated results. A pooled win cannot establish generality if one domain fails.

## Publication decision rules

1. **No-go empirical paper:** no authenticated held-out evidence, no independent execution record, or no defensible source provenance.
2. **Methods-only paper:** proofs and tests pass but comparative AI results or originality remain unresolved; disclose that explicitly.
3. **Empirical candidate:** preregistered held-out protocol executed with complete provenance, uncertainty accounting, baselines, negative controls, and a primary-source prior-art comparison. A statistically favorable result alone is not sufficient for novelty.

## Reproducibility and cost guardrails

Use only GitHub-hosted standard runners in a public repository after checking current eligibility and repository Actions settings; no larger runners, GPU instances, paid API calls, credit-card registration, or persistent infrastructure. A cloud job must have explicit timeouts, bounded data sizes, and no secrets in logs. GitHub Actions eligibility is not a guarantee of unlimited availability. The user's laptop is for browser access only; no local model inference, training, simulation, or downloads.

## Scientific-integrity ledger

Retain exact prompts, code commit hashes, archival evidence references, model identifiers, excluded cases and reasons, and all unsuccessful runs. Report AI assistance in accordance with venue requirements. Do not claim original theorem status for separable endpoint optimization until a comprehensive primary-literature review establishes what, if anything, is new.
