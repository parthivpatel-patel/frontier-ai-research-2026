# Temporal-evidence ablation and negative-control protocol (2026-11-20)

Status: preregistration / design only. No experimental outcome or novelty claim.

## Narrow research question

At a fixed verification budget and a fixed acceptance coverage, does an independently specified temporal-consistency signal reduce incorrect accepted answers beyond a strong confidence-only verifier, on held-out NLP, mathematics, and physics tasks? The null hypothesis is no improvement; the alternative is a reproducible reduction under paired, independently adjudicated evaluation. The research must not claim that selective prediction, conformal risk control, exact audit bounds, or temporal logic are new.

## Definitions and units

An evaluation unit is a frozen prompt, model response, and independent ground-truth adjudication. Group all variants of a source problem (paraphrases, translated versions, numeric substitutions, shared derivations) into one family, and split by family before any threshold selection. Let y_i=1 denote a wrong response. Let A_i^p in {0,1} indicate acceptance by policy p. For fixed acceptance count k>0, the accepted error rate is R_p=(sum_i A_i^p y_i)/k. Report coverage k/n separately and never silently substitute an intersection-only sample.

For two policies p,q with the same k, the exact paired identity is:

k(R_p-R_q) = sum_{i:A_i^p=1,A_i^q=0} y_i - sum_{i:A_i^p=0,A_i^q=1} y_i.

This is an accounting identity, not a new theorem. If k=0, R is undefined and the comparison is not certified.

## Precommitted arms

- C: baseline answer confidence / verifier score without temporal features.
- T: identical budget and scoring pipeline with temporal-consistency features.
- S: sham temporal features computed from time-shuffled or randomly paired trajectories with the same feature dimension and extraction cost.
- F: a stronger conventional non-temporal feature baseline with the same number of learned parameters or comparable tuning effort, to guard against generic feature-capacity gains.

All feature definitions, time windows, scoring code, seeds, thresholds and adjudication rules must be frozen before held-out labels are accessed. If real temporal traces are unavailable, label the study as not feasible rather than fabricating trajectories.

## Negative controls and leakage

1. Shuffle temporal order within a task while retaining token counts and marginal score distributions. If T's benefit persists unchanged, temporal ordering is not supported as the cause.
2. Pair each response with a different task's trace matched by length and difficulty. A gain here suggests confounding or metadata leakage.
3. Evaluate family-held-out splits, and leave-one-domain-out transfer for NLP, mathematics and physics. Cross-domain transfer must not be inferred from pooled averages.
4. Repeat without source-identifying fields, timestamps, answer length and formatting artifacts; record the effect of each exclusion.
5. Use independent correctness adjudicators blinded to the policy arm. Record unresolved disagreements; do not convert missing labels into correct answers.

## Statistical comparison

For each frozen domain and coverage target, report k, n, error counts, exclusive-acceptance error counts, paired risk difference, and uncertainty intervals. The primary estimand is the paired accepted-error-rate difference at equal coverage, not an intersection-only error difference. Preserve the complete accepted and rejected pools; audit both for false acceptance and false rejection. Account for multiple domains, coverages, and looks; a fixed-size holdout is the default. No post-hoc choice of the best coverage is permitted. Report abstention cost and wall-clock/compute budget.

## Falsification / no-go conditions

- No independent ground-truth labels or genuinely held-out source families.
- Missing genuine temporal evidence or uncontrolled extra compute for T.
- Improvement disappears against C or F at matched coverage and budget.
- Sham or mismatched temporal features match T's gains.
- Results reverse materially across domains or are driven by a single source family.
- Confidence bounds cannot exclude a prespecified negligible effect, or selective-risk guarantees fail their validity assumptions.
- Literature establishes the same combined experimental contribution.

Each outcome, including null or inconclusive results, should be published transparently. No causal mediation or physical-world reasoning improvement follows from a positive paired-risk comparison alone.

## Publication gate for 2026-11-22

A methods/preregistration release may describe this as a testable synthesis, with explicit prior art and disclosure. An empirical discovery paper requires independent held-out results, reproducible free-cloud runs, robust ablations and documented comparison with the closest full-text prior work. A new theorem requires a genuinely new statement and proof checked independently. The date is a checkpoint, not evidence.

## Execution and resource constraints

Use only free, standard GitHub-hosted runners for lightweight Python tests after verifying repository and account eligibility, workflow configuration, and current GitHub pricing. Do not enable larger runners, paid APIs, cloud billing, GPUs or model downloads. Do not execute any compute on the user's laptop. If free hosted access cannot be verified, leave experiments unrun and record the blocker. Avoid presenting synthetic mathematical checks as model validation.
