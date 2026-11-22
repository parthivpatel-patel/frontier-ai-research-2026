# Audit: estimand validity, denominator invariance, and constrained-label falsification

Date: 2026-11-22. Status: theoretical review only; **not a new experiment or novelty claim**.

## Scope and source inspected
Inspected `research/paired_archival_linear.py` and `research/HELD_OUT_TEMPORAL_VERIFICATION_PREREG_2026-11-22.md` on the repository default branch. This note does not assert that any new tests have run. The paired function computes a *difference of policy-specific selective risks*, not a causal treatment effect or a difference on a common accepted subset.

## Formal object
For a common set of n claims, fixed binary predictions p_{ji} and fixed acceptance a_{ji} for policy j in {A,B}, define k_j=sum_i a_{ji}. For k_A,k_B>0, D(y)=sum_i a_{Ai}1[p_{Ai}!=y_i]/k_A - sum_i a_{Bi}1[p_{Bi}!=y_i]/k_B. Verified labels contribute a fixed base. For unconstrained missing labels, each missing y_i in {0,1} may vary independently; therefore min D = base + sum_i min{d_i(0),d_i(1)} and max D = base + sum_i max{d_i(0),d_i(1)}. Both endpoints are attained by choosing the corresponding label independently for each i. This establishes sharp *finite-sample identification* conditional on the frozen predictions, acceptance flags and known labels. It is a special case of separable optimization; no theorem novelty is asserted.

## Validity boundaries and concrete falsifiers
1. **Policy-dependent denominator:** The two denominators need not be equal, but each must remain fixed over all missing-label completions. If an abstention rule uses the unknown true label, k_j(y) varies; this derivation fails.
2. **Cross-item constraints:** If y_1=y_2, independent per-item minima can be mutually incompatible. Example: two missing items, both policies accept both, A predicts (0,1), B predicts (1,0). For y_1=y_2, both policies make one error, D=0. If labels vary independently, assignments (0,1) and (1,0) produce D=-1 and +1 respectively. Thus the unconstrained [-1,1] envelope is *not sharp* under equality constraints.
3. **Missingness mechanism:** Bounds conditional on an observed missingness pattern do not justify population transport or missing-at-random claims.
4. **Coverage tradeoff:** If A accepts only easy items and B accepts all, a smaller selective error for A does not imply higher overall accuracy or superiority at matched coverage. Report k_A/n and k_B/n; predefine matched-coverage analysis separately.
5. **Undefined risk:** If k_A=0 or k_B=0, D is undefined, not zero. Exclude from defined-risk aggregation and report undefined cases.
6. **Label provenance:** Evidence timestamps authenticate availability, not truth. Separate source availability adjudication from truth-label adjudication.
7. **Complexity:** The loop evaluates O(m) item contributions in the arithmetic-operation model; exact Fraction arithmetic and integer sizes prevent an unconditional O(m) bit-time or constant-space assertion. The current code materializes tuple(missing) and computes 2**m counts.
8. **Sampling uncertainty:** The sharp interval is not a confidence interval. A population confidence procedure requires its own assumptions and coverage validation; endpoint bootstrap alone is not automatically valid.

## Next cloud test specification (not yet executed)
- Exhaustive compare the separable oracle against all 2^m assignments for m<=8, with k_A,k_B nonzero, including unequal coverage.
- Assert the equality-constrained two-item example has constrained interval [0,0], while unconstrained formula returns [-1,1]; never present the latter as sharp under constraints.
- Check zero-acceptance returns undefined, rather than a numeric risk.
- Construct a label-dependent acceptance counterexample and verify the implementation rejects or explicitly declares it outside scope.
- Exercise large m with bounded CI input sizes and timeout, recording whether Fraction bit growth affects runtime.
- Require a public, no-cost standard GitHub Actions runner with explicit timeout; check account/repository eligibility and billing before any new job. No GPU, model download, or laptop execution.

## Publication consequence
The defensible contribution candidate is a transparent, historically authenticated evaluation *protocol* with paired partial-identification accounting and explicit failure tests. The algebra alone is not sufficient for a novel AI/ML/NLP/math/physics paper. Proceed to held-out domain-specific data only after provenance and literature gates pass. Disclose AI assistance and negative outcomes.
