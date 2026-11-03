# Protocol 032 — Independent evidence and novelty decision gate

Status: preregistered design only (3 November 2026). No cloud execution, measured result, or novelty claim is implied by this document.

## Research question

Can a language-model-generated temporal specification be checked against a physical transition system with **sound counterexample handling**, while detecting when an erroneous abstraction suppresses a real discrepancy? This is a verification research question, not yet a demonstrated AI performance improvement.

## Closest prior art that must be compared

1. Clarke, Grumberg, and Peled, *Model Checking* (1999): classical transition-system verification and counterexample semantics.
2. Clarke et al., *Counterexample-Guided Abstraction Refinement* (CAV 2000): refining abstractions using spurious counterexamples.
3. Alur and Dill, *A Theory of Timed Automata* (TCS 1994): formal semantics for time-dependent systems.
4. Fainekos and Pappas, *Robustness of Temporal Logic Specifications for Continuous-Time Signals* (TCS 2009): temporal properties of physical signals.
5. Donzé and Maler, *Robust Satisfaction of Temporal Logic over Real-Valued Signals* (FORMATS 2010): quantitative signal semantics.

These are relevant starting points, not an exhaustive or freshly verified literature review. Search contemporary LLM-to-formal-specification and neuro-symbolic verification work before drafting any priority claim. Cite exact editions/DOIs after bibliographic verification.

## Soundness distinction

For a physical model M with trace set T(M), a constraint C is **sound** only if every trace of M satisfies C. An unsound constraint can eliminate genuine counterexamples. A finite collection of sampled trajectories cannot establish this universal property. Protocol 031's exact-rational checks validate the enumerated trajectories only; they do not prove that an abstraction is sound for all admissible states.

The implication Q => P for Q=(x>=1), P=(x>=0) is a theorem of the ordered rationals. The reverse implication fails at x=0. That example is a negative control, not a discovery.

## Independent reference check

Before relying on the current implementation:
- Derive expected values from hand-specified traces, not from the same code that generates the input.
- Independently validate each finite-trace transition and predicate label.
- Check one-state and multi-state boundary cases, fractional dt, and intentionally malformed input.
- Make a second implementation use a different representation or proof argument.
- Preserve exact input, output, source commit, run identifier, tool versions, and content hashes.

## Baseline matrix

| Method | Input | Expected scientific role |
| --- | --- | --- |
| Unconstrained Boolean model checking | Boolean valuations | Measures spurious witnesses when physical transitions are ignored |
| Exact transition-constrained model checking | Explicit rational transition relation | Strong baseline for sound physical restrictions |
| Predicate abstraction plus CEGAR | Abstract predicates and refinement loop | Tests whether the proposed method adds anything beyond established refinement |
| Incorrect identity constraint | P iff Q | Negative control: should be exposed as unsound |
| Syntax-only LLM output checking | Candidate formulas | Tests whether semantic checks offer benefits beyond parse validity |

## Falsification criteria

Stop or substantially revise the hypothesis if (a) a physically admissible witness is suppressed by the proposed constraints; (b) the independent oracle disagrees on a counterexample; (c) the apparent benefit vanishes against transition-constrained checking or CEGAR; (d) results depend on hand-picked formulas; or (e) LLM-generated specifications cannot be evaluated reproducibly without unavailable paid services.

## Evidence and cost gates

No new cloud job should be dispatched until account-level GitHub Actions allowance, billing/spending controls, and current availability are checked. A public repository does not by itself prove zero billing risk. Keep all workloads on verified free hosted compute; never run them on the user's laptop. Do not require a payment card or paid model API. If free compute cannot be verified, retain the executable design and report execution as blocked.

## Publication decision

The November 22 target is an internal goal, not a publication promise. Publish a research paper claiming a novel contribution only after baseline superiority or a clearly distinct theorem, independent verification, representative evaluation, and a defensible contemporary prior-art audit. Otherwise publish a clearly labeled reproducibility/negative-results technical report. Disclose AI assistance in accordance with the destination venue's rules.
