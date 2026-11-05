# Protocol 086 — Prior-art collision audit and decision gate
Date: 2026-11-05
Status: literature triage; no experimental results; not a novelty claim.

## Research question
Can an assumption-explicit, abstaining scientific claim verifier reduce *unsafe acceptance* at a fixed acceptance coverage and evidence budget, when some physical truth labels are unavailable? The target is a conditional, empirical systems contribution—not the invention of physics verification, selective prediction, partial identification, or symbolic checking.

## Closest prior art (verify full texts before asserting a gap)
| Work | Overlap | Required differentiation |
| --- | --- | --- |
| SCI-Verifier / SCI-VerifyBench (2025), https://arxiv.org/abs/2509.24285 | Explicit scientific verification across mathematics and physics | Show that assumption applicability + abstention + partial labels changes risk beyond this verifier, under equal evidence budget |
| TPBench symbolic weak verifier (2025), https://arxiv.org/abs/2506.20729 | Symbolic step verification for theoretical physics | Compare with symbolic verifier, not only equation matching |
| PhysicsEval (2025), https://arxiv.org/abs/2508.00079 | Physics problems and multi-agent verification | Control for additional agents and inference cost |
| PHYBench (NeurIPS 2025), https://papers.nips.cc/paper_files/paper/2025/hash/01e793f8cf5689aa0ea46a1b01071bea-Abstract-Datasets_and_Benchmarks_Track.html | Curated difficult physics evaluation | Do not call eight elementary examples a novel physics benchmark |
| UGPhysics (ICML 2025), https://proceedings.mlr.press/v267/xu25ai.html | Physics benchmark and rule-assisted judgment | Compare adjudication quality and task overlap |
| ABench-Physics (2025), https://arxiv.org/abs/2507.04766 | Dynamic condition variation | Counterfactual premise perturbations are not independently novel |
| CLAIM-BENCH (2025), https://arxiv.org/abs/2506.08235 | Scientific claim/evidence validation | Compare evidence provenance and claim-level judgment |
| Manski, Partial identification with missing data (2005), https://doi.org/10.1016/j.ijar.2004.10.006 | Missing-outcome bounds | Do not claim partial identification as a new mathematical invention |
| Lakkaraju et al., Selective Labels Problem (KDD 2017), https://doi.org/10.1145/3097983.3098066 | Selectively observed labels | Explicitly account for selective adjudication rather than complete-case accuracy |

This is a targeted initial search, not an exhaustive systematic review. The above links identify real published or preprint prior art; their abstracts alone do not prove an unoccupied niche.

## Pre-registered comparison
Unit: a *claim with fixed premises and evidence*, not an individual token. Split by source family and underlying physical principle before any tuning. Lock the evaluation set and labels. Record model version, prompt, tools, costs, and provenance.

Baselines: (B0) equation-only check; (B1) assumption-aware rule check; (B2) symbolic weak verifier; (B3) scientific LLM verifier if legally accessible at zero cost; (B4) equal-budget multi-agent verifier if feasible. An unavailable baseline is reported as unavailable, not silently replaced with a weak proxy.

Outcomes: supported / refuted / underdetermined / out-of-scope. A claim's model being inapplicable is not sufficient evidence that the claim itself is false. Independently adjudicate ambiguous claims while blinded to verifier identity. Maintain an unresolved label when no defensible truth exists.

Primary metric: false acceptance per all adjudicated claims, with acceptance coverage reported separately. Compare risk at matched coverage; also report the full risk-coverage curve and per-family errors. When labels are selectively missing, give worst-case partial-identification intervals instead of complete-case point estimates as though identified. Never use synthetic hidden labels in a real-data estimator.

## Falsification / stop criteria
1. Any proposed gain disappears against assumption-aware rules or symbolic verification at matched coverage and evidence budget.
2. Gains rely on the same source family in development and test, or on leakage from answer keys.
3. Apparent gains reverse or are unidentified under missing-label bounds.
4. The method rejects valid but out-of-model claims as 'false'.
5. Independent adjudicators cannot consistently classify a meaningful share of benchmark items.
6. No free, permissible, reproducible compute path exists for the required comparison by manuscript cutoff.

## Feasibility and publication gate
No paid API, credit-card activation, trial with possible automatic charges, or local laptop compute. Before any GitHub Actions or cloud job, verify current repository Actions policy, spending limit, remaining quota, runner type and billing behavior; document the verification date and evidence. Public-repo runner free eligibility is not by itself proof that this account's configuration cannot incur charges. Do not trigger workflows without those checks.

The eight numerical physics cases and existing test modules are software fixtures, not a statistically meaningful physics evaluation. Test execution, independent adjudication, strong baseline results and a comprehensive novelty search remain pending. Nov 22 is an internal decision point: publish a scoped methods/negative-results manuscript if warranted; otherwise defer empirical superiority claims. Disclose AI assistance and limitations according to venue rules.
