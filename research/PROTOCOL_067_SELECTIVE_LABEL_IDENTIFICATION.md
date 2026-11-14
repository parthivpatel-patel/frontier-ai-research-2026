# Protocol 067 — Identifiability of false acceptance under selective verification

Date: 2026-11-14 UTC. Status: analytical design note; **no theorem of novelty, empirical result, or completed experiment**.

## Why this matters

Protocol 066's primary endpoint, false acceptance among released claims, cannot generally be calculated from labels observed only for claims selected for verification. In particular, evaluating a policy on the labels it chose to inspect creates selective-label bias. The outcome definition must also distinguish a *pre-release audit used by a policy* from a *separate evaluation audit that measures the policy*. This note formalizes the identification problem before a frozen experiment.

## Units, populations, and estimands

Let i index candidate claims and g(i) index a provenance family. Each claim has domain d(i) in {NLP, mathematics, physics}, pre-audit features X_i, fixed but potentially unobserved truth Y_i in {0,1} (1 means false), and a policy-specific release indicator R_i(pi) in {0,1}. Let A_i denote inclusion in a **separate blinded evaluation audit** and O_i whether that audit yields a valid truth label. The primary finite-population false-acceptance fraction for a fixed policy pi is

FAR(pi) = [sum_i w_i R_i(pi) Y_i] / [sum_i w_i R_i(pi)],

where nonnegative weights w_i and a positive denominator are prespecified. This is an error fraction *conditional on release*, not a guarantee of conditional risk. Release coverage is C(pi) = [sum_i w_i R_i(pi)]/[sum_i w_i]. Define an explicit coverage target c and tolerance epsilon, and compare only policies satisfying |C(pi)-c| <= epsilon. For a population where release decisions depend on results of the policy's own verification, compute R_i(pi) using only that policy's allowed audit budget and information. Never use the evaluation-audit label to decide release.

## Identification pathways

**Complete independent labeling.** When all candidate claims have reliable blinded truth labels, compute FAR directly; retain adjudicator disagreement and label uncertainty rather than silently treating judgments as infallible.

**Probability-sampled evaluation labels.** If the evaluation audit independently samples units with known positive inclusion probabilities q_i, and observed labels are valid, a Horvitz–Thompson numerator estimate is sum_i A_i w_i R_i(pi) Y_i/q_i. Its denominator sum_i w_i R_i(pi) is known from all release decisions, so the resulting FAR estimator is design-unbiased conditional on fixed release decisions and a fixed finite population (assuming the evaluation audit does not affect those decisions). If only a ratio of two estimated totals is used, do **not** claim exact design unbiasedness. Under unequal probability sampling, use the actual joint inclusion probabilities or a defensible replicate/cluster design for uncertainty; an IID claim bootstrap is not sufficient when claims share provenance families.

**Unobserved outcomes.** If a selected evaluation unit has no adjudicated label, q_i alone does not repair nonresponse. Define p_i = P(O_i=1 | A_i=1, predeclared information) only if its assumptions can be defended; inverse-response weighting requires positive p_i and a valid missing-at-random argument. If labels are missing not at random, report sensitivity or partial-identification bounds, not a point estimate as ground truth.

## Honest worst-case bounds

For a finite population with known release decisions, let W_R = sum_i w_i R_i(pi) > 0. Among released claims, let W_F be the weight with *verified false* labels and W_U the weight with **unobserved or unresolved** labels. Without assumptions about unresolved truth,

W_F/W_R <= FAR(pi) <= (W_F + W_U)/W_R.

This deterministic bound requires trustworthy labels for the resolved subset; it does not imply random-sampling confidence coverage. If the bounds for candidate and baseline overlap, do not claim the candidate is better without stronger justified evidence. Bounds can be very wide; that is an honest failure of identification.

## Budget and policy comparison

Distinguish three budgets: B_policy for the verifier's operational actions, B_eval for independent ground-truth adjudication, and B_compute for cloud execution. Match policies on B_policy and release coverage; report B_eval and adjudicator hours separately. A policy must not gain an advantage by using more evaluation truth. Pre-register the utility of audit outcomes, verifier error rates, and whether a verification action can revise the release decision. Separate provenance-family and domain slices must be reported; domain weights are fixed before seeing test labels.

## Falsification and adversarial controls

1. **Audit-on-release trap:** candidate chooses which labels are revealed; evaluator mistakenly treats observed-label error as population FAR. Reject.
2. **Zero-probability stratum:** a provenance family can never enter the evaluation sample (q_i=0). Design-based full-population identification fails.
3. **Nonresponse trap:** sampled claims with ambiguous physics truth go unresolved. An inclusion weight does not correct missingness.
4. **Correlated-family trap:** repeated paraphrases are counted as independent units in uncertainty estimation. Reject IID uncertainty.
5. **Budget leakage:** evaluation adjudications influence policy thresholds or release. Reject.
6. **Denominator collapse:** release coverage near zero makes FAR comparisons unstable or undefined. Reject unless preregistered admissibility holds.
7. **Strong-baseline equivalence:** a proposed family-aware policy is mathematically equivalent to existing stratified sampling/active auditing at matched information and budget. Novelty claim fails.

## Closest methodological collisions still requiring source-level audit

- Horvitz and Thompson (1952), *A Generalization of Sampling Without Replacement From a Finite Universe*, JASA, https://doi.org/10.1080/01621459.1952.10483446 — inverse inclusion probability estimation is established.
- Manski (1990), *Nonparametric Bounds on Treatment Effects*, AER, https://www.jstor.org/stable/2006592 — worst-case/partial-identification reasoning is established; the bound above is an elementary missing-binary-outcome bound, **not a new result**.
- Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, https://papers.nips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html — selective release is established.
- Angelopoulos et al. (2024), *Conformal Risk Control*, https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html — calibrated risk control is established.

These are pointers for direct bibliographic verification, not a completed literature search. Next review must include active learning, off-policy evaluation, positive-unlabeled learning, verification economics, and benchmark contamination.

## Cloud-only execution and publication gate

No laptop compute, downloads, model inference, or local experiments. All future execution must use independently verified zero-cost cloud infrastructure with account-specific quota, card, billing, and capacity checks documented **before** running anything. Do not infer that a GitHub Actions public repository automatically guarantees a free entitlement. Current evaluation manifest remains DRAFT_NOT_FROZEN. No empirical claims, theorem claims, or November 22 publication promise arise from this protocol. Disclose AI assistance as required by the chosen venue.
