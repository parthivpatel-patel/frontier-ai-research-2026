# Protocol 051 — Observation Semantics, Identification Assumptions, and Negative Controls

Date: 2026-11-12. Status: methodological audit, **not** experimental evidence.

## Critical terminology correction

In the current exact-arithmetic fixtures, `q = P(V1=1,V2=1)` is the **joint-positive frequency**, not the total verifier agreement rate. Total agreement is `P(V1=V2)=P(++)+P(--)`. They are not interchangeable. All manuscripts, plots, and benchmarks must explicitly name the observed statistic. This audit corrects the interpretation of Protocols 049–050 wherever "agreement" might imply both-positive and both-negative outcomes combined.

## Identification contract

Let `Y` be binary truth, `V1,V2` binary verifier outputs, `pi=P(Y=1)`, `s_i=P(V_i=1|Y=1)`, and `f_i=P(V_i=1|Y=0)`. Define `a=P(++|Y=1)`, `b=P(++|Y=0)`. Fréchet constraints give
`max(0,s1+s2-1) <= a <= min(s1,s2)` and analogously for `b` using `f1,f2`.
If `q=P(++)>0` is known in the **same target population**, then `q=pi*a+(1-pi)*b` and the posterior is `P(Y=1|++)=pi*a/q`. Intersecting this equality with the feasible rectangle yields sharp bounds under exactly these assumptions. Sharpness means attainable by some joint distributions, **not** that the intervals are narrow, causal, or calibrated on shifted data.

The supplied `pi,s_i,f_i` are typically unknown in unlabeled deployment. Treating them as known is an oracle experiment; an operational method must estimate them from labeled data and propagate uncertainty. If the estimates were fitted on test labels, reported coverage is invalid.

## Two separate observational regimes

**Regime A: labeled calibration data.** Estimate prevalence, conditional verifier marginals, and dependence using claim-family-disjoint calibration folds. Assess uncertainty from clustered source/claim components; evaluate on untouched target components.

**Regime B: unlabeled deployment.** Joint-positive frequency can be observed, but prevalence and conditional error rates are generally not identified without additional transport assumptions. Do not claim target posterior guarantees from `q` alone. A deliberately shifted target with identical `q` but different `P(Y=1|++)` is a mandatory negative control.

## Falsification and evaluation gates

1. **Terminology unit test:** Construct two joint distributions with equal `P(++)` but unequal `P(V1=V2)`; reject any implementation that equates the two.
2. **Oracle mathematical test:** Compare exact-rational interval implementation with independent geometric vertices over feasible and infeasible configurations. Passing validates code consistency, not scientific novelty.
3. **Coverage test:** For synthetic distributions sampled *within explicitly specified uncertainty sets*, check whether truth lies in derived intervals; test deliberately violated transport assumptions separately and expect coverage failure.
4. **Operational calibration:** Compare to constant prior, single-verifier, majority vote, duplicate-collapse, logistic stacking, isotonic/Platt calibration, conformal/selective prediction, and lineage-aware ablations. Report risk–coverage curves, Brier score, ECE with binning details, and confidence intervals.
5. **Leakage:** Split connected components of paraphrased claims, shared evidence, shared source families, and derived synthetic templates; log components and overlap checks before fitting.
6. **Null result:** If lineage-aware methods do not beat simpler baselines on held-out components with uncertainty quantified, report that finding and do not claim improvement.
7. **Failure to identify:** If interval width is too broad to support nontrivial selective decisions at a prespecified risk threshold, report the abstention rate and do not imply a usable verifier.

## Mathematics/physics integration without invented novelty

Evaluate domain-labeled claims from mathematics and physics only after licensing, truth-label provenance, and claim-equivalence checks. Distinguish formal proofs from empirical physical claims: evidence quality, independence, and ground truth are different. No claim of a new physical law or theoretical novelty is justified by these probability bounds.

## Prior-art audit queue (not yet exhaustively verified)

Review Fréchet–Hoeffding bounds; latent-class diagnostic testing with conditional dependence; Dawid–Skene-style annotator reliability; conformal risk control and conformal factuality; selective classification and risk–coverage; correlated ensemble calibration; dataset leakage via semantic duplicates. For each candidate contribution, record exact theorem/assumptions, method, code, license, benchmark and explicit distinction. Until this comparison is completed, label the project a hypothesis.

## Reproducibility and zero-cost execution gate

The existing `research/fixtures/exact_dependence_checks.py` and `test_geometric_oracle.py` are committed but not confirmed executed. Do **not** claim passing tests. Before running GitHub Actions, verify repository visibility, standard-runner eligibility, repository Actions settings, organization/account billing policy, spending controls, and availability. Avoid larger/self-hosted/paid runners, external APIs, model downloads, and all local laptop execution. If account-specific controls cannot be confirmed, leave execution blocked. Record runner image, workflow URL, commit SHA, exit code and stdout/stderr for any permitted run. Zero dollars is a hard constraint, not an expected average.

## Publication gate

A November 22, 2026 submission is conditional on independent code execution, a reproducible non-leaking evaluation, defensible comparison with closest prior art, and clear AI-assistance/disclosure statements as required by the venue. No novelty or empirical result is asserted in this document.
