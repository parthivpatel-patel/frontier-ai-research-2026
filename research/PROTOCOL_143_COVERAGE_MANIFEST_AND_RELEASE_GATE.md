# Protocol 143 — Coverage manifest and no-execution release gate (2026-11-17)

## Evidence reviewed
Inspected `.github/workflows/toy-falsification.yml`, `research/fixtures/test_protocol_140_coupled_uncertainty.py`, and `research/fixtures/test_protocol_141_independent_joint_enumeration.py` from the public default branch. The workflow is triggered by changes under `src/**`, `tests/**`, `data/external/**`, or its own workflow file; it omits `research/fixtures/**`. Its only pytest collection/execution commands target `tests`. Thus neither fixture is certified by the existing workflow. A green status for an older SHA is not transferable to these files.

## Important additional audit finding
Protocol 141 imports `risk` from Protocol 140 using `from test_protocol_140_coupled_uncertainty import risk`. This succeeds when the fixtures directory is placed on Python's import path by test discovery, but **may fail** when an individual test module is imported by a differently configured runner. The execution contract must specify the test root and import mechanism. Avoid claiming runner portability without testing both supported invocations.

## Proposed CI patch (NOT applied; no cloud compute authorized)
After account-specific GitHub Actions zero-charge eligibility and limits are verified, add `research/fixtures/**` to the push path filter and explicitly collect and run fixture tests, e.g.:

```sh
python3 -m unittest discover -s research/fixtures -p 'test_protocol_*.py' -v
```

Run discovery and execution with a fixed Python version and recorded runner image; collect separately from `tests/`. If dependencies in earlier fixtures require external packages, pin and audit those packages first. Ensure the workflow does not silently skip import errors or tests. Prefer explicit separate commands per fixture family for failure attribution.

## Required evidence manifest
For each job archive: triggering event; immutable commit SHA; workflow file SHA; Python version; dependency lock or standard-library-only statement; collection command and count; execution command and count; skipped/error/failure counts; exit code; run URL; execution date; and machine-readable test report. A green job without evidence that fixtures were collected is **not** a pass for these protocols.

## Falsification gates
1. Mutation check: deliberately broken synthetic fixture on a separate disposable branch must cause a failing job; never alter published main merely to demonstrate this.
2. Import-path check: discovery from repository root must collect Protocol 140 and 141, and any test import error must fail the job.
3. Probability-model check: the eight-state enumeration agrees with its own analytical conditional model, **not** with empirical verifier calibration. Independently test unequal marginals, label-dependent dependence, prevalence shift, and nonrectangular feasible sets before external claims.
4. Release check: no publication claims of verified robustness without held-out, source-disjoint NLP, mathematics, and physics evidence, budget-matched baselines, uncertainty intervals, and completed closest-prior-art review.

## Execution and disclosure
No workflow was modified or launched in this protocol. No laptop compute, paid service, model download, or new experimental result. GitHub Actions pricing/free allowance and account-specific eligibility must be checked before any cloud run. November 22 is a conditional checkpoint, not a publication promise.
