# Protocol 122 — Sharp dependence bounds and robust decisions (2026-11-16)

Status: analytical protocol only; no code execution, empirical data, performance claim, or novelty claim.

## Identification without a dependence estimate

Let T∈{0,1} denote independently adjudicated truth, A,B∈{0,1} two verifier outputs, π=P(T=1), a_t=P(A=1|T=t), b_t=P(B=1|T=t), and q_t=P(A=1,B=1|T=t). Knowing both marginal verifier rates does **not** identify q_t. Probability nonnegativity gives the sharp Fréchet bounds:

L_t=max(0,a_t+b_t−1) ≤ q_t ≤ U_t=min(a_t,b_t).

The four conditional cells are (++):q_t, (+−):a_t−q_t, (−+):b_t−q_t, (−−):1−a_t−b_t+q_t. Every q_t in [L_t,U_t] yields a valid table, so the interval is sharp absent further assumptions.

For an observed ++, if D=πq_1+(1−π)q_0>0, P(T=1|++)=πq_1/D. With π∈(0,1), the posterior increases in q_1 and decreases in q_0, giving candidate sharp bounds

p_min = πL_1/[πL_1+(1−π)U_0],
p_max = πU_1/[πU_1+(1−π)L_0],

provided the respective denominators are positive. If a boundary produces D=0, the observation is impossible at that boundary; report undefined conditional probabilities and use limits over feasible positive-probability tables, not a fabricated posterior. A prior at 0 or 1 is degenerate and should be handled separately.

## Exact illustrative example

Take π=1/2 and both verifiers with sensitivity and specificity 4/5. Thus a_1=b_1=4/5 and a_0=b_0=1/5. The sharp intervals are q_1∈[3/5,4/5] and q_0∈[0,1/5]. Consequently the ++ posterior can range from (3/5)/[(3/5)+(1/5)]=3/4 to 1 (the upper endpoint uses q_0=0 and q_1>0). Conditional independence instead fixes q_1=16/25 and q_0=1/25, yielding 16/17. Perfect duplication fixes q_1=4/5 and q_0=1/5, yielding 4/5.

**Correction to interpretation:** the 80%-to-100% range previously explored along a particular dependence path is not the entire feasible range when the truth-conditional dependence parameters are allowed to vary independently. The sharp marginal-only range is **75%-to-100%**. This is a modeling distinction, not an empirical discovery.

## Robust decision gate

For each observed signal o, and each admissible pair of joint tables (q_0,q_1), calculate conditional expected loss for accept, reject and abstain with prespecified nonnegative loss matrix. Two distinct criteria must not be conflated:

1. *Posterior-robust action:* minimize worst-case conditional loss over feasible tables with P(o)>0. This conditions on the observed signal and is undefined if the event is impossible under all admissible tables.
2. *Ex-ante minimax verification policy:* enumerate all observation-contingent action policies and minimize worst-case **unconditional** expected loss over feasible joint tables, including verification cost. This correctly weights rare observations and is the primary robust-policy target.

For fixed policy, unconditional expected loss is affine in q_0 and q_1, so its maximum on the rectangular feasible set occurs at one of four corners. The ex-ante minimax policy can therefore be found by enumerating policies and evaluating the four corners. Compare against no verification, independence plug-in, and duplicate-verifier baselines under identical loss matrices. A robust improvement claim requires lower held-out realized loss, not merely a favorable synthetic minimax objective.

## Falsification and implementation checklist

- Check four cell probabilities sum exactly to one, are nonnegative, and reproduce both margins for each truth state.
- Confirm posterior bounds with independent exact-rational grid or endpoint enumeration; check impossible-event behavior.
- Enumerate 3^4=81 deterministic policies for the four joint binary observations; for each compute worst-case ex-ante loss at four rectangle corners. Include no-verification actions and any verification cost.
- Add randomized policies only as a separately specified extension: deterministic minimax may be strictly worse than mixed minimax in some games.
- Preregister truth adjudication, source-cluster-disjoint splits, dependence-model estimation, calibration metrics and loss matrices. Do not tune against held-out outcomes.
- Compare with existing partial-identification, robust Bayes, imprecise probability, correlated diagnostic testing and distributionally robust decision literature. These bounds and corner arguments are standard; no novelty assertion follows from them.
- For NLP, mathematics and physics, use provenance-tracked, independently adjudicated examples. Domain labels do not substitute for executed domain experiments.

## Resource and publication gate

No laptop computation. Do not dispatch cloud jobs until free eligibility, quotas, card/billing requirements and spend controls are verified for the actual account. November 22 is a conditional review date, not a promise of an empirical paper. If independent validation remains unexecuted, report a methods protocol only and explicitly disclose AI assistance as required.
