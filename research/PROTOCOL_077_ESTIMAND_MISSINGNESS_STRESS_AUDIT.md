# Protocol 077 — Estimand, sampling, and missing-label stress audit

Date: 2026-11-14. Status: preregistered design note; no experimental execution, novelty claim, or empirical findings.

## A distinction the previous protocol must not obscure

Let the frozen finite population have N claims. A policy makes a deterministic release decision R_i in {0,1} on the frozen frame; K=sum_i R_i is known without acquiring truth labels. For released claim i, let Y_i=1 if a *resolved* adjudication establishes falsity and 0 if it establishes truth. The target false-release fraction is theta=(sum_i R_i Y_i)/K, provided K>0 and all Y_i are well defined. This is a finite-frame estimand, not an automatically valid population-generalization claim.

Under probability sampling with known first-order inclusion probabilities pi_i>0, the Horvitz–Thompson numerator estimate is sum_{i sampled} R_i Y_i/pi_i; dividing by fixed K is design unbiased **only if the sampled labels are valid and complete for the target**. If labels are missing not at random, known sampling probabilities alone cannot restore identification.

## Missingness must be separated from sampling

Record three separate fields: (1) probability-sampling selection S_i, (2) adjudication attempted A_i, and (3) adjudication resolved D_i. A sampled unresolved claim is not an observed true claim. Conditioning on D_i=1 can induce selection bias. For each released claim define unresolved indicator U_i=1-D_i. With a fully observed census of resolved labels and known K, the deterministic logical bounds are [F_resolved/K,(F_resolved+U_released)/K]. With sampled labels, these are NOT directly available: sampled counts are estimators and require design-based uncertainty and partial-identification treatment. Never clip an HT estimate into [0,1] and then call it unbiased.

## Design-sensitive uncertainty

For the fixed released-frame total T=sum_i R_i Y_i, an HT estimator with joint inclusion pi_ij has design variance sum_{i,j}(pi_ij-pi_i*pi_j) z_i*z_j/(pi_i*pi_j), z_i=R_i Y_i. A plug-in unbiased variance estimator requires observable pairs with pi_ij>0 whenever their covariance contribution is nonzero. In fixed-size designs with impossible pairs, a conventional unbiased pairwise estimator need not exist. If family sampling is the unit, calculate family totals and use family-level inclusion probabilities; never count correlated claims as independent sample units.

## Falsification matrix (before observing outcomes)

1. Census with no unresolved labels: HT total equals observed total.
2. Census with unresolved labels: report logical interval, not a point estimate.
3. Fixed K=0: false-release fraction undefined; report zero coverage separately.
4. Sampled missingness depends on Y: demonstrate that naive resolved-only estimates are not generally identified.
5. pi_i=0 for any released target unit: reject unbiased point-identification claim.
6. pi_ij=0 for required pairs: refuse a generic unbiased variance-estimator claim.
7. Duplicate all claims within a provenance family: preserve independent-family count.
8. Hold the release decisions and adjudication budget fixed across competing policies; rerun on a separate held-out frame.
9. Stratify by NLP / mathematics / physics and report worst-domain coverage and risk without pooling incompatible adjudication standards.
10. If the proposed method does not outperform properly corrected active testing under matched cost, record a negative result rather than redefining the target.

## Prior-art collision ledger and novelty gate

Selective classification (Geifman & El-Yaniv 2017): https://papers.nips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html — abstention/risk-coverage already studied.

Active Testing (Kossen et al., ICML 2021): https://proceedings.mlr.press/v139/kossen21a.html — adaptive label acquisition and corrected evaluation already studied.

Conformal Risk Control (Angelopoulos et al., ICLR 2024): https://research.google/pubs/conformal-risk-control/ — expected-loss calibration already studied.

Sampling-theory HT estimation, joint inclusion, cluster sampling, and missing-data identification are established mathematics. The conjunction of these components is not itself a novel theorem. A publication-worthy claim requires a documented baseline gap and held-out discriminating evidence; otherwise position the work as a reproducible protocol or negative-result note.

## Cloud-only $0 gate

Candidate: standard GitHub-hosted Linux runners on the **public** repository; GitHub documents standard public-repository runner usage as free, unlike larger runners. Official billing reference: https://docs.github.com/en/billing/concepts/product-billing/github-actions . Confirm repository visibility, Actions policy, standard-runner availability, account restrictions, and any storage/artifact charges before triggering jobs. Use no larger runners, paid services, persistent artifacts, external API calls, local training or local model inference. A theoretical free category is not confirmation of account-specific eligibility. No job is authorized by this document.

## Decision gate

November 22, 2026 is a conditional internal target. A paper claiming model improvements requires genuine held-out data, verified cloud logs, a documented adjudication process, and source-level novelty review. AI assistance and limitations must be disclosed as applicable.
