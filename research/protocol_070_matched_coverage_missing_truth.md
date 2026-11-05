# Protocol 070 — Matched-coverage inference with unresolved physical truth

Date: 2026-11-05. Status: mathematical design, not empirical validation.

## Research question

Do assumption-explicit physical certificates reduce the probability of accepting physically unsafe AI-generated claims relative to strong verification baselines **at the same coverage**, on source-disjoint physics problems?

This is a falsifiable hypothesis, not an established novelty claim. Existing work in selective classification, partial identification, conformal risk control, proof checking, and physics reasoning benchmarks is relevant and must be compared before any priority claim.

## Estimands and bounds

For each evaluation claim i, let a_i and b_i be fixed binary acceptance decisions for two verification policies, and let y_i=1 indicate an independently adjudicated physically unsafe claim. y_i is either 0, 1, or unresolved. The paired unsafe-acceptance difference on the *full* fixed evaluation set is

D = (1/N) sum_i (a_i - b_i) y_i.

For adjudicated claims, contributions are observed. For unresolved claims, define d_i=a_i-b_i. The **sharp** identification interval, assuming no restrictions beyond 0<=y_i<=1, is

L = [sum_known d_i y_i + sum_unknown min(0,d_i)] / N,
U = [sum_known d_i y_i + sum_unknown max(0,d_i)] / N.

Sharpness follows by choosing y_i=1 for each negative d_i to attain L, and y_i=1 for each positive d_i to attain U. This uses the *same* latent y_i for both verifiers, avoiding the unnecessarily wide interval obtained by bounding their unsafe rates separately. If a_i=b_i, an unresolved y_i cancels exactly. This is elementary partial identification, not a new mathematical theorem.

Interpretation: D<0 favors A (fewer unsafe acceptances). A safety improvement is **identified** only when U<0. If 0 lies in [L,U], the available labels do not identify the sign, regardless of bootstrap confidence intervals. Sampling uncertainty must be evaluated separately.

## Matched coverage and selection

Let c_A=N^{-1}sum a_i and c_B=N^{-1}sum b_i. Compare policies only at predeclared common coverage c (or an explicitly reported tolerance). Thresholds must be chosen on a development set, then frozen before evaluating the held-out test set. If exact coverage is unattainable because scores tie, report achievable coverage and deterministic tie-breaking; do not choose thresholds based on test truth labels.

Equal coverage implies sum_i d_i=0 but does NOT imply D=0, since safety depends on the association between acceptance and truth. A low overall unsafe acceptance count obtained merely by abstaining more is not evidence of a better verifier.

A counterexample: A accepts only claim 1 and B only claim 2, so both have 50% coverage. If claim 1 is unsafe and claim 2 safe, D=+1/2: A is worse despite equal coverage. If both truths are unresolved, the sharp interval is [-1/2,+1/2], so the sign is not identified.

## Audit of independence and leakage

1. Freeze source-family assignments before tuning. Variants, translations, and perturbations of one physical problem belong to the same family.
2. Separate generator, verifier, and adjudicator roles. Model self-assessment is not independent truth.
3. Store problem source, physical regime, units, boundary conditions, assumed idealizations, claim, certificate, adjudication method, reviewer identity/provenance, and unresolved reasons.
4. Blind adjudicators to verifier decisions when feasible. Adjudicate a precommitted random sample of rejected and accepted claims to reduce verification-selection bias.
5. Include deliberately invalid assumptions, formally valid but inapplicable derivations, unit errors, and underspecified boundary conditions.
6. Preserve raw predictions and abstentions; never silently discard unresolved truth or failed generations.
7. Report subgroup results by physics domain and source family, and confidence intervals that respect source-family clustering.

## Competitive baselines

Compare: (i) unverified answer confidence, (ii) direct LLM critique, (iii) independent LLM verifier, (iv) symbolic/unit/constraint checks, and (v) assumption-explicit certificate verifier. Match evaluation inputs, access to tools, and test coverage. Any model API use must be explicitly authorized and verified to cost $0 before execution.

## Falsification and publication gates

- Reject a superiority claim if the safety difference is nonnegative or its uncertainty/partial-identification interval includes zero.
- Reject a generalization claim if an advantage disappears on held-out source families or independently constructed perturbations.
- Reject a physical-soundness claim if certificate validity is systematically confused with truth under physical assumptions.
- If independent adjudication is insufficient, report identification intervals and label the comparison inconclusive.
- Do not report software regression tests as empirical physics reasoning performance.
- Before a paper claims novelty, complete a dated closest-prior-art table with exact citations and distinct contributions.

## Execution safeguards

No laptop compute. Do not start cloud jobs until the public-runner eligibility, account-specific quota/billing state, workflow permissions, and zero-charge conditions have been checked. Public GitHub-hosted standard runners may be eligible for free usage, but eligibility alone does not establish the account-specific state. No paid runner, external model API, GPU rental, or credit-card signup is authorized.

## Immediate next artifacts

1. Add executable tests for the interval endpoints, shared unknown truth cancellation, and matched-coverage counterexample.
2. Obtain genuinely independent physics truth labels with explicit evidence, not invented benchmark outcomes.
3. Run tests on confirmed free cloud only, archive job URLs and immutable commit SHAs.
4. Write the empirical paper only if evidence supports its claims; otherwise publish methods and negative findings transparently.
