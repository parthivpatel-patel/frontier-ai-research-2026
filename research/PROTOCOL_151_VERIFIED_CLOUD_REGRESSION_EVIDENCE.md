# Protocol 151 — Verified cloud regression evidence (2026-11-17)

## Evidence

- GitHub Actions run: https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/44177021148
- Source commit: `62ecea129a03f0904eb675a9bc1576bc58d702f3`
- Job: `exact-regressions` (job ID `134370981345`)
- Run event: push; created 2026-11-17 21:10:33 UTC; completed successfully.
- Runner: GitHub-hosted Ubuntu 24.04.5, Linux x64; Python 3.12.3; runner image `ubuntu-24.04` version `20261111.370.1`.
- Recorded checkout SHA matched source commit.
- Protocol 146: **5 passed**.
- Protocol 149: **5 passed**.
- Protocol 150: **6 passed**.
- Total: **16 passed, 0 failures**. These are deterministic standard-library regression fixtures, not empirical AI model evaluations.
- Logs additionally warn that `actions/checkout@v4` targets deprecated Node.js 20 and is being forced to run under Node.js 24; this did not fail the run. Update the action in a separate controlled change.

## Interpretation and limitations

This closes the *execution-evidence gap only for fixtures 146, 149, and 150*. It does not establish correctness of assumptions, external validity, model performance, theoretical novelty, or coverage of earlier fixtures 132–145 and 147–148. CI success must not be described as a scientific replication. No held-out NLP, mathematics, or physics model evaluations were run.

## Follow-up release gates

1. Enumerate all regression fixtures and compare them with actual CI discovery; fail on omitted files, rather than treating a green subset as complete.
2. Check independence and representativeness of labelled source clusters before applying risk bounds.
3. Complete theorem-level comparisons to selective risk control, partial identification, sequential verification, and adversarial selection.
4. Require preregistered, source-disjoint, held-out cross-domain model results before empirical superiority or novelty claims.
5. Keep model inference and large downloads off the user's laptop. Any further cloud compute must be confirmed free and within eligibility limits before execution. No paid runner, service, or billing change is authorized.

Evidence obtained from the GitHub Actions run metadata, job status, and decoded job logs; counts were read from the log's three `Ran N tests ... OK` summaries.
