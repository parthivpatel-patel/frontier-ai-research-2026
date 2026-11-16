# Protocol 115 — Correlated verifier evidence and non-identifiability audit

Prepared 2026-11-16. Status: analytical protocol, **not an executed experiment**. No novelty or performance claim.

## Audited implementation boundary

Inspection of `research/fixtures/protocol_113_exact_noisy_decision.py` and `test_protocol_114_independent_action_enumeration.py` confirms a single binary test with stipulated sensitivity/specificity and terminal ACCEPT/REJECT/ABSTAIN losses. Protocol 114 enumerates three no-test actions and nine one-test contingent plans. It does **not** test repeated evidence, conditional dependence, learned likelihoods, or cross-domain calibration. Protocol 112 already identifies the perfect-verifier failure mode.

## Exact counterexample: identical single-test calibration, different joint evidence

Let T be Bernoulli(1/2). Two binary verifier outputs Y1,Y2 each have sensitivity and specificity 4/5, and are symmetric under truth inversion. Compare two observation models:

* Model I: Y1 and Y2 are conditionally independent given T.
* Model C: Y2=Y1 deterministically, with the same individual 4/5 sensitivity and specificity.

For either model, one positive gives P(T=true | Y1=+)=4/5. For two positives:

* Model I: P(++ | T=true)=16/25; P(++ | T=false)=1/25, so P(T=true | ++)=16/17.
* Model C: P(++ | T=true)=4/5; P(++ | T=false)=1/5, so P(T=true | ++)=4/5.

Both models have exactly the same marginal confusion matrix for each verifier. Thus marginal accuracy and calibration alone do not identify the joint likelihood needed for sequential Bayesian verification. Treating duplicated evidence as independent generates overconfidence.

With false-accept and false-reject losses 1 and abstention loss 1/4, the Bayes risk after ++ is 1/17 in Model I and 1/5 in Model C. These are conditional risks, not ex-ante values or measured outcomes.

## Required falsification tests

1. Create an exact-rational two-test joint likelihood representation P(Y1,Y2 | T) with nonnegative entries summing to one for each truth state.
2. Assert that both models reproduce 4/5 marginal sensitivity/specificity for each test, while their ++ posteriors differ exactly as above.
3. Confirm a sequential optimizer does not multiply likelihoods under Model C unless conditional independence is explicitly stipulated and checked.
4. Add a duplicate-verifier negative control: querying an identical deterministic copy cannot yield additional information after the first observation; any strictly positive incremental gross value fails the model.
5. Test ordering and symmetry invariance when tests have equal costs and identical joint distributions, and distinguish invalid probabilities from resource-limit refusal.
6. Evaluate joint calibration with independent held-out truth labels and provenance of shared model, data, prompt, and retrieval sources; report uncertainty and clustered errors.

## Research implications and baselines

A cross-domain evaluation spanning NLP factual claims, mathematical assertions, and physics reasoning must distinguish evidence diversity from apparent verifier agreement. Pre-register terminal loss, query budgets, verifier dependencies, and independently adjudicated truth labels. Compare against no verification, one verifier, random verification, myopic value of information, and an information-matched Bayesian policy with a joint observation model. Report failures and domain-specific error correlations rather than pooling away heterogeneity.

Prior-art families requiring systematic citation checks before novelty claims: Bayesian experimental design and value of information; correlated sensor fusion; sequential diagnosis/POMDPs; ensemble error dependence; selective prediction and abstention; LLM self-consistency and multi-agent correlated failure. The counterexample itself is standard Bayesian probability, not a new theorem.

## Execution and publication gate

No cloud run is authorized here. Before running, verify GitHub-hosted public-repository standard-runner free eligibility, account billing restrictions, and available concurrency; enforce job timeout and bounded matrix size, capture immutable commit SHA and full logs. Never use laptop computation or paid services. The November 22, 2026 checkpoint is a go/no-go assessment, not a guaranteed publication date.
