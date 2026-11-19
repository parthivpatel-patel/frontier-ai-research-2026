# Closest-prior-art correction: risk control under shift (2026-11-19)

**Status:** primary venue records checked; conceptual novelty audit, not experimental evidence or a comprehensive systematic review.

## Verified overlap

1. Angelopoulos, Bates, Fisch, Lei and Schuster, *Conformal Risk Control*, ICLR 2024, https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html . Extends conformal calibration to monotone losses and explicitly discusses distribution shift, multiple/adversarial risk and NLP examples. Therefore **risk calibration, shift awareness and NLP applicability are not new**.
2. Xu, Karampatziakis and Mineiro, *Active, anytime-valid risk controlling prediction sets*, NeurIPS 2024, https://papers.nips.cc/paper_files/paper/2024/hash/6eb05d8bc6bd7bb6868c64b5802125bd-Abstract-Conference.html . Addresses adaptive labels, anytime-valid risk, label budgets and covariate-conditioned risk estimation. Therefore **budgeted label auditing and sequential monitoring are not new**.
3. Almeida et al., *High Probability Risk Control Under Covariate Shift*, COPA/PMLR 266 (2025), https://proceedings.mlr.press/v266/almeida25a.html . Uses importance-weighted calibration loss to extend learn-then-test risk control under covariate shift. Therefore **weighted risk calibration under covariate shift is not new**.

These primary venue abstracts establish significant overlap, but do not establish equivalence of selective accepted-answer risk and prediction-set risk. Inspect complete methods and assumptions before formal comparison.

## Consequences for this project

- Do **not** claim novelty for abstention, risk-coverage curves, shift-aware calibration, paired error arithmetic, domain stratification, active labeling, or generic conformal risk control.
- A defensible incremental contribution might be an **empirically validated, pre-registered cross-domain verifier benchmark** with identical candidate answers, frozen thresholds, independent adjudication, explicit costs of accepted and rejected answers, source-family-held-out evaluation, and a transparent failure analysis. It must be compared to selective prediction, conformal risk control, and importance-weighted shift baselines, and may still not be novel.
- Physics is a **task domain** here, not evidence of a new physical theory or physics-based mechanism. Avoid claiming an AI–physics synthesis absent an explicit falsifiable physical model.

## Hard falsification / release gates

1. Source-held-out accepted-error improvement vanishes under domain-balanced weights or within-family estimates.
2. Gains vanish at matched coverage and matched total verifier compute, including abstentions.
3. Target labels cannot be independently adjudicated, or benchmark contamination cannot be bounded.
4. A conventional confidence threshold, CRC or importance-weighted baseline matches the proposed method.
5. Target distribution violates assumed conditional-label invariance or lacks source support: no shift guarantee.
6. No genuinely novel method or empirical result survives closest-paper comparison: publish a **methods/preregistration report**, not a discovery paper.

## Cloud execution boundary

GitHub's current billing documentation (https://docs.github.com/en/billing/concepts/product-billing/github-actions) states that **standard GitHub-hosted runners in public repositories are free**, while larger runners are billable. This is not evidence of unlimited resources, permission for continuous compute-intensive workloads, or account-specific eligibility. Use only bounded, standard-runner, CPU-only test jobs, without paid storage, external paid APIs, large downloads or local compute. Verify the precise workflow runner and repository visibility before launching. No card enrollment is required for the public-standard-runner route according to the cited billing description; account-specific controls remain to be checked.

**Research integrity:** This audit is AI-assisted. No experiment, new theorem, performance gain, or publication-ready novelty is asserted. November 22 is a conditional review date.
