# Protocol 178 — Counterfactual pair validity and leakage audit

Date: 2026-11-10. Status: prospective, not executed. This protocol supplements Protocols 176–177; no independent annotations, benchmark scores, or novelty claims.

## Critical distinction: changing the premise versus changing the reasoning step

A fixed step can become valid or invalid after a premise edit only if the edited premise is both physically coherent and causally relevant to that exact step. Editing a numeric value may alter the final answer while leaving the step's inference rule valid. Conversely, a step can be invalid in both versions. Neither outcome supports a successful intervention merely because the verifier's output flips.

Define a paired unit i = (x_i, x'_i, r_i), where x is the original problem, x' is a single controlled edit, and r is the **byte-identical** reasoning step evaluated in both contexts. Adjudicators assign y_i and y'_i independently in {valid, invalid, underdetermined}; only then classify the pair as truth-changing, truth-preserving paraphrase, irrelevant placebo, or ambiguous. A 'valid' step must follow from the stated assumptions; physical plausibility alone is insufficient.

## Three illustrative synthetic cases (not observations)

1. **Truth-changing**: Context A states an ideal frictionless horizontal surface; context B states kinetic friction coefficient 0.20 on the same surface. Fixed step: 'The horizontal friction force is zero.' Under an explicitly sliding object and nonzero normal force, this is valid in A and invalid in B. The pair requires confirmation that the object is sliding and the normal force is positive.
2. **Truth-preserving**: 'Ignore air resistance' versus 'Assume drag is negligible' with the same fixed step 'No drag term enters the equation.' Both are valid within the stipulated idealization; a verifier flip is a false sensitivity signal.
3. **Irrelevant placebo**: Change the object's color from blue to green, leaving the dynamics and fixed step unchanged. A verdict flip is spurious unless color was explicitly made physically relevant.

These examples are author-created test specifications, not a pilot dataset and not independent ground truth. Avoid distributing them as empirical evidence.

## Mandatory leakage and confound checklist

- **Answer leakage**: remove solution keys, benchmark labels, editorial explanations, and verifier-specific cues from all input variants. Maintain separate sealed annotation and evaluation records.
- **Edit artifacts**: balance edit lengths, syntax, and location; a model must not infer the label from which sentence was changed.
- **Source-span shortcuts**: compare correct span+scope links with shuffled links **within matched constraint types**. Unrestricted shuffling may create trivially nonsensical inputs and overstate the benefit.
- **Rule inventory parity**: provenance and non-provenance checkers receive identical equations, numerical tolerances, rule inventory, and compute budget; only provenance links differ.
- **Correlated variants**: all edits, paraphrases, and step variants from one source problem remain in one split and one resampling cluster.
- **Underdetermination**: missing assumptions must permit an 'underdetermined' label, not be silently converted to invalid.
- **Selection**: report counts of proposed, rejected, adjudicated, unresolved, and evaluated pairs, by physics family and intervention stratum.
- **Contamination**: identify whether source problems are public benchmark items and whether the candidate verifier or judge may have encountered them in training. No contamination-free claim without evidence.

## Blind adjudication decision rule

Two independent adjudicators label each (context, step) without seeing model outputs or whether the context is original/edited. They record the governing source span, scope, assumptions, and a short derivation. Disagreements go to a documented third-party resolution; unresolved pairs remain reported and excluded from primary accuracy analysis. No invented annotators or adjudication outcomes.

## Prospective metrics and falsification

Primary: difference in source-equal-weighted **correct verdict yield over all eligible pairs** at frozen, matched coverage, with abstentions counted separately and explicitly in the denominator. Secondary: false rejection of valid steps, false acceptance of invalid steps, false flips on truth-preserving/placebo edits, and directionally correct flips on truth-changing edits. Present paired source-cluster uncertainty and per-family breakdowns; do not treat variants as independent. Freeze evaluation choices before test-label access.

Failure conditions: provenance advantage disappears when rule inventory is matched; shuffled **type-matched** linkage performs equally well; false-flip rates increase substantially; gains occur only on public/seen physics families; or label ambiguity prevents a reliable comparison. An underpowered or incomplete pilot is inconclusive, not positive.

## Minimal cloud execution gate

No new workload until GitHub Actions account-specific free entitlement, spending cap/billing behavior, storage, and runner permissions are verified. Existing 696 passing tests establish code regression health only. A low-cost CPU-only pilot is preferable to model training, but even that must not run until zero-charge eligibility is established. No local laptop workload.

## Publication integrity

Separate synthetic examples, authored specifications, independently annotated observations, and model-generated outputs in all tables. Archive protocol version, commit, input hashes, licenses, annotation decisions, and code. Disclose AI assistance as required. November 22 is a conditional internal target, not a publication promise.
