# Linear paired bounds: complexity and verification audit (2026-11-22)

**Status:** source-level review only; no new CI execution result is asserted here. Reviewed `research/paired_archival_linear.py`, `research/test_paired_archival_linear.py`, and `.github/workflows/archival-identification.yml` on main at `ff3f6496672a8fdec490db3bb46a748c72faf036`.

## Precise theorem and complexity caveat

For fixed acceptance decisions and binary predictions, write the paired selective-risk difference as
`D(y) = e_A/k_A - e_B/k_B + sum_i [a_i [p_Ai != y_i]/k_A - b_i [p_Bi != y_i]/k_B]`,
where `k_A` and `k_B` are **fixed positive** accepted-case counts, and every unresolved binary label `y_i` is shared by both policies. Because each `y_i` occurs in exactly one summand, the minimum and maximum of `D` over all assignments are the base term plus the sums of per-case minima and maxima. Each endpoint is attainable by choosing the optimizing label separately for each case. This proves sharpness under these assumptions; it is not a new general result about dependent labels or adaptive policies.

The algorithm requires O(m) case visits and O(1) additional case storage after materializing its input, **under a unit-cost arithmetic model**. The current implementation first converts the input to a tuple, requiring O(m) additional storage, and returns `2**m` as an exact integer. Arbitrary-precision rational arithmetic and this exponentially large *value* have bit costs that depend on `m` and denominator sizes. Consequently, describing the complete Python implementation as unconditionally O(m) time or O(1) space in bit complexity is too strong. A tighter description is **linear number of case evaluations**, with arithmetic and output-size costs explicitly excluded. No measured runtime or memory benchmark is claimed.

## Assumptions that can break sharpness

1. Unknown labels must be freely assignable binary variables. Logical, physical, temporal, or cross-claim constraints between labels destroy separability and require a constrained optimizer.
2. Acceptance and predictions must be fixed independently of unresolved truth assignment. If either changes with the label, denominators or summands change.
3. The two policies must refer to the same unresolved cases and truth labels; merely equal counts are not sufficient evidence of identical provenance.
4. The observed error counts must be correctly adjudicated and the acceptance totals must be valid. The bounds do not repair annotation or timestamp errors.
5. The interval is an **identification region**, not a confidence interval; finite-sample uncertainty needs separate treatment.

## Validation requirements

The six authored tests include small exhaustive comparisons and a 100-case construction. The workflow source invokes them on a standard Ubuntu GitHub-hosted runner. **Source inspection alone does not verify that the updated workflow passed on commit `ff3f649...`.** Record the exact GitHub Actions run URL, run conclusion, job conclusion, and commit SHA before calling the linear implementation cloud-validated.

Add future tests for: mixed acceptance with nonzero observed error counts; symmetry under policy exchange; permutation invariance; monotonicity under additional admissible label constraints (using a separate constrained oracle); and adversarial invalid input. Preserve the exhaustive oracle as an independent reference.

## Scientific decision

Do not claim novelty from separable minimization alone. Compare against partial-identification, paired selective classification, missing-label evaluation and constrained inference literature. A publication claim requires a distinguishable experimental contribution, authenticated historical evidence, and predeclared falsification tests. This audit contains no model results and does not authorize paid compute.
