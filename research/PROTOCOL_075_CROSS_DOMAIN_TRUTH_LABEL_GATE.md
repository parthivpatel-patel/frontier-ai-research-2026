# Protocol 075 — Cross-domain truth-label and estimand freeze gate

Date: 2026-11-14. Status: preregistration design, **not** executed empirical research, a new theorem, or an established novelty claim.

## Why another gate is needed

Exact design-unbiasedness of the family-sampling estimator (Protocols 068–074) only addresses **sampling error conditional on a fixed finite population of resolved labels**. It does not identify the true error rate if adjudicators disagree, labels are missing selectively, claims change meaning after retrieval, or a purported physics “truth” is only a model-dependent numerical approximation. Statistical correctness is necessary but not sufficient for scientific-claim verification.

## Frozen estimand

For domain d, candidate policy p, and a prespecified finite test frame U_d, let R_ip be the binary indicator that policy p releases claim i; Y_i=1 if the *frozen* claim is false under a prespecified adjudication rule and Y_i=0 if true. Claims not adjudicable under that rule receive Y_i=? and are **not** silently coded true or false. Define

FAR(p,d) = [sum_{i in U_d} R_ip Y_i] / [sum_{i in U_d} R_ip]

only when all released labels are resolved and the release denominator is nonzero. For unresolved released claims, report the identification interval [F/K, (F+M)/K], where F is the number of resolved false releases, M unresolved releases and K all releases. A policy difference is defined as FAR(candidate,d)-FAR(baseline,d); use a paired, probability-sampled evaluation design with fixed policy release denominators. This interval is a *logical bound*, not a confidence interval; sampling uncertainty must be handled separately. Do not claim the endpoint bounds are sharp when adjudication constraints connect labels.

## Domain-specific claim cards

* **NLP / source-grounded claims:** Freeze claim text, document edition and retrieval timestamp, evidence spans and source licensing. Label entailment, contradiction, insufficient evidence and ambiguity separately. Unsupported is not automatically false. Record evidence contamination and source circularity.
* **Mathematics:** Freeze exact proposition, quantifiers, assumptions and accepted proof standard. A numerical example or LLM agreement is not a proof. Label verified proof, verified counterexample, unresolved and malformed proposition separately. Use deterministic proof checking only where a trustworthy formal environment is available.
* **Physics:** Freeze physical system, units, parameter ranges, boundary conditions, precision/tolerances and whether the target is a theorem, empirical measurement or model prediction. A model prediction conflicting with another model is not automatically false. Record uncertainty, instrument/source provenance and scope of applicability.

Each claim card must have a persistent identifier, immutable text hash, provenance-family identifier, domain, truth protocol, adjudicator evidence, resolution status, and release decision for each policy. No adjudicator may see policy assignment when avoidable.

## Predeclared comparisons

Compare (a) calibrated selective release, (b) random verification at matched cost, (c) provenance-family-stratified verification, and (d) proposed adaptive provenance-aware verification. Use identical frozen test frames and truth protocols. Measure false-release rate and released coverage jointly; additionally report audit cost and abstention, per-domain outcomes, provenance-cluster sensitivity, and unresolved-label bounds. Any claim of improvement requires a specified effect size and uncertainty procedure established *before* inspecting held-out labels. No significance threshold or power claim is implied by this document.

## Falsification and negative controls

1. **Unresolved-label reversal:** Recompute differences with every unresolved released claim assigned false and then true; disclose when conclusions reverse.
2. **Claim-scope mutation:** Reject evaluation if a claim's quantifiers, units or evidence version change between policy runs.
3. **Provenance duplication:** Add duplicate paraphrases from the same evidence family and check that family-level analysis does not treat them as independent evidence.
4. **Physics tolerance sweep:** Report whether the ranking changes under preregistered measurement/solver tolerances, without tuning thresholds to results.
5. **Proof-versus-plausibility:** Ensure a persuasive natural-language mathematical argument without a valid proof is not automatically labeled true.
6. **Selective adjudication:** Audit whether unresolved labels concentrate among released claims or policy disagreements; apply logical bounds and do not assume missing at random.
7. **Budget mismatch:** Reject a comparison where candidate and baseline have different verification costs or access to evidence.
8. **Leakage:** Quarantine test claims, label files, and adjudicator notes from policy selection and calibration.
9. **Sampling-design mismatch:** Reject Bernoulli variance estimates for fixed-size family samples; use the design-specific formulas and report non-estimable cases.
10. **Multiplicity:** Record the number of domains, metrics, policy variants and tolerance sweeps; do not select a single favorable result post hoc.

## Novelty and publication boundary

This protocol assembles established evaluation concepts and is **not** evidence of original methodology. Closest prior-art categories requiring source-level audit: selective classification; conformal risk control; active learning/auditing; survey sampling with partial response; off-policy policy evaluation; evidence attribution and factuality benchmarks; formal proof verification; and scientific measurement uncertainty. Do not present the cross-domain combination as novel without demonstrating a specific difference from the closest existing methods.

## $0 execution gate

No experiment is authorized until the exact cloud account and provider terms are verified: free compute quota, card/billing prerequisites, current capacity, permitted public-repository use, and a reliable stop condition before any paid usage. GitHub Actions is a candidate only after its current free-tier and account-specific usage are checked. Never execute on the user's laptop. Record cloud run URL, commit SHA, runtime, dependencies, exit code, and full logs; otherwise mark tests unexecuted.

## Decision on November 22

A results paper requires independently executed, reproducible tests and a defensible prior-art distinction. Otherwise publish an explicitly labeled protocol/methods note or defer publication. Do not convert theoretical checks into empirical AI results.
