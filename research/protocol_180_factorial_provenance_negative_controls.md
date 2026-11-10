# Protocol 180 — Factorial provenance interventions and a negative-control estimand

Date: 2026-11-10. Status: prospective design and mathematical deductions only; no experimental observations. Builds on Protocols 177–179.

## Research question

Does a verifier use the *correct binding* between a source passage and a physical constraint, rather than relying on rule text, answer cues, surface edit patterns, or extra context? A gain from correct provenance links is not enough if the link also supplies additional facts. We therefore require a crossed, information-matched intervention design.

## Factorial design

For each independently adjudicated source problem s and fixed candidate reasoning step, create a controlled physical-context intervention E in {0,1} and a provenance assignment L in {correct, matched-shuffle}. E=0 retains the original physical constraint; E=1 makes one adjudicated physical change. Retain identical rule inventories, numbers of rules, text budgets, inference budgets, and answer visibility across L. Within each E condition, shuffled links must connect spans of the same physical-constraint type and scope. Reject cases without a valid match *before* observing verifier outcomes.

Every crossed cell must have its own independently adjudicated truth label Y_s(E); do not presume Y_s(0) differs from Y_s(1). Pre-register three edit strata: (i) truth-changing edits, (ii) truth-preserving equivalent edits, and (iii) irrelevant-placebo edits. A physical edit is not necessarily a label-changing edit.

Randomize presentation order and provenance assignment using a recorded seed. If the same verifier sees all variants in a stateful conversation, contamination invalidates independence of decisions; use isolated calls or deterministic stateless evaluation. Split by original source problem and, where possible, by physics family before tuning prompts or thresholds.

## Primary paired estimand

Let C_s(E,L) be 1 if the verifier returns the independently adjudicated label, 0 for a wrong verdict or abstention. Average variants *within source* before averaging sources. The provenance effect within edit stratum k is

  tau_k = mean_s [ mean_{E,j in k} { C_s(E,correct) - C_s(E,matched-shuffle) } ].

This is an intervention-specific correct-verdict-yield difference, not a general claim of causal physics understanding. Report coverage and selective accuracy alongside tau_k; report matched-coverage risk with thresholds fixed on source-disjoint development data.

A secondary **edit-response interaction** for paired original/edited cases is

  delta_s = [C_s(1,correct)-C_s(0,correct)] - [C_s(1,shuffle)-C_s(0,shuffle)].

Its mean measures how the provenance advantage changes *across the edit*. It is NOT, by itself, a measure of correct sensitivity to a truth change: both correct labels and difficulty may change, and a method can be correct on both variants without flipping its decision. Report the two cell-wise yields and the interaction; never substitute the interaction for them.

## Directional metamorphic checks

For truth-changing edits, independently determine whether the correct verdict transitions valid->invalid, invalid->valid, or involves underdetermined. Define a *correct transition* only when BOTH outputs match their respective adjudicated labels. For equivalent and irrelevant edits, count false flips separately, including flips to or from abstention. These metrics must not be pooled into a single undifferentiated 'sensitivity' score. Pre-register treatment of underdetermined and abstentions.

For any reported effect, stratify by edit type, label transition, physics family, and presence of explicit numerical constraints. Preserve every unsuccessful edit/adjudication attempt in an attrition log; otherwise filtering may manufacture an apparent advantage.

## Negative controls and failure modes

1. **Link shuffle control:** Type- and scope-matched shuffled spans, with unchanged constraint content.
2. **Formatting control:** Correct and shuffled inputs must have matched token counts and layout; independently flag unnatural shuffled inputs.
3. **No-link control:** All physical rule text retained, links removed; this is not identical to shuffled links.
4. **Placebo edit:** Alter irrelevant surface text without changing physics or adjudicated truth.
5. **Answer-cue control:** Remove final-answer leakage from both methods and verify no benchmark labels appear in prompts.
6. **Blind annotation:** Adjudicators see problem and candidate step, not model identity, link condition, or desired direction of the hypothesis.

If link shuffles are detectable from unnatural text or the correct-link condition carries extra information, the contrast does not isolate provenance. If equivalent/placebo edits trigger many wrong flips, a positive truth-changing edit score is insufficient. If adjudicators disagree or cannot determine labels, report the unresolved proportion and restrict conclusions.

## Inference and stop/go

Primary unit is the original source problem. For a small pilot, publish per-source paired effects and exact counts rather than pretending paraphrases provide independent sample size. Confidence intervals must account for clustering and any family structure; no asymptotic claim with very few clusters. Declare minimum practically meaningful improvement before examining test labels; do not set it from observed effects. Null or negative contrasts, including strong matched-shuffle performance, are legitimate falsifying outcomes.

A pilot may proceed only after: source-disjoint labels and licenses verified; matched interventions pass blinded validity checks; all comparison implementations are executable and frozen; and cloud account entitlement, remaining no-charge quotas, billing/card requirements, and spending safeguards are verified. Do not start jobs merely because a public repository's CI previously passed. Strict $0; no laptop inference or training.

## Publication integrity

This protocol proposes a testable contribution; it does not demonstrate novelty or accuracy. Review 2026 counterfactual verification, process reward, provenance attribution, and formal premise-selection prior art in full text before any novelty claim. Preserve dataset manifests, code hashes, prompt versions, randomization seeds, annotation decisions, failed cases, and AI-assistance disclosures. The November 22 manuscript target is conditional on reproducible evidence.
