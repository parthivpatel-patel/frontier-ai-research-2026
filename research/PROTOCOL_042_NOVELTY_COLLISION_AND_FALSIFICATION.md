# Protocol 042 — novelty collision and falsification gate (2026-11-03)

## Decision
**No novelty claim is currently defensible.** Prior art already covers natural-language-to-temporal-logic translation, proposition grounding, verification against environment traces, verifier-in-the-loop learning, and selective abstention. The project must not describe any of these individually as novel.

## Closest prior art requiring head-to-head comparison
1. Chen et al., *NL2TL: Transforming Natural Languages to Temporal Logics using Large Language Models* (arXiv:2305.07766). Lifted translation and grounding are existing methods.
2. English et al., *Verifiable Natural Language to Linear Temporal Logic Translation: A Benchmark Dataset and Evaluation Suite* (arXiv:2507.00877). VLTL-Bench explicitly tests proposition grounding, verification, and end-to-end verifiability. This directly challenges any claim that end-to-end grounded verification is new.
3. Quansah and Bonnah, *NeuroNL2LTL* (arXiv:2605.22874). Neurosymbolic intermediate representations, satisfiability checks, repairs, and verifier-in-the-loop training are prior art.
4. Wang et al., *SCP-NL2TL: Selective Conformal Prediction with Semantic Verification* (arXiv:2608.05439). Selective acceptance/abstention and calibrated semantic verification are prior art.
5. Clarke et al. (2000), *Counterexample-Guided Abstraction Refinement*; Alur and Dill (1994), *A Theory of Timed Automata*. Forward simulation, abstraction, and model checking are classical foundations.

Bibliographic records and reported metrics require checking against full papers before final manuscript citation; this is a screening audit, not a completed systematic review.

## Narrow remaining hypothesis (unproven)
For scientific language statements referring to measurable physical dynamics, an independently audited physical-model provenance and simulation/trace-inclusion certificate may reduce **unsafe acceptance** relative to a matched NL-to-logic pipeline with conventional satisfiability and semantic checks, at a prespecified useful coverage.

The claim is about **incremental empirical reliability**, not invention of formal methods, natural-language translation, physical constraints, or abstention.

## Locked experiment
- Unit: a *source-level scientific claim*, not multiple paraphrases counted as independent.
- Split by source document, physical system, and formula family. Freeze the test split before model selection.
- Use independently authored ground-truth state transitions, parameter domains, units, boundary conditions, and admissible uncertainty; do not derive the oracle from model-generated text.
- Baselines: literal NL-to-LTL, lifted NL2TL with oracle grounding (diagnostic upper bound), grounded VLTL-style pipeline, verifier-only checks, and selective conformal/abstention method. Compare with the identical language model, prompts budget, and data exposure where feasible.
- Ablations: remove physical certificate; replace sound abstraction with underapproximation; remove independent grounding; remove abstention; remove units/boundary conditions.
- Negative controls: contradictory claims, ambiguous referents, unknown physical parameters, impossible transitions, spurious abstract counterexamples, valid physical counterexamples, deadlocks, and out-of-domain systems.
- Report accepted-case correctness, unsafe-acceptance rate (numerator and denominator), coverage, selective risk at matched coverage, false rejection, cost, and confidence intervals clustered by source/system.
- Require the verifier to distinguish verified-under-assumptions, falsified-by-valid-witness, and inconclusive. Never equate finite trace sampling with a universal proof.

## Preregistered failure conditions
1. If matched baselines have indistinguishable or lower unsafe-acceptance rates at equal coverage, reject the claimed reliability improvement.
2. If the independent oracle disagrees with the claimed physical model or cannot establish soundness, withhold verification claims.
3. If performance disappears on held-out systems or source-disjoint splits, reject cross-domain generalization.
4. If any claimed certificate excludes an admissible physical counterexample, treat this as a critical unsoundness failure.
5. If the effect is explained entirely by abstaining on more cases, reject any superiority claim without matched-coverage comparison.
6. If model inference cannot be conducted within verified zero-cost cloud resources, report only the finite-state methods result; do not invent an LLM evaluation.

## Infrastructure and integrity
Repository is public. GitHub documentation (https://docs.github.com/en/actions/concepts/billing-and-usage) states that standard GitHub-hosted runners are free for public repositories, while larger runners are chargeable. Restrict future workflows to standard `ubuntu-latest`, use strict timeouts and minimal/no artifact retention. Account-specific budget and payment settings have not been independently inspected; no new workflow is launched by this protocol. Existing public Actions run 41600884695 concluded success on 2026-11-03, but that run only demonstrates the Protocol 030 negative control, not Protocols 034–041.

No laptop compute, GPU, paid service, or unverified empirical result is required or claimed. Target date 2026-11-22 is conditional on valid evidence.
