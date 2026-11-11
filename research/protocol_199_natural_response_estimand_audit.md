# Protocol 199 — Pre-execution audit of the inference target and a stop/go decision

Date: 2026-11-11. Status: analytic audit only; not an executed experiment.

## Critical distinction: observed response versus forced-answer potential outcome

Protocols 197–198 bound a latent binary answer when the observed response is abstention or failure. A forced answer is **not** identified merely by treating an abstention as a missing binary outcome. A forced-answer intervention may change the model's response distribution; the resulting estimand is a *different intervention* from natural prompting. Accordingly, do not label an interval formed by replacing U with [0,1] as a bound on an empirically observed natural-response discrimination effect.

For natural responses, define the fully observable successful-request outcome in {accept, reject, abstain, refusal}. Report category probabilities and paired transitions, preserving failure as a separate operational outcome. The binary acceptance indicator 1{accept} is well-defined even with abstentions (they contribute zero), but measures **acceptance frequency**, not latent correctness conditional on answering. If a paper wants a hypothetical forced binary judgment, it must explicitly specify a forced-response prompt and evaluate that intervention independently; unobserved potential answers from the natural prompt cannot be assumed equivalent.

## Identification and pairing

A pair of prompts run sequentially on a nondeterministic, potentially drifting service does not by itself establish a causal effect. Randomized arm order, fixed model/version, balanced surface changes, and repeated problem-level sampling support a design-based contrast. The primary scientific interpretation must remain narrower than a causal claim about internal model reasoning. Observed rejection of corrupted provenance can result from surface cues, distribution shift, answer leakage, or memorized content.

An explicit sham intervention should change identifiers or formatting while preserving the semantic graph. A valid-reassignment control should change the graph without invalidating scientific provenance. The corruption arm must be independently labeled by a physics reviewer without access to model outputs. A sham effect comparable to corruption defeats a provenance-specific interpretation.

## Exact paired natural-response statistics

For n preselected pairs with successful responses, let A_iz be 1 if the response in arm z is accept, otherwise 0, including abstentions/refusals. Define D_accept = (1/n) sum_i (A_i0 - A_i1). This is an acceptance-rate contrast, not forced-choice accuracy. Publish the complete joint response table. Separately report per-arm success and abstention rates; never condition the primary target on both arms answering A/J without acknowledging selection. For technical failures, report an attempt-level composite outcome and sensitivity analyses rather than quietly deleting failures. Predeclare what population is represented by successful pairs.

## Failure modes that would falsify the intended contribution

1. Corruption-vs-sham contrasts are indistinguishable at the preregistered resolution.
2. Independent experts disagree materially on which physics provenance links are invalid.
3. The negative certificate checker fails even one exhaustively enumerated small graph.
4. Performance depends on identifier names, edge order, answer location, or prompt phrasing.
5. Baseline systems already detect the same provenance faults with equal or better performance and simpler machinery.
6. A closest-prior-art study already implements the same intervention and estimand, defeating a methodological novelty claim.
7. Model access or cloud resources cannot be confirmed strictly zero-cost; in that case, no empirical execution occurs.

## Prior-art audit matrix to complete before a novelty claim

| Area | Representative work to inspect in full | Potential overlap | Distinguishing evidence required |
| --- | --- | --- | --- |
| Faithfulness of explanations | Jacovi & Goldberg (2020), *Towards Faithfully Interpretable NLP Systems* | Definition of faithfulness and intervention criteria | Demonstrate an experimentally distinct provenance-graph target |
| Unfaithful rationales | Turpin et al. (2023), *Language Models Don't Always Say What They Think* | Counterfactual cues and explanation mismatch | Show physics evidence links, not merely rationale perturbation |
| Process supervision | Lightman et al. (2023), *Let's Verify Step by Step* | Verification of intermediate reasoning steps | Show independent evidence-provenance evaluation rather than step scoring |
| Citation faithfulness and attribution | Attribution/citation-grounding and retrieval-augmented verification literature (specific full texts pending) | Support checking, evidence swaps, source attribution | Show genuinely distinct graph intervention and adversarial baselines |
| Graph intervention | Degree-constrained bipartite matching and max-flow/min-cut (classical) | Feasibility and cut certificates | No novelty claim for established graph mathematics |
| Missingness | Manski partial-identification literature (classical) | Worst-case response bounds | No novelty claim for established missing-data bounds |

This is a *reading and falsification checklist*, not proof that these are the closest papers. Search for 2024–2026 work on causal attribution, provenance graph editing, evidence substitution, scientific claim verification, and LLM citation faithfulness. Record exact paper titles, versions, experimental manipulations, datasets, estimands and baseline scores with verified citations before asserting novelty.

## Priority order and publication decision

**Gate A:** Execute and pass Protocols 191–194 on a cloud runner with independently verified $0 billing exposure, quotas, and eligibility. **Gate B:** Independently label a small physics corpus with agreement statistics. **Gate C:** Complete full-text overlap review and pre-register baselines. **Gate D:** Run a bounded, genuinely free pilot; preserve raw outputs, costs and model versions. Until all gates are satisfied, present a methods proposal or negative feasibility report, not an empirical frontier-model finding.

No cloud execution, inference, model training, local workload, or paid service was performed for this protocol. November 22 remains a conditional target.
