# Protocol 156 — Conformal-risk collision and claim boundary (2026-11-18)

## Evidence status
Bibliographic and methodological comparison, not a new theorem or experiment. Primary publisher/author sources were checked on 2026-11-18. No new model inference, cloud run, or laptop computation was performed.

## Closest primary literature
1. Angelopoulos, Bates, Fisch, Lei and Schuster, *Conformal Risk Control*, ICLR 2024: https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html . Provides finite-sample expected-risk control for monotone bounded losses; includes multiple/adversarial risk control, distribution shift, and NLP examples. **Collision:** generic bounded-loss risk control and its NLP application are not novel here.
2. Angelopoulos, *Conformal Risk Control for Non-Monotonic Losses* (2026): https://arxiv.org/abs/2602.20151 . Studies generic algorithms, non-monotone losses and stability-dependent guarantees. **Collision:** abstention-cost objectives may be non-monotone; do not imply prior CRC is inapplicable without specifying the loss and algorithm.
3. Xu, Karampatziakis and Mineiro, *Active, anytime-valid risk controlling prediction sets* (2024): https://arxiv.org/abs/2406.10490 . Handles adaptive label querying and anytime-valid risk control. **Collision:** adaptive-label-budget guarantees cannot be presented as a new general direction.
4. Hultberg, Zachariah and Ribeiro, *Anytime-Valid Conformal Risk Control* (2026): https://arxiv.org/abs/2602.04364 . Addresses high-probability guarantees over cumulatively growing calibration data. **Collision:** do not claim novelty from repeated looks alone.
5. *Conformal risk control for non-monotonic losses* (2026 journal treatment): https://doi.org/10.1098/rsta.2025.0068 . Explicitly discusses algorithmic stability and non-monotonic risk control.

## Exact guarantee distinction requiring care
Protocol 155 uses a high-probability, fixed-family, source-i.i.d. Hoeffding lower bound on **paired improvement** E[L_baseline - L_policy]. The original CRC target is a marginal **expected loss** guarantee for a data-dependent calibrated prediction set, under its own monotonicity and exchangeability assumptions. These guarantees are not identical. Neither is inherently new; a contribution requires showing a practical verifier-specific advantage under appropriate baseline and assumptions.

## Physics and domain definition
The physics component must be a **physics reasoning task domain** with independently labeled physical-law or numerical answers, not a claim to discover new physical laws. Source provenance should distinguish textbook/problem-family origin, paraphrases and shared templates. A pooled NLP+math+physics result does not establish improvement in each domain.

## Falsifiable experimental gate
Freeze candidate policies, loss including abstention and compute cost, source-level sampling, labels, and independent source families before evaluating. Compare to (a) fixed threshold/selective-classification baseline, (b) risk-calibrated monotone CRC baseline where assumptions apply, and (c) equal-cost uncalibrated verifier. Report paired source-level confidence bounds with all selection multiplicity counted. Treat policy family modifications after test-label inspection as exploratory. Require nonvacuous, positive improvement bounds and per-domain confidence statements for per-domain claims. If all gains vanish under independent source aggregation or matched budgets, reject the proposed improvement claim.

## Publication decision
As of this audit, mathematical novelty is **not established**. The plausible contribution is a reproducible, source-provenance-aware, cross-domain evaluation of verifier abstention under matched budgets. Publication by Nov 22 is conditional on real held-out data, actual executed tests, and a credible comparison with the above prior art. Do not claim model performance, calibration, or generality from deterministic synthetic fixtures.
