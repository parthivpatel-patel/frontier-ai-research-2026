# Protocol 002 — Physics-grounded semantic-reference completeness benchmark (PROVISIONAL)

**Status:** preregistered plan, not yet an executed benchmark, original method, accepted dataset, or established novelty. Budget $0. Use free standard GitHub Actions cloud runners; never user's laptop.

## Question and hypotheses

Question: Under linguistic ambiguity and interventions in physical environments, how do single-reference, set-reference and calibrated-selective evaluation schemes behave when the supplied semantic oracle is incomplete?

- H0: Any observed change is entirely explained by existing ambiguity-aware calibration / selective prediction methods or reference information advantage; no new benchmark value.
- H1 (descriptive only): Exact physical witnesses can reveal specific classes of *oracle incompleteness* that single-reference evaluation masks, even when model-side mathematical certificates are valid.
- An improvement in a synthetic stress case is not proof of a novel method or generalization.

## Ground truth and identifiability

A controlled grammar specifies a latent intended predicate *before* a paraphrase is produced. Store its AST, units, physical domain and intended quantifiers. Separately generate an intentionally incomplete candidate-reference set. Distinguish (i) actual latent grammar intent, (ii) annotator plausible readings, (iii) reference set supplied to scorer, and (iv) formalization output. Do not pretend the grammar-derived latent intent represents unconstrained natural language.

For each candidate predicate and intended predicate, use an independent exact physical oracle on supported dynamics to obtain an equivalence result and a rational witness if they differ. If dynamics are approximate, report solver tolerances and do not call the witness mathematically exact.

## Physics and language families

Phase A (no inference): one-step reflecting particle, rational intervals, threshold predicates, controlled paraphrases. Grammar variables include threshold, initial-state domain, action domain, negation, inclusive/exclusive comparisons and quantifier scope; **implement support before claiming these features were evaluated**.

Phase B (only if justified and $0 feasible): second independent physical family such as a rational discrete-time damped system; separate derivation and exact solver required. Hold out entire dynamics families and language templates to prevent leakage. No invented LLM results.

## Matched-information baselines

A. Single supplied reference.
B. Majority/reference-set scoring (when independently adjudicated).
C. Worst-case supplied-set finite-sample envelope (existing code; elementary baseline).
D. Existing ambiguity-aware method(s) from 2023 Stutz et al. and 2026 Fushimi et al., **only if method, license, and comparable inputs allow a fair reproduction**.
E. Existing selective risk method(s) SCoRE and SCP-NL2TL, **only if available code/labels and compute permit fair comparison**.

Do not compare method C with extra oracle access to methods A/B without reporting that advantage. Never relabel finite-sample envelopes as conformal population guarantees.

## Splits, metrics and resource constraints

- Freeze generation seed and source code commit before producing final evaluation.
- Proposed splits: 60% train/dev, 20% calibration, 20% held-out test, stratified by physics family and ambiguity type. Template/family disjointness is required for generalization claims; if only one physics family exists, report *no cross-family generalization*.
- Report exact semantic mismatch rate (when latent intent is known), ambiguity-set recall, error envelope width, selected-only error, joint error, acceptance, invalid-certificate rate, and exact physical counterexample rate.
- Report 95% intervals for empirical proportions when enough independent samples exist, with a stated method; do not mistake these for formal semantic guarantees.
- Include negative controls (unambiguous same-meaning paraphrases, tautological references, impossible thresholds), oracle-omission ablations, boundary cases, and leakage checks.
- Compute cap: single standard `ubuntu-latest` job, 5-minute timeout, Python standard library, no caches, no artifact upload, no external inference.
- If any candidate requires a paid model or large GPU, **skip**; do not request card or run local experiments.

## Failure and stop rules

1. If a prior published benchmark already measures this phenomenon under comparable physics and reference assumptions, reject novelty.
2. If the intended semantics cannot be independently specified or adjudicated, reject accuracy claims.
3. If there is no fair baseline or only hand-constructed toy evidence, publish no empirical superiority claim.
4. If results disappear on held-out templates/physics, report the failure and revise/pivot.
5. If a venue requires AI-assistance disclosure, comply.

## Near-term executable checkpoint

Run `python3 -m unittest discover -s tests -v` and `python3 -m src.oracle_stress` on GitHub's free standard hosted runner. Check the Actions job outcome before calling it verified. The output is a *sanity check*, not a study result.
