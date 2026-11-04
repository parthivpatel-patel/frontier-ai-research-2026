# Protocol 062 — Physics benchmark pilot and leakage-resistant evaluation

Date: 2026-11-04
Status: preregistered design; no new empirical results. Prior head: 337e6236b66247e447030888ee1773474f403d0f.

## Research question
At a fixed acceptance budget, can assumption-explicit, machine-checkable physical certificates reduce the fraction of *incorrect claims accepted* compared with (i) model confidence, (ii) answer-only self-verification, (iii) independent verifier judgments, and (iv) a symbolic or numerical checker without a certificate? This is a hypothesis, not a demonstrated contribution.

## Pilot record contract (one JSON object per claim)
Required: `claim_id`, `source_family_id`, `source_uri`, `source_revision`, `license`, `domain`, `problem_text`, `claim_text`, `assumptions`, `units`, `ground_truth` (true/false/unknown), `adjudication_method`, `adjudication_evidence_uri`, `certificate_kind`, `certificate_payload`, `certificate_checker_version`, `split` (development/validation/test), `derivation_family_id`. Unknown truth is an admissible record, not a negative label. Blank evidence cannot be silently counted as independently adjudicated. Source/license restrictions must be honored.

## Candidate physical domains and independent adjudication
1. Classical mechanics: dimensional consistency, energy conservation within stated closed-system assumptions, limiting-case checks.
2. Electromagnetism: Maxwell-equation consistency for explicitly stated boundary conditions and units.
3. Thermodynamics: first-law bookkeeping and domain restrictions; distinguish reversible from irreversible transformations.
4. Elementary quantum mechanics: normalization and Hermiticity for specified finite-dimensional operators.

Start with a small **curated pilot**, not a claimed benchmark. Each candidate requires an independently written solution and a checker with an explicit validity domain. Do not treat dimensional consistency or a numerical spot-check as a proof of the full claim. Include adversarial near-misses (wrong units, omitted boundary conditions, sign errors, physically impossible limiting cases) and correct claims with nonstandard wording.

## Leakage control
All records sharing a source_family_id OR derivation_family_id must remain in the same split. Freeze validation thresholds before test. Record prompt templates, model versions, decoding parameters, retrieval corpus snapshots, and the exact source commit. Audit paraphrases and textbook variants for cross-split leakage. Treat unverified source independence as a limitation.

## Estimands and rejection criteria
Primary estimand: paired difference in unconditional unsafe acceptance, certificate minus comparator, on the full held-out population, at matched acceptance coverage. A negative difference is desirable. Report coverage itself and selective risk separately. For unknown labels, report sharp paired identification bounds rather than deleting them. Use source-family cluster resampling for sampling uncertainty, and avoid presenting identification intervals as confidence intervals. If a bound includes zero, do not claim an identified strict improvement. If matched coverage is unattainable, report that fact rather than extrapolating. Report exact counts and per-domain strata; avoid significance claims on tiny pilots.

## Negative controls
- Identical acceptance decisions must yield a zero paired difference.
- Deliberately invalid certificates must be rejected by the checker.
- A checker that sees the adjudicated truth or test answer is disallowed.
- Certificates generated from false assumptions must be reported as conditional, not proof of physical reality.
- An abstain-all system cannot win through reduced unsafe acceptance.
- Source-family permutations and threshold sensitivity must be disclosed.

## Novelty boundary and closest prior art
Physics reasoning benchmarks (PHYBench, TPBench, QuantiPhy) already exist. Formal theorem-proving/verifier tooling (LeanDojo), process supervision, selective classification, conformal risk control, and neuro-symbolic verification are established. The only candidate contribution is an *empirically supported integration* of explicit physical assumptions, executable certificate checks, paired uncertainty under unresolved truth, and matched-coverage evaluation. None of the components alone is novel. Conduct a dated systematic literature search and archive titles/DOIs and exclusion reasons before making priority claims.

## Cloud and budget gate
No new workflow, model endpoint, hosted runner, storage, or API usage may be launched solely on the assumption that a public repository is free. Before any new compute, verify the exact account's remaining free minutes/storage, runner type, billing configuration, spending limits, and whether a payment method is required. Only standard free public-repository runners are candidates; no larger runners. Fail closed if verification is unavailable. User laptop is browser-only. Existing hosted regression run 41883906747 demonstrates previous execution, not future billing safety.

## Evidence and publication gate
A passing unit-test suite proves only that selected software cases behave as expected. No new benchmark examples, independent adjudications, model comparisons, calibration results, or novelty claims are reported in this protocol. Release a methods/preregistration note if experiments are not ready by November 22, 2026; disclose assistance and limitations under the target venue's policy.
