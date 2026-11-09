# Protocol 156 — Family-weighted evaluation and dependence audit (9 November 2026)

Status: preregistered analysis specification only. No model execution, verified novel contribution, or empirical finding.

## Problem with the Protocol 155 pooled estimand

Protocol 155 defines case-averaged correct-answer yield. That estimand implicitly weights a physics family in proportion to its number of test cases and paraphrases. If a benchmark contains 100 paraphrases of one mechanics problem and one instance of another family, naive pooling can make the first problem dominate. This is a benchmark-design choice, not a mathematical guarantee of generalization.

Predeclare two different target populations rather than selecting the more favorable result afterward.

**Case-mix estimand:** for frozen cases i=1,...,n, u_case(m) = (1/n) sum_i S_mi Y_mi. This measures performance on the actual manifest's case distribution.

**Equal-family estimand:** for F nonempty held-out physics families, u_family(m) = (1/F) sum_f [(1/n_f) sum_{i in f} S_mi Y_mi]. This measures a uniformly sampled family followed by a uniformly sampled case within that family. It is *not* the same as a uniformly sampled real-world problem unless that sampling design is justified.

For comparisons A vs B, calculate paired differences within each family before averaging. Report both estimands with their distinct denominators, alongside return rate, unconditional wrong-answer rate, and conditional correctness. A family with no returned answers has undefined selective accuracy, but still has well-defined unconditional correct-answer yield (zero).

## Dependence and paraphrases

A paraphrase is not a new independent physical phenomenon. Define an immutable base_problem_id and family_id in the evaluation manifest. Keep all paraphrases, numerical variants with shared solutions, and correlated interventions in the same split group. No training, calibration, prompt tuning, or threshold selection may use a held-out base problem or its paraphrases.

For uncertainty, the resampling unit must reflect the sampling design. If families themselves are sampled as exchangeable independent units, resample whole families and carry all their problems and paraphrases together. If families are fixed and problems are sampled independently within families, a stratified problem-cluster bootstrap can instead target conditional inference on those fixed families. Do not claim population-level inference across new physics families from a fixed, handpicked set of families.

Small numbers of families make asymptotic intervals unreliable; report raw family-level paired differences, the number of independent families, and sensitivity to leave-one-family-out removal. Never substitute the number of paraphrases for the number of independent clusters.

## A deterministic counterexample

Family A has 100 cases, all correct for method X and all wrong for method Y. Family B has one case, wrong for X and correct for Y. Both always answer.

- Case-mix correct-answer yield: X = 100/101, Y = 1/101.
- Equal-family correct-answer yield: X = 1/2, Y = 1/2.

This is a constructed arithmetic example, not an AI experiment. It demonstrates why a strong pooled benchmark result alone cannot justify a family-generalization claim.

## Predeclared robustness and falsification gates

1. Freeze the primary target estimand before viewing held-out outcomes; show the other as sensitivity analysis.
2. Report per-family sample sizes, base-problem counts, paraphrase counts, return rates, and error rates.
3. Treat a sign reversal between case-mix and family-weighted effects as evidence of target-population sensitivity, not as a success.
4. Do not claim transfer to unseen physics families unless held-out families were selected independently and performance survives a family-level evaluation.
5. Reject an NLP robustness claim if gains disappear when correlated paraphrases are grouped by base problem.
6. Include leave-one-family-out sensitivity; no post-hoc deletion of a difficult family.
7. Separate point-estimate correctness, physical consistency, calibration/coverage, and abstention; a favorable score in one cannot stand in for another.
8. Preserve failed and undefined runs and report denominators and predeclared handling.

## Implementation-ready, cloud-only plan

Add manifest fields: family_id, base_problem_id, paraphrase_id, split, answer_key_version, physics_parameter_units, scoring_rubric_version, and immutable content digest. Add a deterministic standard-library test for the counterexample and zero-return edge case. Execute tests only on a verified zero-cost cloud runner with account-specific quota and billing checks. No local training, inference, downloads, or simulations are authorized.

## Novelty boundary

Family-weighted evaluation, clustered uncertainty, and hierarchical generalization are established methodological ideas. This protocol is a safeguard against misleading claims, not a new AI method or proof of novel physics reasoning. Compare against selective prediction, conformal risk control, and verification research before asserting a contribution. All actual empirical conclusions await cloud-executed, independently reproducible experiments.

Strict spending: $0. Publication target: 22 November 2026, conditional on evidence and disclosure compliance.
