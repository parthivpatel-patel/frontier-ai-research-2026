# Protocol 118 — Fixed-Marginal Dependence Stress Test

**Status:** Analytical design and falsification specification; not an executed experiment.  
**Scope:** Independent frontier AI research; no model-training claim or new theorem claim.

## Research question

Can a verifier-selection policy infer the incremental decision value of a second AI/scientific verifier from each verifier's individual sensitivity and specificity alone? **No.** Marginals do not identify the joint observation law. Protocols 115–117 compare independent and duplicated verifiers; this protocol specifies a continuous family of couplings with identical per-verifier accuracy, to test whether a proposed planner improperly substitutes marginal calibration for dependence calibration.

## Exact construction

Let the latent binary truth be T, with prior P(T=1)=1/2. Each of two exchangeable binary verifiers has sensitivity and specificity 4/5. Write X,Y in {+,-}. Define q_T=P(X=+|T). Thus q_1=4/5 and q_0=1/5.

For each truth state, let c_T=P(X=+,Y=+|T). A valid exchangeable coupling with these marginals has

- P(++|T)=c_T
- P(+-|T)=P(-+|T)=q_T-c_T
- P(--|T)=1-2q_T+c_T
- max(0,2q_T-1) <= c_T <= q_T.

Use the symmetric one-parameter subfamily c_1=3/5+(lambda)(1/5) and c_0=(lambda)(1/5), for lambda in [0,1]. Both truth-state rows normalize exactly. At lambda=0 the two positive reports are as anticorrelated as the margins permit (under both truth states); at lambda=1 the two verifiers are duplicates. **Conditional independence is not a member of this particular symmetric line**: for independent errors c_1=16/25 and c_0=1/25, which correspond to lambda=1/5 for the false state and lambda=1/5 for the true state only if c_1=3/5+lambda/5=16/25, so lambda=1/5 indeed; thus independence is lambda=1/5.

With prior 1/2 and observed ++, posterior truth probability is c_1/(c_1+c_0), when the denominator is nonzero:
- lambda=0: posterior 1 (the false-state ++ likelihood is zero);
- lambda=1/5: posterior 16/17;
- lambda=1: posterior 4/5.

These are **stipulated-model identities**, not observed AI-model accuracy.

## Decision-theoretic falsification

For each lambda in {0, 1/5, 1/2, 1}, construct the exact four-outcome likelihood tables using fractions. Compare:
1. Protocol 116 `expected_risk` and `first_only_risk`;
2. Protocol 117 independent 81-policy and 9-policy enumeration;
3. an intentionally incorrect baseline that always multiplies the two marginal likelihoods.

Use the pre-existing accept/reject/abstain loss schedule (unit error losses; abstention cost 1/4). Require equality between methods (1) and (2) at every grid point. The independence baseline must be recognized as **misspecified** away from lambda=1/5, rather than treated as ground truth. Check nonnegative incremental value of observing Y, and exactly zero incremental value at lambda=1. The dependence sensitivity must be reported even if the optimal policy and its risk happen to coincide for some parameter points.

## Additional checks

- Marginal P(X=+|T)=P(Y=+|T)=q_T at all lambda values.
- Every joint cell is nonnegative and rows sum to one.
- Swapping X and Y leaves posterior and full-information risk invariant.
- Impossible observations return no posterior rather than a fabricated certainty.
- At lambda=0, a ++ report has zero probability under T=0, but posterior 1 is justified only within the stipulated model, not as an empirical truth certificate.
- Repeat with asymmetric losses and priors; avoid extrapolating the example to all applications.

## What would falsify a practical scientific claim?

A claimed verifier-selection improvement fails if it disappears under dependence-aware likelihoods, under cost-matched Bayesian baselines, or under held-out joint calibration. Distinguish algorithmic implementation correctness from empirical accuracy of likelihood estimates. A held-out dataset must record truth adjudication, verifier identities and versions, shared prompts/retrieval, confidence intervals, missingness, and cost. Split by problem/source family to reduce leakage. Compare NLP factual claims, mathematical statements, and physics claims only when independent adjudication and rights to use the datasets are established.

## Prior-art and novelty boundaries

Fréchet–Hoeffding bounds, Bayesian decision theory, dependent evidence aggregation, ensemble error correlation, and value of information already establish the central mathematics. No novelty is claimed for these identities. Any defensible paper contribution must instead be a reproducible *empirical* or algorithmic advance over established correlation-aware, cost-sensitive verification baselines. Search and cite specific closest work before a novelty claim; do not equate code volume or regression counts with research novelty.

## Execution and resource gate

This is a source-only specification. Do not execute tests or launch cloud runners until public-repository GitHub Actions eligibility, account-level billing/card status, runner limits, and the relevant current free-use terms are verified. Add explicit job timeout and concurrency controls, avoid artifacts containing secrets, and retain exact commit, runner and log provenance. Never use the user's laptop for computation. Zero spending is mandatory.

## Publication gate

November 22, 2026 is a conditional review date, not an unconditional submission deadline. A manuscript must label unexecuted tests as specifications, report null/negative results, cite related work, and disclose AI assistance as required by the venue.
