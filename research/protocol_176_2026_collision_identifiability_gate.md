# Protocol 176 — 2026 prior-art collision and counterfactual identifiability gate

Date: 2026-11-10. Status: literature-screening and prospective design only. No model experiments, independent annotations, or novelty claim.

## New 2026 collision evidence (primary preprint abstracts; not independent replication)

1. Zhang, *Testing Frontier Large Language Models' Physics Literacy in Parallel Physical Worlds* (2026-06-30), https://arxiv.org/abs/2607.00276 — counterfactual physical worlds, pre-registered diagnostic stages, human audit, and self-review are already proposed. Therefore counterfactual physics testing and preregistration are **not** novel here.
2. Zhao et al., *SCI-PRM: A Tool Aware Process Reward Model for Scientific Reasoning Verification* (2026-06-03), https://arxiv.org/abs/2606.04579 — science-specific process verification and tool traces already exist. Do not claim scientific step verification as novel.
3. Chen et al., *Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries* (2026-03-31), https://arxiv.org/abs/2603.29500 — structured intermediates verified by a formal prover are prior art. Do not claim formal step intermediates as new.
4. Belz et al., *Beyond Outcome Verification: Verifiable Process Reward Models for Structured Reasoning* (2026-01-23), https://arxiv.org/abs/2601.17223 — deterministic rule-based process verification and evidence grounding are established in another domain.
5. Gao et al., *CCRV-Bench: Constraint-Based Evaluation of Causal Reasoning in Vision-Language Models* (2026-09-25), https://arxiv.org/abs/2609.30979 — constraint intervention, adversarial constraints, and causal evaluation in visual physical scenarios are existing work. The proposed study is **text-grounded** and must show a substantive distinction rather than modality relabeling.
6. Ananthula and Kumarappan, *Decodable but Not Faithful: Coupling Natural-Language Rationales to Programmatic Verifiers* (2026-06-19), https://arxiv.org/abs/2606.21678 — verifier coupling does not imply faithful reasoning. A change in verdict is not evidence of the model's internal causal reasoning.

These are candidate closest neighbors from targeted discovery, **not** a complete systematic review. Inspect full texts, methods, benchmarks, licenses, and follow-up citations before priority claims.

## Candidate narrow question, not novelty claim

Can a **text-span-anchored, scope-aware physical-constraint verifier** identify invalid *fixed* reasoning steps more reliably than (a) identical rule checks with source spans hidden and (b) a matched-budget physics step judge, on independently adjudicated, paired physical-constraint edits, while controlling false rejection and abstention?

This question concerns *external auditability*, not proof of internal model faithfulness, mechanistic interpretability, or improved end-to-end solving.

## Causal contrast and identifiability

For original problem x, intervention x', fixed candidate step r, and human-adjudicated truth labels y(x,r), y(x',r), define verifier outputs V(x,r), V(x',r). An intervention is **diagnostic** only if a human expert confirms the edit changes the relevant constraint while other conditions are preserved. If y does not change, a verdict flip can be an undesirable false positive; if y changes, a flip in the correct direction can be desirable. A raw flip rate is uninterpretable without these paired truth labels.

Create three preregistered strata: (A) truth-changing physical edits; (B) truth-preserving constraint paraphrases; (C) nonconstraint placebo edits. Freeze r, decoding, thresholds, and evaluation code. Report per-stratum directionally correct decision rate, false flip rate, abstention, coverage, and source-equal-weighted correct-answer yield. Distinguish correctness of the *step* from correctness of the *final answer*. Never compare only selectively retained cases.

Potential confounds: intervention-induced lexical cues, changed answer difficulty, equation leakage, span-selection bias, correlated paraphrases, model familiarity with physics families, and labeler disagreement. Require blinded dual adjudication with an explicit unresolved label; unresolved cases are excluded from primary analysis and counted transparently.

## Prospective preregistration gates

- Unit of splitting/resampling: original physics source problem; no paraphrase or intervention family may cross calibration/test boundaries.
- Baselines: answer-only, dimensional-consistency, process judge, deterministic rule checker without provenance, and the proposed span+scope checker. Unavailable baselines must be reported, never fabricated.
- Primary outcome: paired difference in source-weighted correct-answer yield at calibration-frozen, matched coverage; also report false rejection and abstention.
- Primary negative control: randomized source-span/constraint linkage with the same constraint inventory. Placebo nonconstraint edits test spurious sensitivity.
- Falsification: no benefit over strongest feasible baseline, effect vanishing with source clustering, or randomized linkage matching proposed method. An ambiguous or underpowered study yields **inconclusive**, not positive.
- No guaranteed risk control without a proven procedure and its assumptions. No generalization claims across physics families without independent held-out-family testing.
- Predefine minimal practically relevant effect and sample-size feasibility **before** test-label inspection; do not invent power estimates or select them after seeing results.

## Execution readiness

Before any cloud job, verify account-specific GitHub Actions billing, free minutes/storage, runner eligibility and workflow permissions, and hard stop conditions. A public repository alone is insufficient evidence of zero cost. No card, paid API, GPU rental, laptop training, inference, or large downloads. Small static text edits via GitHub API are permitted. Record immutable dataset/manifests, software SHA, adjudication protocol, dataset redistribution rights, and AI assistance disclosure.

## Go/no-go

**NO-GO for scientific superiority or novelty claims today.** The strongest 2026 collisions are direct. The next defensible deliverable is a small independently labeled pilot and transparent baseline feasibility table, *after* free-cloud eligibility is verified. November 22 is conditional and should be deferred rather than publish an unsupported breakthrough.
