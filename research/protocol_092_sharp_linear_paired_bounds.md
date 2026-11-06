# Protocol 092 — Sharp linear-time paired selective-risk bounds

Date: 2026-11-05. Status: implementation and tests committed; **not executed**. No empirical results.

## Result

For a fixed held-out sample with n claims, let a_i and b_i denote the two methods' frozen binary acceptance decisions, and y_i their shared unsafe-acceptance truth (0 or 1). Let n_a=sum a_i>0 and n_b=sum b_i>0. The empirical selective-risk difference is

D = sum_i (a_i/n_a - b_i/n_b) y_i = sum_i c_i y_i.

For adjudicated claims y_i is known. For each unadjudicated claim, y_i can independently be 0 or 1 absent additional constraints. Therefore the **sharp** identification interval is

L = sum_{observed i} c_i y_i + sum_{missing i} min(0,c_i)

U = sum_{observed i} c_i y_i + sum_{missing i} max(0,c_i).

Proof: each missing binary variable appears linearly and independently; minimizing (maximizing) its term selects 1 exactly when c_i is negative (positive). These selections attain the endpoints simultaneously, proving sharpness. Claims accepted by both methods can cancel partially or entirely. Computing both endpoints requires one pass and exact rational arithmetic; unlike the Protocol 091 enumeration oracle, complexity is O(n) arithmetic operations. Large rational numerators may still grow, so runtime is not guaranteed constant per operation.

## Interpretation and limits

The bound is conditional on a **fixed sample and fixed acceptance policies**; it is not a sampling confidence interval, causal effect, model-generalization guarantee, or new mathematical theorem. Sharpness requires that each missing y_i may vary freely. Correlated constraints, multilabel uncertainty, or partially adjudicated truth can change the identified set. Any uncertainty in acceptance decisions must be treated separately. Zero acceptance for either method makes its selective risk undefined. Different acceptance coverage is permitted algebraically but cannot be interpreted as a matched-coverage comparison; preregister coverage matching and thresholds separately.

## Falsification and implementation audit

1. Enumerate all assignments of missing binary labels for up to three claims and compare extrema exactly with the linear formula.
2. Test identical acceptance sets with shared missing labels: D=0.
3. Test disjoint accepted sets with missing labels: interval [-1,1].
4. Reject invalid label types and zero acceptance.
5. On a verified eligible $0 hosted runner, run `python -m unittest discover -s tests -p 'test_paired_bounds_linear.py'` from the repository root. Record runner, SHA, exit status and test output. No local laptop execution.
6. Compare against the Protocol 091 reference oracle for larger randomized small instances only after establishing safe cloud eligibility.

## Novelty and publication guardrail

The linear optimization is elementary partial identification, not itself a novel contribution. The potential research contribution, if any, requires independently adjudicated scientific claims, stronger competitive baselines, assumption-sensitive generalization and matched-coverage reliability improvements. Relevant foundations include Manski's partial-identification framework and selective prediction literature; verify precise bibliographic claims before manuscript submission. No performance or superiority is asserted.

No paid cloud, model inference, or laptop workload authorized.
