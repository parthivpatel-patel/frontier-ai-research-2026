# Protocol 152 — Preflight/point equivalence and execution-order audit

Date: 2026-11-08. Status: static source audit; no tests executed and no empirical claims.

## Inspected production files

- `research/analytic_preflight.py`
- `research/common_acceptance_bootstrap.py`
- `research/preflight_gated_bootstrap.py`
- `research/admitted_preflight_bootstrap.py`
- `research/safeguarded_admitted_bootstrap.py`

This protocol resolves Protocol 151's remaining question about whether the analytic gate can pass while the original paired contrast is undefined.

## Proof under valid complete-pair inputs

Let F+ be the families with strictly positive weights. For family f, let k_f be the number of distinct lineages containing at least one intervention jointly accepted by both systems. The preflight computes `original_defined = all(k_f > 0 for f in F+)` and sets `interval_eligible = original_defined and q_any <= threshold`.

The bootstrap's original multiplicity assigns one copy to every observed lineage in each active family. Its denominator for family f is therefore the number of jointly accepted interventions in that family. This denominator is positive exactly when k_f > 0. Since positive weights are finite and their sum is positive, the original contrast is defined exactly when every active family's denominator is positive.

Consequently, for the same validated complete-pair records, weights and system ordering, **G implies P**; indeed **P iff original_defined**. The converse P implies G does not hold when the exact conditional undefined probability exceeds the preflight threshold. This is an implementation-specific equivalence, not a general theorem about bootstrap methods.

With scientific admission succeeding, normal execution, B >= 1, and safeguard M >= 2, the final interval-return indicator simplifies to

`R(X,D) = 1{G(X)} 1{K(X,D) >= M}`.

The explicit P factor in Protocol 151 is logically redundant *under these assumptions*. For malformed inputs or exceptions, the pipeline fails rather than reporting a statistical abstention. These outcomes require separate end-to-end accounting.

## Operational observation: preflight does not avoid bootstrap work

`preflight_gated_bootstrap` computes the analytic gate **before** invoking `common_acceptance_bootstrap`, but invokes the full requested B-replicate bootstrap **regardless of gate eligibility** and only then suppresses the interval if the gate fails. Thus the current gate is a *reporting* safeguard, not a compute-saving early exit. It preserves undefined-draw diagnostics on ineligible populations. An early-exit optimization would change the diagnostics contract and must not be introduced silently. This matters for zero-cost cloud planning: setting B=2000 still requests 2000 draws on ineligible admitted inputs.

## Falsification and regression specifications

1. Enumerate small valid paired populations with two or more lineages per positive-weight family; assert `analytic_preflight(...)["original_defined"] == (common_acceptance_bootstrap(...)["point"] is not None)`.
2. For gate-eligible inputs, assert the point is defined.
3. Construct a positive-weight family with no jointly accepted interventions; assert `original_defined=False`, `point=None`, and no reported interval.
4. Construct a defined original estimate with a high exact undefined probability and a strict threshold; assert P=true and G=false.
5. Include zero-weight families with no joint acceptance; confirm they do not change point-defined status or preflight active-family calculation.
6. On gate-ineligible but otherwise valid data, assert bootstrap diagnostic counts still sum to B; this captures the existing execution-order contract.
7. For admitted heldout fixtures, verify `interval_reported == (interval_eligible and defined_replicates >= min_defined_replicates)` when calls complete successfully.
8. Test invalid data and admission failures separately; never silently classify exceptions as valid statistical abstentions.

These are proposed tests, not executed results.

## Publication and novelty limits

The proof is a software-contract derivation from the inspected source, not a novel statistical result. Neither interval calibration nor AI/ML/NLP/physics performance is established. Compare future work against established selective prediction, conformal risk control, clustered bootstrap and abstention literature, and disclose any AI assistance required by the eventual venue. Independent physics adjudication, source-disjoint language evaluation, and strong baselines remain prerequisites for any frontier-relevant empirical claim.

## Resource and execution status

No local/laptop computation, model inference, cloud workflow, or paid resource was initiated. GitHub Actions account-specific remaining free quota, billing settings, and card requirements were not established. The previously diagnosed missing-pytest CI issue remains unresolved. The November 22 manuscript target is conditional on verified reproducible evidence.
