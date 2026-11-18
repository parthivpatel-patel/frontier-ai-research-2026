# Matched-budget selective-risk estimand and leakage audit (2026-11-18)

**Status:** prospective methodological specification, not an experiment, preregistration amendment, or evidence of novelty. Complements `CROSS_DOMAIN_VERIFIER_FALSIFICATION_GATE_2026-11-18.md`. Do not describe this as frozen until its Git object, external timing, and pre-outcome status have been independently verified.

## Exact estimand

Let domain `d` range over NLP, mathematics, and physics. Let `g` index independent source families and `i` examples within each family. A fixed candidate answer has adjudicated binary error `E_dgi ∈ {0,1}`. For method `m`, `A_m,dgi(t) ∈ {0,1}` indicates answering under a threshold selected *exclusively on calibration families*. Define test coverage `C_md = sum(A)/N_d` and selective risk `R_md = sum(A E)/sum(A)`. If `sum(A)=0`, risk is undefined and must be reported as such, never as zero.

For each prespecified target calibration coverage `c ∈ {0.50,0.70,0.90}`, use the calibration-family score quantile to choose threshold `t_mdc`, with deterministic hash-based tie-breaking fixed before outcomes. On the held-out families report **both achieved coverage and risk**, rather than forcing test coverage by using held-out scores/labels. The primary contrast is `Δ_dc = R_proposed,dc − R_strongest-eligible-baseline,dc`; negative favors the proposed rule. Select the strongest baseline on calibration/validation families, never on held-out outcomes. Macro-average the three domain contrasts with equal domain weight; also show every domain and coverage cell.

## What is a matched budget?

Measure verifier cost per item as at least (1) number of additional model calls, (2) input/output tokens if available, (3) tool invocations, and (4) wall-clock time in the cloud environment. Fix a primary resource constraint *before evaluation*; do not use dollar cost alone, which can hide unequal free-tier subsidies. Every baseline must receive the same candidate answer and comparable allowed evidence. If a method exceeds the limit, count it as a budget violation and report separately; never drop expensive failures. When a method uses privileged labels or retrieval, mark the comparison non-equivalent.

## Clustered inference

Resample source-family identifiers with replacement **within each domain**; carry all examples and all methods for each sampled family together. Recompute held-out selective risks using the frozen thresholds; obtain paired bootstrap contrasts and percentile intervals. The effective replication unit is the family, not the question. Report the number of independent families and per-domain family-size distributions. With very few families, bootstrap intervals can be unstable; disclose that and use descriptive analysis rather than spurious precision. Prespecify a practical improvement margin `ε > 0` based on an independently justified deployment loss, not on observed results. A superiority claim requires the upper confidence bound for the primary macro contrast below `−ε`, with no material domain-specific harm under a separately fixed safety margin. If these margins are not frozen before outcomes, report exploratory estimates only.

## Data firewall and contamination audit

1. Record dataset version, original source URL, publication date, licensing, collection timestamp, candidate model and generation date, and whether any labels were publicly available during model training.
2. Normalize whitespace and notation for candidate duplicate detection; retain original text and hashes. Use exact hashes, near-duplicate text similarity, template/author provenance and source metadata. A text similarity score alone cannot establish independence.
3. Assign whole source-family clusters to calibration, validation, or held-out evaluation before fitting thresholds, feature weights, prompts, or baseline choices. Preserve an immutable assignment manifest.
4. Avoid benchmark test sets that were used to select prompts or score weights. If contamination cannot be excluded, label the evaluation as potentially contaminated and refrain from clean generalization claims.
5. In physics, verify units/dimensions and numerical tolerances separately from conceptual correctness; dimensional consistency is necessary in some problems but not sufficient for a correct physical explanation. In mathematics, a correct final numeric answer does not certify the reasoning chain. In NLP, answer–evidence agreement does not guarantee evidence truth.
6. Store blinded adjudication protocol and disagreement resolution. Never let the proposed verifier assign its own ground-truth labels.

## Negative controls and ablations

- **Randomized signal:** permute verifier scores only *within calibration strata* for a negative-control comparison; a nontrivial gain suggests leakage or an implementation error.
- **Missing-evidence control:** remove retrieval/evidence features without altering the candidate answers; check whether claimed verification relies on unavailable privileged information.
- **Domain ablation:** compare domain-specific models to one shared scoring rule, with the same training/calibration budget.
- **Physics-specific control:** test dimensionally valid but physically false answers, to prevent unit-checking from masquerading as correctness.
- **Math-specific control:** test correct final answers accompanied by invalid derivations, and incorrect answers with plausible intermediate steps.
- **NLP-specific control:** test fluent but unsupported claims and contradiction/entailment edge cases with independent evidence.

## Predeclared stop/go decision

**NO-GO** for confirmatory superiority until the complete held-out source inventory, baseline selection rule, cost meter, label policy, margins, sample-size feasibility and calibration assumptions are frozen with verifiable provenance. If no independently verified $0 cloud quota is available, publish the protocol or a clearly labeled toy demonstration only; do not claim empirical model improvement.

## Closest methodological antecedents to check in full text

Selective classification (Geifman & El-Yaniv, 2017); conformal risk control (Angelopoulos et al., 2024); language-model uncertainty elicitation (Kadavath et al., 2022; Lin et al., 2022); verifier training (Cobbe et al., 2021; Lightman et al., 2023). These are candidate references, not a complete novelty search. Audit recent literature and release dates before submitting any priority claim.

**Scientific integrity:** Negative results, null gains, and infeasibility are publishable findings if the underlying evaluation is reproducible and honestly characterized. No results are reported in this document.
