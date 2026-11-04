# Protocol 050 — Honest matched-coverage inference and deployment estimands

Date: 2026-11-04
Status: preregistered analysis plan; **not** experimental evidence.

## A distinction that must not be erased

The validation-frozen threshold protocol and a comparison at exactly matched *test* coverage answer different questions. In deployment, thresholds are frozen before encountering a test population. Under distribution shift, the methods may have different realized test coverage. Re-ranking test examples to force identical coverage uses test-set information and must not be presented as deployment performance.

Report both analyses, under different names:

1. **Prospective deployment estimand (primary):** choose each method's threshold from validation examples for target coverage c in {0.25, 0.50, 0.75}. Freeze thresholds. On held-out test data, report realized coverage C_m and unsafe-acceptance probability U_m = count(accepted AND unsafe)/N, as well as selective risk R_m = count(accepted AND unsafe)/count(accepted) when denominator > 0. For empty acceptance, R_m is undefined, not zero. Do not claim matched test coverage when C differs.
2. **Descriptive risk-coverage estimand (secondary):** compare error at shared coverage on the test set using score rankings, explicitly labeled *retrospective* and not a deployable threshold policy. Tie blocks remain intact; interpolate only with clearly stated randomized acceptance assumptions. Never tune hyperparameters or choose a headline operating point using held-out results.

The two error metrics are not interchangeable. U rewards abstention; R conditions on acceptance. A system that accepts no claims has U=0 and undefined R, and cannot be declared superior.

## Independent physical adjudication

Each test case must contain a physical system specification, initial conditions, observables, an intended claim, adjudication provenance, and an uncertainty status. Keep formally provable claims distinct from empirical model adequacy. For ambiguous or non-identifiable physical claims, use an explicit 'indeterminate' ground-truth category and report its frequency; do not silently count it as correct or incorrect. Predefine a sensitivity analysis treating indeterminate accepted cases as unsafe and, separately, excluding them.

## Unit of independence and uncertainty

Randomly partition by source family and physical model family, not individual paraphrase. Report per-domain outcomes and macro averages; prevent paraphrases and near-duplicate physical instances crossing splits. For inference, resample *source/model-family clusters*, maintaining all examples within a selected cluster. If too few independent clusters exist, provide descriptive estimates without misleading narrow confidence intervals. For comparing systems, use paired cluster bootstrap differences on the same examples, and report both coverage difference and risk difference. Never infer causality from synthetic-only experiments.

## Competitive falsification

At minimum compare: (i) unconstrained language-model claims, (ii) calibrated abstention without certificates, (iii) language-to-logic with standard model checking, and (iv) the proposed independent physical-certificate pipeline. Hold model, prompt budget, test cases, and adjudication rules constant where possible. Report failures of the certificate generator and checker, abstentions, runtime, and unknown outcomes. If improvements disappear after controlling for coverage or grounding fidelity, reject the incremental safety claim.

## Closest intellectual ancestors

- Counterexample-guided abstraction refinement (Clarke et al., 2000): https://doi.org/10.1007/10722167_15
- Selective classification / risk-coverage framework (Geifman and El-Yaniv, 2017): https://arxiv.org/abs/1705.08500
- Temporal-logic model checking (Clarke, Grumberg, Peled, 1999): https://mitpress.mit.edu/9780262032704/model-checking/
- Previously identified directly relevant recent language-grounding and physical-verification papers must be read in full and compared claim-by-claim before asserting novelty.

## Zero-cost execution gate

Do not start cloud jobs until repository visibility, standard-runner eligibility, available free quota, artifact-storage limits, billing configuration, and any payment-card requirements have been verified for this account. Use only documented free standard runners and bounded CPU-only jobs; avoid large runners, paid hosted inference, and third-party services. No laptop compute is required.

## Release gate

No positive research claim without independently executed code, immutable run identifiers, actual logs, predeclared primary metrics, non-leaking splits, and competitive baselines. Negative results remain publishable as a rigorous audit, not rebranded as algorithmic novelty. Record AI assistance and disclosures required by the target venue.
