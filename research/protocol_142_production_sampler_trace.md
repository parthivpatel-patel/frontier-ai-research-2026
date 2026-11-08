# Protocol 142 — Production sampler trace (2026-11-08)

Static source inspection only; not an executed experiment.

Inspected research/common_acceptance_bootstrap.py, research/analytic_preflight.py, research/preflight_gated_bootstrap.py and research/admitted_preflight_bootstrap.py on main.

## Finding
The production bootstrap initializes Random(seed) once, then for every replicate iterates over sorted positive-weight families. Within each family it independently makes n_f calls to rng.randrange(n_f), accumulating multiplicities keyed by (physics_family, lineage_id). It does NOT reuse a common index vector across families. A common RNG stream does not imply common-index coupling. Under the ideal independent uniform draw model, the appropriate denominator-failure oracle is Protocol 135, not the counterfactual shared-index Protocols 137–140.

The analytic preflight computes q_f=((n_f-k_f)/n_f)**n_f, where k_f counts lineages with at least one jointly accepted intervention, then q_any=1-product_f(1-q_f). This is consistent with the inspected sampler's design. The wrapper gates percentile CI output on this analytic eligibility criterion, while retaining bootstrap diagnostics.

## Limitations
Static inspection is not an instrumented execution trace. Confirm index sequences with deterministic tiny fixtures and verify no alternate sampler is used for reported results. PRNG calls are pseudorandom; statistical independence is a design model. Undefined replicates are excluded from the percentile distribution; nominal coverage remains unverified. This finding does not establish scientific novelty or improved physics/NLP reasoning.

A real GitHub Actions run on 2026-11-08, https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/42498363883, failed at "Run Python standard-library tests". The jobs metadata does not expose the traceback. Obtain logs before diagnosing or claiming passing tests.

## Next gates
(1) Obtain CI traceback and repair verified failure. (2) Test the production sampler against a separate independent-family exact oracle on tiny fixtures. (3) Estimate independent repeated-sample coverage and abstention with uncertainty. (4) Compare scientific-language and physics baselines with leakage controls. (5) Verify account-level free CI quota and billing/card conditions before dispatching new cloud workloads.

No new cloud job, laptop computation, inference, or spending was initiated for this audit.