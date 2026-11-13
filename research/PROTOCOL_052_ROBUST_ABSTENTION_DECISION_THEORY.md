# Protocol 052 — Decision-theoretic abstention under partially identified verifier reliability

Status: analytical research design, **not** an established novel result or empirical finding. 2026-11-12 (US Eastern).

## Scope and observation semantics

Let (Y\in\{0,1\}) denote claim truth and (V_1,V_2\in\{0,1\}) two binary verifier decisions. Condition on the event (E=\{V_1=1,V_2=1\}), not the different event (V_1=V_2). Suppose the identification analysis yields a sharp interval (p=P(Y=1\mid E)\in[L,U]), with (0\le L\le U\le1). If the target distribution, label prevalence, or verifier error rates are not transportable, even this interval may be unjustified; the correct response is to widen it or declare the decision unidentified.

## Robust decision rule and proof

Consider three possible actions: **accept** the claim, **reject** it, or **abstain**. Let a false acceptance cost (C_{FP}>0), a false rejection cost (C_{FN}>0), and an abstention cost (C_A\ge0), all expressed in the same units. Correct decisions have zero loss.

For a fixed (p), the conditional expected losses are:
- (R_{accept}(p)=C_{FP}(1-p));
- (R_{reject}(p)=C_{FN}p);
- (R_{abstain}(p)=C_A).

Their worst cases over the identified set ([L,U]) are respectively
(C_{FP}(1-L)), (C_{FN}U), and (C_A). This follows from the first loss decreasing in (p), the second increasing in (p), and the third constant. Therefore a deterministic minimax rule selects an action with the smallest of these three quantities. State a tie-breaking policy in advance (default: abstain on ties involving abstention). This is elementary robust Bayes decision theory, not a novel theorem.

Example (purely synthetic): (L=3/4,U=1,C_{FP}=4,C_{FN}=1,C_A=1/5). Worst-case risks are 1, 1, and 1/5; abstention is minimax. At (C_A=2), accept and reject tie at worst-case risk 1; abstention is not preferred. Reporting a single confidence estimate would obscure this cost-sensitive distinction.

**Caution:** Minimizing maximum expected loss over the identified set is not equivalent to establishing frequentist error guarantees for a deployed selective classifier. Nor does it justify an unconditional safety guarantee: the interval pertains only to the specified conditioning event and population.

## Falsifiable empirical hypotheses

H1: On held-out claim-equivalence and evidence-lineage connected components, an interval-aware decision rule has lower pre-registered cost-weighted loss than a calibrated point-estimate rule, with abstention rates matched or reported on a risk-coverage curve.

H2: Under controlled dependence shift, interval-aware risk estimates maintain nominal coverage more often than independence-assuming confidence estimates. Evaluate both joint-positive and all four verifier-output cells; report when identification intervals become vacuous.

H3 (negative control): With correctly specified conditional independence, the interval method should not be credited for improvements that disappear against an equally calibrated, cost-matched independence baseline.

Reject any claimed advantage if confidence intervals include no improvement, if the effect reverses across reasonable cost ratios, if claim-family leakage is found, or if selective coverage collapses. Report negative findings. Bootstrap over independent claim/evidence-lineage clusters, not individual repeated citations. Calibrate on a disjoint development set; do not tune costs, thresholds, or model selection on the final test set.

## Reproducibility and execution gate

A minimal exact-arithmetic standard-library unit test can check the three risk formulas, monotonicity, tie policy, and boundary cases (L=U), (L=0,U=1). A later benchmark must publish dataset provenance, truth labels, dependency-group assignments, fixed seeds, environment lockfile, baseline hyperparameters, cost grid, calibration plots, abstention rates, and all failed runs. No model weights or heavy downloads should run on the user's laptop.

**Strict zero-cost gate:** Do not start GitHub Actions or another cloud job until account/repository billing controls, standard-runner eligibility, permissions, and currently available free quota are independently confirmed. Do not use larger or paid runners; no credit card or paid upgrade. If those checks are unavailable, keep tests unexecuted and say so.

## Prior art and novelty boundary

The decision rule above is a straightforward instance of classical statistical decision theory with a reject option and robust/minimax inference. Relevant established areas include Chow's reject-option classification (1970), selective classification/risk-coverage analysis, imprecise probabilities, partial identification, and distributionally robust optimization. This document makes **no** claim that these concepts are original. A publishable contribution requires a demonstrably new estimator, bound, or scientifically useful experimental result beyond these baselines, verified against the closest primary literature. Physics analogies must not be represented as physical laws without a separately testable physical model.

## Publication integrity

Distinguish analytical examples from actual model evaluations; disclose AI assistance as required by the target venue. The November 22, 2026 internal date is a checkpoint, not a promise to publish unsupported conclusions.
