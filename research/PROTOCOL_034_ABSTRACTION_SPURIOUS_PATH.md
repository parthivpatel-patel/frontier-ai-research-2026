# Protocol 034 — Predicate abstraction: a soundness proof and a spurious-path control

Status: analytical derivation and preregistered test design (2026-11-03). No experiment executed; no novelty claim.

## Exact bounded semantics

Fix a nonempty physical state set S, initial states I subset S, a transition relation T subset S×S, an atomic-proposition set AP, and a labeling L:S→2^AP. A length-(H+1) physical trace is s_0,...,s_H with s_0 in I and (s_t,s_(t+1)) in T for every t<H. H is a nonnegative integer. For a formula phi, define finite-trace satisfaction at t with strong next: X phi is false at t=H; F phi holds if phi holds at some j in [t,H]; G phi holds if phi holds at all j in [t,H]; phi U psi holds if some j in [t,H] satisfies psi and all k in [t,j) satisfy phi. These semantics must not be conflated with infinite LTL.

Define alpha(s)=L(s). Let A=2^AP. Define abstract initial valuations I#={alpha(s):s in I} and existential abstract edges T#={(alpha(s),alpha(s')):(s,s') in T}. The abstract checker enumerates all length-(H+1) valuation paths starting in I# and following T#.

**Inclusion lemma.** Every physical trace maps to an abstract path. Proof: alpha(s_0) is in I# by definition; each concrete edge maps to an edge in T#. Induction over t establishes path membership. Therefore, for a property interpreted solely over AP with the same finite-trace semantics, absence of abstract counterexamples implies absence of physical counterexamples within the stated horizon and state domain.

**Important qualification.** The converse is false: abstract edges may be witnessed by incompatible concrete states at successive steps. A path in T# is not necessarily concretizable. The proof is a standard existential-abstraction argument, not a new theorem. If T# is generated from a sample rather than all T, the inclusion lemma no longer follows.

## Explicit spurious path (negative control)

Let S={0,1,2}, I={0}, and T={(0,1),(1,1),(2,2)}. Label alpha(0)=alpha(2)=a and alpha(1)=b. The abstract edges include a→b (witness 0→1), b→b (1→1), and a→a (2→2). Hence the abstract path a,a is admitted for H=1, even though the only concrete path from initial state 0 is 0,1 and its labels are a,b. A checker that reports a,a as a physical counterexample is wrong. This demonstrates why independently validating counterexamples is necessary even under a sound overapproximation.

For the AP={p} interpretation a={p}, b=empty, the physical system satisfies X not-p at the initial state for H=1, while the abstract path a,a violates it. This is a *spurious counterexample*, not a soundness failure of the overapproximation.

## Deliberately unsound underapproximation

Delete abstract edge a→b while keeping only a→a and b→b. The actual initial physical trace a,b is now excluded. A checker may incorrectly verify X p over its remaining a,a path even though the physical initial trace falsifies X p. The failure is missing trace inclusion, not a defect in temporal logic.

## Preregistered executable checks

1. Enumerate the three-state example with H=1 and compare the physical paths against abstract paths; assert inclusion and the existence of the spurious a,a path.
2. Assert the physical verdict for X not-p is true and the existential abstraction reports a violating path; independently test whether that path is concretizable.
3. Assert that deleting a→b breaks inclusion and permits a false verification of X p.
4. Repeat with H=0 and H=2, checking strong-next boundary behavior and the independent physical oracle.
5. Report counts only after a verified cloud run; preserve the full input relation, labels, enumerated paths, oracle output, commit SHA, and workflow URL.

The example is deliberately tiny and analytically determined. It is a diagnostic baseline, not evidence of a new AI/ML method. A later language-model specification experiment must use held-out natural-language requirements, human-reviewed reference specifications, explicit ambiguity categories, and an independently validated physical system. No model accuracy claim is permissible from this toy system.

## Falsification and novelty gate

Reject any claimed verification guarantee if an admissible physical trace is omitted by the proposed constraint construction. Reject a claimed precision improvement if it disappears against an equally informed exact-transition or CEGAR baseline. Do not present existential predicate abstraction, counterexample refinement, or finite-trace temporal logic as original contributions. Their foundational literature must be checked against bibliographic originals before publication.

## Cloud and reproducibility boundary

This note is source-only. No compute is authorized until the specific GitHub account's Actions allowance, spending cap, billing requirements, and availability are verified as zero-cost. Never use the user's laptop for experiments.