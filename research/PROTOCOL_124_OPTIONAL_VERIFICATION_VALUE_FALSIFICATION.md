# Protocol 124 — Robust verification value, optional acquisition, and deployment falsification (2026-11-16)

**Status:** Prespecified analytical protocol only. No cloud execution, empirical evaluation, or novelty claim.

## Decision-theoretic correction: robust verification is optional

Protocols 122–123 optimize decisions after acquiring a pair of verifier signals. That optimization is not equivalent to deciding whether to purchase the signals. For a fixed prior π, loss ℓ(t,a), verification fee k≥0, and conditional joint-likelihood uncertainty set Q, define

B = min_a [πℓ(1,a)+(1−π)ℓ(0,a)].

Let M = min_{x∈X} max_{q∈Q} Σ_{t,o,a} P(t)p_t(o;q_t)x(o,a)ℓ(t,a), where X contains all randomized policies over the four binary observation patterns. This **excludes** the acquisition cost. The robust optional-acquisition value is

V = B − min{B, k+M} = max{0, B−k−M}.

This is an ex-ante robust guarantee under the specified uncertainty set, **not** an estimate of empirical accuracy, a posterior probability, or a proof that the verifier improves held-out outcomes.

A crucial invariant: a signal-ignoring policy x(o,a)=1[a=a*] for every o, where a* attains B, is feasible. Hence M≤B. Nevertheless k+M may exceed B, in which case the rational optional decision is **not to verify**. Any implementation that reports negative optional verification value, or treats the verification-only risk as the overall optimum, fails.

## Information-set and timing audit

1. Nature selects the pair of conditional joint tables q∈Q **after** the policy is committed but **before** the random truth and observations are drawn. Nature does not choose a different q after seeing each realized observation. Otherwise the game and corner reduction change.
2. Policy randomization is private; the adversary observes the distribution x, not the realized random seed. An adversary observing realized actions would create a different objective.
3. Verification cost k is incurred only if signals are acquired. Abstention costs, if any, belong in ℓ and must not be silently identified with k.
4. Margins, prior, and loss are fixed known quantities in this idealized game. Estimation uncertainty, nonstationarity, and label noise are **not** captured by the Fréchet rectangle.
5. Robust minimax is not Bayesian expected utility under a probability distribution over q. Report both objectives separately if a prior over dependence structures is introduced.

## Independent validation gates

- Exact rational evaluator: for each t, enumerate the four joint cells from (a_t,b_t,q_t) and verify nonnegativity, unit mass, and the specified margins.
- At zero verification cost, check 0≤V≤B when losses are nonnegative; with increasing k, V must be nonincreasing and reach zero at k≥B−M.
- Compare the LP optimum M with direct 81-policy deterministic enumeration D. Assert M≤D≤B. Do not assert strict inequality unless a concrete independently verified counterexample is produced.
- At a zero-width dependence interval, compare LP with direct Bayes action selection per observation; both must match to solver tolerance.
- At prior π=0 or π=1, signal-independent optimal action must be sufficient when truth is known; any positive gross value of information is a failure.
- With an exactly duplicated second verifier, adding its report cannot improve gross value over the first when costs and admissible policies are otherwise identical.
- Compare no verification, single verifier, two-verifier independence plug-in, dependence-aware fitted Bayes, deterministic robust, and mixed robust **under the same loss matrix and signal-acquisition accounting**.
- A separate independently implemented solver or rational certificate is required before declaring a numerical optimum validated.

## Falsification for a cross-domain AI claim

The empirical hypothesis is not that Fréchet bounds or robust LPs are novel. It is that dependence-aware optional verification yields lower **held-out, cost-adjusted realized decision loss** than calibrated single-verifier, independence, and no-verification baselines across provenance-disjoint NLP, mathematical-reasoning, and physics claims.

Prespecify source-cluster splits, independent truth adjudication, confidence intervals clustered by source, calibrated margins, proper scoring rules, abstention losses, and cost sensitivity. Falsify the practical claim if gains vanish under held-out evaluation, if calibration or source leakage explains them, if adjudication is unreliable, or if acquisition costs erase the gains. A cross-domain headline requires actual cross-domain data; a synthetic fixture is not a physics experiment.

## Literature and novelty checklist

Before any originality claim, compare explicitly with: Blackwell's comparison of experiments and value of information; Wald's statistical decision theory; Fréchet–Hoeffding bounds; robust Bayes and imprecise probability; Gilboa–Schmeidler maxmin expected utility; correlated classifier ensembles; selective prediction; LLM-as-judge dependence and multi-agent debate evaluation. Verify exact bibliographic metadata and closest modern empirical studies from primary sources. These are candidate prior-art families, **not yet a completed literature review**.

## Execution and publication gate

All tests must run remotely only after confirming the *specific* cloud account's zero-cost eligibility, remaining quota, payment-card/billing exposure, and bounded workflow configuration. Public GitHub repository status is not proof of account-specific free capacity. No user laptop workloads, model downloads, or GPU training. The November 22 checkpoint permits a clearly labeled analytical methods draft if validation is incomplete; do not present unexecuted tests or synthetic arithmetic as empirical findings. Preserve source, solver versions, logs, and AI-assistance disclosures.
