# Protocol 175: Process verification, formal premises, and risk-control collision audit

Date: 2026-11-10
Status: primary-literature comparison and prospective theory only. No experiments executed; no novelty established.

## Three additional adjacent research programs

1. Lightman et al., *Let's Verify Step by Step* (2023; ICLR 2024), https://arxiv.org/abs/2305.20050 . Process-supervised reward models evaluate intermediate mathematical reasoning, with PRM800K human feedback labels. **Collision:** step-wise grading, process supervision, and preferring intermediate feedback over final-answer checking are not new. This project must not claim to invent process verification or to reproduce its trained-model results.
2. Yang et al., *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models* (NeurIPS 2023), https://proceedings.neurips.cc/paper_files/paper/2023/hash/4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_Benchmarks.html . Premise retrieval, provenance of accessible mathematical premises, and generalization to novel premises are established. **Collision:** linking formal steps to premises is not by itself new. Physical text-span scope and counterfactual perturbation would need a genuinely different validated mechanism, not merely a relabeling of premise retrieval.
3. Angelopoulos et al., *Conformal Risk Control* (ICLR 2024), https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html . Risk control for monotone losses has established statistical machinery. **Collision:** calibration and selective risk control cannot be claimed as invented here. Existing threshold-selection code is not automatically a conformal guarantee.

## Formal decision boundary

For source problem g, paraphrase j, frozen answer a, extracted physical constraint c with source span s and scope q, define a verifier decision V(g,j,a,c,s,q) in {accept,reject,abstain}. A span intervention T changes only one preregistered constraint-bearing span, with all other text and candidate reasoning frozen. The intended diagnostic contrast is D = V(original) versus V(T(original)); its expected direction must be manually labeled BEFORE inference. Interventions that change the problem's correct solution cannot be evaluated against unchanged ground truth without fresh adjudication.

The primary outcome is source-weighted correct-answer yield at a calibration-frozen acceptance threshold, with source-level paired contrasts and an independently reported false-rejection rate. Avoid selecting the best result from multiple families, prompts, and thresholds post hoc.

## Statistical guarantee boundary

Paraphrases within a source problem are dependent. A conformal or other finite-sample guarantee requires the assumptions of its actual procedure (e.g., exchangeability of independent calibration/test *source clusters*, monotonicity of a specified loss, and a correctly implemented calibration rule). Equal-source weighting alone supplies no finite-sample coverage or risk guarantee. Distribution shift across physics families, nonexchangeable interventions, small cluster counts, and adaptive benchmark selection may invalidate a nominal guarantee. Report descriptive intervals without guaranteed coverage unless a theorem and assumptions are established for this exact design.

## Falsification and required comparisons

- Matched-budget answer-only, dimensional, process-judge, and provenance-blind baselines; report any unavailable baseline as unavailable.
- Source-span and constraint shuffling controls, plus placebo edits to nonconstraint text.
- A change in verifier decision under a true constraint intervention must be evaluated jointly with its effect on physical validity; indiscriminate sensitivity to edits is not evidence of understanding.
- Held-out source problems and held-out physics families; group paraphrases with their parent source before splitting.
- Explicit failure if matched-coverage correct yield does not improve over the strongest feasible baseline, the effect disappears after clustering, or span-shuffled controls perform similarly.
- Explicit negative or inconclusive outcome if adjudication, independence, or sample-size requirements fail.

## Execution and authorship gates

No new compute authorized here. Before launching GitHub Actions or any provider, verify actual account-specific remaining free minutes, storage, billing/payment settings, runner eligibility, and bounded workflow permissions; public-repository free-runner policies alone do not verify the account. Never use laptop compute or require a payment card. Record SHA, exact test counts, immutable manifests, primary-source citations, limitations, and any required AI-assistance disclosure. The November 22 date is a target, not evidence of readiness.

## Still missing

2026-specific prior art, systematic citation chaining, exact matched baselines, independent physics/NLP labels, cloud account quota verification, and genuine held-out experimental results. This audit is a collision warning, not a novelty proof.
