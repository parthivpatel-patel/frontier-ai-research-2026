# Closest-prior-art collision and new dataset candidate — 2026-11-02

**Status:** Evidence-based scope correction. This is not a novel theorem, model-performance result, or independent reproduction. No paid services, model inference, GPU, or laptop compute.

## A. Material novelty collisions

1. **SENTINEL** (Zhan et al.; arXiv:2510.12985, initially posted October 14, 2025; repository reports NeurIPS 2026 acceptance): https://arxiv.org/abs/2510.12985 and https://github.com/NU-IDEAS-Lab/SENTINEL . It already unifies natural-language safety interpretation, temporal-logic checking of plans, and verification of physically grounded trajectories, including counterexamples. The public repository's currently inspected \`ai2thor\` branch is a trajectory-level ALFRED/AI2-THOR implementation and explicitly says code organization is ongoing. **We cannot claim to introduce the first semantic/plan/physical formal-verification pipeline.**
2. **MANIGUARD** (Peng et al., August 18, 2026; arXiv:2608.17386): https://arxiv.org/abs/2608.17386 and https://github.com/NU-IDEAS-Lab/ManiGuard . It uses physics-grounded predicates and LTLf runtime monitoring, with 200 base tasks and 1,000 locked ID/OOD scenarios. **We cannot claim that physical safety monitoring or perturbation-based stress tests are original.** Full reproduction would require substantial simulation infrastructure, unsuitable for this $0 small-cloud project.
3. **SCP-NL2TL** (Wang et al., August 5, 2026; arXiv:2608.05439): https://arxiv.org/abs/2608.05439 . It already combines back-translation fidelity, exact semantic dispersion, conformal risk control, and abstention. **We cannot claim novelty for selective formalization or calibrated abstention alone.**
4. **SecDev 2026 NL2LTL** (Danso et al., July 2026; DOI:10.1145/3805773.3806005): https://doi.org/10.1145/3805773.3806005 and https://github.com/ochowdhu/NL2LTL-SecDev26 . It already evaluates LLM NL-to-LTL semantic equivalence using model checking. **We cannot claim semantic equivalence checking as a new method.**
5. Classical incomplete-system may/must verification, robust temporal logic, source-clustered evaluation, McNemar testing, and selective classification are established ingredients. An intersection of existing ingredients is not automatically novel.

### Revised research question (hypothesis only)

Can an **assumption-uncertainty diagnostic**, defined over a predeclared family of physically plausible transition models, detect unsafe natural-language-to-formal translations that existing semantic-consistency and selective-prediction baselines accept **at genuinely matched coverage**, without using the held-out gold interpretation during inference?

Critical separation: an independently adjudicated human-intended formalization may be used to *score* predictions after they are frozen, but **must never be supplied to the proposed verifier or used to tune its acceptance rule on the test set**. If a method needs the gold interpretation to flag a failure, it is an evaluation oracle, not a deployable verifier.

To be considered a contribution, the paper must (a) specify the admissible model-family construction independently of held-out outcomes; (b) show a nontrivial theoretical or empirical distinction from may/must verification and SENTINEL; (c) use source-disjoint, independently adjudicated human requirements and authentic model outputs; (d) compare against SENTINEL-style checking, SCP-NL2TL-style selection, and an appropriate domain-agnostic baseline with frozen budgets and coverage; (e) falsify the claim when benefits disappear under alternative plausible dynamics, invalid constraints, or independent source-level inference. Until then, **novelty unproven**.

## B. New real-data candidate: SecDev 2026

Upstream repository: https://github.com/ochowdhu/NL2LTL-SecDev26 . Inspected public commit \`35b2b28069531f3ca5cea938182f652bacd4922a\` on \`main-branch\`.

- \`input_data/nl2ltl_finalized.csv\`: 39,432 bytes; Git blob SHA-1 \`9a0939aad2ecce0a20094f29e7cc87dd2e88d731\`; columns \`Natural Language, Ground Truth, Atomic Proposition\`. This is a promising *input* benchmark; independent human adjudication and source-family independence have **not** been verified.
- The inspected \`output_data/\` directory has WFF results and an effectively empty NL2PL placeholder; **no NL2FutureLTL per-item model outputs were found in the published output tree**. The README describes experiments and supported model APIs but does not establish that recorded NL2FutureLTL predictions are included. Do not invent or infer them.
- **Licensing ambiguity:** README states CC BY-NC-ND 4.0; root \`LICENSE\` contains GPL-3.0 text. Neither alone resolves licensing scope for data, code, derivatives, or downstream redistribution. For now, inspect small pinned source in ephemeral cloud memory, publish aggregate counts only, and seek clarification before sharing/adapting dataset content.
- The dataset is not evidence of model accuracy, and unique strings are not independent original requirements. Repeated paraphrases may inflate counts. Protocol 021 freezes a hash-verified, metadata-only audit.

## C. Next go/no-go

The highest-value immediate work is to complete Protocol 021's actual cloud run, verify how many *lexically distinct* NL/formula records exist, inspect source provenance and duplication, and determine whether any **authenticated** per-item NL2FutureLTL outputs can be obtained lawfully at $0. The currently inspected SecDev repository alone does not meet that last condition. If it cannot, do not treat WFF outputs as NL2FutureLTL predictions.

A second route is the publicly described VLTL-Bench (English et al., 2025, https://arxiv.org/abs/2507.00877), which already offers state spaces and trace examples. Its licensing, download/card conditions, raw prediction availability, and independence must be checked before use. No Kaggle download or new account is authorized by this note.

**Decision:** Continue narrowly as a falsifiable methods study, not a general claim to have invented physics-grounded AI verification. If the data and novelty gates fail, publish a transparent methodological/negative result rather than a superiority paper. November 22, 2026 is an internal conditional target, not a promised publication date.
