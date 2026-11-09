# Protocol 165 — Physics-verifier novelty collision audit (2026-11-09)

Status: literature triage, NOT a completed systematic review, novel method, or empirical result. Public abstracts and proceedings pages inspected on 2026-11-09. No experiments executed.

## Material closest prior art

| Work | Established scope | Consequence for our contribution |
| --- | --- | --- |
| Lightman et al., *Let's Verify Step by Step* (2023), https://arxiv.org/abs/2305.20050 | Process reward models evaluate intermediate mathematical reasoning. | Step verification itself is not new. |
| Zhang et al., *The Lessons of Developing Process Reward Models in Mathematical Reasoning* (2025), https://arxiv.org/abs/2501.07301 | Process reward evaluation and misleading best-of-N scoring. | Evaluator bias and flawed intermediate steps are known concerns. |
| Zhang et al., *PhysReason* (ACL 2025), https://aclanthology.org/2025.acl-long.811/ | 1,200 physics questions; answer- and step-level automatic scoring. | **Direct collision** with generic physics-step verification and physics-specific scoring claims. |
| Xu et al., *UGPhysics* (ICML 2025), https://proceedings.mlr.press/v267/xu25ai.html | 5,520 English/Chinese physics questions; model-assisted rule-based judgment. | Physics-specific hybrid scoring and multilingual physics evaluation are not inherently novel. |
| *PhysUniBench* (2025 preprint), https://arxiv.org/abs/2506.17667 | 3,304 diagram-based undergraduate physics questions. | Broad physics evaluation and diagrammatic reasoning are existing areas. |
| *PHYBench* (2025 preprint), https://arxiv.org/abs/2504.16074 | Original physics problems and expression-sensitive grading. | Symbolic similarity grading alone is not a novel contribution. |
| *PhysicsEval* (2025 preprint), https://arxiv.org/abs/2508.00079 | Physics problem solving with cumulative verification by smaller LLM agents. | **Direct collision** with generic multi-agent physics verification. |
| Geifman and El-Yaniv, *Selective Classification for Deep Neural Networks* (2017), https://arxiv.org/abs/1705.08500 | Risk versus coverage under abstention. | Selective answering is established methodology. |

This table is not evidence of an exhaustive novelty search. Read full methods, appendices, code and later follow-up work before any priority or novelty assertion.

## Narrow testable hypothesis, not a claim

At a fixed answer rate, a **predeclared physically grounded constraint checker** (e.g., units, conservation-law applicability, domain/boundary conditions) might reduce wrong-answer yield on held-out source problems relative to: (1) answer-only checking; (2) a step-verification baseline; (3) confidence-based abstention; (4) matched random abstention. Novelty, if any, must rest on a *specific previously unreported algorithm, theory, or validated empirical phenomenon*, not the combination of known words or tools.

## Design that can falsify the hypothesis

- Freeze source-problem clusters and physics-family splits before tuning. Keep all NLP paraphrases of a source problem in one split. Disclose benchmark contamination and benchmark licensing.
- Match answer coverage *on the same held-out source problems*; report selection overlap and paired correct/wrong/abstain outcomes, case-, cluster-, and family-weighted effects.
- Distinguish false rejection of physically valid solutions from catching genuine violations. Include adversarial cases where dimensional analysis passes but physics is wrong, and where unusual but correct units appear.
- Ablate units, conservation, boundary-condition checks, and the abstention rule. Report cost and abstention burden.
- Require sensitivity to physics-family removal, source-cluster uncertainty, paraphrase duplication, and random-abstention controls.
- Stop any advantage claim if matched-coverage improvement is absent, disappears under equal-family weighting, or depends on leakage; label inconclusive confidence intervals as inconclusive.
- Report negative results. No post-hoc selective threshold changes.

## Feasibility and cost gates

Only propose executable workloads after account-specific verification of GitHub Actions entitlement/remaining minutes, workflow billing behavior, runner availability and any applicable card requirement. Public GitHub repository status does not by itself prove free quota. Avoid local compute entirely. No API keys, paid inference, or unverified free trials. Until verification, protocol-only development is permitted.

## Next decision

Prioritize full-text comparisons against **PhysReason**, **UGPhysics**, and **PhysicsEval** before adding more evaluation infrastructure. If their methods already implement the proposed constraint checker, change the contribution claim or pivot to a rigorous replication/negative-results study rather than claiming novelty. A Nov 22 paper is contingent on this gate and real independently reproduced experiments.
