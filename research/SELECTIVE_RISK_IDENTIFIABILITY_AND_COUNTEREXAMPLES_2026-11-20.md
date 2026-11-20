# Selective-risk identifiability and paired-policy comparison (2026-11-20)

## Scope and claim status
This note gives algebraic identities and counterexamples for the proposed NLP/mathematics/physics verification study. They are elementary derivations, **not claimed as novel theorems**, empirical findings, or evidence of AI welfare, consciousness, or physical-law discovery. They make the planned experiment falsifiable and protect against misreporting.

## Definitions
For a frozen evaluation set of n independently adjudicated questions, let Y_i in {0,1} indicate correctness of the original answer (1=correct). For policy p, let A_pi in {0,1} indicate acceptance and let K_p=sum_i A_pi. For K_p>0, selective error R_p = sum_i A_pi(1-Y_i)/K_p; coverage C_p=K_p/n. Rejected items are retained in n. Abstention is **not** automatically an incorrect answer.

For two policies T (temporal evidence) and B (baseline) evaluated on the **same** n questions, if K_T=K_B=k>0, the difference is

D = R_T-R_B = (1/k) sum_i (A_Ti-A_Bi)(1-Y_i).

Because sum_i(A_Ti-A_Bi)=0, equivalently

D = -(1/k) sum_i (A_Ti-A_Bi)Y_i.

Thus only **discordant acceptance decisions** contribute. If policies accept exactly the same items, D=0 regardless of their different confidence scores or explanations. A negative D favors T on accepted-answer error, but is not by itself proof of a temporal mechanism.

## Counterexample: matched coverage does not establish matched compute
Consider two items. Policy T uses 100 and 0 tokens; B uses 50 and 50. Their total observed tokens are both 100, yet per-item resource vectors differ. Aggregate-budget comparisons and strict per-item matching answer different questions. Conversely, two policies can each use 50 tokens and one call per item but have different wall time, accelerator utilization, energy and API price. Do not describe either token matching scheme as equal compute without independent measurement.

## Counterexample: selective-risk improvement can hide missed correct answers
Four labeled questions have Y=(1,1,0,0). T accepts items (1,2), while B accepts (1,3). Both cover 2/4; R_T=0 and R_B=1/2. T's error reduction is real on this frozen set, but says nothing about behavior on other domains or whether a time feature caused the difference. Separately report correctly rejected errors and incorrectly rejected correct answers, plus their family-cluster uncertainty. A verifier that rejects every answer has undefined selective error, not zero error at useful coverage.

## Protocol implications
1. Freeze item IDs, source-family splits, correctness labels, policy thresholds, cost budgets and comparison order before evaluating held-out questions.
2. Record for every item and policy: acceptance, calibrated score, correctness adjudication, input/output tokens, calls, latency, and provenance. Never fill missing latency with zero or use missing costs as proof of free computation.
3. Compare T with confidence-only C, shuffled temporal S, and stronger conventional-feature B. Preserve paired item IDs; report risk-coverage curves and family-cluster confidence intervals with family counts.
4. Require a predeclared primary domain-weighting scheme and three leave-one-domain-out transfer tests. Publish failures and unresolved adjudications.
5. **Mechanistic falsification:** If T fails to outperform S or B under matched budget and family-level uncertainty, reject the claim that temporal evidence contributes distinctive information. If cross-domain transfer fails, restrict any positive claim to supported domains.
6. **Novelty gate:** Algebra here is not novel. A publishable research contribution requires a defensible distinction from selective classification, conformal risk control, existing verifier evaluation, and any 2026 selective-risk LLM work, demonstrated in a documented full-text comparison.

## Zero-dollar execution gate
Use only standard public-repository GitHub-hosted runners if free eligibility and workflow configuration are checked before execution. Do not invoke paid model APIs, GPU runners, local training, or model downloads on the user's laptop. A CI unit test of these identities is software validation, not a model result. No new experiments were run to produce this note.

## Publication decision
The November 22 checkpoint can release a transparent protocol/methods artifact with explicit AI-assistance disclosure if appropriate. A discovery paper requires separately verified independent labels, held-out experiments, uncertainty, matched-budget evidence and a credible novelty comparison.