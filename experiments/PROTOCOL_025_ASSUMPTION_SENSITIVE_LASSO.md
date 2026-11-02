# Protocol 025 — Bounded infinite-lasso witness sensitivity under proposition assumptions

Date: 2026-11-02 (US Eastern). Session 028. **Exploratory post-hoc diagnostic**, not preregistered confirmatory evidence. We previously inspected Protocol 023/024 mismatches and observed the alias counts. This protocol is frozen before the new cloud execution.

## Research question

When two VLTL-Bench formulas become equal only after collapsing proposition IDs with identical recorded metadata, are they necessarily equivalent without assuming that the recorded proposition IDs denote the same physical predicate? No. We will search for concrete *infinite-lasso* traces that distinguish the formulas under (A) unconstrained proposition valuations and (B) the additional assumption that recorded identical-metadata proposition IDs always share valuations.

This is **not** a new algorithm or theorem. It tests a previously disclosed, metadata-conditional evaluation criterion for sensitivity to unverified assumptions. It cannot establish correctness against human intent.

## Mathematical statement and interpretation

Let φ and ψ be LTL formulas, let D be an upstream proposition dictionary, and let M(D) denote the set of physical interpretations compatible with *independently validated* constraints. The robust equivalence claim requires that **every** interpretation I in M(D), at every trace, satisfy φ iff ψ. Equality of two serialized dictionary entries alone does not prove this physical constraint. For example, with formulas F p and F q, the one-state infinite lasso p=true, q=false distinguishes the formulas, while imposing p=q at every state removes this witness.

We enumerate finite representations of **infinite** ultimately periodic traces, consisting of n states with the final state looping to one earlier state. LTL X, F, G and U are evaluated on the resulting infinite trace by finite-state least-fixpoint semantics. A found witness is a valid counterexample to equivalence *under the enumerated proposition assumptions*. No witness within the bound is **not** a proof of equivalence. The search is exhaustive only for the stated fragment, proposition count and lasso bound. Classical bounded model checking predates this project (Biere et al., 1999, DOI 10.1007/3-540-49059-0_14).

## Frozen data and compute

- Reuse Protocol 023's VLTL-Bench pinned commit 383baea8210b93fe9fa7d14edd4757e5b3464e82, file translation_eval/nl2tl/gt_lifting/navi.jsonl, expected Git blob c21575fca5e224968b56f0192b8bc0ddbaedac46 and 356248 bytes. No source files or predictions redistributed.
- Run only on existing public GitHub Actions standard ubuntu-latest, timeout 5 minutes, Python standard library, no model/API calls, paid service, card, GPU, laptop compute, external data retention or artifact uploads.
- Preserve 485 exact matches, 11 metadata-alias-only and 4 unresolved from Protocol 024. Analyze the 15 nonexact records without printing their text, IDs, formulas, valuations, or proposition dictionaries.
- For each nonexact record, parse the restricted grammar: atomic prop_N, true/false, not, and, or, implication, next, finally, always, until and parentheses (documented synonyms supported). Reject unsupported operators, unknown characters or malformed expressions. Do not silently reinterpret unsupported syntax.
- Enumerate all proposition assignments on infinite lassos up to **3 states**, at most **3 distinct propositions**, and at most **20,000 checked lasso assignments per comparison**. Report a witness only if the formulas differ at the initial state on an enumerated lasso. Explicitly distinguish unsupported syntax, too many propositions, incomplete budget and no witness within bound.
- For mode A, allow independent valuations for all proposition IDs. For mode B, group only complete, nonempty and exactly equal serialized proposition metadata; treat that equality as an *assumption*, not a verified physical fact. If metadata is missing or malformed, mark unavailable.
- Output only aggregate counts by previous alias-only vs unresolved category and by unconstrained vs metadata-equality mode. No individual external records, trace assignments or human-language claims.
- Include network-free constructed tests, especially the counterexample to F p versus F q when metadata falsely asserts p=q, plus X/F/G/U semantics, syntax rejection and budget exhaustion.

## Falsification and publication boundaries

- If the witness engine reports no witness for F p versus F q with unconstrained valuations, the implementation fails the core falsification test.
- If it reports a witness for p versus q while an explicit p=q equality constraint is imposed at every lasso state, the assumption implementation fails.
- If any nonexact row cannot be parsed, report it as unsupported rather than infer equivalence.
- If no bounded witness is found, report *inconclusive*, never 'semantically equivalent'.
- A witness between model output and benchmark reference does not tell which formula captures the human instruction; both could be wrong. Benchmark reference labels and proposition mappings remain unverified.
- Even if all 11 metadata-conditional matches admit unconstrained witnesses, this is not 11 observed unsafe model actions or a measured safety rate.
- The current method cannot support a frontier-model superiority claim or an original physics-aware verification theorem. A human-adjudicated, source-disjoint, blinded, matched-coverage study remains required.

## Closest prior art and relevance

- English et al., VLTL-Bench (2025): https://arxiv.org/abs/2507.00877 .
- Wang et al., ConformalNL2LTL (2025): https://arxiv.org/abs/2504.21022 .
- Wang et al., SCP-NL2TL (2026): https://arxiv.org/abs/2608.05439 .
- Wang et al., VerusEval (October 19, 2026): https://arxiv.org/abs/2610.26464 . Their six-dimensional contract evaluation and reference-quality warnings are a direct conceptual collision with broad 'verification beyond acceptance' claims, though Verus contracts differ from LTL and physical uncertainty.
- Biere et al., *Symbolic Model Checking without BDDs* (1999): https://doi.org/10.1007/3-540-49059-0_14 .

**Decision gate:** If the proposed contribution does not improve over formal checking and calibrated abstention under independently validated physical assumptions, publish only a transparent methodological or negative result. November 22 is conditional.
