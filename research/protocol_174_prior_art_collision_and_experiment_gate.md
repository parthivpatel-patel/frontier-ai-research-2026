# Protocol 174: Prior-art collision and zero-cost experimental gate

Date: 2026-11-10
Status: literature audit and prospective design only; not a novelty proof or experimental result.

## Verified adjacent research (primary publication records)
- Zhang et al., **PhysReason** (ACL 2025), https://aclanthology.org/2025.acl-long.811/ : 1,200 physics problems and answer/step-level automated evaluation. **Collision:** neither physics-specific step checking nor a physics reasoning benchmark is novel by itself.
- Xu et al., **UGPhysics** (ICML 2025), https://mlanthology.org/icml/2025/xu2025icml-ugphysics/ : 5,520 bilingual undergraduate problems and model-assisted rule-based judgment. **Collision:** physics-aware hybrid judging is existing work.
- Feng et al., **Physics: Benchmarking Foundation Models on University-Level Physics Problem Solving** (Findings ACL 2025), https://aclanthology.org/2025.findings-acl.610/ : 1,297 expert-annotated problems with automated evaluation. **Collision:** robust automated physics answer validation is not a unique contribution.
- Siddique et al., **PhysicsEval** (Findings IJCNLP/AACL 2025), https://aclanthology.org/2025.findings-ijcnlp.43/ : 19,609 physics problems and inference-time multi-agent solution verification. **Collision:** an extra verification agent or inference-time checking is not novel by itself.

This targeted review is not exhaustive. Extend to process reward models, verifier-guided search, theorem provers, dimensional-analysis checkers, selective classification, conformal risk control, and 2026 publications before a novelty statement.

## Narrow falsifiable hypothesis (NOT an established contribution)
Given a frozen candidate answer and matched acceptance coverage, a verifier that checks **typed physical constraints and provenance-linked assumptions** may detect physically invalid steps more reliably than (i) answer-only grading, (ii) dimensional consistency alone, (iii) step-level LLM judging, and (iv) constraint-blind judging. A measured gain must persist on independent physics source groups and NLP paraphrase families under equal-source weighting.

Potentially distinctive mechanism to test, not to advertise: attach each extracted constraint to its source-text span and physical scope; perturb or remove the span, then ask whether the corresponding verification decision changes in a logically predictable direction. This requires a formally defined entailment/constraint interface and manual adjudication of ambiguous text; simple string overlap does not suffice.

## Predeclared baselines and negative controls
1. Frozen answer-only exact/symbolic or expert adjudication.
2. Frozen dimensional/unit consistency checker.
3. Step-level physics-aware judge approximating published evaluation paradigms, only when reproducible and permitted by cost/licensing.
4. Constraint-blind checker with identical model, tokens, time and abstention policy.
5. Constraint-shuffled and source-span-shuffled controls within family, with labels kept hidden from threshold selection.
6. Valid alternative units, equivalent coordinate conventions, and legitimate approximations as false-rejection stress tests.

If an unavailable paid baseline is scientifically essential, report the comparison as blocked; do not substitute a weak baseline and claim superiority.

## Data and decision protocol
- Register source and parent provenance IDs, physics family, prompt/paraphrase generation mechanism, solution, label adjudication, span-to-constraint map, and permissions.
- Split at parent provenance group before any prompt or threshold tuning. Freeze one primary paired source-level correct-yield contrast and a coverage tolerance using calibration only.
- Report source-level paired differences, coverage, false acceptance and false rejection, uncertainty conditional on independent clusters, family-level sensitivity, and compute costs.
- Require a blinded adjudication subset; disagreement is recorded, not silently overwritten.
- Failure criteria: no improvement over the strongest feasible matched baseline; advantage disappears under source-level weighting or held-out families; source-span shuffling performs similarly; false rejection of valid solutions is excessive; or contamination/provenance cannot be ruled out.
- An observed failure or insufficient sample yields a negative/inconclusive paper, not a positive novelty claim.

## $0 cloud and publication gate
No new cloud execution authorized by this document. A previously reported passing GitHub Actions run does not verify remaining included minutes, storage limits, account billing state, payment method, or eligibility. Before each new workload: verify the actual account's free entitlement, current usage and applicable billing policy; require a bounded CPU-only job with explicit timeout and no paid runners/services. If any of these cannot be verified, do not launch. The laptop is browser-only.

Record dependency versions, hashes, immutable splits, code SHA, actual logs, and test collection counts. Distinguish written protocols, passing software tests, and real independent model results. Disclose AI assistance as required by the target venue and accurately identify authorship and contributions. Target 2026-11-22 only if evidence meets these gates.
