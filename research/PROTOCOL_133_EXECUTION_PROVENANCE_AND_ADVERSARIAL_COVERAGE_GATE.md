# Protocol 133 — Execution provenance and adversarial coverage gate

Date: 2026-11-16 (US Eastern). Status: source audit, not empirical result.

## Verified repository evidence
- Protocol 132 source is published at `research/fixtures/test_protocol_132_heterogeneous_sequential.py`.
- Its five `unittest` methods cover marginal feasibility, reduction to symmetric Protocol 129, fee accounting, nested deterministic policy classes, and an interior-point comparison.
- The latest GitHub Actions run returned by the repository workflow-runs endpoint was run 42747243786, completed successfully on 2026-11-10 for commit `c46167a165f082b732a0fdcb1cc778c264e9f1c8`. This **does not validate Protocol 132**, which was published later. A green historical CI badge must not be treated as current test evidence.
- No Protocol 132 execution, empirical accuracy, or research novelty is established by this audit.

## Specific coverage gap
`test_corners_dominate_interior` samples only three points along the diagonal joining the lower-lower and upper-upper dependence corners. It does not explicitly sample the off-diagonal corners, independent mixtures with different interpolation weights for the true and false conditional dependence, or a separately implemented risk oracle. The existing `minimax` routine does enumerate all four corners, but the interior test is narrower than its name suggests.

## Required independent falsification
1. For each of 144 deterministic policies, compare the worst loss at all four corners against a 3x3 grid of independent interpolation weights for each conditional dependence coordinate, including off-diagonal points.
2. Compare the risk function against a separately coded enumeration of conditional truth and verifier outcomes; avoid importing the implementation under test as the oracle.
3. Check all inputs satisfy probability constraints and reject out-of-range prior, marginal accuracies, fees, and negative losses.
4. Report randomized-policy minimax as a separate experiment; deterministic 144-policy enumeration cannot establish randomized optimality.
5. Verify current commit SHA and workflow execution logs before reporting any tests as passing. Record exact Python version, command, elapsed time, and failure traceback.
6. Use only a standard GitHub-hosted runner on the public repository if account billing and workflow permissions are confirmed no-charge; do not enable paid runners or external compute. Never run compute on the user's laptop.

## Scientific novelty and publication gate
Blackwell comparisons, Fréchet coupling bounds, robust Bayes, sequential information acquisition, and selective prediction are established prior art. Do not claim them as new. A defensible contribution requires source-verified closest-paper comparison and a held-out, source-disjoint NLP/mathematics/physics evaluation against calibration, selective prediction, fixed verification, and cost-aware acquisition baselines. Report negative results and AI assistance transparently.

This is a documentation checkpoint only: no new experiment was executed and no spending occurred.
