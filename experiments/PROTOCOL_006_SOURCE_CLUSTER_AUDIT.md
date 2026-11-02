# Protocol 006 — Source-clustered temporal-label audit and novelty stop gates

Date: 2026-11-01 US Eastern. Status: **exploratory; no publication or novelty claim**.

## Objective
Extend the earlier five-row, one-original requirement audit to additional **independent original requirements** without treating sibling mutations as independent samples. Use only a pinned, MIT-licensed 25-row external CSV; avoid model inference, new downloads, paid APIs, and laptop compute.

## Data and provenance
Chiari & Mateis (2026-10-25), *Datasets supporting automated requirement formalization from natural language to temporal logic*, https://zenodo.org/records/23649257 ; public source https://github.com/michiari/requirements-datasets . The authors explicitly state that inherited annotations are **not verified ground truth**. Local pinned copy: `data/external/robustifai_number_mutations.csv`; Git blob SHA-1 `6f6d2e01707e777be9cd0197698f8f19b4381fc8` from upstream commit `a38a73a351c07a3d17cb561098485cd4416c5375`. License is MIT, credited in `data/external/requirements_datasets_LICENSE`.

The source data include 25 mutations from five original English requirements. Only **three** originals satisfy our intentionally narrow grammars:
1. Fixed offset: a at t implies b at t+N. Source formula `G(a -> X X X b)`.
2. Relative offset: a at t and b at t+1 implies c at t+1+N. Source formula `G((a & X b) -> X X c)`.
3. Cardinality: at least N of a,b,c hold at each time. Source formula `G(a | b | c)`. The source's phrase 'one of' may mean *exactly one* or *at least one*; we **do not adjudicate source equivalence** on this family.

We do not adjudicate the two other original requirements: 'two of them' conflicts with 'never together' and 'can only hold every N timestamps' is semantically underspecified relative to its inherited formula.

## Method
`src/independent_source_audit.py` parses only exact supported English strings and three exact source formula shapes. Each candidate mismatch receives an **ultimately periodic infinite-trace witness**: a finite prefix followed by a repeating loop. A restricted temporal evaluator checks the inherited formula and the strict changed-English meaning separately. A witness with inherited formula TRUE and changed English FALSE establishes non-equivalence for that particular row. No witness or a passing witness establishes **no equivalence**.

For cardinality, a trace with only a true at every time makes the inherited disjunction true and 'two of a,b,c' false under either exact-two or at-least-two interpretation. This avoids relying on the ambiguity of the original 'one of' phrase for the mismatch claim. All other meanings remain outside scope.

**Independence and leakage:** the unit is the original requirement, not a mutation row. Deduplicate identical changed English strings when counting distinct perturbations. No statistical confidence intervals or population estimates from three source clusters.

## Prespecified integrity checks
- Fail if the vendored file differs from the pinned upstream Git blob.
- Reject unsupported formulas or English, rather than silently interpreting them.
- Require the inherited source formula to hold on every proposed witness.
- Require the changed English to fail on every reported witness.
- Test infinite lasso periodicity, cardinality negative controls, and relative offsets from b (not from a).
- Report unsupported rows and unresolved supported rows explicitly.

## Next stage: what would be publication-grade
1. Obtain at least 30 **independently authored** requirements across three nontrivial grammar families with independently checked intended meanings. Three originals here are insufficient.
2. Use original-source AND paraphrase-template disjoint train/dev/test splits; no mutations of a held-out original in training. Publish a cluster-level uncertainty analysis, not row-level pseudo-replication.
3. Acquire lawful, documented, real NL-to-LTL/STL model predictions (ideally released outputs) without paid inference or large weights. A number-word naive Bayes classifier does not qualify.
4. Compare reference-only scoring, semantic probes, verified behavioral counterexamples, and clarification-based baselines at matched oracle access and query budgets.
5. For physics integration, specify admissible dynamics and input domains, independently adjudicate human intent, and compare counterexample detection under reachability constraints. A logical trace alone is **not** a physical trajectory.
6. Predefine primary metrics: independently adjudicated mismatch precision, coverage, accepted-prediction error, oracle calls, and per-source abstention. Include uncertainty and negative controls.
7. Kill or pivot if closest prior art already covers the claimed contribution, no independent annotations can be obtained at $0, or gains disappear on source/template-disjoint holdout.

## Closest prior art and feasibility
- Nair et al., *Beyond Type-checking*, 2026-10-07, https://arxiv.org/abs/2610.10604 : behavioral adequacy and evidence scope for generated formal specifications. Already covers a large part of our original idea.
- Suo & Emami, *Quizzing the Translation*, EMNLP 2026, https://aclanthology.org/2026.emnlp-main.310/ : theorem-prover-based positive and contrastive semantic probes; cannot claim these probes as new.
- Ye et al., *ReasonSTL*, 2026-05-07, https://arxiv.org/abs/2605.06483 : tool-augmented and signal-grounded NL-to-STL, including a 4B model. We are not reproducing their training.
- *Translating Natural Language Requirements into Signal Temporal Logic: A Replication and Extension Study*, artifact dated 2026-10-24, https://zenodo.org/records/23617396 : 120 requirements across eight domains, reported maximum accuracy 55%, and a **222.2 MB** artifact. Strong overlapping domain; full dataset license, source independence and output accessibility remain unverified, so do not download or treat it as a clean benchmark.
- Chiari & Mateis, https://zenodo.org/records/23649257 : 36 originals / 1,790 augmented rows and 360 formulas / 1,080 NL descriptions; annotations explicitly unverified. Do not count generated paraphrases as independent human requirements.

## Compute and publication policy
Only standard `ubuntu-latest` GitHub-hosted runners in this **public** repository; no larger runners, self-hosted compute, external paid APIs, GPU instances, model weights or laptop workloads. Five-minute CI timeout, Python standard library, no artifact or cache writes. Official billing policy checked 2026-11-01: https://docs.github.com/en/billing/concepts/product-billing/github-actions — standard hosted runners in public repositories free; larger runners billed. GitHub Actions access has already been demonstrated in prior runs. A specific new run is not considered verified until its GitHub status and logs are checked.

No human-subject intent, physical safety, LLM performance, new theorem, or provider-specific result is claimed. Disclose AI assistance as required by the eventual venue. November 22 remains a conditional internal target.
