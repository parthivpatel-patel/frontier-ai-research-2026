# Protocol 171: CI environment reproducibility gate

Date: 2026-11-09
Status: diagnostic specification; no execution claimed.

## Observed failure
The preceding GitHub Actions run 42709222348 reported 661 discovered tests, two exact-floating-point assertion failures, and four import errors involving `pytest`. Commits 6903d35 and 8f02908 changed the two assertions to tolerance comparisons. A successful rerun has not been verified. The workflow's precise file path and dependency installation steps have not yet been independently inspected.

## Required remediation before experiments
1. Identify the actual workflow YAML and record its commit SHA, Python version, runner image, command, and dependency installation.
2. Install `pytest` explicitly in the CI job that discovers pytest-importing modules, or remove those imports through a reviewed conversion to standard-library `unittest`. Do not silently skip tests.
3. Pin the test runner dependency in a versioned manifest with a documented upgrade procedure. Check that all third-party imports in test modules are declared.
4. Run the complete test suite on a verified no-cost GitHub-hosted runner only after account-specific billing/quota eligibility is confirmed. Capture run ID, commit SHA, full test counts, failures/errors/skips, and Python version.
5. Keep CI test correctness separate from model-performance evidence. No model inference or training is authorized by this protocol.

## Failure criteria
A green job with skipped or undiscovered test modules is insufficient. A suite is verified only when the expected test inventory is reconciled with actual discovery and all required tests execute successfully. A dependency installation failure, quota/billing uncertainty, or missing workflow provenance blocks claims of verified reproducibility.

## Scientific status
This protocol does not demonstrate physics reasoning improvement, statistical significance, or novelty. Independent source-clustered, held-out physics/NLP experiments and direct comparisons with prior art remain necessary.
