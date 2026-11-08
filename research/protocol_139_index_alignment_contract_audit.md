# Protocol 139 — Index alignment as an identifiable part of the bootstrap contract

Date: 2026-11-08. Status: analytical audit and preregistered tests; no cloud tests or model experiments run.

## Why this matters

Protocols 137–138 assume a *shared ordered lineage index space* across all positive-weight physics families. Equal array lengths are necessary but not sufficient. If index 0 refers to different physical units in different families, reusing index 0 is not a meaningful paired bootstrap. The probability of an undefined denominator then depends on an arbitrary ordering convention. In contrast, family-independent resampling is invariant to permutations within each family.

## Exact counterexample

Consider two equally weighted families with n=2 and acceptance flags A=(True, False). If family B has flags (True, False) on the **same aligned lineage identifiers**, the common-index resampling failure event for both families is identical. Two replacement draws both select index 1 with probability (1/2)^2=1/4. Thus P(any undefined)=1/4.

If B's *array positions* are reversed to (False, True), while the shared draw index vector is unchanged, the family failure events become disjoint: A fails only on (1,1), and B only on (0,0). Thus P(any undefined)=1/2.

The per-family acceptance counts and marginal undefined probabilities remain identical (1/4 each). The family-independent union probability is 7/16 in both configurations. These are exact mathematical results, not empirical observations.

## Valid and invalid invariance requirements

- **Valid:** simultaneously permuting the same lineage IDs across *every* family, with acceptance vectors permuted consistently, must leave the shared-index probability unchanged.
- **Invalid:** permuting only one family's vector without carrying a mapping between the original shared lineage identifiers need not preserve the probability.
- **Valid:** zero-weight families do not affect the event; strictly positive weights affect inclusion but not its probability.
- **Invalid:** inferring shared-index calibration from matching lineage counts or a common random seed alone.

## Required production contract trace

1. Identify the stable lineage key used by each family and the physical meaning of each key.
2. Verify a one-to-one common key set across families before invoking the shared-index oracle. If key sets differ, explicitly define the resampling design and missingness handling; do not silently zip arrays.
3. Trace whether the actual sampler reuses *drawn key identifiers*, positional indices, independent per-family draws, or another coupling.
4. Test a joint permutation of all family arrays and their keys; require unchanged probability.
5. Test a single-family permutation with unchanged positional coupling; expect a changed probability in the counterexample, documenting why it is not a valid invariance.
6. Compare the production preflight with the oracle appropriate to its verified coupling; reject exactness claims if the contracts differ.

## Preregistered falsification

For the two-family two-lineage fixture, a claimed shared-key preflight returning 1/4 for both aligned and complementary configurations is falsified. A claimed permutation-invariant shared-key implementation is falsified if a *joint* reordering changes its output. A claimed independent-family preflight is falsified if reordering a single family's flags changes its output. These checks require only exact rational arithmetic and small deterministic test fixtures.

## Interpretation and publication boundary

This is an implementation and identifiability risk, not a new theorem. It does not show population coverage, improved physics reasoning, NLP performance, model safety, or novelty. Before empirical claims, verify zero-cost cloud execution eligibility, run the exact tests in eligible CI, conduct independent physics-language experiments with strong baselines and negative controls, and compare against contemporary calibration, selective prediction, hierarchical bootstrap, and paired-resampling literature. No laptop compute or paid service is authorized.
