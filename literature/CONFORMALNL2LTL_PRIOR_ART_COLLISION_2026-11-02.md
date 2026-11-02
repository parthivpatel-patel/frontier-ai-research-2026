# Prior-art collision and reusable-data candidate — 2026-11-02

## ConformalNL2LTL is direct prior art, not a new baseline invented here

Wang, Sundarsingh, Deshmukh and Kantaros, *ConformalNL2LTL: Translating Natural Language Instructions into Temporal Logic Formulas with Conformal Correctness Guarantees*, arXiv:2504.21022 (first posted 2025-04-22), https://arxiv.org/abs/2504.21022 . The authors already combine LLM-driven NL-to-LTL translation, conformal uncertainty quantification, selective escalation, and claimed user-specified success-rate guarantees. Therefore **conformal risk control, abstention, or human escalation for NL-to-LTL cannot be claimed as novel** in our paper.

The upstream implementation is public at https://github.com/kantaroslab/ConformalNL2LTL . Its GitHub repository metadata reports an Apache-2.0 license, and the root LICENSE text contains Apache License 2.0. Its `Dataset/` directory contains `final_calib.json` (106,725 bytes) with `nlTask` and `ltlequ` fields and `max_scores.json` (73,129 bytes) with `nlTask` and `score` fields. Direct inspection of the initial records supports **calibration-data availability**, not proof of independent human semantic adjudication or of original model predictions. Code and data rights must still be checked for upstream third-party content and attribution; no records are copied here.

**Falsification implication:** A proposed physics-assumption uncertainty diagnostic must improve on ConformalNL2LTL and SCP-NL2TL at matched coverage and controlled human-help/inference budgets. If a baseline achieves equal or lower unsafe acceptance, we cannot claim incremental benefit. If source-family-level human meaning is unavailable, do not claim empirical reliability guarantees.

## Additional overlap

- Wang et al., *SCP-NL2TL* (2026-08-05), https://arxiv.org/abs/2608.05439 : selective conformal semantic verification, back-translation, dispersion, OOD screening.
- Zhan et al., *SENTINEL* (2025-10-14), https://arxiv.org/abs/2510.12985 : multi-level semantic/plan/physical-trajectory safety checking.
- English et al., *VLTL-Bench* (2025-07-01), https://arxiv.org/abs/2507.00877 : grounding, trace verification, and end-to-end NL-to-LTL benchmark.
- Aruta et al., *Translating Natural Language to Strategic Temporal Specifications via LLMs* (2026-06-29), https://arxiv.org/abs/2606.30441 : expert-validated strategic temporal logic data and human-judge reliability limitations. Its ATL/ATL* target is not interchangeable with LTL; any reuse requires semantic and license review.
- *ChaosBench-Logic v2* (2026, revised 2026-10-14), https://arxiv.org/abs/2605.24305 : reasoning over dynamical systems and robustness; another reason not to claim generic physical-dynamics benchmark novelty.

## Decision

The potential contribution, if any, is **incremental deployable risk reduction from independently specified uncertainty over physical dynamics**, measured on authentic blinded model predictions with human-adjudicated semantics and independent source families. Existing mathematical may/must verification, conformal prediction, selective risk control, and grounding are baseline components, not inventions.

The current project does not yet have the human-verified source families, proven model-output provenance, or comparative results needed for a novel empirical paper. A rigorous negative/methodological paper remains an acceptable outcome. All proposed computation stays on the public GitHub standard free hosted runner, no laptop or paid inference.
