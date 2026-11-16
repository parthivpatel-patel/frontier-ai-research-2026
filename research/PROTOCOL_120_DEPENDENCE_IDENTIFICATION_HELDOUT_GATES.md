# Protocol 120 — Dependence identification and held-out falsification (2026-11-16)

Status: preregistered evaluation design only. No empirical data, executed tests, or novelty claim.

## Identifiability boundary
For binary truth T and binary verifier outputs A,B, the two marginal conditional accuracies do not identify P(A,B|T). The Fréchet bounds constrain the joint probability but leave a continuum of couplings. Protocol 119 is a mathematical fixture demonstrating this fact; its exact-rational checks do not estimate dependence in deployed systems.

The 80%-accurate symmetric example uses P(++|T=1)=3/5+lambda/5 and P(++|T=0)=lambda/5 for lambda in [0,1]. At prior 1/2, P(T=1|++)=(3+lambda)/(3+2 lambda), ranging from 1 to 4/5. Conditional independence occurs at lambda=1/5, giving 16/17. These are stipulated model values, not measured verifier accuracies.

## Evaluation protocol
1. Build independently adjudicated, provenance-recorded binary claims in NLP, mathematics and physics. Separate claim generation, verifier training/calibration, and test labels; record sources and dates. Do not call an LLM's agreement a ground-truth label.
2. Estimate each conditional 2x2 verifier-output table on a calibration split with explicit uncertainty intervals. Report sample counts for each truth state, base rate, missingness and abstentions. Do not assume symmetry or exchangeability in empirical fits.
3. Freeze the joint-likelihood model, marginal-only independence baseline, duplicated-evidence baseline, and abstention/decision costs before opening the held-out test split.
4. Primary metrics: held-out log loss and Brier score for truth probabilities; secondary: calibration by domain, decision risk net of verification cost, and coverage versus abstention. Compare paired claim-level differences with cluster-aware uncertainty when claims share sources or models.
5. Falsification: reject the claim that dependence modeling helps if held-out proper scoring rules or cost-adjusted decision risk fail to improve relative to independence under preregistered uncertainty criteria. Report harmful subgroups and calibration failures. A method that merely fits synthetic couplings cannot pass.
6. Leakage controls: keep paraphrases, derived mathematical statements, same-source physics claims, and shared answer keys in the same split. Independently adjudicate contested labels; mark unresolved claims as unresolved rather than force binary truth.
7. Resource gate: run only on a verified no-charge cloud environment after checking current quota, card/billing requirements, spending controls and account eligibility. Do not run on the user's laptop. Preserve immutable commands, dependency versions, hashes, job logs and exit codes.

## Closest prior-art families to audit before novelty claims
- Bayesian decision theory and value of information (classical; not novel).
- Correlated diagnostic tests, latent-class models, and conditional dependence in diagnostic accuracy studies.
- Forecast combination, ensemble calibration, and correlated classifier errors.
- Selective prediction and abstention; conformal risk control.
- LLM-as-a-judge agreement biases and multi-agent debate/evaluation.

Novelty would require a specific new method or convincing empirical cross-domain contribution beyond these traditions, with explicit comparisons to their strongest applicable baselines. The current work does not establish either.

## Publication gate for November 22
Publish a methods/preprint paper only with clearly labeled analytical results and independently executed reproducibility evidence. Do not market an unexecuted regression specification as validated or claim an empirical improvement. If held-out evidence is unavailable, publish a transparent research protocol or postpone the empirical paper.
