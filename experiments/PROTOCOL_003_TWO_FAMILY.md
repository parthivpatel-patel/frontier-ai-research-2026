# Protocol 003 — Two-family exact-oracle reference-omission controls

**Status:** Engineering controls implemented; scientific benchmark NOT executed. No NLP model outputs or human-intent annotations exist. Zero-cost cloud only.

## Goal

Establish that the exact physical oracle, reference-set bookkeeping, and intentional omission controls work across two different toy dynamics, before any expensive or publication-facing NLP evaluation.

## Controlled test matrix

Two dynamics:
1. One-step reflecting particle: y = reflect(x+v+u) on the supported one-reflection domain.
2. Two-step damped motion: v_(t+1)=rho*v_t+u_t; x_(t+1)=x_t+v_(t+1); fixed rational rho in [0,1].

Five conditions per dynamics: exact reference, threshold drift, omitted intended reference, multiple supplied references, restricted-domain observational equivalence. A deterministic grammar renders the latent predicate as a short English *instruction to check a property*. It does **not** demonstrate that an NLP model can parse language or that an instruction is genuinely ambiguous.

Matched reachable images: [1/2,1] for wide boxes and [1/2,3/4] for restricted boxes. The constructed intended/candidate thresholds are 9/10 and 4/5 for the mismatch conditions. Exact arithmetic uses `fractions.Fraction`.

## Preregistered sanity-check expectations

- 10 deterministic cases total, 5 per family.
- 6 deliberately injected latent disagreements, each with a rational physical witness.
- Supplied-reference envelope: 2/10 certain errors and 4/10 possible errors.
- Constructed latent rate: 6/10, deliberately outside the supplied envelope.
- The two restricted cases have distinct global thresholds but no observable disagreement on their specified reachable sets.
- No empirical confidence intervals or population-level risk claims apply to this deterministic ten-case matrix.

## Verification steps

1. GitHub public standard-runner CI runs `python3 -m unittest discover -s tests -v`.
2. CI prints `python3 -m src.physical_probe_suite` to logs.
3. Confirm the workflow status and inspect failing logs before claiming it passed.
4. Ensure every reported separating trajectory is inside its physical box and produces opposite truth values.
5. Compare exact reachable endpoints to independently enumerated corner cases for the damped family.
6. Check invalid parameters and out-of-domain inputs fail closed.

## Next scientific experiment — NOT YET RUN

1. Expand to several hundred examples with template-held-out and physics-family-held-out splits. Add independent paraphrases and natural language from external contributors only if provenance, consent and semantic annotation quality can be established without payment.
2. Evaluate actual NL-to-formal outputs, with provenance and model versions. Prefer openly released model predictions or tiny CPU-feasible open baselines after verifying license, cloud resource requirements and no large downloads. Do not pretend a hand-written perturbation is a model output.
3. Match information available to single-reference, multi-reference, reference-free and selective baselines. Include strong methods from TLA+-Bench, Faithfulness Gap, Fushimi et al. and SCP-NL2TL where their task and released resources are actually comparable.
4. Use independently adjudicated intended semantics, not the same model that generated a candidate, to label actual semantic error. Report inter-annotator disagreement and ambiguous inputs separately.
5. Freeze code, data, split and hypotheses before held-out testing. Report uncertainty with independent sampling units; no confidence intervals from deliberately chosen fixtures.
6. Kill this research direction if equivalent benchmarks already exist or if there is no meaningful advantage beyond reference-information access.

**Compute:** Standard public GitHub Actions `ubuntu-latest` only, short timeout, standard-library code, no paid resources, no user laptop. **Novelty:** not established. **Publication:** not authorized by these controls alone.
