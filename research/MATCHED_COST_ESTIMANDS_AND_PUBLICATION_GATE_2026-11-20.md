# Matched-cost estimands and publication gate (2026-11-20)

## Finding from executable contract review
At commit f0661c14, `paired_selective_error_difference` requires **per-item equality** of input tokens, output tokens, verifier calls and USD cost. This is an appropriate strict diagnostic for a controlled ablation, but it is **not a general matched-compute evaluation**. A temporal verifier that uses extra calls on one question and fewer on another may have the same total budget while failing this function. Conversely, identical token counts and call counts do not imply identical wall time, hardware, energy, or financial cost. Report the current function as a *per-item resource-vector matched selective-error contrast*, never as a full compute-equivalent result.

## Pre-registered two-track analysis
1. **Strict resource-vector ablation:** Preserve existing per-item equality guardrail. For identical item pools and equal accepted counts k>0, compute (errors accepted by T - errors accepted by C)/k. This is descriptive; shared item labels and disjoint acceptances give an exact algebraic identity, not a causal effect. Retain all rejected items in the denominator of coverage.
2. **Operational budget comparison (new analysis, not yet implemented):** Freeze a common per-domain aggregate token/call ceiling *before* held-out scoring; compare policies at matched observed coverage, and report each policy's input tokens, output tokens, calls, latency and USD separately. If costs cannot be measured or controlled, call it token/call-budget matching, not matched compute. Do not choose a threshold or budget using held-out labels. Report the selective risk versus coverage curve, not just a single cherry-picked point.
3. **Uncertainty:** Cluster resampling at source/problem-family level, not at individual policy rows; paired differences share questions. Report family counts and sensitivity to domain weighting. Do not claim valid confidence intervals from resampling overlapping source families as independent units.
4. **Temporal feature test:** Compare T against C, shuffled temporal S and conventional-feature B on frozen held-out items. A gain over C but not S or B does not establish a distinctive temporal mechanism. Require blinded independent correctness adjudication.
5. **Transfer:** Leave one of NLP, mathematics and physics held out, rotating all three. Avoid source-family, paraphrase and answer-hash overlap. Report each domain independently before any pooled average.

## New falsification and decision rules
- **Stop performance claims** if independent labels, provenance, budget logs or preregistered splits are missing.
- **Reject temporal-specific explanation** if T is indistinguishable from shuffled S or stronger B under uncertainty and sensitivity analyses.
- **Reject transfer claim** if improvements occur only after target-domain tuning or collapse in any held-out domain without a qualified domain-specific claim.
- **Reject novelty claim** unless a full-text comparison demonstrates an uncaptured technical contribution beyond selective prediction, conformal risk control, abstention and existing LLM verifier evaluation.
- **Publication on Nov 22:** Only a clearly labeled methods/preregistration release is justified without validated held-out model results. Never present code tests as empirical evidence of reliability.

## Cloud and spending constraints
GitHub's official documentation (checked 2026-11-20) states standard GitHub-hosted runners for public repositories are free; larger runners are billed even in public repositories. Use only standard `ubuntu-latest` or equivalent, no GPU or larger runner, no paid APIs, no persisted large artifacts, and no local user-machine workloads. Docs: https://docs.github.com/en/actions/concepts/billing-and-usage and https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job . These published conditions do not verify account-specific billing settings or runner availability at execution time; check workflow configuration and actual run before any experimental claim.

## Status
This note is a methodological correction and experimental decision gate. No new model experiments, theorem, or novel result is claimed. Existing code has not been modified by this note.
