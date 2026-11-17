# Protocol 136 — Behavioral randomization equivalence and audit of adversary timing

Status: theoretical derivation and test specification, **not executed empirical evidence**. 2026-11-17.

## Why this matters

Protocol 135 proposes randomizing over 144 complete deterministic sequential policies. A solver may instead randomize separately at each observable decision node. These are equivalent for the distribution of terminal outcomes **provided the randomization is sampled independently of truth, verifier outputs, and the adversary's coupling, and the adversary cannot condition its choice on the realized random seed**. This equivalence is a property of finite perfect-recall decision problems; it is not an original theorem. It must not be mistaken for evidence of better AI verification.

## Exact policy count and behavioral parametrization

After observing first binary output i in {0,1}, a deterministic policy has 12 choices: three terminal actions, or acquire verifier 2 and choose one of three actions for each of its two possible outputs (3^2=9). Hence 12^2=144 deterministic policies. For randomized policies define for each i: three probabilities s[i,a] of stopping with action a, and nine probabilities h[i,a0,a1] of acquiring then using the specified contingent terminal actions. Each row sums to one. This behavioral form can represent the same terminal distribution as an ex-ante mixture over complete policies by drawing all contingent decisions before any observations. Conversely a mixture over complete policies induces conditional behavioral distributions at each reachable information set; correlation among choices at mutually exclusive nodes cannot affect terminal risk.

**Caution:** a simplified factorization into 'acquire probability' and independent terminal-action distributions is adequate for expected risk only when its conditional distributions correctly preserve the mixture and randomization cannot be revealed to the adversary. In particular, a randomized seed observed by the adversary *before* choosing a coupling changes the objective to E_p[max_c L(p,c)], which can exceed max_c E_p[L(p,c)]. The Protocol 135 LP models the latter, not the former.

## Analytical identity and falsification

For any policy mixture x over P and fixed corner c, linearity of expectation gives R(x,c)=sum_p x[p] L[p,c]. Consequently

    max_c sum_p x[p] L[p,c] <= sum_p x[p] max_c L[p,c].

The inequality can be strict. An implementation that samples p and then reports the average of each policy's own worst-case risk is evaluating the right side, **not** the precommitted mixed minimax objective.

Toy counterexample: L(A,c1)=0, L(A,c2)=1; L(B,c1)=1, L(B,c2)=0. A fair mixture has worst-case loss 1/2 when the adversary chooses c without observing the realized policy, but expected policy-specific worst-case loss 1 if the adversary observes each draw. This toy is an optimization sanity check only.

## Regression requirements

1. Enumerate all 144 complete policies independently; assert 9 never acquire, 81 always acquire and 54 conditionally acquire.
2. For each exact-rational test mixture, compute all four corner risks both by mixing complete-policy losses and by a separately implemented outcome-tree enumerator. Compare exactly.
3. Check a nontrivial mixture, including off-diagonal corners and unequal verifier marginals, where risk is sensitive to dependence.
4. Test both adversary timings explicitly: hidden policy draw (max of mixed risks) and revealed policy draw (mixture of per-policy maxima). Assert the latter is never smaller; use the 2x2 toy to force a strict gap.
5. Test seed independence and nonanticipation: a stopping decision may depend only on the first output; acquisition cost is paid only on acquisition paths.
6. Verify corner sufficiency only for the declared rectangular coupling uncertainty set. Do not silently extend it to nonrectangular uncertainty, learned coupling sets, or adaptive adversaries.
7. Compare the LP optimum with the deterministic optimum and an independently solved dual; do not claim a strict randomized gain unless actually observed in executed tests.

## Relevance to the empirical paper

If a system selects a verifier policy using a public deterministic seed, the hidden-draw minimax guarantee may not describe its threat model. Report both seed visibility and the adversary's knowledge. In real-world NLP, mathematics and physics evaluations, distinguish uncertainty over a fixed population distribution from a strategic adversary that can select examples after seeing the policy. Neither the toy matrix nor synthetic couplings establishes calibrated performance on language models.

## Publication and compute gate

Closest mathematical prior art includes finite zero-sum minimax games, behavioral versus mixed strategies in perfect-recall extensive-form games (Kuhn's theorem), and robust sequential decision making. Cite original bibliographic sources after verification; do not claim these identities as novel. Keep the candidate novelty restricted to an empirically demonstrated, source-disjoint and budget-matched application, if any. All execution requires independently verified free cloud entitlement and zero-charge billing controls. No laptop computation, local inference, or paid resources.
