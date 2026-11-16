# Protocol 111 — Cross-oracle validity boundaries and falsification gates

Status: design and source audit only; **not an executed experiment**. Prepared 2026-11-15. This protocol is independent of other projects.

## Source inspection

Inspected `research/fixtures/test_protocol_107_cross_oracle.py` and `research/fixtures/test_protocol_110_cross_oracle_negative_controls.py` at their published default-branch versions. Protocol 107 compares the Bellman value, exhaustive enumerator value, and separately scored witness. Protocol 110 deliberately mutates three outputs to test whether comparison assertions reject mismatches.

The comparison matrix contains 12 one-claim, 45 two-claim, and one three-claim cases. It is a *test-input matrix*, not 58 independently observed scientific outcomes. The negative controls test the comparison mechanism, not the mathematical validity of the reward function.

## Shared-assumption failure mode

All three oracles accept the same joint world distribution, verification costs, budget, and definition of reward. If those inputs or the reward definition misrepresent actual scientific verification, exact agreement is compatible with a scientifically wrong decision. In particular, the following remain outside cross-oracle validation:

1. **Distribution misspecification.** Estimated correlations may be unstable under domain shift; calibration must be evaluated on held-out cases.
2. **Observation-model misspecification.** Real verification tools may have false positives, false negatives, abstentions, and correlated errors; perfect-revelation synthetic worlds do not model these.
3. **Reward misspecification.** Counting verified true claims may encourage easy low-value claims rather than important correct adjudications; false-acceptance and false-rejection penalties must be explicit.
4. **Budget misspecification.** A unit verification cost is not a measured latency, compute, token, monetary, or human-review cost.
5. **Selection bias.** Claims sampled from one model, benchmark, or difficulty level cannot justify generalization to frontier models or other domains.

## Required empirical baselines

Compare a preregistered dependency-aware policy against (a) random valid verification order, (b) fixed prior-probability ranking, (c) cost-normalized myopic value of information, and (d) a Bayesian adaptive planning baseline with the *same* information and budget. Use exact enumeration only for small cases where it is computationally tractable. Do not describe Bayesian planning or adaptive selection as novel.

For NLP, mathematics, and physics, define separate claim datasets with independent answer keys and provenance. No LLM judge may be treated as ground truth without human or formal verification. Record tool uncertainty, abstentions, and correlated failures. Evaluate both decision quality and verification resource use; report per-domain results rather than only pooled averages.

## Falsification and stop conditions

- **Implementation:** Any Bellman/enumerator/witness disagreement on a supported exact-rational instance fails the cross-oracle gate until diagnosed.
- **Mutation sensitivity:** A deliberately corrupted comparator input that is not rejected fails the negative-control gate.
- **Calibration:** If held-out probabilities or dependency estimates are not calibrated, refrain from causal or deployment claims and report sensitivity to misspecification.
- **Value:** If the proposed method fails to outperform the strongest information-matched baseline on the preregistered primary outcome, report the null or negative result.
- **Generalization:** If effects disappear under domain-held-out evaluation, restrict claims to the observed domain.
- **Novelty:** If the contribution reduces to known Bayesian decision theory or adaptive verification without a new validated result, position it as a reproducibility or negative-results study, not a new algorithm.

## Free-cloud execution gate

No job is authorized by this document. Before any GitHub Actions run, verify that the repository is public, the runner is a GitHub-hosted **standard** runner, the current GitHub billing terms permit free public-repository use, the workflow does not invoke paid services or larger runners, and account/repository policy permits the action. Record exact commit, workflow, runner label, timestamps, exit code, and logs. Set job timeout and process memory limits where supported; reject unbounded enumeration. Do not use the user's laptop for computation. If eligibility or billing cannot be verified, do not launch.

## Publication integrity

Distinguish mathematical deductions, authored test cases, executed tests, and real-domain evidence in every figure and abstract. Cite primary prior art, publish negative findings, preserve full reproducibility logs, and disclose AI assistance as required by the target venue. November 22, 2026 is a conditional decision checkpoint, not a guaranteed publication date.
