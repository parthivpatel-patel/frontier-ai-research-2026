# Protocol 138 — Robustness-claim scope and falsifiable empirical design

Status: preregistration and theoretical audit only. 2026-11-17. No model experiments or test execution are claimed.

## Scope correction

Protocols 135–137 distinguish a hidden random policy draw from a draw visible to an adversary. That distinction is necessary but not sufficient for an operational robustness claim. The corner-based minimax guarantee is conditional on (i) fixed class prevalence, (ii) fixed verifier sensitivity/specificity, (iii) a rectangular set of conditional pairwise couplings, (iv) bounded losses, and (v) a nonanticipatory acquisition policy. An adversary able to change the input distribution, marginal verifier accuracy, or truth labels is outside this guarantee. The synthetic exact-rational oracle is a *model validation* tool, not a certification of deployed AI safety.

## Dependence geometry and a falsification check

For each truth stratum y, let a_y=P(V1=1|Y=y), b_y=P(V2=1|Y=y), and t_y=P(V1=1,V2=1|Y=y). Feasibility requires

    max(0,a_y+b_y-1) <= t_y <= min(a_y,b_y).

The four joint cells are (t_y, a_y-t_y, b_y-t_y, 1-a_y-b_y+t_y). With two truth strata and independent interval restrictions on t_0 and t_1, expected loss of any fixed policy is affine in (t_0,t_1); hence its maximum occurs at a rectangle corner. A mixture of policies remains affine when the mixture weights do not depend on the unknown coupling. This corner claim fails as a general proof for uncertainty sets that also vary prevalence, calibration, marginal accuracy, or permit adversary adaptation after observations. For a nonrectangular *convex polytope* with fixed marginals, evaluate its actual vertices instead; the four rectangular corners may be infeasible.

**Falsification:** construct a nonrectangular coupling set (e.g., t_0+t_1=k within the feasible box). Reject any implementation that uses infeasible rectangle corners as if they were realizable worst cases; compare to a direct exact-rational evaluation of the segment endpoints. Repeat with a prevalence interval and test the correct expanded uncertainty geometry rather than silently reusing the original four corners.

## Primary empirical estimand (pre-register before outcomes)

On a source-disjoint held-out collection of AI-generated candidate answers from NLP, mathematics and physics, estimate the paired difference in expected decision loss between adaptive verification and the strongest budget-matched baseline. Report per-domain results, macro-average, and 95% uncertainty intervals using resampling at the **source/problem family** level, not answer level. Include abstention/deferral and verifier acquisition costs in the loss. Predefine losses and cost units before inspecting test outcomes.

A defensible primary null is that adaptive verification does **not** lower held-out loss relative to the best predeclared budget-matched baseline. Reject any superiority claim if uncertainty intervals include zero, if advantage disappears under source-disjoint splits, or if cost-matched baselines close the gap. No claim of novelty follows merely from a significant improvement.

## Baseline and leakage requirements

Include: always answer; always abstain; confidence-threshold selective prediction; fixed first-verifier-only; fixed two-verifier; and an adaptive strategy calibrated without dependence robustness. If applicable, include conformal risk control and published self-verification methods, carefully matching API/model calls and verifier cost. Report failure when a baseline cannot be reproduced without paid compute; do not quietly omit it.

Use separate sources and problem families for training/calibration and final evaluation. Freeze prompts, model versions, verifier templates, sampling rules, ground-truth adjudication, costs and exclusions before test access. Audit contamination, duplicated problems, benchmark overlap and leakage from verifier explanations. No fabricated data or cherry-picked cross-domain aggregate.

## Closest conceptual prior art to verify bibliographically

- Kuhn (1953), extensive games and behavioral/mixed strategies: behavioral equivalence is established theory.
- Wald, statistical decision functions and minimax risk: minimax formulation is established theory.
- Chow (1970), optimal reject option in pattern recognition: selective decisions are not new.
- Geifman and El-Yaniv (2017), selective classification: confidence-based coverage/risk tradeoff.
- Angelopoulos et al., conformal risk control: calibrated risk constraints.
- Manakul et al. (2023), SelfCheckGPT: black-box factuality checking.
- Dhuliawala et al. (2023), Chain-of-Verification: LLM verification workflow.

These are *candidate* closest sources; bibliographic metadata and specific technical overlaps require independent source checks before publication. No original theorem or empirical novelty is asserted here.

## Cloud-only execution gate

Before launching any job, document provider name, dated official quota/pricing documentation, account-specific entitlement, whether payment card is mandatory, public/private repository implications, minutes/CPU/RAM/timeout caps, and a hard no-billing stop condition. Do not treat a free-tier advertisement as account-specific availability. Prefer a tiny standard-library CI regression on verified free hosted runners before any hosted model evaluation. Never run workloads on the user's laptop, download large models, enable paid runners, or assume a spending alert prevents charges.

## November 22 decision

Release a public research paper only if: executed regression evidence exists; full prior-art audit is completed; independently adjudicated held-out cross-domain evidence supports a narrow defensible contribution; uncertainty and negative controls are reported; and AI assistance is disclosed as required. Otherwise publish a clearly labeled *preliminary methods note* or defer, with no invented results.
