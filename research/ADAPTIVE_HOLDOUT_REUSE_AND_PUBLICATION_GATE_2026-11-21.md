# Adaptive reuse and publication gate (2026-11-21)

Status: methodological safeguard, not an empirical result or a novelty claim.

## Problem
A held-out evaluation ceases to be genuinely confirmatory if its labels, error examples, or summary scores are repeatedly inspected while modifying a verifier, threshold, prompt, evidence selection rule, or domain weighting. Frozen thresholds alone do not prevent adaptive overfitting. A public repository can inadvertently leak held-out decisions through issue discussions, CI logs, figures, or intermediate artifacts.

## Split and access policy
1. Assign source-family clusters to development, calibration, and final test partitions before model selection. Record the split algorithm, seed, input manifest digest, grouping keys, date, and the person/process that finalized the partition.
2. Permit iterative debugging only on development examples. Calibration may be used to select thresholds and prespecified hyperparameters; after a threshold is frozen, do not repeatedly revise the method against calibration outcomes without declaring a new exploratory phase.
3. Lock the final test manifest, predictions, adjudication protocol, cost accounting, and analysis script *before* the first final test evaluation. Record Git commit SHA and cryptographic digests. A timestamp on its own is not evidence of a genuine freeze.
4. Run the final test once for the preregistered primary comparison. Subsequent fixes after observing outcomes must be reported as post-hoc, with the original run retained and an entirely new independent test set required for renewed confirmation.
5. Prevent leakage through near-duplicates, same-source derivations, reused benchmark answer keys, temporal revisions of the same underlying problem, and contamination of adjudicators by verifier outputs. Disclose any inability to establish independence.
6. Public release should include code, synthetic fixtures, schemas, hashes, protocols, and appropriately licensed data. Do not publish private test labels before the confirmatory lock; later release only if rights and evaluation integrity allow it.

## Required immutable decision ledger
For every analysis decision, record: decision ID; UTC timestamp; responsible actor; input dataset hash; code commit; affected domains and source families; prespecified versus exploratory status; justification; whether held-out outcomes had been viewed; and superseded decision ID. Record missing entries as missing, not inferred.

## Statistical interpretation
Let A and B denote acceptance indicators, Y_A and Y_B error indicators, and c a target coverage. The operational estimand is E[Y_A | A=1] - E[Y_B | B=1] at equal coverage; it compares potentially different accepted sets. A shared-accepted-set estimand E[Y_A-Y_B | A=B=1] answers a different question and must be separately reported. Neither estimand alone proves a causal temporal mechanism. Shuffled timestamps, evidence deletion, chronology-preserving controls, and matched non-temporal baselines are needed, with the limitation that shuffling may introduce out-of-distribution artifacts.

If the number of independent source-family clusters is small, naive item-level confidence intervals are unreliable. Report cluster counts and sensitivity to individual families; do not assert significance from nominal item counts alone. If independent labels or matching resource accounting are absent, the empirical claim is not identifiable.

## Publication decision on 2026-11-22
- **Discovery paper:** only if genuine held-out independent adjudication, baseline matching, control outcomes, uncertainty, prior-art comparison, and full provenance are all available and withstand falsification.
- **Methods/preregistration:** permissible without experimental findings, explicitly labeled unvalidated, and without claiming novelty established by results.
- **No publication-ready claim:** if provenance, permissions, or analysis integrity cannot be defended.

No GPU, paid API, local laptop compute, or model inference is required to implement this protocol. Cloud resources must be checked for current free eligibility and billing restrictions before use. This document itself does not certify any provider's quotas or access.

## Prior-art boundaries to investigate
Adaptive data analysis and reusable holdouts (Dwork et al., 2015); selective classification and risk-coverage evaluation (Geifman and El-Yaniv, 2017); conformal risk control (Angelopoulos et al., 2024); benchmark contamination and leakage literature. These are conceptual collision candidates, not a completed exhaustive literature audit. Any distinctive contribution must survive comparison with these existing frameworks and temporal fact-verification work.
