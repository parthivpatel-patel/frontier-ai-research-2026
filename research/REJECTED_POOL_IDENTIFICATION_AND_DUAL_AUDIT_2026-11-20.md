# Accepted-only auditing cannot certify rejected-answer quality
Date: 2026-11-20
Status: theoretical identification note; no model results

## Scope and relationship to existing work
This note strengthens the preregistered NLP, mathematics, and physics verifier evaluation. The target remains **accepted-answer error at matched domain-specific coverage and compute**. This is not a new theorem or a claim of superior AI performance.

Related work: Anthony and Salehzadeh Nobari, *Finite-Sample Coverage Audits for High-Recall Candidate Generation: Certification and Learning-Theoretic Design* (2026), https://arxiv.org/abs/2607.21480, shows why auditing only included candidates cannot certify missed relevant mass. Also compare selective classification and selective conformal risk control. A full-text novelty comparison remains pending.

## Identification distinction
For each domain d, freeze an evaluation population of N_d prompts, generated answers, verifier decisions A_i in {0,1}, and independently adjudicated correctness Y_i in {0,1}. Define:
- coverage C_d = sum_i A_i/N_d;
- accepted error R_d^+ = sum_i A_i(1-Y_i)/sum_i A_i (undefined if no accepted answers);
- rejected correct-answer mass M_d^- = sum_i (1-A_i)Y_i/N_d;
- rejection false-negative rate F_d^- = sum_i (1-A_i)Y_i/sum_i (1-A_i), undefined if none rejected.

Accepted-only audits can estimate R_d^+ under an appropriate probability sample. They **cannot identify** M_d^- or F_d^- without additional assumptions: hold accepted answers and their observed labels fixed, then assign all rejected Y_i=0 versus all rejected Y_i=1. Both worlds yield identical accepted-only observations but opposite rejected correctness. The sharp logical bound for M_d^- without rejected labels is [0, 1-C_d]. This is a basic nonidentification argument, not original mathematics.

## Preregistered dual-pool audit
1. Freeze tasks, model-generated answers, verifier scores, threshold, domain, source identifier, answer provenance, and compute logs **before** any independent labels are revealed.
2. Randomly sample accepted and rejected pools separately with recorded inclusion probabilities; sample without replacement within each domain and source stratum.
3. Independently adjudicate both pools using domain-specific protocols: exact proofs or symbolic checks plus expert review for mathematics, dimension/assumption/physical-law checks for physics, and reference-supported human adjudication for NLP. Record ambiguous/invalid labels as unresolved, not correct.
4. Report accepted error and rejected correct-answer mass with design-valid confidence intervals; if a stratum is unsampled, report worst-case partial-identification bounds instead of a point estimate.
5. Compare frozen baseline and proposed verifier on the **same** tasks and generated answers at matched coverage and compute, reporting paired disagreements and all four acceptance/correctness cells. Cross-domain macro averages must not conceal domain failures.
6. Do not claim distribution-free future-shift guarantees from finite-population audits. Hold out sources/time periods; report uncertainty and shift failures explicitly.

## Falsification and publication gates
- If rejected-pool correctness is substantial, an accepted-only audit cannot support a broad quality claim about the verifier's decision policy.
- If gains disappear at matched coverage, model/answer provenance, or compute, reject the performance hypothesis.
- If gains reverse for any domain or held-out source, disclose heterogeneity and do not claim universal improvement.
- If independent adjudication is too incomplete to distinguish hypotheses, publish partial-identification bounds only.
- If this design is already covered by closest prior art, present it as a replication or integration protocol, not a novel algorithm.
- No claimed theorem, new empirical results, or deployment guarantee until code, cloud CI, source-held-out evaluation, and independent review are available.

## Cloud feasibility and cost gate
GitHub documentation (checked 2026-11-20) states standard GitHub-hosted runners in **public** repositories are free; larger/GPU runners are billable, and artifact/cache storage has separate quotas: https://docs.github.com/en/actions/concepts/billing-and-usage and https://docs.github.com/en/billing/concepts/product-billing/github-actions. Account-specific billing settings and remaining storage are not verified. Therefore do not dispatch compute or store large artifacts until checked. No local laptop workload is authorized.

## Next reproducibility deliverable
Implement a small standard-runner CI test (no model inference, no downloads) that enumerates toy accepted/rejected labels and checks sharp bounds, undefined-denominator handling, and stratified sampling calculations. Then obtain independent held-out labeled tasks with licensing/provenance records. Until then, Nov 22 is a conditional methods-paper checkpoint, not an empirical discovery deadline.
