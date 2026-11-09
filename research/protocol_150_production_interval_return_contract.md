# Protocol 150 — Production interval-return contract and correction to the binomial-tail abstraction

Date: 2026-11-08. Status: static source audit only; no experiment or CI execution.

## Inspected implementation

On the public main branch, inspected `research/admitted_preflight_bootstrap.py`, `research/preflight_gated_bootstrap.py`, and `research/safeguarded_admitted_bootstrap.py`. The first validates heldout matched interventions and exact family-weight keys, then invokes the preflight wrapper. The wrapper computes an analytic eligibility gate before calling `common_acceptance_bootstrap` with `max_undefined_fraction=1.0`, preserving its bootstrap diagnostics. It replaces `ci95` with `None` whenever `gate["interval_eligible"]` is false. The safeguard then additionally suppresses `ci95` when `defined_replicates < min_defined_replicates` (default 1000), and validates any non-null endpoints for finiteness and ordering.

## Corrected contract

Protocols 148–149 correctly label the binomial-tail expression as conditional on an **if and only if** rule requiring at least m valid replicates. That rule is NOT the complete production interval-return contract. For a fixed admitted dataset X, let G(X) denote analytic eligibility, K the number of finite bootstrap replicates, M the configured minimum, and U(X,draws) denote upstream interval construction returning a non-null valid interval. The safeguarded reporting indicator is

R = 1{G(X)} 1{K >= M} 1{U(X,draws)}.

The gate is seed-independent for fixed X; K and U may depend on the bootstrap draws. Therefore, conditional on X,

P(R=0 | X) = 1 - 1{G(X)} P(K >= M and U | X).

If U is guaranteed whenever K>=M, and the replicate-validity indicators are conditionally independent Bernoulli with invalidity probability q(X), the expression reduces to

P(R=0 | X) = 1 - 1{G(X)} [1 - g_{B,M}(q(X))],

where g is the Protocol 148 binomial lower tail. If U has additional failure modes, this reduced expression is a **lower bound** on interval unavailability when G=1, not an equality. For G=0, interval unavailability is exactly one, even when every replicate is defined. For admitted outer datasets, average the conditional unavailability over X; never plug in mean q or mean G as if the expression were linear.

The analytic gate threshold on *single-replicate* denominator failure must not be conflated with interval-return probability or nominal 95% coverage. A 1% analytic gate does not imply 99% interval availability or 95% coverage.

## Deterministic falsification cases (cloud only after verified free eligibility)

1. Construct a valid admitted heldout fixture with analytic gate false but K>=M. The final safeguarded interval MUST be null.
2. Construct a gate-true fixture with K<M. The final interval MUST be null and suppression reason must identify insufficient defined draws.
3. Construct a gate-true fixture with K>=M and valid upstream interval. The final interval MUST be reported.
4. Construct a gate-true fixture with K>=M but upstream interval null. The final interval MUST be null and suppression reason must identify upstream eligibility or undefined estimate.
5. Confirm malformed/nonfinite upstream interval endpoints cause validation failure, not a false success.
6. Compare fixed-X exact small-case enumeration with the complete three-factor return indicator; separately report admission failures, analytic gate failures, insufficient finite replicates, and upstream construction failures.
7. Evaluate outer-dataset abstention, conditional coverage, and unconditional coverage separately with independent outer datasets. Do not treat bootstrap draws as independent outer observations.

These are specifications, NOT claims that fixtures have run or passed. In particular, whether U is guaranteed when K>=M requires inspecting and instrumenting the upstream bootstrap implementation. The analytic preflight's actual edge-case behavior must also be tested.

## Publication and novelty boundary

The factorization is ordinary conditional probability and software contract tracing, not a novel statistical theorem. Existing bootstrap, selective-inference, abstention, and scientific verification literature remain closest-prior-art categories. A defensible AI/ML/NLP/physics contribution requires a frozen physical estimand, independently adjudicated natural-language claims, heldout source-disjoint comparisons, uncertainty accounting, and demonstrable advantage against non-LLM and competitive baselines. Falsify the claimed advantage if gains vanish under source-disjoint evaluation or depend on post-hoc selection. Do not claim paper readiness based on protocol count.

## Resource and execution boundary

No local compute, model inference, simulation, cloud job, or paid resource initiated. Account-specific GitHub Actions free quota, billing limits and runner eligibility remain unverified; do not dispatch workflows. Existing pytest dependency CI failure remains open. November 22 remains a conditional internal target.
