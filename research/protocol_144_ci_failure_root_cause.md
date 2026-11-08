# Protocol 144 — GitHub Actions failure root-cause audit

Date: 2026-11-08. Evidence: [workflow run 42498363883](https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/42498363883), job 128785523205, downloaded job log.

## Observed failure, not an experimental result

The runner used Ubuntu 26.04.1 and Python 3.14. The workflow executed Python standard-library unittest discovery. It reported **618 tests** and **four import errors**, not four failed scientific assertions. All four tracebacks end in `ModuleNotFoundError: No module named 'pytest'`:

- `tests/test_analytic_preflight.py`
- `tests/test_precision_reported_admitted_bootstrap.py`
- `tests/test_protocol_135_closed_form_oracle.py`
- `tests/test_protocol_140_keyed_shared_oracle.py`

The remaining workflow research steps were skipped after the test command failed. This run predates the Protocol 143 commit and therefore does not test Protocol 143.

## Root cause and constrained remediation

The standard-library discovery command imports modules that explicitly depend on `pytest`, while the job did not install that dependency. This is a test-environment/dependency mismatch, not evidence that the underlying mathematical claims are false or true.

**Preferred corrective change, subject to verified zero-cost GitHub Actions entitlement:** Pin a Python version and a reviewed pytest version, install pytest in the ephemeral hosted runner, and execute the suite with `python -m pytest -q`. Preserve fail-closed behavior; do not suppress import errors, skip the affected modules, or label a partially run suite as passing. Review repository dependency constraints before choosing exact versions. An alternative is to convert all four pytest-dependent modules to standard-library unittest, with preserved assertions and test collection.

Do not dispatch another hosted job until the account's public-repository Actions eligibility, spending controls, and available included quota have been verified. Public repository hosting alone does not prove that every workflow is cost-free for this account.

## Scientific publication gates still open

1. Run the complete regression suite and retain immutable run URL, commit SHA, runtime/dependency versions, and test counts.
2. Verify Protocol 143 against the actual production sampler, including conditional versus unconditional undefined-resample probability semantics.
3. Conduct independent repeated-sampling coverage experiments with predeclared seeds, sample sizes, and negative controls.
4. Compare against published selective prediction, conformal risk control, formal verification, NL-to-temporal-logic, and physics-grounded reasoning baselines. Distinguish known bootstrap identities from any proposed original contribution.
5. Publish only results that survive falsification checks; disclose assistance and data/model licenses as required.

No cloud workload, model inference, local laptop workload, or expenditure was initiated in preparing this audit.
