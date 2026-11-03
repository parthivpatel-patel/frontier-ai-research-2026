# Protocol 031: verification gates and baseline comparison (3 November 2026)

## Status and scope
This is a prospective analysis plan, **not an experimental result**. The repository currently includes an exact-rational constant-velocity trajectory audit and nine source-level regression tests. Their existence does not prove they passed on a cloud runner. All traces are constructed; there is no observed language-model performance, independent physical measurement, or established novelty.

## Exact model
For rational initial position x0, constant rational velocity v, and positive rational timestep dt, x[t+1] = x[t] + v*dt and v[t+1] = v[t]. Define P[t] := (x[t] >= 0), Q[t] := (x[t] >= 1), R[t] := (v[t] >= 0). For every state Q implies P. P does **not** imply Q; x=0 is a counterexample. These claims are elementary mathematical facts and cannot be presented as a new research contribution.

The implemented audit checks a supplied finite trace, including optional declared predicate labels. It does not prove completeness for all rational states, infer dynamics from data, verify a language model, or validate any physical sensor. It is not an independent parser for the temporal-logic evaluator.

## Competing baselines (required)
1. Explicit finite-state transition-system model checking with the same allowed physical transitions.
2. Predicate abstraction with sound implication constraints and a counterexample refinement procedure (CEGAR).
3. Unconstrained Boolean proposition enumeration, with identical formula corpus and search budget.
4. A deliberately *incorrect* P == Q assumption, reported only as a negative control.
5. A no-physics / syntax-only formula checker, to isolate the benefit of dynamics.

Compare on **soundness**, false equivalence rate, true counterexample retention, bounded completeness, runtime, and witness size. Match input formulas, horizon, and hardware. Report confidence intervals only for genuinely sampled tasks; do not invent significance for exhaustive constructed grids.

## Falsification and leakage controls
- If a correct transition-constrained baseline matches all outcomes at comparable cost, do not claim a new verification capability.
- If adding constraints removes any physically realizable counterexample, the soundness claim fails.
- If a false identity constraint hides a counterexample, record it as an assumption failure, not as a model error.
- If a separate evaluator disagrees with the main evaluator, publish the smallest counterexample and suspend correctness claims.
- If a result depends on manually selected examples, it cannot support generalization to AI-generated specifications.
- Keep generated formulas and test traces separated; lock evaluation cases before tuning methods.
- A bounded search finding no witness is not a proof of global equivalence.

## Literature audit targets (not claims of priority)
Check classic counterexample-guided abstraction refinement (Clarke et al., 2000), predicate abstraction (Graf and Saidi, 1997), bounded model checking (Biere et al., 1999), and established LTL/finite-trace semantics, as well as recent text-to-temporal-logic specification and neuro-symbolic verification papers. Record bibliographic identifiers, exact methodological overlap, and what remains untested. Novelty remains **unestablished** until this comparison is completed.

## Cloud execution and financial gate
Do not trigger a workflow until the repository visibility, account's GitHub Actions allowance and usage, payment settings, and risk of billable overage have been checked from account-specific evidence. Public-repository hosted runner eligibility is not proof of the account's current zero-cost status. No laptop computation. Use short timeouts, read-only permissions, explicit concurrency controls, no external paid APIs, and artifact retention limits. Preserve logs, raw JSON, code commit SHA, runner environment, and file hashes.

## Publication decision
A November 22 manuscript can be a clearly labeled methods/protocol or negative-results preprint if supported by evidence. A novel AI/physics verification claim requires independently executed baselines and adversarial validation. Disclose AI assistance according to venue policy; do not describe unrun tests as passing.
