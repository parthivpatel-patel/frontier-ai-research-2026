# Protocol 157 — Evaluation unit, selection leakage, and preregistered decision gate (2026-11-18)

## Status and scope
This is a design and falsification record, not experimental evidence, a novel theorem, or a claim of model improvement. It supplements Protocols 149–156. No model inference, training, or paid compute was authorized.

## Estimand: avoid a silent target-population change
For domain d in {NLP, mathematics, physics}, draw independent *source families* S_i from a defined target population P_d. Each family may contain multiple prompts, paraphrases, or derived items. For policy h and baseline b, predefine a family-level aggregation a(S_i,h) in [0,B] and c(S_i,b) in [0,B], including abstention and any budget penalties. The paired improvement is D_i(h)=c(S_i,b)-a(S_i,h), with target Delta_d(h)=E_{S~P_d}[D_i(h)]. Family-level equal weighting answers a different question from prompt-weighted performance; both may be reported, but neither may silently replace the other. Multiple prompts within a family do not increase independent n.

## Freeze before held-out labels
Record (1) source-family construction and deduplication rules, (2) domain-specific target populations and sampling frames, (3) ground-truth adjudication and uncertain-label exclusion rules, (4) exact frozen model/provider versions and decoding settings, (5) verifier policies, abstention thresholds and policy family size M, (6) baseline and matching rule for verification tokens/calls/latency, (7) B and loss function, (8) calibration versus test partitions separated by family, (9) confidence level, multiplicity across policies and domains, and (10) decision criteria. Hash the manifest before the test labels or outcome statistics are inspected. Missing any key field prevents a confirmatory claim.

## Statistical decision
If source families are i.i.d. within a prespecified domain, each candidate policy is fixed before testing, and paired losses are in [-B,B], then with a union bound over K total precommitted policy-domain claims, a conservative one-sided simultaneous lower bound is mean(D) - B sqrt(2 log(K/delta)/n_d). This is a standard Hoeffding bound, not a new result. Use the actual n_d and K, not the pooled number of prompts or only the eventual selected winner. For multiple domains with different sample sizes, apply the appropriate n_d per claim. Report both point estimates and bounds even when negative or vacuous. For dependence between source families, this bound is not licensed by simple deduplication; change the sampling design or explicitly downgrade to descriptive evidence.

## Source provenance and label audit
A source manifest should include family_id, original provenance URL or citation, publication date where known, licensing/access restrictions, template lineage, split assignment, domain, item count, annotation method, ambiguous-label status, and potential pretraining exposure flag. If origin is missing or the family construction is disputed, exclude from confirmatory analysis and report exclusions. Model-generated paraphrases inherit the original family ID. Exact-string deduplication alone is insufficient.

## Falsification and negative results
- If the source-level lower bound is <=0, do not claim certified improvement even if the prompt-level mean is positive.
- If the improvement disappears with equal verification budgets, reject the efficiency advantage.
- If an established conformal-risk or selective-classification baseline matches or exceeds the proposed policy, do not claim method superiority.
- If a domain fails its prespecified test, do not claim improvement in that domain; a pooled success cannot rescue it.
- If source provenance is inadequate, policies were edited after test-label inspection, or family dependence is unresolved, label findings exploratory.
- If the requisite independent families are unavailable at $0, publish a methods/negative-feasibility report rather than fabricate cross-domain empirical evidence.

## Feasibility and resource gate
Before any cloud model run, verify current provider-specific free quota, whether a card/billing account is required, whether the requested model and region are actually available, rate limits, data-use/licensing terms, and a hard spending stop. A public GitHub Actions standard runner may be appropriate for short standard-library regression tests, but does not imply free hosted LLM inference or sufficient CPU/RAM for large models. Do not use the user's laptop for computation. Do not run model experiments or enable billing merely because a cloud workflow exists.

## Claim boundary and next executable artifact
The next useful deliverable is a machine-readable *blank* source-family manifest and preregistration template, plus executed CI logs for existing deterministic fixtures. Do not add synthetic results as if they were observed outcomes. Compare against conformal risk control, selective classification, adaptive data analysis and source-cluster evaluation literature before asserting novelty. Disclose AI assistance according to venue policy. The November 22, 2026 target is conditional on actual evidence.
