# Protocol 112 — Noisy verification and decision-value stress test

Status: exact hand derivation and proposed falsification protocol; **not an executed experiment**. Prepared 2026-11-15. Independent of all other projects.

## Why this matters

Protocols 106–111 use exact-rational optimization with a joint distribution over true claims. Their synthetic verification abstraction must not be interpreted as evidence that real NLP, mathematics, or physics verifiers reveal truth perfectly. This protocol provides a minimal exact counterexample in which the perfect-observation abstraction materially overstates the value of verification.

## Exact binary example (analytical, not empirical)

Let hidden claim truth T be Bernoulli(1/2). A verifier returns Y in {positive, negative} with sensitivity P(Y=positive | T=true)=4/5 and specificity P(Y=negative | T=false)=4/5. Conditional error rates are symmetric, and the prior is balanced.

Bayes' rule yields P(Y=positive)=1/2, P(T=true | Y=positive)=4/5, and P(T=true | Y=negative)=1/5. Thus an observed positive is **not** a truth certificate. The Bayes-optimal decision given either observation still has error probability 1/5.

Define terminal actions ACCEPT, REJECT, ABSTAIN. Wrong ACCEPT or REJECT incurs loss 1, correct classification loss 0, and ABSTAIN incurs loss 1/4. The optimal loss for posterior p is L*(p)=min(p, 1-p, 1/4). Before observing, L*(1/2)=1/4 (abstain). After observing Y, the optimal action is ACCEPT for positive and REJECT for negative, with conditional loss 1/5 each; expected posterior loss is 1/5. Hence the **gross expected decision value** of this noisy verification is 1/4 - 1/5 = **1/20**.

If the same test were incorrectly modeled as perfectly revealing T, its expected posterior loss would be 0 and its alleged gross value would be 1/4 — a **fivefold overstatement**. For a verification cost of 1/10 in the same loss units, the true net value is 1/20 - 1/10 = **-1/20**, whereas the perfect-revelation model predicts 1/4 - 1/10 = **3/20**. Thus the incorrect observation model reverses the test/no-test recommendation. These are stipulated rational inputs, not measured verifier characteristics.

## Required implementation extension

1. Introduce a separate likelihood kernel P(Y=y | T=t, action=a, history=h) with rational normalization checks. Keep this extension separate from the current perfect-revelation oracle, which remains a valid solver for its stated model.
2. For each nonzero-probability observation, update the posterior with Bayes' rule. Skip zero-mass observations rather than conditioning on them. Allow explicit abstention, false-positive, false-negative, and asymmetric-loss outcomes.
3. Use terminal decision loss rather than count of verified true claims as a distinct objective; do not compare values across objectives as though they were interchangeable.
4. Build a small independent brute-force noisy-observation oracle and compare it with a noisy Bellman recursion on rational fixtures. Include the 1/20 value example, deterministic perfect-test limit, uninformative-test limit, and a correlated-error example.
5. Record numerical bounds, state limits, timeouts, and complete logs before any cloud execution. No job is authorized by this protocol.

## Falsification and empirical boundaries

- If a noisy oracle assigns posterior 1 after a positive under the stipulated 4/5 sensitivity/specificity, the conditioning implementation fails.
- If it reports gross decision value 1/4 rather than 1/20 for the stipulated noisy test, the decision-value implementation fails.
- If it recommends purchasing the test at cost 1/10, the decision rule fails under the stated assumptions.
- Real verifier confusion matrices must be estimated from independent labeled data, with uncertainty intervals, abstentions, and correlated errors. This exact example cannot establish real-world calibration or deployment benefit.
- For NLP, mathematics, and physics, preregister the same decision-loss definition and information-matched baselines. Publish negative outcomes and held-out-domain failures.

## Novelty boundary and publication integrity

No novelty is claimed for Bayesian updating, value of information, noisy observation kernels, or abstention-aware decision theory; these are established concepts. A defensible contribution would require independently validated evidence or a genuinely new result beyond these standard tools. Label this as a theoretical stress test, not a measured improvement or an executed regression.

## Cost and hardware guardrails

Only verified free GitHub-hosted standard public-repository runners may be considered after checking current terms and account eligibility. Do not use paid APIs, larger runners, the user's laptop for compute, or any service requiring spending or card activation. November 22 remains a conditional scientific decision checkpoint.
