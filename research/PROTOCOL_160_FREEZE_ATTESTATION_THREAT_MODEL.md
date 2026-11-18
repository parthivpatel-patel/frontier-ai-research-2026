# Protocol 160 — Freeze-attestation threat model and empirical stop/go gate

Status: methodological audit, 2026-11-18. No held-out model results are claimed.

## Confirmed implementation boundary

Inspection of `research/tools/validate_preregistration.py` at commit `a51db6f` shows that the strict API now requires a separate attestation, rejects duplicate JSON keys, checks canonical manifest bytes and compares the manifest's SHA-256 digest. These are useful integrity checks, **not** independent proof of when the study was frozen.

The attestation's `git_commit`, `freeze_utc`, `canonicalization` and `protocol_version` are presently checked for nonemptiness only. They are not cross-checked against Git history, commit timestamps, a canonicalization identifier or a version registry. A fabricated attestation with a valid digest could therefore pass structural checks. A mutable branch name is not an immutable freeze witness.

## Required evidence before any preregistered empirical claim

1. Store the canonical manifest and separate attestation in an immutable Git commit; record the full commit SHA and public GitHub URL.
2. Check that the attested manifest blob matches the bytes in the cited commit. Independently inspect the commit's public timestamp and history. Treat Git timestamps as provenance evidence, not a cryptographic trusted timestamp.
3. Preserve the evaluation data acquisition log, source-family identifiers, model revisions, sampling seed, and evaluation script hash; freeze them before looking at confirmatory outcomes.
4. Separate exploratory runs from the confirmatory analysis; report all exclusions and amendments with timestamps. If the freeze timing cannot be established, label the results exploratory.
5. Fail closed on unverified free-cloud quotas, card requirements, payment risk, benchmark licensing or data access. No local model computation.

## Primary empirical estimand and falsification

For each independently sampled source family `i`, define `d_i = utility(candidate,i) - utility(baseline,i)` under a matched verification budget and a preregistered abstention penalty. Cluster all paraphrases, prompts and derived tasks within their original source family. Estimate the mean family-level difference and a source-family bootstrap confidence interval, with correction over the complete confirmatory family of policies, baselines and domains.

Reject the superiority claim if the corrected lower confidence bound is not positive; if the benefit vanishes under matched budget; if leakage or source overlap is detected; or if a strong abstention/conformal-risk baseline matches the candidate. Report domain-specific effects even if the pooled result appears favorable. A single source family with many paraphrases is not a large independent sample.

## Scientific novelty gate

The project cannot claim a new general verifier, new mathematical theorem or physical insight merely from cross-domain application, source-family clustering or preregistration. Prior-art review must explicitly cover selective prediction/abstention, conformal risk control, process verification and test-time compute allocation. Any novelty statement requires a dated comparison against the closest methods and an explicit technical difference that survives an ablation.

## Immediate execution priority

Verify GitHub Actions at the latest commit; add adversarial tests that demonstrate fabricated nonempty metadata currently passes; then implement provenance validation with a documented trust model. Only after independent datasets and a genuinely available no-card/no-charge cloud inference route are verified should held-out experiments start.

This document is a research-integrity gate, not evidence that experiments have run.
