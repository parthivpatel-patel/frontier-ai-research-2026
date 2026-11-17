# Protocol 142 — CI coverage gap and execution gate (2026-11-17)

## Verified repository evidence
The public `.github/workflows/toy-falsification.yml` push filter covers `src/**`, `tests/**`, `data/external/**`, and its own YAML file, but **not** `research/fixtures/**`. Its test commands collect and execute only `tests`. Thus the successful November 10, 2026 workflow run at commit `c46167a165f082b732a0fdcb1cc778c264e9f1c8` does not certify Protocols 132–141, regardless of the green status. This is a CI coverage issue, not evidence that any test fails.

## Reproducible correction (not yet enabled)
After verifying GitHub-hosted Actions billing and the account's free allowance, amend the workflow push path filter to include `research/fixtures/**`, and add explicit standard-library unittest discovery, e.g.:

```bash
python3 -m unittest discover -s research/fixtures -p 'test_protocol_140_*.py' -v
python3 -m unittest discover -s research/fixtures -p 'test_protocol_141_*.py' -v
```

Run earlier protocols in separate named jobs, with deterministic dependency checks, before claiming suite-wide success. Publish run URL, head SHA, collected test count, exit status and exact command. Never use a prior green run as evidence for new files.

## Independent audit observation
Protocol 141's `independent_enumeration` computes all eight `(Y,V1,V2)` states and uses `Fraction`. This independently enumerates probability mass but shares the same synthetic conditional model and loss definition as Protocol 140. Agreement is a useful implementation consistency check, not independent validation of the model's scientific assumptions. To falsify those assumptions, separately test unequal verifier marginals, conditional dependence outside the selected family, prevalence shift, and source-level calibration.

## Publication and compute gate
Do not claim empirical improvements or a novel theorem from these synthetic fixtures. Do not launch GitHub Actions or other cloud jobs until free quota, billing/card requirements and account-specific eligibility are verified; no local compute or model downloads. The November 22 date remains a conditional internal checkpoint. Prior-art audit and held-out NLP/mathematics/physics experiments remain pending.
