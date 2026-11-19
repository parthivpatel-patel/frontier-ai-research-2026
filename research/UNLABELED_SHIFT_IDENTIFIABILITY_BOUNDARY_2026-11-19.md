# Unobserved shift: an identifiability boundary for verifier reliability

**Date:** 2026-11-19. **Status:** mathematical counterexample and preregistration guidance, not an original theorem, empirical finding, or verified deployment guarantee.

## Setup

Let X be the observable information available to a frozen verifier (candidate answer, confidence score, provenance metadata, and any permitted verifier features), Y in {0,1} indicate an incorrect answer, and A(X) in {0,1} denote acceptance. The target selective risk is R_Q(A)=E_Q[Y A(X)]/E_Q[A(X)] for a target distribution Q with positive acceptance probability. If E_Q[A]=0, selective risk is undefined, not zero. The target population and denominator must be stated before evaluation.

## Indistinguishable-target counterexample

Take X=x0 almost surely and a fixed verifier A(x0)=1. Construct two target distributions Q0 and Q1 with **identical observed X distributions** but Q0(Y=1|X=x0)=0 and Q1(Y=1|X=x0)=1. Any monitoring procedure observing only unlabeled X, scores, verifier decisions, and costs receives identical observable data under Q0 and Q1, regardless of sample size. Yet R_Q0(A)=0 and R_Q1(A)=1.

Therefore, without assumptions connecting target correctness labels to observable quantities, no unlabeled-target-only procedure can provide a nontrivial uniform guarantee of target accepted-answer error. A threshold or family-aware calibration procedure learned on a source distribution cannot remove this identification problem merely by measuring target score histograms or matching coverage. The argument is elementary indistinguishability reasoning, **not a novel impossibility theorem**.

For a nontrivial acceptance fraction, take X in {x0,x1}, with Q(X=x0)=Q(X=x1)=1/2, A(x0)=1 and A(x1)=0. Set correctness among accepted x0 to be always correct in Q0 and always wrong in Q1, keeping all observables unchanged. Both distributions have 50% coverage and opposite accepted-answer risk.

## Assumptions that can restore limited identification

- **Covariate shift**: if P(Y|X)=Q(Y|X), source labels plus adequate support and valid density-ratio estimates can identify target risk in principle. The assumption is not testable from unlabeled target X alone; support failure blocks extrapolation.
- **Target labels**: a probability-sampled, independently adjudicated target audit can estimate target selective risk with uncertainty; the sampling design, nonresponse, shared source families, and adjudicator disagreement must be accounted for.
- **Worst-case bounds**: absent target labels or credible shift assumptions, a risk interval [0,1] is generally the honest bound for a nonempty accepted subset. This is not useful certification.

## Proposed falsification experiment (not executed)

1. Freeze candidate answers and verifier thresholds on source/calibration splits. Preserve full-roster IDs, domain labels (NLP, mathematics, physics), and verifier costs including rejected answers.
2. Construct paired target conditions with the same observable verifier-score/acceptance distribution but deliberately permuted or adversarially altered correctness assignments **only in a labeled synthetic stress test**. Do not present manipulated labels as real model outputs.
3. Assert that any monitoring statistic computed exclusively from observable X, scores, decisions, and cost is identical across paired conditions, while true accepted-error risk differs.
4. Repeat with source-family stratification and equal pooled/family coverage; confirm that matching those quantities does not identify target correctness.
5. On genuine held-out target data, require independent ground-truth adjudication, preregistered uncertainty intervals and source-family-aware sensitivity analyses before any reliability claim.
6. Declare the hypothesis of **unlabeled shift-robust certification without extra assumptions** falsified by the counterexample. Do not claim an empirical improvement from synthetic stress tests.

## Nearest conceptual literature and novelty gate

This is a direct instance of established distribution-shift and identifiability limitations. Compare primary texts before claiming originality: Sugiyama et al. (2007), covariate-shift adaptation by importance weighting; Geifman & El-Yaniv (2017), selective classification; Angelopoulos & Bates (2023), *Conformal Prediction: A Gentle Introduction*; and Barber et al. (2023), *Conformal Prediction Beyond Exchangeability*. Confirm exact theorem scope and assumptions against the full papers. Distribution-free marginal coverage under exchangeability is **not** a guarantee of conditional correctness under arbitrary target shift.

A possible contribution must be demonstrated through a new assumption-explicit method or reproducible held-out cross-domain evidence against these baselines, not through this counterexample alone.

## Resource and publication constraints

This note is analytical only. No laptop compute, local model inference, dataset download, cloud job, paid API, or billing action is authorized by it. Before running experiments, independently verify that the exact public repository and account permit no-charge standard hosted CI; avoid larger/billable runners and any card-required provider. The November 22 checkpoint is conditional: without genuine results, release a clearly labeled methods/preregistration manuscript, not a results paper. Record AI assistance and all limitations according to the destination's disclosure rules.
