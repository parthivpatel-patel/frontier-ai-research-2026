# Protocol 198 — Operational failures, estimand scope, and publication gates

Date: 2026-11-11. Status: preregistration refinement; no executed tests or model observations.

## Motivation and correction to Protocol 197

Protocol 197 appropriately distinguishes an explicit model abstention U from an infrastructure or API failure F, but its sharp binary-acceptance interval assigns both [0,1]. That interval is mathematically conservative only for a **hypothetical completed response** on a specified attempt. An operational failure is not itself an observed model decision; without a stable target model/version and an explicit retry policy, the counterfactual completed response may not be well defined. Consequently, a single interval that pools F and U must never be described as a measured property of the model's scientific judgment.

## Predeclare two distinct targets

**Attempt-level operational outcome.** For every randomized requested pair, record whether each arm returned a parseable answer, explicit abstention, policy refusal, timeout, provider error, or protocol violation. Report paired joint completion, per-arm failure, and time-to-completion distributions. These quantities describe the deployed evaluation process, not necessarily scientific reasoning.

**Model-response provenance contrast.** For a fixed version, prompt and decoding policy, define the latent binary acceptance contrast only under a clearly stated hypothetical successful completion. A/J determine binary acceptance; U yields [0,1] if the desired target is a forced binary answer, but that target is hypothetical and distinct from natural-response behavior. F yields [0,1] only under the additional assumption that a stable hypothetical completion exists. Report results both (i) with F excluded from the model-response estimand and its resulting target-population restriction explicitly stated, and (ii) with F included in conservative sensitivity bounds if that counterfactual is defensible. Neither analysis can remove selection concerns by silently dropping F.

For natural behavior, use the fully observed three-category A/J/U distribution on successful requests as a separate outcome; do not collapse abstention into rejection. Failed requests remain a fourth operational state.

## Precommitted failure handling

1. Assign a unique request ID, physics-problem ID, randomized arm order, model/version identifier, timestamp, exact prompt hash, and evaluator version before dispatch.
2. Classify technical failures using observable transport/provider evidence, not model answer content. A text refusal or uncertainty response is not a network failure.
3. Predefine maximum retries, backoff, and whether retries are part of the primary estimand **before** any model calls. Keep all attempts and outcomes; never substitute a successful retry without an audit trail.
4. If a model version changes between arms, flag the pair as non-comparable for the fixed-version contrast; report its exclusion separately, and do not silently replace it.
5. Preserve denominators: randomized pairs, attempted calls, completed calls, valid A/J responses, abstentions, policy refusals, and technical failures.
6. Do not run an experiment if quota, billing protection, provider terms, or free-tier access cannot be independently confirmed.

## Falsification and sensitivity analysis

A purported provenance effect fails the primary scientific interpretation if the presentation-sham effect is comparable to the provenance manipulation, if independently adjudicated labels are unstable, if controls based on valid graph reassignment produce similar rejection, or if the lower partial-identification bound does not exceed the preregistered meaningful threshold after uncertainty accounting. Strong arm-specific failure imbalance is a separate operational warning, not proof of model discrimination.

Report the best-case/worst-case interval for incomplete pairs, the fraction of its width attributable to U versus F, and results stratified by fixed model/version and physics problem. For repeated prompts, cluster at the original problem level; avoid treating permutations as independent physics cases.

## Exact algebraic sanity checks (not executed)

For one pair A/J, contrast is exactly +1. For A/U, latent forced-binary contrast is [0,1]. For A/F, the same numerical interval is only a hypothetical-completion sensitivity interval, **not** an observed model response. For F/F, [-1,1] carries no direct information about scientific discrimination. For an A/J pair from different model versions, the numerical difference is observed but cannot identify a within-version paired effect.

## Prior-art and novelty boundary

Missing-data partial identification, principal-stratum selection concerns, and intention-to-treat versus per-protocol distinctions are established methodological ideas. This protocol is a design correction, not a new theorem. A defensibly novel contribution still requires a documented comparison to prior provenance intervention, explanation faithfulness, citation grounding, process supervision, and selective-prediction work, plus reproducible physics-grounded empirical evidence. Relevant starting points include Manski's partial identification, Turpin et al. on unfaithful chain-of-thought explanations, Lightman et al. on process supervision, and Jacovi & Goldberg on faithfulness. Verify full texts, bibliographic details, and exact claim overlap before a novelty assertion.

## Execution and publication constraints

No inference, training, simulations, cloud jobs, or laptop computation was conducted for this protocol. Do not spend money or trigger any workflow until account-specific free-cloud availability, card/billing conditions, quota and safeguards have been verified. Maintain public artifact provenance, accurate AI-assistance disclosure when required, and a strict distinction between proposed tests and executed results. November 22 is an internal conditional target, not a promised publication date.
