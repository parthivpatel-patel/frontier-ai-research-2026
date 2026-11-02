# External requirements-data integrity and licensing audit — 2026-11-02

**Status:** Direct source/metadata inspection only. No dataset downloaded to the user's laptop, no model inference, no independent human adjudication, no claimed AI-model accuracy. Candidate data are not yet approved as ground truth.

## Source and reproducible identifiers

- Michele Chiari and Cristinel Mateis, *Datasets supporting automated requirement formalization from natural language to temporal logic*, Zenodo, **published October 25, 2026**, DOI: https://doi.org/10.5281/zenodo.23649257 .
- GitHub source: https://github.com/michiari/requirements-datasets ; inspected commit `a38a73a351c07a3d17cb561098485cd4416c5375` (October 25, 2026).
- Repository LICENSE at blob `4f9557e42d341d6736cc99d81ac28cb1a4ae5afb`: MIT, copyright 2026 Michele Chiari. The README separately credits the upstream nl2spec authors and their MIT license. Preserve copyright and license notices for any future redistributed substantial copies; none are redistributed here.
- `SyGuS/labeled_dataset.csv`: Git blob `05f60c1661c0d33b1e625fd37fb7dfad8cb4f781`, GitHub metadata size 573,851 bytes.
- The specific augmented file inspected below: Git blob `6f6d2e01707e777be9cd0197698f8f19b4381fc8`, size 5,682 bytes, at `nl2spec-augmented/nl2spec_WordEditDistance_RandomWordsMutation_WordSwapChangeNumber_eps2_n5.csv`.

## Two separate collections, two separate leakage problems

1. **Augmented nl2spec:** README reports 1,790 mutated rows from **36 original NL/LTL pairs** across 12 CSV files. These are not 1,790 independent requirements. Split by original source, not by row or transformation.
2. **SyGuS-guided STL:** README reports 1,080 natural-language realizations for **360 formal formulas**. The `formula_id` groups realizations; all `semantic_validation` fields are documented as `not_checked`. This is not a set of 1,080 independently adjudicated human-intended requirements, and the 360 formula seeds are not automatically independent human authors or physical environments.

Neither collection directly supplies authenticated outputs from GPT-5/Claude/Gemini or independently adjudicated real-world physical meanings. The published license is permissive, but it does not make the labels scientifically valid.

## Directly observed potential label mismatch (not merely theoretical)

The pinned augmented CSV contains an original requirement:

> Whenever a is enabled, b is enabled three steps later.

with unchanged formal label `G(a -> X (X (X b)))`. Its first mutated row changes the English instruction to **two steps later** while keeping that same three-next-operator formula. A second row says **one steps later**, again retaining the same formula. Other rows say four or six steps later with the same formula.

Source: https://github.com/michiari/requirements-datasets/blob/a38a73a351c07a3d17cb561098485cd4416c5375/nl2spec-augmented/nl2spec_WordEditDistance_RandomWordsMutation_WordSwapChangeNumber_eps2_n5.csv#L1-L6

Under standard discrete-time future-LTL semantics these are **not semantically equivalent**. A simple infinite-trace witness sets `a` true only at time 0 and `b` true only at time 3. Then `G(a -> X^3 b)` is true, while `G(a -> X^2 b)` is false. This proves that at least the two-step mutation cannot be treated as an automatically verified label-preserving paraphrase of the three-step original.

**Interpretation:** The file explicitly describes perturbations/robustness examples; retaining the original label may be intentional for measuring sensitivity. This observation does not imply dataset fraud, and it is not evidence that any model generated an incorrect formula. It **does** rule out using the mutated text plus retained formula as unquestioned semantic ground truth without re-annotation. Any measured model error rate against these rows could conflate translation errors with label inconsistency.

## Feasibility decision and next gate

- **Potentially useful:** license-verifiable, small, source-grouped adversarial robustness pilot; semantic-preservation audit and independent re-annotation of a preselected subset. This may supply deliberately changed meanings for falsification testing.
- **Not yet usable as confirmatory gold standard:** 36 originals are fewer than the earlier independent-source risk target; SyGuS `semantic_validation=not_checked`; physical models and human-intended semantics are not independently validated; no authenticated real-model predictions.
- **Do not** count 1,790 mutations or 1,080 realizations as independent sources. Do not silently relabel changed numbers as preserving the original formula.
- **Next research step:** construct a bounded, exact, pre-registered mutation-consistency audit with explicit temporal witnesses on a small pinned subset; then seek independent annotators or a trusted benchmark with genuine NL-to-formal model outputs. Separate this adversarial-data study from the main assumption-aware physics verifier claim.

## Prior art and novelty limits

This is a dataset-quality observation in a deliberately augmented robustness corpus, not a new temporal-logic theorem. The original nl2spec benchmark is established work (Cosler et al., CAV 2023): https://github.com/realChrisHahn2/nl2spec . NL2SpaTiaL (2025) already integrates geometric semantics and translation verification: https://arxiv.org/abs/2512.13670 . VLTL-Bench (2025) already studies grounded verifiability: https://arxiv.org/abs/2507.00877 . The novelty of an eventual physics-assumption-aware diagnostic remains unproven.

**Cost/computation:** Metadata and small text were inspected through cloud-connected GitHub access. No laptop compute, paid service, GPU, large artifact, or API inference.
