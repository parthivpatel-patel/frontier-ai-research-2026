# Held-out cross-domain validation protocol (draft; 2026-11-23)

Status: preregistration proposal, **not executed**. No novelty or performance claim. Keep independent from all other projects.

## Claim under test

For selective AI predictions whose ground-truth labels are partly unavailable, source-attributed logical evidence can produce valid, sharper *conditional identification intervals* for the difference in selective error rates than the unrestricted missing-label baseline, without excluding independently authenticated truth under the stated source-corruption budget. This is a conditional mathematical claim, not a distribution-free coverage guarantee. A narrower interval is not itself evidence of improved AI accuracy.

## Unit, estimand, and provenance

Freeze item IDs, paired model predictions, abstentions, accepted-case denominators, observed labels, and evidence source IDs **before** inspecting hidden labels or comparing bound widths. One item is a separately authored question with a binary correctness outcome for each evaluated answer; distinguish truth of an underlying proposition from correctness of a model response. For accepted counts K_A,K_B > 0, define Delta = E_A/K_A - E_B/K_B, where E are error counts over accepted items. Undefined denominators must be reported separately and never assigned zero risk.

Evidence records (i,j,p,source) assert y_i XOR y_j = p only when the two y variables have a defensible shared semantic interpretation. Source IDs correspond to independent originating documents/derivations, **not** URL count, retrieved snippet count, or repeated quotations. Derivative sources inherit the original source cluster. Authenticated hard labels must be independently verified and cannot be relaxed.

## Domain-specific task construction

* NLP: atomic entailment/contradiction propositions from a versioned, openly licensed corpus; use human adjudication or source-backed determinate labels. An entailment relationship between statements is not automatically an XOR relation between *model correctness* labels.
* Mathematics: independently checked binary theorem or counterexample propositions with machine-checkable certificates when feasible. Distinguish unverified proof text from an independently validated proof.
* Physics: dimensionally specified, boundary-conditioned questions with independently established solutions or verified reference measurements. Conservation constraints alone do not certify the answer to a natural-language physics question.

Do not pool results across domains until item-level definitions, labels and provenance are shown comparable. Record license, acquisition timestamp, transformations, exclusion reasons, and public hashes. Avoid benchmark contamination by separating model-output collection from adjudication and by reporting possible training-data overlap.

## Baselines and ablations

B0 unrestricted missing-label sharp bounds; B1 hard-label-only bounds; B2 record-level budget; B3 source-cluster budget; B4 independent deletion-subset exhaustive oracle on tiny instances. Report each under budgets k=0..number of source clusters, with an explicit fixed budget policy chosen without inspecting held-out truth. Ablate duplicate sources, provenance coarsening/refinement, hard-label proportion, and deliberately corrupted clusters. Never choose source partition or k to optimize observed results.

## Falsification gates

1. Any authenticated held-out truth assignment excluded at or above the *verified* number of corrupted source clusters falsifies the stated containment claim for that instance; investigate annotation, variable semantics, and provenance.
2. Any violation of monotonicity in k or partition-coarsening nesting indicates a software/specification defect.
3. A mismatch of complete feasible sets against independent source-deletion enumeration on small cases blocks empirical claims.
4. If the interval is not materially narrower than B0 under predeclared budgets, the proposed practical advantage is unsupported.
5. If a width advantage disappears after collapsing derivative evidence into common source clusters, report the original advantage as provenance-sensitive.
6. If the true corruption budget cannot be justified or verified, report sensitivity curves only; do not claim unconditional reliability.
7. A cross-domain result must survive per-domain analysis; an aggregate improvement masking a domain failure is insufficient.
8. Missing/undefined risk, abstention differences, and selection bias must be disclosed, not filtered away.

## Metrics and uncertainty

Primary descriptive endpoint: sharp interval width W=B_upper-B_lower, paired with truth containment conditional on a certified corruption budget. Secondary: abstention/coverage, fraction of undefined estimands, source-cluster counts, fraction of instances with nonempty feasible set, and compute/runtime. Report item-level and source-cluster bootstrap sensitivity only where exchangeability is defensible; bootstrap confidence intervals do not turn partial-identification sets into probability statements. Record all failures and empty feasible sets.

## Execution and cost gate

Use only verified no-cost standard GitHub-hosted public-repository CI for tiny deterministic reference tests, after checking current runner entitlement, public status, billing and Actions policy. Do not invoke larger runners, paid hosted model APIs, credit-card-gated cloud accounts, or any local computation on the user's laptop. No heavy model inference is authorized by this protocol. Larger held-out model comparisons remain blocked until an actually available $0 cloud execution path, licensing and quotas are verified. No new cloud account or payment method is requested.

## Research integrity and publication gate

Predeclare hypotheses and primary metrics before held-out evaluation. Keep raw predictions, independent adjudication, source-grouping decisions, hashes, code revisions, and failures in a reproducible release. Clearly disclose AI assistance, any inability to access model internals, and that relevance to frontier laboratories does not imply endorsement or use by OpenAI, Anthropic, or Google DeepMind. Compare directly to partial identification (Manski), budgeted robust optimization (Bertsimas-Sim), grouped corruption, constraint deletion/MAX-SAT, and selective prediction; novelty remains **unestablished** until direct comparison and demonstrated empirical advantage.
