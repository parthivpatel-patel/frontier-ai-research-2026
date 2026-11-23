# Hosted independent-oracle CI evidence — 2026-11-23

## Verified run

- Workflow run: https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/45234066422
- Tested commit: `ec9302ae33bc0c48c47ec688413a277d7bdff5f9`
- GitHub-hosted job: `exact-small-frame`, job ID `137900973530`
- GitHub conclusion: `success`
- Pytest version: `8.3.5` installed in job
- Observed log result: **71 passed in 0.28s**.
- Workflow explicitly includes `research/test_source_deletion_independent.py` and `research/test_source_deletion_metamorphic.py` in the pytest invocation.

## Interpretation and limitations

This confirms execution of the expanded exact-small-frame test suite, including the independently structured source-deletion oracle and metamorphic tests, at the specified revision. It is evidence of software checks, not of novelty, statistically calibrated coverage, model reliability, or held-out cross-domain generalization. The later evaluation-leakage audit commit was not the tested revision. The next evidence gate is independently adjudicated held-out truth with documented source provenance and falsification criteria. No model inference, paid compute, or laptop workload was required for this record.
