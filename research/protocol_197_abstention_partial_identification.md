# Protocol 197 — Abstention-robust paired identification bounds

Date: 2026-11-11. Status: analytic specification only; no executed tests, model responses, or scientific findings.

## Problem

Protocol 196 defines D=E[T(0)-T(1)] for binary acceptance T, while also requiring abstentions to be retained. These requirements are not jointly sufficient: T is undefined for abstention, and dropping such cases can create selective attrition. This protocol preregisters identification bounds that do not require missing-at-random assumptions.

## Three-category observation and complete-pair estimand

For each preselected independent physics problem i and condition z in {0,1}, record R_i(z) in {A=accept, J=reject, U=abstain}; distinguish abstention from technical failure F (request error, unavailable model). Do not equate F with U. Define K_i=1 if both responses are A/J and K_i=0 otherwise. Let n be the number of preselected pairs, m the number with K_i=1, and S=sum over K_i=1 of [1{R_i(0)=A}-1{R_i(1)=A}]. The complete-pair descriptive contrast is D_CC=S/m if m>0, but is not a population effect without additional assumptions. Publish m/n and each condition's abstention and failure counts.

## Worst-case bounds

If an abstention is treated as an unobserved binary acceptance, each incomplete pair's latent difference lies in [-1,1], yielding conservative bounds (S-(n-m))/n <= D <= (S+(n-m))/n. These bounds are valid but can be sharpened using observed outcomes on the other arm. For each pair define acceptance interval [l_iz,u_iz]: A -> [1,1], J -> [0,0], U or F -> [0,1]. Then define d_i lower=l_i0-u_i1, upper=u_i0-l_i1. The sharp finite-sample bounds under unrestricted missing acceptance values are L=sum(lower)/n and U=sum(upper)/n. They are sharp because each missing acceptance can independently attain either endpoint. This is partial identification, not a confidence interval. Report the interval width and how much missingness drives it. For repeated templates, average bounds within problem before averaging across problems; predefine the weighting.

## Abstention as a substantive outcome

Report unconditional rates of correct accept on genuine provenance, correct reject on corrupted provenance, incorrect responses, and abstention, with technical failures separate. A conservative correct-classification rate counts U as not correct but does not assert that U is an incorrect scientific belief. Publish the 3x3 paired response transition table (A/J/U); report F separately. The binary complete-case 2x2 table is secondary.

## Decision gates and falsification

A claim that D exceeds preregistered minimum meaningful threshold delta>0 requires the *lower identification bound* L>delta before uncertainty is considered. If L<=delta, an unconditional discrimination claim is not identified without assumptions. If all pairs are complete, L=U=D and Protocol 196 applies. Sampling uncertainty must be computed separately (e.g. cluster bootstrap of pair-level lower and upper endpoints, with explicit small-sample caveats); never present identification bounds as 95% confidence bounds. A formal confidence region for partially identified parameters needs an appropriate procedure fixed in advance. Never impute U or F after inspecting outcomes, or silently exclude requests that failed.

## Additional threats

The graph intervention can affect abstention probability itself, so answered-only contrasts condition on a post-intervention variable. Model refusals may reflect policy or uncertainty rather than provenance reasoning. If original and corrupted arms are run at different times, model drift and service failures can induce nonexchangeable missingness. Randomize order and record version/timestamp. Bounds do not solve semantic-label errors, presentation confounding, or model-version drift.

## Verification examples (analytic, not executed)

- One complete (A,J) pair: S=1, m=n=1, L=U=1.
- One pair (A,U): d in [0,1]; coarse bound [-1,1] is valid but not sharp.
- One pair (U,J): d in [0,1].
- One pair (U,U): d in [-1,1].
- Two pairs (A,J) and (J,U): sharp aggregate bounds [0,0.5], not a positive lower bound.
- One pair (F,J): acceptance contrast in [0,1] for the unobserved counterfactual response; F must be separately flagged as an operational failure.

## Prior art and contribution boundary

Worst-case missing-outcome bounds are standard partial-identification reasoning, associated with Charles Manski's work on nonparametric bounds. This protocol makes no claim that these bounds are novel. A novel empirical contribution would require a demonstrably distinct scientific question and rigorous physics-grounded evidence beyond existing citation attribution, counterfactual explanation faithfulness, and selective prediction studies. Full-text novelty audit remains open.

## Execution and cost

No cloud runner, model, inference API, test or local compute was used to establish this document. GitHub account-specific free eligibility, runner quota, billing/card constraints and availability are not verified. Do not dispatch until the recorded cost gate in Protocol 195 is satisfied. Laptop remains browser-only; no paid fallback. November 22 is conditional on reproducible evidence.
