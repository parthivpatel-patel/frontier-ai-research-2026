# Protocol 055 — Prior-art collision and falsification gate (13 November 2026)

**Status:** Research planning and critical literature audit; not an empirical result, novelty claim, or proof of publication readiness.

## Central claim under examination

A dependence-aware, partially identified posterior interval for AI-generated scientific claims may support decisions to accept, reject, or abstain under explicitly stated loss and shift assumptions. The mathematical building blocks are **not new**. The open research question is whether an operational method, with estimable assumptions and claim-disjoint evaluation, offers a reproducible benefit over strong existing alternatives.

## Closest prior art and collision risks

| Area | Representative prior work | Collision / required distinction |
| --- | --- | --- |
| Classification with a reject option | Chow (1970), *On optimum recognition error and reject tradeoff*, IEEE Transactions on Information Theory, doi:10.1109/TIT.1970.1054406 | Cost-based abstention thresholds are established. No novelty from deriving a threshold or an abstain action. |
| Selective prediction | Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, NeurIPS, https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html | Risk-coverage tradeoffs are established. Compare at matched coverage and with calibrated confidence. |
| Partial identification | Manski (2003), *Partial Identification of Probability Distributions*, Springer | Bounds under incomplete identification are established. Distinguish the scientific application and any novel estimable restriction. |
| Multiple noisy annotators | Dawid and Skene (1979), *Maximum Likelihood Estimation of Observer Error-Rates Using the EM Algorithm*, Applied Statistics, doi:10.2307/2346806 | Combining fallible annotators is established; assumptions about conditional independence and latent truth need explicit treatment. |
| Conformal uncertainty | Angelopoulos and Bates (2023), *Conformal Prediction: A Gentle Introduction*, Foundations and Trends in Machine Learning, https://arxiv.org/abs/2107.07511 | Distribution-free predictive guarantees under exchangeability are an important baseline, but they are not the same estimand as posterior truth confidence. |
| Robust decision theory | Classical minimax / least-favorable-prior theory | The deterministic/randomized minimax gap and dual certificates from Protocols 053–054 cannot independently establish novelty. |

Bibliographic pointers are a **starting list, not an exhaustive systematic search**. Before submission, verify bibliographic metadata and review subsequent and concurrent work on correlated LLM judges, verifier ensembles, uncertainty calibration, and selective generation.

## Operational identifiability gate

The joint verifier-output frequencies alone cannot identify truth-conditioned accuracy. Before any empirical claim, specify exactly which labeled audit data, conditional-dependence constraints, or sensitivity ranges identify the interval. Estimate these on training/calibration claims only. Report sensitivity to violation, prevalence shift, and dependence shift. An oracle supplied with true verifier error rates is not an operational baseline.

## Pre-registered falsification tests

1. **Claim-family split:** split by source problem, theorem, dataset, and paraphrase family; prohibit near-duplicate leakage.
2. **Baselines:** majority vote, deduplicated vote, independently calibrated confidence, cost-sensitive deterministic abstention, selective prediction, and a conformal approach where its assumptions and estimand apply.
3. **Matched evaluation:** compare error and loss at equal coverage, and coverage at fixed error, with claim-cluster bootstrap intervals.
4. **Dependence stress:** clone verifier outputs and vary correlated error without changing marginal rates; require the method not to count duplicated evidence as independent confirmation.
5. **Shift:** vary prevalence and verifier-dependence structure across claim families. Measure calibration and coverage degradation.
6. **Assumption failure:** include settings where the identification interval is vacuous, calibration is poor, or abstention costs dominate. A useful method must be allowed to lose.
7. **Randomized policy:** compare expected costs using independently seeded randomness, but never interpret a randomized accept decision as a guarantee for an individual high-stakes claim.
8. **Ablation:** isolate the incremental effect of dependence bounds from deduplication, calibration, and the decision rule itself.

## Publication decision rule

Do **not** claim an original theorem from interval arithmetic, minimax duality, or randomized abstention alone. A paper should proceed only if it identifies a genuinely differentiated algorithm, assumption/guarantee, or compelling reproducible empirical finding and shows that the improvement survives the baselines and falsification tests above. A rigorous negative result may still merit publication if framed accurately.

## Zero-cost execution gate

No cloud job may be launched until the account-specific GitHub Actions eligibility, public-repository standard-runner terms, billing/spending controls, and runner availability are verified. No self-hosted runner, paid GPU, cloud trial with uncertain charges, local model inference, or laptop-intensive work. Record run URL, workflow SHA, runner label, execution time, cost status, and test outputs for each approved cloud run.

**Current status:** All prior fixtures are committed but no cloud execution has been verified in this protocol. November 22, 2026 is an internal target, contingent on evidence, not a publication commitment.
