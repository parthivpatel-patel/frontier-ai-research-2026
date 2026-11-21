# Bitemporal admission: threat model and testable correction plan (2026-11-21)

Status: methodological audit, not empirical evidence. No GPU, inference, or paid infrastructure used.

## Code inspection
Reviewed `research/bitemporal_admission_preflight.py` at commit `9c204f4a738b09edd3af53d9f96c0f9f7bc27893`. The current function is a conservative *metadata chronology filter*, not a historical availability oracle. Its seven embedded tests cover seven hand-constructed cases but do not prove historical authenticity, correct content hashing, source identity, or that the capture represents the exact published version.

## A consequential estimand distinction
There are at least two scientifically legitimate evaluation populations:

1. **Strict archived-at-cutoff population:** a version has a trusted immutable capture timestamp no later than the question cutoff. Current `admit` targets this restrictive subset.
2. **Documented-public-at-cutoff population:** a version has independent, sufficiently strong evidence of publication by cutoff, even if its archival capture occurred later. The current implementation rejects these records. This is a conservative false negative relative to documented public availability, and may induce selection bias toward sources with unusually good historical archiving.

Never silently interpret results on population 1 as representative of population 2. A later capture alone cannot authenticate earlier content; neither can an unverified `first_public_at` field.

## Required schema additions before confirmatory experiments
- `provenance_method` and independently auditable provenance reference (archived snapshot, signed release, immutable publication record, etc.).
- Hash computed from canonicalized source bytes, not merely a syntactically valid 64-character string.
- A version-to-capture binding, with explicit revision history and trusted capture clock.
- A policy version and an admission reason code, both saved with every decision.
- A distinct `first_observed_at` vs `claimed_public_at`; disputed times are unresolved, not silently backdated.
- A record of sampling exclusions to estimate archival selection and domain/source-family coverage.

## Additional regression tests to implement
1. Same `source_id` and `version_id` with different bytes must fail a global consistency check.
2. A forged but well-formed digest must fail byte-level verification.
3. A timestamp supported only by publisher metadata must be classified as unverified unless a predefined provenance tier explicitly permits it.
4. A later archive capture with independently verified earlier exact-version publication must remain excluded from the *strict archive* population, but eligible for a separately reported *documented public* sensitivity analysis.
5. Conflicting independent timestamps must be flagged for adjudication, not resolved by choosing the earliest.
6. Timezone-offset-equivalent instants must yield identical decisions.
7. Missing or malformed provenance must not be transformed into an inferred timestamp.
8. Duplicate and revised scientific measurements must be versioned separately; a modern correction cannot overwrite the historical source.

## Physics and mathematics falsification probes
Physics: historical numerical constants, measurements, and published revisions. Check that newer revised values are never silently attributed to earlier source versions.

Mathematics: the *truth* of a theorem is distinct from the public availability of a proof. The evaluation cutoff governs evidence availability, not timeless logical validity. A theorem's later proof must not leak into an earlier evidence condition.

NLP: revised documents and corrections require version-level passage hashes and retrieval trace preservation.

## Confirmatory reporting rule
Report strict-archive and documented-public populations separately; do not pool their denominators. Publish exclusions, accepted-question overlap, source-family composition, coverage, compute costs, and failure counts. The chronology-aware advantage is falsified if it disappears under matched coverage and cost, or survives equally under shuffled temporal metadata. These tests are necessary but not sufficient for a causal mechanism claim.

## Publication gate
No claim of a novel model, novel bitemporal concept, empirical improvement, or complete prior-art audit. This audit supplies an explicit, testable threat model. The November 22 checkpoint should produce a methods/preregistration artifact unless independent held-out evidence and a defensible novelty review are available.
