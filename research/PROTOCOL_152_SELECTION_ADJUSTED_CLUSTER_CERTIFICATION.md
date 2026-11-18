# Protocol 152 — Selection-adjusted source-cluster risk certification (2026-11-17)

## Scope and provenance

This is a **theoretical analysis and preregistration proposal**, not an empirical result, a novel theorem, or a certification of a deployed model. It extends Protocols 147–150 and is deliberately separated from all other projects. No inference, cloud job, or local computation is required.

## Statistical object

Let independent evaluation source clusters `Z_1,...,Z_n` be drawn i.i.d. from a stated target source population. For each policy `k` in a **precommitted finite family** of size `K`, define cluster loss `L_k(Z_i) in [0,B]`. Within-source questions can be arbitrarily dependent; the cluster-level aggregation rule must be fixed before observing evaluation outcomes. Define `R_k=E[L_k(Z)]` and `Rhat_k=n^{-1} sum_i L_k(Z_i)`.

For any `alpha in (0,1)`, Hoeffding plus the union bound gives, simultaneously for all precommitted policies,

`R_k <= Rhat_k + B sqrt(log(K/alpha)/(2n))`

with probability at least `1-alpha`. Consequently, **selecting a policy based on these same evaluation clusters** is allowed *within this finite, fixed family*, provided the simultaneous bound is used. The naive single-policy radius `B sqrt(log(1/alpha)/(2n))` is not justified for the selected policy without additional independence or selection correction.

This is an established concentration/union-bound construction, not an original mathematical contribution.

## Concrete falsifiable predictions

1. For `K=1`, the simultaneous radius reduces exactly to the single-policy Hoeffding radius.
2. For fixed `n,alpha,B`, increasing `K` cannot decrease the radius.
3. Duplicating prompts inside an existing source cluster must not increase `n`.
4. Adaptive generation or modification of candidates after examining evaluation labels invalidates the fixed-family premise; recording only the final number `K` does not repair it.
5. Adversarial or convenience sampling of clusters invalidates population-risk coverage even when source IDs are unique.
6. Non-identically distributed source populations, cross-cluster dependence, noisy labels, or missingness require different assumptions and potentially different bounds.
7. A large `K` or small `n` may make the upper bound vacuous; no claimed certification should hide this.

## Experiment preregistration gate

- Freeze policy definitions, loss range, aggregation rule, target population, selection budget `K`, alpha, source sampling, and dataset provenance **before** inspecting evaluation labels.
- Split sources, not prompts, across development and evaluation. Record exact source IDs, dataset licenses, transformations, and duplicate groups.
- Compare three valid designs: independent holdout after selection; finite-family simultaneous bound; and a precommitted sequential/martingale approach with its separately proven assumptions.
- Run matched comparisons across NLP factuality/entailment, mathematical reasoning, and physics reasoning only when independently labelled sources and permitted cloud execution are available.
- Publish null results and failures. Do not claim AI welfare, experience, universal safety, or frontier-model superiority from verifier agreement or synthetic fixtures.

## Prior-art collision register

The finite-family correction is standard Hoeffding (1963) plus Bonferroni/union-bound multiple comparisons. Closest conceptual areas requiring theorem-level comparison before novelty claims: selective classification and risk-controlling prediction sets; adaptive data analysis and reusable holdouts; partial identification (Manski); conformal risk control; sequential testing/e-values; and distributionally robust optimization. The 2026 joint finite-sample selective conformal certificate flagged in Protocol 144 is a high-priority collision to check against its **actual theorem statements and assumptions**. No priority or novelty claim is made without a full-text comparison.

## Publication decision

The contribution, if any, must come from a carefully defined new **operational regime or empirical finding** under explicit adversary information, verification costs, dependence and source-sampling constraints. If established baselines match performance under matched budgets, or the gains disappear under source-disjoint tests, report the negative result rather than presenting the framework as novel.

## Resource gate

Only standard GitHub-hosted runners in this public repository are currently contemplated for small deterministic tests. Account-specific billing and eligibility are not inferred from public pricing; do not enable paid runners, external inference endpoints, billing upgrades, or downloads. User laptop remains browser-only.
