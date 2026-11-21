# November 22 evidence-based publication decision (prepared 2026-11-21)

## Decision
The current record supports a **methods/preregistration manuscript**, not an empirical discovery claim. This is a conditional assessment, not an assertion that all repository experiments have been independently audited. A novelty claim remains unverified. Do not describe proposed mathematics, physics, or NLP tasks as tested until independently labeled results and run artifacts exist.

## Minimal release gates
1. **Identity and provenance:** freeze source URL, license, retrieval date, content hash, source family, evidence chronology, and correctness-label adjudicator for every example. A timestamp without a changing knowledge/evidence state does not establish temporal reasoning.
2. **Evaluation isolation:** record model/prompt versions, code commit, calibration split, held-out family split, frozen thresholds, cost budget, and all post-holdout revisions. Reused test data must be designated exploratory.
3. **Comparators:** temporal verifier vs timestamp-blind verifier at matched compute and coverage; timestamp permutation and source chronology placebo; acceptance-set overlap and common-accepted prediction comparisons.
4. **Inference:** predeclare primary pooled selective-risk estimand, positivity checks, family-level uncertainty and sensitivity to source-family concentration. Report undefined family risks rather than silently dropping them.
5. **Cross-domain validity:** NLP claims need changing documentary evidence; mathematics needs evolving proof/knowledge availability, not changing theorem truth; physics needs evolving observations/measurements, not changing physical laws.
6. **Free execution:** use cloud-only jobs after verifying current entitlement and billing settings on the account. Public-repository GitHub Actions may run bounded CPU unit tests; this does **not** establish free access to hosted model inference or a GPU. Never attach a payment method, start billable services, or run laptop workloads.
7. **Publication disclosure:** state AI assistance and authorship contributions as required by venue policy; provide data/code access where permitted; distinguish demonstrations, synthetic fixtures, and independent measurements.

## Stop/go rule for 2026-11-22
- **Discovery GO** only if all gates above are evidenced by immutable artifacts and novelty comparisons show a defensible incremental contribution.
- **Methods GO** if the protocol is reproducible and limitations and closest prior art are candidly documented, but performance evidence is missing.
- **No public scientific claim** if even provenance, research question, or falsification criteria cannot be adequately specified.

## Next execution artifact
A machine-readable evidence manifest should include: `example_id,domain,source_family,source_uri,source_license,retrieved_at,evidence_time,knowledge_cutoff,content_sha256,label,label_adjudication,split,model_id,prompt_hash,verifier_variant,accepted,prediction,compute_units,run_id`. Validate missingness, duplicate IDs, split contamination, and chronology before any confirmatory test.

## Scientific interpretation
Selective-risk improvements are policy-level outcomes and can arise from changed accepted sets rather than improved predictions. Claiming a distinctive temporal mechanism requires successful negative controls, chronology-sensitive tasks, and a credible comparison with non-temporal explanations. No empirical superiority or originality is claimed in this document.
