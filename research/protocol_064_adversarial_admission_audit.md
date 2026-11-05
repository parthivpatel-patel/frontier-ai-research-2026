# Protocol 064 — adversarial admission tests and label-provenance audit

Date: 2026-11-04
Status: preregistered test design; **not an executed benchmark or empirical finding**.

## Objective
Challenge the Protocol 063 physics-record admission validator with adversarial records before any paper claims reliable physics verification. A schema-valid record is not necessarily a scientifically admissible record. Admission, adjudication, and evaluation must remain separate gates.

## Required invariant
An admitted *known-truth* label requires independently inspectable evidence about the physical proposition, its boundary conditions, units, and applicable regime. The mere presence of a nonempty evidence string is insufficient. Unknown truth must remain unknown, even if a derivation is formally valid.

## Adversarial fixtures (all illustrative; not observed data)
1. **Missing provenance:** known-truth record has a plausible derivation but no independent source or adjudicator. Reject known-truth admission.
2. **Self-adjudication:** the candidate model generated both the answer and its ground-truth explanation. Quarantine for independent review.
3. **Split alias:** identical source family appears under different casing, whitespace, URL fragments, or mirror domains across train and test. Normalize provenance and reject leakage.
4. **Paraphrase leakage:** two differently worded claims share the same textbook exercise or generating template. Require source-family linkage; reject split independence if linked.
5. **Assumption mismatch:** correct ideal-gas derivation applied outside equilibrium. Mathematical certificate may pass, physical truth cannot be inferred.
6. **Dimensional mismatch:** numerical equality is obtained by mixing SI and CGS quantities without conversion. Reject physical correctness.
7. **Boundary-condition omission:** conservation argument omits an external force or flux. Mark unresolved or false only with independent evidence.
8. **Ambiguous target:** proposition has no stated tolerance or measurement uncertainty. Do not assign binary physical truth.
9. **Unknown-truth preservation:** valid formal certificate with unknown physical truth remains unknown after serialization and scoring.
10. **Duplicate identity:** same claim under two identifiers or Unicode normalization variants. Reject or consolidate before evaluation.
11. **Adjudicator conflict:** two independent adjudicators disagree. Retain disagreement and quarantine; never resolve by majority without a predeclared policy.
12. **Negative control:** deliberately corrupted physical units should be detected at a higher rate than valid controls, conditional on matched acceptance coverage.

## Executable acceptance criteria
- Unit tests should construct minimal positive records and mutate exactly one field per negative case.
- Each test must assert both rejection reason and unchanged input; malformed records must not silently disappear from denominators.
- Source-disjointness must be checked by provenance-family identifiers, not just claim IDs.
- Report per-domain admission counts, exclusions, unknown-label rates, adjudicator disagreement, and abstention.
- Store deterministic fixture seeds and cryptographic hashes of input and output files.
- CI job must use a standard GitHub-hosted public-repository runner only after verifying repository visibility, workflow permissions, account billing policy and current free eligibility. Do not use larger runners or external paid APIs.

## Falsification
The physical-certificate hypothesis fails its strong form if the method does not improve unsafe acceptance at matched coverage against strong baselines; if gains vanish under source-family splits; if identification bounds include no improvement; or if apparent gains are driven by unresolved physical truth or greater abstention. A statistically significant difference alone is not sufficient to establish physical reliability.

## Closest methodological precedents
- Selective classification and risk–coverage evaluation (Geifman & El-Yaniv, 2017).
- Conformal risk control (Angelopoulos et al., 2024).
- Process supervision and learned verifiers (Lightman et al., 2023).
- Physics reasoning benchmarks PHYBench, TPBench, QuantiPhy (see Protocol 061 for exact citations).

None of the above techniques is claimed to originate here. The prospective contribution, if supported, is a reproducible combination of assumption-explicit physical certificates, provenance-aware adjudication, and paired partial-identification-aware risk comparison.

## Next execution gate
Implement these fixtures against the actual Protocol 063 module, inspect failure diagnostics, run only on a verified zero-cost cloud runner, and archive the run ID, source SHA, command, logs and output hashes. No claim of completed testing until those artifacts exist.
