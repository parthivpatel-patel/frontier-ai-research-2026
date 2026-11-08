# Protocol 130 — Exact finite-resampling oracle and falsification specification

Date: 2026-11-08. Status: preregistered test design, not executed. This protocol follows Protocol 129 and does not claim novelty or experimental success.

## Objective

Verify the *conditional Monte Carlo* interpretation of the existing bootstrap diagnostics against an exact, finite resampling oracle. Keep this separate from population confidence-interval coverage, physics competence, and any claims about improved AI safety.

## Exact oracle construction

Consider two independent resampling units (physics families), each selected with replacement twice. Let the first unit have joint acceptance A=1 and unsafe-outcome contrast Y=+1; let the second have A=0 and Y undefined. Define the resampled contrast as the mean of Y among accepted sampled units. The four equally likely ordered resamples are (1,1), (1,2), (2,1), (2,2). The first three yield T=+1 and the last has an undefined denominator. Thus P(D=0)=1/4 and the conditional CDF of T given D=1 is a point mass at +1. This deliberately degenerate oracle tests denominator accounting and exact conditional CDF agreement, but **cannot** test percentile endpoint calibration.

Second oracle: two units both accepted, with contrasts -1 and +1, two draws with replacement. The four resamples yield T=-1,0,0,+1 with probabilities 1/4,1/2,1/4. There are no undefined draws. Compare exact CDF values at -1, 0, +1 with empirical frequencies; quantify Monte Carlo deviations, not inferential coverage.

Third oracle: three units with accepted contrasts -1 and +1 and one unaccepted unit; draw three units with replacement. Enumerate all 27 ordered outcomes, count undefined draws (only the all-unaccepted outcome), and compute the exact conditional distribution over the other 26 outcomes. Do not replace family-cluster resampling by record-level resampling if the implementation resamples families.

## Frozen acceptance criteria

1. For each oracle, enumerate all outcomes in pure standard-library Python, independently of the production bootstrap code. Assert exact total probability one, exact undefined mass, and conditional CDF monotonicity.
2. For the first oracle, assert exact undefined probability 0.25 and that all defined statistics equal +1. For the second, assert the three masses 0.25/0.50/0.25.
3. For the third, compare the exact undefined probability 1/27 to the analytic preflight, subject to the production code's actual sampling and weighting contract. If the contracts differ, document the mismatch and do not silently alter the oracle.
4. For independently generated fixed-budget bootstrap draws, evaluate whether the observed conditional CDF deviation is at most the DKW bound at alpha=0.05. The DKW statement is probabilistic; **do not** demand that every seed satisfy it. Across many independent runs, report the failure fraction with a binomial uncertainty interval.
5. Report requested draws R, defined draws M, exact undefined probability, observed undefined count, DKW epsilon(M), and maximum conditional CDF discrepancy. Suppress diagnostics when M=0.
6. Freeze all random seeds and the code commit before looking at outputs. Do not choose seeds based on favorable outcomes.
7. Explicitly report that a DKW rank bound does not imply endpoint-value precision or 95% population coverage.

## Coverage experiment: separate estimand

Generate independent datasets from a prespecified family-clustered model with a known target parameter. Include: balanced acceptance, rare acceptance, outcome-dependent acceptance, unequal family sizes, and a discrete/bimodal outcome. For each dataset, compute the admitted bootstrap interval only if its preflight and minimum-defined-draw gates pass. Report both (a) unconditional coverage with suppressed intervals counted as nonreports, and (b) coverage conditional on an interval being reported, together with reporting probability. Neither can be replaced by DKW precision.

For informative acceptance, distinguish the population mean contrast across all interventions from the common-acceptance contrast. The latter is descriptive for the selected stratum and must not be described as the former.

## Physics/NLP scientific falsification

A separate preregistered evaluation must use source-grounded physics interventions, independent human or mechanically verifiable adjudication, heldout problem families, and a baseline that matches model and inference budgets. Test whether any improvement survives family-level holdout, paraphrase perturbations, answer-label permutation controls, and abstention-rate matching. Do not infer model reasoning improvement from statistical wrapper tests.

## Prior-art audit gates

Before claiming novelty, compare against selective classification (Geifman and El-Yaniv 2017), risk-controlling prediction sets (Angelopoulos et al.), conformal risk control (Angelopoulos, Bates et al.), clustered and conditional bootstrap literature, and contemporary physics reasoning evaluation protocols. Record exact paper titles, versions, dates, methodological overlap, and what the proposed method adds beyond each. These are *search targets*, not a completed 2026 literature review.

## Execution and publication safeguards

Only execute on a verified zero-cost cloud runner after checking account-specific billing state, public-repository eligibility, workflow permissions and limits. No local laptop compute or large downloads. Store code revision, environment, seed manifest, full logs, failed cases, and provenance. Do not claim passing tests until actual cloud logs are reviewed. November 22 is a conditional internal target; a limitations report is preferable to unsupported novelty claims.
