# Exact linear-time sharp bounds for paired binary verification

Date: 2026-11-22. Status: mathematical derivation, **not** a tested implementation or novelty claim.

## Result and assumptions

Consider two fixed binary-label verification policies A and B evaluated on the **same** finite set of cases. Each policy has fixed predictions and acceptance decisions before the unresolved labels are assigned. The verified cases have known accepted-error counts `e_A,e_B` and accepted counts `v_A,v_B`. For each of the `m` unresolved cases `i`, the prediction `p_{ji} ∈ {0,1}` and acceptance indicator `a_{ji} ∈ {0,1}` are fixed for policy `j`. Each unresolved case has one common unknown binary truth `y_i`, shared by both policies. No constraints couple different unknown labels. Set `K_j = v_j + Σ_i a_{ji}`.

When `K_A>0` and `K_B>0`, the paired selective-error difference is

`D(y) = e_A/K_A - e_B/K_B + Σ_i [a_{Ai} 1(p_{Ai}≠y_i)/K_A - a_{Bi} 1(p_{Bi}≠y_i)/K_B]`.

Define the per-case contribution for candidate truth `t` as

`d_i(t) = a_{Ai} 1(p_{Ai}≠t)/K_A - a_{Bi} 1(p_{Bi}≠t)/K_B`.

Then the **sharp finite-frame identification interval** is exactly

`L = e_A/K_A - e_B/K_B + Σ_i min(d_i(0),d_i(1))`

`U = e_A/K_A - e_B/K_B + Σ_i max(d_i(0),d_i(1))`.

Proof: the feasible set of unresolved truths is the Cartesian product `{0,1}^m`. The objective is a sum of functions each depending on exactly one coordinate. Every term can therefore attain its minimum (respectively maximum) simultaneously by selecting that coordinate's minimizing (maximizing) truth. Both endpoints are attained. This takes O(m) exact-rational operations instead of the reference oracle's O(2^m) enumeration. It is an elementary separability observation, not an assertion of mathematical originality.

If either `K_j=0`, the corresponding selective error rate is undefined for **all** label assignments (because acceptance is fixed). In that case the paired difference has no defined endpoints; do not substitute zero or an artificial interval.

## Reference pseudocode

```python
from fractions import Fraction

def sharp_linear(a, b, missing):
    # a and b are validated Counts on the identical frame.
    # missing is an iterable of validated MissingCase.
    missing = tuple(missing)
    if a.n != b.n or a.m != b.m or len(missing) != a.m:
        raise ValueError("sampling frame mismatch")
    ka = a.accepted + sum(c.accept_a for c in missing)
    kb = b.accepted + sum(c.accept_b for c in missing)
    if not ka or not kb:
        return None
    base = Fraction(a.errors, ka) - Fraction(b.errors, kb)
    low = high = base
    for c in missing:
        def contribution(t):
            return (Fraction(int(c.accept_a and c.predict_a != t), ka)
                    - Fraction(int(c.accept_b and c.predict_b != t), kb))
        d0, d1 = contribution(0), contribution(1)
        low += min(d0, d1)
        high += max(d0, d1)
    return low, high
```

## Required falsification and validation gates

1. Compare the linear formula **exactly** with `sharp_paired_difference` for all small, exhaustively enumerated admissible frames, including zero unresolved cases, opposing predictions, unequal acceptance, and abstention.
2. Check policy-swap antisymmetry: `[L_AB,U_AB] = [-U_BA,-L_BA]`.
3. Check permutation invariance of unresolved cases and invariance under simultaneous binary-label/prediction complementation where applicable.
4. Check the resulting interval is contained in the conservative marginal-difference envelope.
5. Add fixed-budget standard GitHub-hosted public-repository CI. **Do not run locally on the user's laptop.** Verify applicable runner billing and quota conditions before running.
6. If verified historical labels have uncertainty, predictions or acceptance decisions depend on unknown truths, or labels obey cross-case constraints, the formula is **not automatically sharp**. Develop a separately specified feasible-set optimization rather than applying it blindly.

## Research interpretation and prior-art guardrail

This is a useful exact computational simplification of the repository's existing paired shared-label archival-identification oracle. It is **not** evidence that an AI model is better, not a statistical confidence interval, and not a new physics or mathematics discovery. Related established ideas include separable discrete optimization, partial identification under missing outcomes, selective classification, and paired evaluation. A primary-source literature review remains necessary before asserting any novel contribution. Physics and mathematics benchmarks must have authenticated temporal provenance and independent ground truth before being used as cross-domain evidence.

## Publication decision

Retain a **methods/preregistration** classification until primary-source prior art, reproducible cloud tests of this formula, and properly held-out authenticated experiments are complete. No empirical result is claimed in this note.
