# Protocol 147 — Labelled Risk Certification and Adaptive Selection Gate (2026-11-17)

## Status and scope
This is a theoretical design and preregistration aid, **not** an executed experiment, empirical certificate, or originality claim. It follows the observational nonidentifiability witness in Protocols 145–146. The objective is to specify precisely what independent truth labels can certify under a bounded-loss assumption, and where adaptive policy selection invalidates naive claims.

## A finite-sample certificate for one frozen policy
Let a policy \(\pi\) (including its prompts, verifier identities, thresholds, randomization and abstention logic) be fixed **before** an independent evaluation sample. Let \(Z_i=(X_i,Y_i,\ldots)\), \(i=1,\ldots,n\), be iid observations from a declared target distribution, with independently adjudicated truth labels \(Y_i\). Suppose the full per-item decision loss \(L_\pi(Z_i)\in[0,M]\), including any declared abstention penalty, is observed and measurable. Then for \(\delta\in(0,1)\), Hoeffding's inequality gives

\[
\Pr\left\{\mathbb E L_\pi > \widehat R_\pi + M\sqrt{\frac{\log(1/\delta)}{2n}}\right\}\le\delta,
\qquad \widehat R_\pi=\frac1n\sum_{i=1}^n L_\pi(Z_i).
\]

If the synthetic loss in Protocol 145 is used, \(M=2\). This is an **upper confidence bound on average risk for the specified target distribution**, not an adversarial distribution-shift certificate, not conditional/selective risk control, and not a guarantee on each individual decision.

For \(n=100\) and \(\delta=0.05\), the additive radius is \(2\sqrt{\log(20)/200}\), approximately 0.245; for \(n=1000\), approximately 0.0774. These are illustrative calculations, not measured performance. If observations share a source, benchmark template, or underlying problem, treating all prompts as iid may invalidate the bound.

## Policy selection and multiple comparisons
If \(K\) **predeclared** policies are all evaluated on the same iid labelled sample, simultaneous one-sided bounds follow by a union bound with radius \(M\sqrt{\log(K/\delta)/(2n)}\). A post-hoc search over an unrestricted policy family is **not** covered by substituting an arbitrary observed K. Preferred design: separate source-disjoint policy-development and final evaluation sets; freeze the chosen policy and uncertainty set before touching final labels. If policy tuning and risk calibration reuse data, use an explicitly justified uniform-convergence, selective-inference, or conformal risk-control procedure; do not report a naive single-policy interval.

## Label quality, selection, and shift
The bound applies to losses computed from valid labels, not merely agreement between two AI verifiers. Adjudicators must be independent of the candidate verifiers and blinded where feasible. Track unknown/ambiguous truths separately; do not silently count them as correct. Missing labels, nonrandom evaluation selection, benchmark contamination, and domain shift can all defeat nominal coverage. A bound calibrated on a convenience sample must not be called deployment-certified.

For domain-specific evaluation: NLP tasks need independently sourced factual or entailment evidence; mathematics needs checked proofs or reference solutions; physics needs dimensionally and physically validated solutions with explicit modeling assumptions. Record source provenance and possible training-data overlap. If ground truth cannot be established, designate that item unscorable rather than fabricating certainty.

## Falsification and release gates
1. Verify exact-rational Protocol 146 fixtures in a trusted **zero-charge cloud** runner and capture runner image, command, exit code, collected tests, SHA and logs.
2. Demonstrate at least one independently implemented oracle agreeing with each analytic witness; report discrepancies, not only passing assertions.
3. Predeclare primary loss, coverage, cost, uncertainty assumptions, policy family, sample unit, and confidence level.
4. Withhold any finite-sample certificate if final labels influence policy selection, sample independence fails, loss is unbounded, or source overlap is detected without an appropriate corrected analysis.
5. Compare budget/coverage-matched baselines; withdraw any performance claim that vanishes under these controls.
6. Do not claim methodological novelty until theorem-level comparison with classical partial identification, Dawid–Skene, robust sequential testing, selective classification, conformal risk control, and recent AI verification papers is complete.

## Compute and integrity
No cloud execution is authorized merely by this memo. Before launching GitHub Actions or any other provider, verify account-specific free quota, spending limits, card/billing requirements, and availability. Do not use the user's laptop for computation. No results, cloud runs, or spending are claimed here. The November 22 publication target remains conditional.
