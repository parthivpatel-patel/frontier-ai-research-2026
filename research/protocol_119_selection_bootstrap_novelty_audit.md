# Protocol 119 — Selection, bootstrap validity and novelty checkpoint

Date: 2026-11-07. Status: methodological audit; no empirical findings or executed tests.

## Verified code boundary

Reviewed `research/admitted_common_acceptance_bootstrap.py` and `research/common_acceptance_bootstrap.py` at repository HEAD `ece36f42c5564604560f027a62784dcec66a6fb0`. The bridge requires Protocol 113 admission and heldout records. The estimator resamples lineages within physics families and computes a family-weighted paired unsafe-response contrast conditional on joint acceptance.

### Important inferential limitation

The bootstrap currently discards replicates for which any positive-weight family has zero jointly accepted observations, then calculates percentile endpoints from the remaining defined draws if the undefined fraction is below a configurable threshold. Consequently the resulting interval is **conditional on a defined resampled denominator**, not an unconditional 95% confidence guarantee. The threshold of 0.01 is an engineering convention, not a theorem. A rare-acceptance family can cause highly unstable intervals even when the original estimate exists. Do not label this interval calibrated, exact, or coverage-guaranteed.

## Required falsification and sensitivity gates

1. Freeze physics-family weights, intervention lineages, system thresholds and primary estimand before heldout labels are revealed.
2. Report family-specific numbers of lineages, interventions, joint acceptances, and original denominators, not only the weighted contrast.
3. Run seeded synthetic coverage experiments with known data-generating distributions **on confirmed free cloud only**, varying lineage count, within-lineage correlation, acceptance rarity and heterogeneous family risks. Evaluate nominal 95% interval coverage and undefined replicate rates. Never use those simulations as evidence of real-world AI performance.
4. Compare percentile bootstrap with a lineage-level studentized or other justified interval where feasible. If coverage fails materially, suppress confirmatory interval claims.
5. Predefine handling of undefined families. Never silently drop difficult families, reweight after observing labels, or interpret missing estimates as zero.
6. Report both systems' marginal coverage, joint coverage, the four acceptance cells, system-specific selective risk, and joint-acceptance paired risk. Do not claim the joint subset represents all interventions.
7. Randomize evidence intervention order; test irrelevant-evidence swaps and label-preserving paraphrases. Separate changes in answer from changes in abstention.
8. Use independent physics adjudication with immutable source provenance and blinded review; explicitly record unresolved disagreements.
9. Compare against no-evidence, shuffled-evidence, confidence-only, and task-specific baselines. If gains vanish under these controls, reject the evidence-reliance claim.
10. Report every preregistered outcome and failure, with a transparent disclosure of AI assistance where required.

## Closest prior art and claim boundaries

- Geifman and El-Yaniv (NeurIPS 2017), *Selective Classification for Deep Neural Networks*: risk/coverage and abstention are established; neither concept can be claimed as new. https://papers.nips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html
- Maasch et al. (ICML 2025), *Compositional Causal Reasoning Evaluation in Language Models*: causal reasoning evaluation is established; a generic causal-evaluation claim is not novel. https://www.microsoft.com/en-us/research/publication/compositional-causal-reasoning-evaluation-in-language-models/
- Han, Lee and Do (arXiv February 2026), *RFEval*: counterfactual reasoning interventions and faithfulness audits already exist. Distinguish evidence-grounded physical interventions from output-level interventions and test whether the distinction yields a genuine methodological contribution. https://arxiv.org/abs/2602.17053
- Cieślak and Czyżewski (arXiv October 2026), *The Price of Choice in Selective Prediction*: predeclared menus, risk/coverage contracts and selection auditing are active prior art. Check overlapping inference guarantees before asserting originality. https://arxiv.org/abs/2610.29067

These are targeted sources, **not an exhaustive literature review**. Potential contribution remains an independently reproducible, physically adjudicated, evidence-intervention evaluation with explicitly matched abstention accounting, if experiments support it. No novelty or empirical performance claim is currently justified.

## Cost and execution gate

No model inference, simulation, training, or laptop execution is authorized by this document. Verify GitHub Actions plan, runner eligibility, available free minutes, spending controls and billing requirements in the actual account before starting workloads. If these cannot be verified, leave cloud execution pending. Never create paid resources or require a card.

## Release gate

A public manuscript may present methods and negative findings, but must not claim model superiority, causal faithfulness, calibrated uncertainty or novelty without appropriate independent evidence and completed prior-art comparison. November 22 is an internal target, not a reason to relax these gates.
