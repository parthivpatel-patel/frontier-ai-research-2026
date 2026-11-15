# Protocol 087 — Adaptive-verification prior-art collision and falsification gate

Date: 2026-11-14. Status: literature audit and prospective protocol, not an empirical result or a novelty claim.

## Source-checked closest prior art

1. Golovin and Krause (2011), *Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization*, Journal of Artificial Intelligence Research 42, 427–486. DOI 10.1613/JAIR.3278; https://mlanthology.org/jair/2011/golovin2011jair-adaptive/ . Establishes a broad theory for sequential information gathering with partial observations, adaptive greedy algorithms, and active learning. A generic claim that adaptive selection under a verification budget is new is untenable.
2. Golovin and Krause (2011), *Adaptive Submodular Optimization under Matroid Constraints*, https://arxiv.org/abs/1101.4450 . Develops adaptive optimization under combinatorial constraints. A new algorithm needs a comparison against relevant constrained adaptive policies, not only static greedy.
3. Lakkaraju, Kleinberg, Leskovec, Ludwig, and Mullainathan (2017), *The Selective Labels Problem: Evaluating Algorithmic Predictions in the Presence of Unobservables*, KDD, DOI 10.1145/3097983.3098066; https://pubmed.ncbi.nlm.nih.gov/29780658/ . Demonstrates the importance of outcomes observed only after selection decisions. Scientific verification may induce an analogous selection mechanism; this is an analogy, not a claim of identical identification assumptions.
4. Sawade, Landwehr, and Scheffer (2010), *Active Estimation of F-Measures*, NeurIPS. Source identification requires checking the original proceedings paper before treating its precise guarantees as established in our manuscript. Active evaluation under label budgets is a serious competing direction.

These are collision candidates, not an exhaustive 2026 literature review. Verify original texts and search newer benchmark-specific work before publication.

## Baseline no-adaptivity result and its boundary

For a fixed census K, independent Bernoulli adjudication successes X_i with fixed known p_i, positive deterministic costs c_i, at most one attempt per claim, and a hard pathwise budget B, the expected reduction in unrestricted identification width from any attempted subset S is sum_{i in S} p_i/K. If a policy chooses future attempts using observed outcomes, independence and unchanged probabilities imply no outcome-conditioned improvement over the optimal feasible deterministic subset: conditioning on any attempted set yields the same additive expected reward. Thus exact knapsack is a ceiling in this model. This is a simple consequence of the assumptions, not an original theorem.

**Important nuance:** A ratio-greedy algorithm is not the adaptive greedy theorem of Golovin and Krause; their guarantees depend on specified structural conditions. Do not conflate these algorithms. Under correlated success outcomes or shared latent adjudication difficulty, a previous outcome may update later probabilities, and the static ceiling need not apply. Even then, existing adaptive optimization literature may already solve the abstract decision problem.

## Falsifiable candidate research question

Can a fully specified provenance-aware verification policy improve **held-out, cost-normalized adjudication yield and calibrated false-release-rate uncertainty** for scientific claims spanning NLP, mathematics, and physics, beyond exact static optimization using calibrated probabilities and a strong adaptive Bayesian baseline?

This is a question, not a finding. The interval-width outcome is mechanically tied to the number of resolved claims under unrestricted census bounds; any advantage must be explained by different resolution probabilities, costs, or assumptions, never by selection order alone.

## Preregistered controls

- Separate a fixed claim census from sampling-based population inference. Do not call a sharp identification interval a confidence interval.
- Include independent-success negative control where adaptive policies must not beat the true-probability static knapsack oracle in expectation.
- Include a latent-family model with explicitly correlated adjudication outcomes; compare static posterior-mean knapsack, posterior-updating adaptive dynamic programming for tiny cases, cost-aware greedy, and a learned policy. Exact dynamic programming is a tiny-case oracle, not a scalable implementation claim.
- Record attempted claims, realized successes, failures, costs, provenance family, adjudicator abstentions, and hidden truth separately; never leak hidden labels into policy features.
- Evaluate cross-domain transfer by holding out entire provenance families and source time blocks. Predeclare primary and secondary metrics, error bars, and stopping conditions.
- Add a selective-label adversary where verification success depends on unobserved claim falsity; report identification sensitivity instead of treating observed resolved-label error as unbiased.
- Reject the proposed novelty if improvement disappears against adaptive baselines, arises only from synthetic probabilities, depends on unverified oracle access, or fails domain-held-out replication.
- Require a human-readable error taxonomy and evidence citations for adjudication, with unresolved status when the evidence is insufficient. No invented scientific ground truth.

## Free-cloud and reproducibility gate

This protocol does not authorize execution. Before any cloud job, confirm the specific account's free eligibility, billing/card prerequisites, runner type, quotas and spending controls. Avoid laptop compute, paid APIs, large downloads, training, and model inference on the laptop. A dependency-free small exact test may be run only on verified free cloud capacity. No compute or empirical results are asserted here.

## Publication decision

November 22, 2026 is an internal conditional target. If closest-prior-art review or empirical replication does not support novelty, publish a clearly labeled negative/replication report or delay the paper. Disclose AI assistance in accordance with the venue's policies.
