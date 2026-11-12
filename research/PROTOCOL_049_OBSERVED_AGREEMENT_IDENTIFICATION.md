# Protocol 049 — Observable agreement tightens dependence bounds

Date: 2026-11-12. Status: analytic protocol; no experiment executed; no novelty claim.

## Question and correction

Protocol 048 conditions on two positive verifier votes using only class-conditional marginal rates. In a labeled calibration population, the **unconditional frequency of joint positives** may also be observable. Ignoring that measurement unnecessarily widens the identified set. Conversely, an empirical joint-positive frequency is *not* automatically transportable to a new population, especially after prevalence or dependence shifts.

Let Y in {0,1}, pi=P(Y=1), s_i=P(V_i=1|Y=1), f_i=P(V_i=1|Y=0). Write a=P(V1=V2=1|Y=1), b=P(V1=V2=1|Y=0), and q=P(V1=V2=1).

Frechet bounds for unequal marginals:
A_lo=max(0,s1+s2-1), A_hi=min(s1,s2);
B_lo=max(0,f1+f2-1), B_hi=min(f1,f2).
The total-probability constraint is q=pi*a+(1-pi)*b.

If 0<pi<1 and q>0, feasible a must satisfy
a_lo=max(A_lo,(q-(1-pi)*B_hi)/pi)
a_hi=min(A_hi,(q-(1-pi)*B_lo)/pi).
If a_lo>a_hi, the asserted inputs are incompatible: reject rather than clip or report a confidence interval. For feasible inputs, the sharp posterior interval is
[P(Y=1|++)_lo,P(Y=1|++)_hi]=[pi*a_lo/q,pi*a_hi/q].
Proof: each class-conditional 2x2 table exists for any joint-positive probability inside its Frechet interval; choose a at either endpoint, set b=(q-pi*a)/(1-pi), and construct both tables. All constraints hold. This is elementary partial identification, not a new theorem.

**Worked mathematical illustration, not model evidence:** pi=0.5, s1=s2=0.8, f1=f2=0.2. Without q, Protocol 048 gives [0.75,1]. If q=0.4, a must lie in [0.6,0.8], b=0.8-a in [0,0.2], and the posterior lies in [0.75,1] (no improvement). If q=0.34, a lies in [0.6,0.68], b=0.68-a in [0,0.08], and the posterior lies in [0.88235294,1]. If q=0.5, a in [0.8,0.8], b=0.2, posterior exactly 0.8. Thus *some* observed agreement rates tighten bounds and others do not.

## Critical transportability warning

If pi, s_i, f_i or q are estimated, plug-in sharp bounds do not have finite-sample coverage guarantees. Quantify uncertainty in each input using preregistered confidence sets; optimize posterior over the joint feasible parameter region, not independent point estimates. If the evaluation distribution can change, q from training is not necessarily valid. Report in-distribution and shifted scenarios separately; do not claim robust guarantees from empirical calibration alone.

## Falsifiable implementation checks

1. Verify unequal-marginal Frechet bounds against exhaustive binary 2x2 tables on a rational grid.
2. Check infeasible q rejects, zero-probability conditioning rejects, and pi in {0,1} is handled separately.
3. Check analytic endpoints against a grid-search oracle with numerical tolerance declared before execution.
4. Compare no-q intervals, observed-q intervals, vote-only calibration, and duplicate collapse. Record whether agreement constraints actually improve useful coverage at fixed selective risk.
5. Split claims and observation lineages into connected components before fitting or tuning. Never use test-set q to calibrate a test prediction.
6. For scientific NLP applications, distinguish semantic claim equivalence from mere lexical overlap; audit false merges and missed paraphrases manually on a small, held-out sample.
7. Run only after account-specific public-repository standard-runner, Actions permission, and billing/card checks; never use paid runners, local laptop computation, external model APIs, or GPU downloads.

## Prior art and novelty gate

These are standard Fréchet-Hoeffding constraints plus the law of total probability. Search literature on partial identification with known margins, dependent diagnostic tests, latent-class diagnostic models, ensemble calibration, and selective prediction before asserting any original method. The research contribution, if any, must be a reproducible *empirical or methodological* advance in claim-provenance-conditioned calibration under verified shifts, not these bounds.

Potential failure: q may add no useful information, be unstable across domains, or be too noisy to support practical abstention. Publish negative results accurately. AI-assisted development and writing must be disclosed according to venue rules. Nov 22 publication is conditional on evidence.
