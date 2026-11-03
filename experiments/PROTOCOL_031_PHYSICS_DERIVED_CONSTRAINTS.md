# Protocol 031 — Physics-derived proposition constraints (preregistered design)

Date: 2026-11-03. Status: **design only; no execution or findings**.

## Research question

Can a verifier distinguish logically valid proposition relationships derived from a physical transition system from unjustified aliases supplied by a language model? Protocol 030 establishes only a constructed warning: assuming two distinct propositions equal can hide a counterexample. Protocol 031 tests a more realistic, explicitly derived relationship, without claiming an advance over model checking or abstraction refinement.

## Physical toy model and units

Use exact rational arithmetic for a one-dimensional discrete-time constant-velocity system, with position x in metres, velocity v in metres/second and timestep Δt = 1 second:

x[t+1] = x[t] + v[t] Δt; v[t+1] = v[t].

For the initial finite experiment, enumerate x[0] in {-2,-1,0,1,2} metres, v[0] in {-1,0,1} metres/second and horizons 1–4 transitions. These are **constructed** physical traces, not sensor observations. Define P[t] := (x[t] >= 0 m), Q[t] := (x[t] >= 1 m), R[t] := (v[t] >= 0 m/s). The genuine invariant Q => P follows by threshold ordering. P <=> Q is **not** valid: x=0 m separates them.

## Experimental arms

A. Raw propositional verifier: treat P and Q as independent atoms (sound for all Boolean traces but may produce physically infeasible witnesses).

B. Physics-constrained verifier: restrict valuations to those realizable by the stated exact transition equations and threshold definitions. Report whether each witness is realizable, and supply x,v for every state.

C. Invalid alias negative control: impose P=Q despite the x=0 counterexample; record whether genuine disagreements are suppressed.

D. Correct implication control: enforce Q=>P only; check that this does not eliminate any physically realizable trace.

Do not interpret no witness on a finite horizon as unrestricted LTL equivalence. Do not identify finite traces with infinite lasso traces without an explicitly justified periodic physical trajectory. In particular, a constant nonzero velocity trajectory cannot be represented by a finite periodic position lasso. Use bounded finite-trace semantics with explicit endpoint conventions, or restrict lasso checks to physically periodic v=0 traces.

## Independent verification

Build two checks: (1) exact-arithmetic transition/threshold validator independent of the LTL search implementation, and (2) separate semantic evaluator for the supported temporal fragment. Save the concrete physical trajectory, Boolean proposition table, formula pair, semantic convention, horizon, search bounds, solver version and source commit. Each figure must be generated from those saved outputs, not aggregate numbers reconstructed by hand.

## Falsification and failure criteria

- Reject a claimed physical witness if any transition or predicate valuation fails independent exact-arithmetic verification.
- Reject a claimed benefit if the physics arm suppresses any realizable counterexample, or if it only gains performance by imposing false identities.
- Do not claim improved semantic accuracy without a separately labeled, independent reference set of physical specifications.
- Compare against conventional model checking with transition constraints and explicit predicate abstraction; if the method reduces to that established baseline, report replication rather than novelty.
- Report all unsupported formulas, incomplete searches, negative findings and uncertainty.

## Prior art to audit before novelty claims

Clarke, Grumberg and Peled, *Model Checking* (1999); Biere et al., *Bounded Model Checking* (1999); Graf and Saïdi, *Construction of Abstract State Graphs with PVS* (1997); Clarke et al., *Counterexample-Guided Abstraction Refinement* (2000); Pnueli, *The Temporal Logic of Programs* (1977); Raman et al., *Sorry Dave, I'm Afraid I Can't Do That: Explaining Unachievable Robot Tasks Using Natural Language* (2013). Verify bibliographic metadata, exact contributions and newer neural specification-generation comparisons before manuscript use. These are comparison targets, not a completed literature review.

## Reproducibility and spending gate

Use standard-library exact fractions for tiny deterministic checks, on GitHub-hosted cloud only **after** confirming Actions eligibility, free allowance and absence of billable runners for this account. Never run on the user's laptop or provision paid compute. Keep the run capped and cancel on timeout. Preserve a JSON record and genuine programmatic SVG of a verified trajectory, clearly labeled constructed.

## Publication gate

A paper by 2026-11-22 is conditional: independently validated physics-derived constraints, reproducible outputs, credible formal-methods and AI baselines, verified literature novelty assessment, and appropriate AI-assistance disclosure. A rigorous negative result is acceptable.
