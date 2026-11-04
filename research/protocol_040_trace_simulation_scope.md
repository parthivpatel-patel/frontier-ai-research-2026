# Protocol 040 — Trace inclusion versus simulation: precise scope and falsification

Date: 2026-11-03. Status: theoretical audit and proposed experiments; no execution or novel theorem claimed.

## A necessary distinction

Let C=(S_C,I_C,R_C) and A=(S_A,I_A,R_A) be finite transition systems and let alpha:S_C -> S_A be a total deterministic abstraction. For a horizon h, define Tr_h(C) as all state sequences (s_0,...,s_h) starting in I_C and following R_C. Define alpha(Tr_h(C)) pointwise. Bounded projected trace inclusion means alpha(Tr_h(C)) subset Tr_h(A).

A sufficient condition is initial inclusion alpha(I_C) subset I_A and edge preservation (alpha(s),alpha(t)) in R_A for every concrete edge (s,t) reachable from I_C. By induction, this implies projected trace inclusion for every finite h. This is a standard functional forward simulation argument.

The converse needs careful quantifiers. If projected trace inclusion holds for *every* finite h, then every reachable concrete edge is preserved, provided each finite concrete prefix is represented in Tr_h(C), the abstract traces retain full state sequences, and there is no hiding, stuttering, observation quotient, or alternate abstract witnesses. A counterexample to a reachable edge appears as a concrete prefix whose projection is absent from A. Unreachable edges are irrelevant to this reachable-trace statement. An assertion about all graph edges without reachability restriction is stronger and is not implied by trace inclusion.

Important caveat: if the compared traces consist only of observable labels rather than the actual alpha-mapped abstract states, or if the relation is nondeterministic rather than functional, trace inclusion need not imply the existence of the proposed pointwise simulation certificate. Likewise, finite-horizon inclusion does not establish all-horizon inclusion.

Deadlock convention must be specified: exact-length traces, prefixes of length <=h, or stutter-completed traces yield different outcomes. The reference experiment should use prefix-closed finite traces, count length-zero traces, and make deadlock handling explicit.

## Protocol 040 test plan

1. Exhaustively enumerate small graphs with reachable and unreachable states; compare reachable-edge preservation to projected prefix-trace inclusion through horizon |S_C|, with a counterexample witness for every discrepancy.
2. Construct a concrete unreachable edge that violates global edge preservation but leaves all reachable traces included; reject a false claim that global edge preservation is necessary.
3. Compare full alpha-state traces to observable-label traces; demonstrate a case where label-trace inclusion holds but alpha-state edge preservation fails.
4. Vary exact-length, prefix-closed, and stutter-completed semantics on deadlocked states; record distinct verdicts.
5. Introduce a deliberately missing abstract edge on a reachable concrete path and verify that the independent oracle returns the shortest witness.
6. Use two independently implemented oracles, mutation testing, fixed deterministic seeds, and JSON outputs containing commit SHA, Python version, input hash, parameters, witnesses, and exit codes.

These are planned checks, not executed results. Avoid describing any number of enumerated cases as completed until cloud logs and artifacts exist.

## Prior-art and novelty gate

Functional simulation, trace inclusion, automata/model checking, CEGAR, timed automata, signal temporal logic, and neural-symbolic verification are established. Starting references to read and compare directly: Clarke et al., *Counterexample-Guided Abstraction Refinement* (CAV 2000); Alur and Dill, *A Theory of Timed Automata* (TCS 1994); Baier and Katoen, *Principles of Model Checking* (2008); Donzé and Maler, *Robust Satisfaction of Temporal Logic over Real-Valued Signals* (FORMATS 2010). Also survey recent LLM-to-formal-specification, proof-carrying code, theorem-proving language agents, and physics-informed verification papers before asserting a research gap.

The potential contribution is an empirically validated, independently checkable pipeline from natural-language physical claims to formally scoped certificates and explicit abstention, **not** a new simulation theorem. Compare against (a) direct LLM verdicts, (b) LLM-generated specifications checked by standard model checking, (c) rule/template extraction with the same checker, and (d) independent formal-specification baselines. Use matched examples, budgets, and information access. Pre-register false-verified rate, false-falsified rate, abstention, specification fidelity, certificate validity, and compute cost.

Falsify the central research hypothesis if the system admits any verified verdict without a valid certificate, if the claimed physical counterexample fails independent validation, or if the proposed integration does not outperform a strong baseline on predeclared metrics. A single soundness violation invalidates an unconditional soundness claim. Benchmark leakage, ambiguous NL labels, and unsupported physical assumptions must be reported, not silently excluded.

## Compute and publication safeguards

Run only on standard GitHub-hosted runners for this public repository **after** verifying the current repository visibility, account Actions policy, applicable free usage/storage limits, and billing protections in the account. No larger runners, external hosted model endpoints, paid credits, or laptop execution. Until eligibility is confirmed, keep experiments as source and plans only.

The November 22 target is conditional on independent reproducibility, negative controls, defensible differentiation from prior art, and transparent AI-assistance disclosures where required by the destination venue. This protocol makes no claim of executed experiments or general continuous-physics soundness.
