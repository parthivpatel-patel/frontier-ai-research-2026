# Protocol 131 — Unequal-verifier dependence and external-validity gate

Status: **research specification only; no execution or empirical findings**. Date: 2026-11-16.

## Audit finding

Protocols 129–130 encode **identical conditional positive rates** for verifier 1 and verifier 2. Their joint function uses `(q, p-q, p-q, 1-2p+q)`, which enforces exchangeability. This is valid for the stipulated symmetric synthetic setting, but is **not a general model of two different AI verifiers**. It cannot directly support claims about heterogeneous models, modalities, or domains. The recent fix for nondefault sensitivity/specificity changes the common marginal of *both* verifiers, not their equality constraint.

## Correct heterogeneous joint law

For truth class `t`, let `a_t=P(Y1=+|t)`, `b_t=P(Y2=+|t)`, and `q_t=P(Y1=+,Y2=+|t)`. In outcome order `(++,+-,-+,--)` the joint vector is

`(q_t, a_t-q_t, b_t-q_t, 1-a_t-b_t+q_t)`.

Feasibility is equivalent to the sharp Fréchet bounds

`max(0,a_t+b_t-1) <= q_t <= min(a_t,b_t)`.

The two truth classes have independent admissible intervals; their Cartesian product has four corners. Expected risk for a fixed deterministic sequential policy is affine in `q_0,q_1`; therefore the maximum over the rectangular uncertainty set is attained at a corner. Enumerating the same 144 deterministic policies remains valid because the observation/action structure is unchanged. **Do not** assume that this establishes optimality over randomized policies.

For policy `(c_minus,c_plus)`, calculate the first signal `Y1` from the appropriate joint cell; if `c` stops, choose its action without consulting `Y2`. If `c` acquires, choose the terminal action based on `Y2` and pay fee once. Mix truth classes using the prior and use one common loss convention throughout.

## Required independent falsification fixtures

1. **Marginal reconstruction:** for nonexchangeable positive rates, e.g. `a_1=3/4,b_1=2/3,a_0=1/3,b_0=1/4`, check nonnegative cells, unit sums, and both marginals at all four corners.
2. **Reduction:** when `a_t=b_t` for both truth classes, heterogeneous risks must agree exactly with Protocol 129 for every policy and corner, not just at the optimum.
3. **Acquisition fee:** a policy acquiring only after `Y1=+` pays `fee * [prior*a_1 + (1-prior)*a_0]`, independent of verifier-2 accuracy and coupling.
4. **No peeking:** stop decisions are invariant to all possible changes in `Y2` conditional distributions preserving the `Y1` marginals.
5. **Minimax nesting:** the 144-policy optimum is no worse than either always-acquire or never-acquire optima, with identical uncertainty sets and losses.
6. **Zero-fee equality:** optimal deterministic sequential and always-acquire risks coincide when `fee=0`; an always-acquire policy can ignore `Y2`.
7. **Adversarial interior points:** compare the four-corner maximum to several exact-rational interior points; no interior point can exceed it.
8. **Independent implementation:** compare against a second oracle written from the probability table directly, not calling Protocol 129's risk helper.

A failure blocks any empirical or paper claim derived from the implementation. A passing fixture verifies only these finite synthetic properties, not AI reliability.

## Empirical design and prior-art novelty gate

Before any claim of new research, compare against established Blackwell information ordering, robust Bayes/minimax decisions, Fréchet-Hoeffding bounds, selective classification, sequential testing, and dependence-aware ensemble calibration. These mathematical components are established; **no novel theorem is claimed**.

For each NLP, mathematics, and physics benchmark, pre-register claim-level ground truth and adjudication, model and prompt versions, data provenance, leakage and near-duplicate checks, verifier-specific sensitivity/specificity estimated from a disjoint calibration set, uncertainty intervals, cost in verification calls, and held-out decision loss. Baselines must include no verification, single verifier, fixed two-verifier acquisition, independence-assuming fusion, and an adaptive baseline. Include paired confidence intervals and abstention coverage, and report negative results. Do not conflate mathematics/physics word-problem QA with experimentally validated physical discovery.

**Primary falsification:** no statistically defensible held-out reduction in decision loss versus the strongest feasible baseline, or gains disappearing after leakage, calibration, multiple-comparison, or verifier-dependence sensitivity checks. In that case present a methods/negative-results note, not a novel performance paper.

## Compute and integrity gate

No local execution or model downloads. Cloud execution only after confirming a standard free hosted runner, account-level spending restrictions and any card/billing conditions. Never select larger paid runners or external inference APIs without approval. A theoretical specification or committed source is not a completed experiment. Preserve provenance and disclose AI assistance as required by the publication venue.

**November 22, 2026 is a conditional checkpoint, not a guaranteed publication deadline.**
