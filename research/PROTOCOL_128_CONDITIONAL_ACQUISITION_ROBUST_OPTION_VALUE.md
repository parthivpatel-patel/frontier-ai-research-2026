# Protocol 128 — Conditional verification acquisition and robust option value (2026-11-16)

**Status:** Analytical specification; no regression execution, empirical validation, or novelty claim. This work is separate from all other projects.

## Motivation and correction

Protocols 124–127 model a fee for acquiring a second verifier *unconditionally*. A realistic sequential verifier can inspect the first report, then decide whether to pay for the second. This conditional option changes both expected cost and the admissible policy class. It must not be conflated with the unconditional decision rule.

Let truth T in {0,1}, first signal Y1 in {+,-}, second Y2 in {+,-}, and a common ambiguity set Q of conditional joint laws with fixed first-signal marginals. A sequential deterministic policy specifies (i) whether to acquire Y2 for each Y1 outcome, and (ii) a terminal action in {accept,reject,abstain} at each reached information state. Its expected loss for q is

R(pi,q) = sum_t P(t) sum_{y1,y2} q(y1,y2|t) L(a_pi(y1,y2),t) + k sum_t P(t) sum_{y1} q(y1|t) I[acquire_pi(y1)].

If Y2 is not acquired at y1, the terminal action must be identical for both possible y2. The acquisition fee k is paid only on paths where acquisition occurs. The robust objective is min_pi max_{q in Q} R(pi,q). With fixed Y1 marginals, the expected acquisition fee is identical across q for any fixed acquisition rule; this ceases to hold when first-signal marginals themselves are uncertain.

## Exhaustive finite-policy oracle

For each first-signal outcome, choose one of three stop actions, or choose to acquire and then select one of 3^2 terminal action pairs. Thus there are (3+9)^2 = **144 deterministic sequential policies**. They include:
- 9 first-verifier-only policies (never acquire);
- 81 full-two-verifier policies (always acquire);
- 27 policies acquiring only after +;
- 27 policies acquiring only after -.

For the fixed-marginal two-verifier model of Protocol 122, evaluate each policy's loss at all four joint-coupling corners (two endpoints for T=1, two for T=0). The loss is affine in the two coupling parameters; therefore its maximum over their rectangular uncertainty set occurs at a corner. This is a mathematical property of this stipulated model, not an empirical result.

For each prior in {0,1/4,1/2,3/4,1}, each nonnegative fee in {0,1/20,1/4,1}, and both symmetric and asymmetric loss tables, calculate:
- the minimax risk of never acquiring Y2;
- the minimax risk of always acquiring Y2, including k;
- the minimax risk across all 144 sequential policies.

Assert **sequential optimum <= min(never, always)** under exactly the same Q, prior and loss. At k=0, always-acquire weakly dominates by policy embedding, so sequential optimum equals the always-acquire optimum. At k>0, do **not** assert a strict conditional-acquisition improvement without an independently computed witness.

## Falsification and implementation traps

1. The cost must be charged only on acquisition paths, not on all claims.
2. A policy that stops after Y1 must not condition its terminal action on unseen Y2.
3. Conditional acquisition probability must be computed using the marginal distribution of Y1, not the joint ++ cell.
4. All strategies must use the **same** ambiguity set Q and loss; otherwise the option-value inequality need not apply.
5. Zero-probability reports contribute zero ex-ante risk; no posterior is claimed for them.
6. Compare a separately implemented 144-policy enumerator to the existing 81-policy oracle; do not use one function to validate itself.
7. If randomization is allowed, the 144 deterministic enumeration is not automatically the mixed minimax solution; solve a separate finite zero-sum game/LP with a verified solver.
8. For actual LLM verifiers, source dependence, prompt leakage, correlated failures, latency, and calibration uncertainty must be measured on adjudicated held-out claims.

## Prior art and novelty boundary

The general ability to condition information acquisition on observed evidence belongs to established sequential decision theory, Bayesian experimental design, and value-of-information research. Blackwell (1953), *Equivalent Comparisons of Experiments*, DOI 10.1214/aoms/1177729032, provides foundational information-ordering context; it is not a claim that Blackwell invented this particular sequential formulation. The proposed 144-policy oracle is a small finite verification fixture, **not a new theorem**. A substantive AI contribution would require a verified source-disjoint empirical advantage against adaptive verification, confidence-based abstention, independent-verifier, and calibration baselines, with uncertainty intervals and transparent failure cases.

## Zero-cost remote execution gate

Use only a verified free standard GitHub-hosted runner in this public repository, with read-only permissions, a short timeout, Python standard library only, no downloads/caches/artifacts, and no paid services. The published code and tests remain **unexecuted** until account-specific permissions, current free eligibility, and billing controls are checked. No laptop workload, paid compute, or card enrollment is authorized.

## November 22 checkpoint

If independent execution and held-out cross-domain evaluation are unavailable, publish only an accurately labeled theoretical/methodological preprint or reproducible research protocol, not a claimed experimental breakthrough. Disclose AI assistance and distinguish conjectures, analytical identities, and measured results.
