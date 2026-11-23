# Prior-art collision and falsification audit (2026-11-22)

Status: **working research audit, not a claim of novelty**. This note separates established mathematical machinery from a potentially publishable AI-evaluation contribution. Bibliographic details and exact theorem coverage must be checked against primary texts before submission.

## Precise mathematical object

For unresolved binary truths (z_i\in\{0,1\}), an evidence record (e=(i,j,b)) asserts (z_i\oplus z_j=b). A budget (k) permits at most (k) violated **records**, counting duplicates separately. For each admissible assignment, compute the difference between two selective-error rates from the same underlying cases, only when both denominators are positive. The sharp set is the minimum and maximum of those differences across admissible assignments. An empty admissible set is **infeasible**, not a zero-width confidence interval; if rates are undefined, report that separately.

The (k=0) connected-component parity reduction is standard graph/XOR reasoning. For (k>0), minimizing violations is a signed-graph frustration / Max-2-LIN-type problem. Exact enumeration is a correctness oracle on tiny instances, **not** a scalable algorithm or new complexity result.

## Closest prior-art families to check

1. **Partial identification / missing outcomes:** Charles F. Manski, “Nonparametric Bounds on Treatment Effects” (1990), *American Economic Review*, 80(2), 319–323. Compare what is identified when missing labels are unrestricted versus constrained; do not call interval optimization itself novel.
2. **Sharp bounds with latent variables:** Alexander Balke and Judea Pearl, “Bounds on Treatment Effects from Studies with Imperfect Compliance” (1997), *JASA* 92(439), 1171–1176. Distinguish a sharp identified set from a sampling-confidence interval and compare linear-fractional optimization.
3. **Binary constraint optimization:** Johan Håstad, “Some Optimal Inapproximability Results” (2001), *Journal of the ACM* 48(4), 798–859. Check Max-E2-LIN2 and related hardness; do not claim a generic polynomial-time exact algorithm for arbitrary bounded-violation parity systems.
4. **Graph frustration / correlation clustering:** Nikhil Bansal, Avrim Blum, and Shuchi Chawla, “Correlation Clustering” (2004), *Machine Learning* 56, 89–113. Check whether treating noisy pairwise same/different labels as record-weighted disagreements is already standard.
5. **Selective prediction:** Yonatan Geifman and Ran El-Yaniv, “Selective Classification for Deep Neural Networks” (2017), *NeurIPS*. Distinguish conditional error among accepted cases from population error; a comparison of selective risks must preserve each policy's acceptance denominator.
6. **Conformal risk control:** Anastasios N. Angelopoulos and coauthors, “Conformal Risk Control” (2024), *ICLR*. Conformal calibration guarantees under exchangeability are not the same as partial identification under unobserved ground truth.

These references are candidate collision checks, not a completed systematic search. Exact source passages, later work, and cross-citations still need examination.

## Defensible contribution boundary

A potential contribution is a **reproducible evaluation protocol** for paired AI verification systems with selectively missing ground truth, auditable provenance of semantic/logical constraints, and record-level contamination sensitivity. Its value must come from an empirically important failure mode, useful diagnostics, and comparisons against appropriate baselines—not from relabeling existing Max-2-LIN or partial-identification results.

NLP equivalence must be adjudicated using independent evidence; mathematical equivalence requires explicit assumptions; physics statements must specify measurement uncertainty, units, and regimes. No automatic cross-domain equality constraints should be inferred from superficial paraphrase.

## Mandatory falsification and stop/go gates

- Compare unrestricted, independently authenticated (k=0), and (k>0) intervals on preregistered held-out examples. Reject any result where a claimed sharp interval excludes a feasible brute-force truth assignment.
- Test inconsistent cycles, duplicated records, self-constraints, empty acceptance sets, and differing policy acceptance patterns. Never silently drop contradictions.
- With a fixed record multiset, the identified set must be nested as (k) increases; at (k\ge |E|) it must equal unrestricted identification.
- Assess provenance mistakes by deliberately inserting incorrect pairwise constraints and measuring undercoverage against fully adjudicated labels. Do not interpret tighter intervals alone as improvement.
- Compare against unrestricted Manski-style bounds, a direct binary optimization formulation, and a simple record-disagreement baseline; report computation cost and abstention denominators.
- Avoid leakage: adjudicators and evidence retrieval cannot see held-out ground truth or the preferred policy's outputs when constructing constraints.
- A public paper requires authenticated data, frozen split and hypotheses, reproducible cloud execution, uncertainty analysis, and disclosure of AI assistance. If these are missing, publish only as a clearly labeled methods/preregistration note.

## Free-compute gate

The existing public-repository GitHub Actions workflow uses a standard hosted Ubuntu runner and a five-minute timeout. Public-repository standard runner billing policy is not evidence that this account has an unlimited usable entitlement. Before new expensive experiments, confirm repository visibility, Actions enablement, account billing settings, and current GitHub pricing/limits. Never configure self-hosted machines, paid larger runners, cloud GPU trials requiring payment credentials, or local laptop inference without authorization.

## Next executable step

Inspect the actual CI run for commit `2495b884ff0ff42770944a91bc691083dd1f2265`, record job ID, conclusion and test counts, and fix any failing regression before interpreting scientific evidence. Then build an independently adjudicated small held-out dataset with provenance and leakage controls; do not substitute synthetic tests for empirical model evidence.
