# Session 007 — Verified CI and constructed physics sanity checks

**Run:** https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/41370711290

- Triggering commit: `17d7253a0a720ab5fd6ee435010d01141d3aa9ee`.
- GitHub Actions public-repository standard `ubuntu-latest` runner.
- Completed **successfully** at 2026-11-02 01:06:53 UTC.
- One job `deterministic-toy-checks`, ID `125040383252`.
- Job logs independently inspected through GitHub: **54 tests passed**, `Ran 54 tests in 0.019s`, `OK`.
- Synthetic sanity checks, oracle stress and two-family fixture commands all completed successfully.
- Two-family fixture output in the job logs:
  - `latent_error_rate: "3/5"`
  - `supplied_lower_rate: "1/5"`
  - `supplied_upper_rate: "2/5"`
  - `latent_outside_supplied_envelope: true`
- The ten cases and their thresholds were deliberately constructed to produce this discrepancy. It is **not an empirical LLM result, novel algorithm, naturally sampled error rate, or population-level guarantee**.
- No user-laptop computation, GPU, model inference, paid API, or large download was used.
- A non-failing `actions/checkout@v4` Node 20 deprecation warning appeared; it did not affect test success. Consider upgrading to a supported checkout release in a future maintenance change.

**Scientific interpretation:** The CI validates that the implemented deterministic arithmetic and control assertions run. It does not validate the latent reference semantics of unconstrained natural language, compare learned NLP systems, or establish a novel contribution.

**Next gate:** Audit equivalent execution-grounded and ambiguity-aware benchmarks, then obtain fair learned-model baselines and independent semantic adjudication within the $0 policy. If unavailable, do not present this fixture as frontier-ML evidence.
