# Protocol 071 — Exact-enumeration fixture boundary audit

Date: 2026-11-14 UTC. Status: source-level audit; no fixture execution, empirical experiment, or novelty claim.

## Verified correction

Protocol 069's one-family Bernoulli example previously asserted that the *realized* variance estimator was 0.04 when a family with p=0.5 and Z=0.2 was sampled. Direct substitution into the documented formula gives (1-p)Z²/p² = 0.08 when sampled, and 0 when not sampled. The design variance and expected variance estimator both equal 0.04. This documentation defect was corrected in Protocol 069. The Protocol 070 implementation uses the correct formula; source inspection is not a claim of passing tests.

## Source-level limitations found in Protocol 070

1. `family_contrast` checks denominators only with `<= 0`. NaN denominators bypass this guard; infinity is also accepted. Require `math.isfinite` and strictly positive denominators.
2. `family_contrast` rejects negative weights but does not reject NaN/infinite weights. Require finite nonnegative weights, and explicit numeric type handling.
3. `exact_design` enumerates 2^G inclusion sets, so the helper is suitable only for small synthetic designs. Add an explicit maximum family count, e.g. G <= 12, and avoid large enumeration.
4. The fixture validates independent Bernoulli family inclusion only. It does not validate fixed-size sampling, adaptive sampling, truth-adjudication accuracy, confidence-interval coverage, or real-world claims.
5. A finite-population variance identity does not establish that policy comparisons have matched release coverage, matched operational verification budgets, or a prespecified scientific safety threshold.

## Required negative controls before an execution claim

- Reject NaN and infinite denominators and weights.
- Reject a family count exceeding the enumeration cap before allocating outcome tuples.
- Confirm the realized variance estimator is 0.08, not 0.04, in the sampled one-family example.
- Verify that all sampled-family claims are adjudicated; partial labels cannot be silently treated as zeros.
- Keep an independent evidence record for each run: commit SHA, Python version, exact invocation, exit code, and logs.

## Interpretation and falsification

If the negative controls fail, treat the fixture as not validated and block empirical claims. Even if all pass, they verify only small-design arithmetic. They cannot establish a novel AI verification method, cross-domain transfer, improved false-acceptance outcomes, or physics ground truth. Literature comparisons and held-out evaluations are separate gates.

## Resource and publication gates

No local laptop execution. Do not trigger cloud workflows until current account-specific zero-cost eligibility, billing/card requirements, usage quotas, and actual workflow availability are verified. Do not claim tests executed based on code inspection. November 22 is conditional on reproducible evidence and a defensible contribution. Preserve publication disclosure and project separation.
