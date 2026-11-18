# Protocol 158 — Machine-readable preregistration and source provenance template

Status: **blank design artifact only** (2026-11-18). No observations, labels, model runs, or scientific results are contained here. Do not interpret example field names as a frozen preregistration.

## Before any confirmatory evaluation

Copy the JSON template below to a versioned, immutable file, replace every `null`, freeze candidate policies and source-family definitions before inspecting held-out labels, and publish its SHA-256 digest. Do not place private credentials, restricted benchmark questions, or identifying participant information in a public repository. A source-family identifier is not a substitute for proving independence or representative sampling.

```json
{
  "schema_version": "0.1",
  "status": "UNFROZEN_TEMPLATE",
  "study_id": null,
  "freeze_utc": null,
  "frozen_manifest_sha256": null,
  "domains": ["nlp", "mathematics", "physics"],
  "target_population_by_domain": {"nlp": null, "mathematics": null, "physics": null},
  "sampling_frame_by_domain": {"nlp": null, "mathematics": null, "physics": null},
  "source_family_construction_rule": null,
  "source_family_dependence_assessment": null,
  "family_weighting": "equal_family",
  "split_rule_and_seed": null,
  "ground_truth_adjudication": null,
  "ambiguous_label_policy": null,
  "models": [],
  "decoding_settings": null,
  "fixed_candidate_policies": [],
  "fixed_baselines": [],
  "verification_budget_matching": null,
  "loss_formula_and_abstention_cost": null,
  "loss_upper_bound_B": null,
  "domain_claim_count_K": null,
  "familywise_delta": null,
  "primary_estimand": "E_source_family[baseline_loss - policy_loss] per domain",
  "primary_decision_rule": "one-sided simultaneous paired source-family lower bound > 0",
  "leakage_audit": null,
  "pretraining_exposure_assessment": null,
  "license_and_access_review": null,
  "free_cloud_provider_and_quota_verification": null,
  "billing_and_card_requirement_verification": null,
  "hard_zero_spend_control": null,
  "publication_ai_assistance_disclosure": null
}
```

## Source-family CSV schema

Create a UTF-8 CSV with the following **header only** until actual source records have been inspected. A row corresponds to a source family, not an individual prompt. The `split` must be assigned at family level; paraphrases and derived tasks inherit the original family.

```csv
family_id,domain,source_title,source_url,source_publication_date,license,access_restrictions,template_lineage,split,item_count,label_method,ambiguous_label_status,pretraining_exposure_risk,independence_notes,exclusion_reason
```

## Statistical and scientific decision gates

For independently sampled source families and precommitted candidate policies, with paired difference in [-B,B], use the conservative lower bound `mean(D) - B*sqrt(2*ln(K/delta)/n_domain)`. This follows from Hoeffding plus a union bound, **not** a novel theorem. If the source families are not independent, the sampling frame is biased, or policy selection used held-out labels, do not apply this as a confirmatory guarantee. Report failures and vacuous intervals.

Do not claim NLP, mathematics, or physics generalization based on a pooled result. Do not claim superiority if an established matched-budget baseline performs as well. Distinguish physics *reasoning evaluation* from discovery of new physical laws. If free cloud inference cannot be verified, restrict work to mathematical analysis and deterministic CI.

## Evidence status at creation

GitHub Actions run [44212661794](https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/44212661794), on commit `54a4f6b58e4de6a0df4d6e1f26422eb013d8d5b5`, completed successfully on 2026-11-18 01:02 UTC. Its job log shows 5 + 5 + 6 + 6 = **22** passing deterministic tests across Protocols 146, 149, 150, 152. This is *not* full-suite coverage or model validation. The inventory step listed additional regression files that were not executed by this job. No model inference, paid cloud, or laptop computation is authorized by this record.

## Publication boundary

November 22, 2026 is a conditional checkpoint, not a promised publication. Disclose AI assistance in accordance with the destination venue's requirements. Scientific novelty and cross-domain empirical improvement remain unproven.
