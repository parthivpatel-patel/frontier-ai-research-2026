# Protocol 114 — admission-to-estimation integration and falsification gates (2026-11-07)

Status: engineering design and preregistration candidate. No empirical result, independent adjudication, or novelty claim. Builds on Protocols 111–113.

## Integration invariant

The paired lineage bootstrap must never receive raw, unvalidated model-response rows. The only admissible path is:

1. Load the immutable evaluation manifest and the two prespecified system identifiers.
2. Validate the complete raw paired intervention table using Protocol 113. On any invalid pair, split leakage, ambiguous truth label, missing adjudication, or inconsistent provenance: fail closed and emit diagnostics only.
3. Produce a canonical, deterministically sorted admitted table with explicit shared physical truth, system-specific accepted/abstained status, system-specific adjudicated unsafe outcome (null on abstention), and lineage/family/intervention keys.
4. Check that the calibrated selection thresholds and matched-coverage target were frozen *before* held-out evaluation. A timestamp field alone is not proof: retain immutable artifact digest, versioned manifest, and audit trail. If chronology cannot be independently established, mark results exploratory.
5. Transform admitted rows to the estimator schema only after validating field semantics. Never map prompt_truth into response_unsafe. Never encode abstention as safe.
6. Estimate family-wise selective risk only where both systems have feasible preregistered coverage; report numerator, denominator, coverage, missingness, and undefined intervals. Resample full lineages jointly across both systems and evidence variants.
7. Preserve source hashes and manifest hashes in every result; reject mismatched digests or changed system identifiers. No inferential table if admission fails.

## Deterministic acceptance checks

A. Valid matched pairs produce the same canonical table under row permutation.
B. Equal row counts with one missing counterpart and one extra intervention are rejected.
C. Different system-specific unsafe labels with identical shared physical truth are allowed only with complete independent adjudication.
D. A system abstention with response_unsafe=false is rejected.
E. A lineage shared across calibration and held-out splits is rejected even if intervention IDs differ.
F. One changed evidence hash within a pair is rejected.
G. Any accepted response missing reviewer/rubric/evidence provenance is rejected.
H. An estimator invocation must not occur after any validation failure (spy/mock test).
I. A changed threshold or split-manifest digest invalidates the inference artifact.
J. Fixed seed and row permutation yield identical lineage-bootstrap output; resampling must not separate paired systems or paraphrases.
K. Zero accepted responses in any required family yields undefined risk, not zero.
L. Missing counterpart cases must not be silently removed to improve coverage.

## Falsification-first experiment

Primary question: do AI scientific verifiers rely on physical evidence rather than linguistic shortcuts? Compare complete evidence, contradictory evidence, shuffled evidence, and text-only controls for the *same* held-out physical scenario lineages. Freeze the intervention generator and independent adjudication rubric before observing competitive model results.

Predeclare: primary metric, expected directional contrast, minimum scientifically meaningful effect, family weights, acceptable coverage tolerance, multiplicity correction, sample-size/power assumptions, and stopping rules. Report both intention-to-evaluate accuracy and selective accepted-response risk; do not substitute one for the other.

Negative controls: proposition-preserving paraphrases and evidence perturbations that should not change physical truth. Positive controls: independently verified interventions that reverse the correct physical decision. A verifier that reacts equally to shuffled and causal evidence fails the evidence-reliance criterion. A method that succeeds only on templated synthetic cases, unblinded reviewer labels, or lineage-leaky splits fails the generalization criterion.

## Prior-art search obligations

Search and compare at least: TruthfulQA (Lin et al., 2022); HaluEval (Li et al., 2023); SelfCheckGPT (Manakul et al., 2023); Physics of Language Models / physical reasoning benchmarks; SciBench (Wang et al., 2023); and recent work on counterfactual or causal evidence interventions, selective prediction, and conformal risk control. These are *candidate comparators*, not a completed exhaustive novelty audit. Record verified title, authors, publication year, DOI/arXiv link, exact overlap, and remaining distinction in a dated matrix before making originality claims. Do not assume an untested distinction is novel.

## Operational and publication gates

Only the GitHub-hosted cloud runner may execute lightweight tests after account-specific free quota and billing eligibility are verified. No laptop computation, paid APIs, or model downloads. A passing synthetic CI suite validates code behavior, not scientific truth. A manuscript may be released as a clearly labeled methods/protocol preprint if experiments remain incomplete; it must not advertise unmeasured gains. Disclose AI assistance as required by the chosen venue. November 22 is an internal target, not evidence of readiness.
