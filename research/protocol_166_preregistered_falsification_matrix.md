# Protocol 166 — Pre-registered falsification matrix and zero-cost execution gate (2026-11-09)

**Status:** prospective experimental specification only. No cloud job, model inference, statistical test, or benchmark evaluation was run. This protocol is not a novelty claim.

## Research question and primary estimand

Does a *predeclared physical-constraint verifier* improve **correct-and-answered rate at the same answer coverage** over established selective-verification baselines on held-out physics source problems, with NLP paraphrases kept inside their source clusters?

For each source problem i, let A_mi be 1 if method m answers and C_mi be 1 if that answer is correct. Define U_mi=A_mi C_mi. For source cluster g containing paraphrases i, define D_g = mean_i(U_constraint,i - U_baseline,i). The primary descriptive effect is mean_g D_g. Report separately the case-weighted and equal-physics-family means. No significance claim without a predeclared cluster-valid uncertainty procedure and adequate independent clusters.

**Coverage matching:** choose thresholds on a disjoint calibration split, freeze them, then report achieved test coverage for every method. If test coverages differ, do not assert matched-coverage superiority; provide risk-coverage curves and clearly mark interpolation. Never tune thresholds on test labels.

## Baselines and ablations

1. Answer-only verifier (no access to intermediate reasoning).
2. Process/step verifier where legally and technically reproducible.
3. Confidence-based selective answering.
4. Random abstention at calibrated coverage, with fixed published seed.
5. Constraint verifier with units only.
6. Constraint verifier with units plus conservation-law checks.
7. Constraint verifier with units, conservation and domain/boundary applicability checks.

All methods must receive the same candidate answers, source problems, evaluation labels and calibration/test partitions. Disclose any extra supervision, prompt budget, inference cost, and access to reference solutions.

## Explicit falsifiers

- **F1:** cluster-weighted primary effect <= 0 against the strongest eligible baseline.
- **F2:** any apparent improvement vanishes under equal-family weighting or leave-one-family-out sensitivity.
- **F3:** false rejections of correct but unconventional formulations erase net benefit.
- **F4:** gains are explained by answer length, confidence, problem difficulty, leakage, or paraphrase duplication.
- **F5:** ablations show physical constraints contribute no improvement beyond generic abstention.
- **F6:** a closest-prior-art full-method comparison shows the allegedly new algorithm is already described.
- **F7:** reproducibility fails with fixed manifests, frozen splits and independent reruns.

F1–F7 are predeclared failure modes, not observed results. Negative results must be retained and reported.

## Benchmark and annotation safeguards

Split by original problem identity *before* creating paraphrases. Require physics-family labels and documented adjudication rules. For dimensional checks, record units and conventions; for conservation checks, record system boundary and assumptions; for domain checks, record approximations and validity range. Add deliberately adversarial cases: dimensionally correct but physically impossible; valid non-SI unit systems; legitimate external forces; and valid boundary exceptions. Report disagreement between annotators or an independently auditable deterministic ground truth.

## Prior-art comparison gate

Read the full methods and appendices of PhysReason (ACL 2025, https://aclanthology.org/2025.acl-long.811/), UGPhysics (ICML 2025, https://proceedings.mlr.press/v267/xu25ai.html), PhysicsEval (https://arxiv.org/abs/2508.00079), and process reward verification (https://arxiv.org/abs/2305.20050). Record exact algorithmic overlap, dataset licensing, baseline definitions, and differences in supervision. **Do not claim priority or novelty from abstract-level review.** If the specific constraint-checking contribution overlaps, pivot to independently reproducible replication or a negative-results paper.

## Execution authorization gate

No local computation. No cloud workflow is authorized by this document. Before triggering any job, verify from the connected account: free Actions entitlement, remaining usable quota, billing/card state, applicable workflow billing rules, runner availability, and hard cost-prevention controls. If any required detail is unavailable, stop before dispatching. A public repository or advertised free tier does not prove account-level eligibility. Record runner image, package hashes, command, start/end timestamps, job URL, artifact hashes, and billed usage when execution becomes permissible.

## Publication integrity gate

Nov 22, 2026 is a planning target only. Manuscript must distinguish prior work, hypotheses, protocol design, actual executed tests, observed outcomes and limitations. Disclose AI assistance according to venue rules. Do not present synthetic examples as empirical findings.
