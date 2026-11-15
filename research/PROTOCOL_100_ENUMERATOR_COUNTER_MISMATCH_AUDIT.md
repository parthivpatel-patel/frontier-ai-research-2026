# Protocol 100 — Enumerator counter mismatch and minimal acceptance repair

Date: 2026-11-15. Status: source-level audit and proposed acceptance tests; **not executed**.

## Confirmed source-level issue

Protocol 098's `structural_count` counts complete policies, while Protocol 093's `count[0]` counts generator entry and yielded non-stop construction events, including repeated generation of left and right continuation sets. Protocol 099 currently passes `max_trees` as the Protocol 093 internal `cap`, and subsequently compares the returned `ntrees` with the structural prediction. Although the final comparison is conceptually appropriate, the earlier internal cap can reject a structurally admitted instance. Thus Protocol 099's advertised structural admission does **not** imply that an admitted certificate will run under the same numerical cap. This is a reproducibility/availability bug, not a demonstrated wrong optimal value.

Smallest witness: one claim, cost 1, budget 1, masses P(0)=P(1)=1/2. Structural policy count is 2 (STOP or verify). The Protocol 093 generator increments its internal counter four times: root entry, two continuation entries, and constructed verify tree. Therefore `bounded_certify((1,),1,worlds,max_trees=2)` is structurally admitted but raises `Intractable` before returning its expected optimal value 1/2 and 2 completed policies. These are **source-derived predictions**, not executed test results.

## Required fix and independently testable contracts

1. Keep distinct names: `max_complete_policies` for the structural admission ceiling, `max_generator_events` for the internal generation ceiling. Never pass one as the other or interpret one as a memory/time bound.
2. Preserve the exact `ntrees == structural_count(...)` assertion **only after** enumeration completes; `ntrees` is the number of completed root policies, not generator events.
3. A tiny-case regression must assert `structural_count((1,),1,2)==2`, `certify((1,),1,worlds,cap=4)==(Fraction(1,2),witness,2)` up to witness shape, and that a cap of 2 raises `Intractable`. Verify STOP and the verify tree both score correctly.
4. Add a separate test asserting that a structurally admitted case with a deliberately insufficient generator-event cap is reported as **resource-refused**, not as failed mathematical optimality.
5. For the three-claim, budget-two case, compare the structural count with the number of completed policies only after a sufficiently permissive internal cap, under an externally imposed cloud process wall-time and memory ceiling.
6. Never use generator-event count as a proxy for peak resident memory: Protocol 093 materializes two continuation tuples at every branching action.

## Experimental and publication gates

This issue must be fixed and cloud-tested before calling Protocol 099 an operational certificate. Run minimal unit tests first in a verified no-cost, account-eligible cloud environment; then run exact cross-oracle comparisons and injected-defect mutation tests. Keep experiments with NLP, mathematics, and physics adjudications separate from these synthetic oracle checks. A numerical optimizer passing synthetic tests cannot by itself support a claim about scientific truth, calibrated probabilities, or novel research.

No model inference, dataset download, or local laptop workload is required for this source audit. No cloud availability, billing eligibility, or quota is established by this document. Do not start jobs without independently confirming the provider's current free terms and the user's eligibility. Nov 22 remains a conditional decision checkpoint, not a publication commitment.
