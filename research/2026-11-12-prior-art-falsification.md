# Prior-art and falsification checkpoint — 2026-11-12

Status: research design only. No experimental results, originality certification, or model performance claims.

## Novelty boundary

The broad claim that conformal prediction can control language-model factuality or abstention is **not novel**. Closest identified literature:

1. Mohri & Hashimoto (ICML 2024), *Language Models with Conformal Factuality Guarantees*: https://proceedings.mlr.press/v235/mohri24a.html
2. Deutschmann et al. (AAAI 2024), *Conformal Autoregressive Generation*: https://doi.org/10.1609/aaai.v38i10.29062
3. Tayebati et al. (2025), *Learning Conformal Abstention Policies*: https://arxiv.org/abs/2502.06884
4. Wang et al. (2025), *SConU*: https://arxiv.org/abs/2504.14154
5. Wang et al. (2025), *SAFER*: https://arxiv.org/abs/2510.10193
6. Oehri et al. (2025), *Trusted Uncertainty*: https://arxiv.org/abs/2509.01455

These papers create substantial overlap with confidence fusion, selective generation, risk-controlled refusal and black-box verification. Their abstracts alone are insufficient for a definitive novelty audit; full texts, references, and newer work must be examined.

## Candidate narrower question (hypothesis, not discovery)

Can a **verifier-evidence conservation ledger** for mathematical/scientific natural-language reasoning identify when apparent agreement among multiple verification channels comes from shared underlying evidence, rather than independent support? Physics inspiration is conservation/accounting of evidence and correlated measurements, **not** a claimed physical law of language models.

Represent each claim as a node and each verifier or source as a provenance-tagged observation. Estimate dependence clusters among observations and compare:
- naive independent-evidence aggregation;
- provenance-aware aggregation;
- single strongest verifier;
- calibrated selective prediction without provenance.

Primary outcome: selective risk-coverage area on held-out mathematical and scientific claims. Secondary: calibration error, abstention rate, and sensitivity to deliberately duplicated/correlated evidence.

## Falsification / stopping rules

- Reject novelty if a prior paper already establishes the same provenance-dependent selective-risk mechanism and evaluation.
- Reject utility if provenance-aware aggregation fails to improve held-out risk-coverage against the strongest calibrated baseline under paired bootstrap intervals, or if gains vanish after matching verifier budgets.
- Reject theoretical claims if any guarantee depends on independence or exchangeability that is violated by the proposed evaluation; report empirical performance separately.
- Treat evidence-source duplication and adversarial paraphrases as required stress tests; prevent shared-source train/test leakage.
- If dataset licensing, free compute availability, or benchmark provenance cannot be verified, do not run or publish the affected experiment.

## Reproducible $0 experiment protocol (not executed)

1. Create a tiny manually auditable public-domain or permissively licensed claim corpus, with provenance and deterministic mathematical truth checks.
2. Pre-register split units by original problem/source, not paraphrase; fix seeds, evaluation code, baseline definitions and budget ceilings before examining test outcomes.
3. Implement pure-Python CPU-only verifier-evidence aggregation and synthetic dependence stress tests on a **standard GitHub-hosted runner in this public repository**; no local laptop computation.
4. Use a short timeout and minimal artifacts; no external paid APIs, large model downloads, or GPU. Do not trigger cloud jobs until runner eligibility, account billing controls and current availability are checked.
5. Only add public lightweight precomputed model outputs when provenance, permissions and contamination risks are documented. Otherwise limit conclusions to synthetic or deterministic verification, not frontier-LLM performance.
6. Publish exact inputs, checksums, environment lock, scripts, negative results and disclosure of AI assistance where required.

## Infrastructure caveat

Public-repository standard GitHub-hosted Actions runners are described as free; larger runners and storage overages may be billed. Account-level billing/card state and actual runner availability are **not yet verified**, so this document authorizes no job or expense. See https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions .

## Publication gate

November 22 is a planning target, not an unconditional publication deadline. A paper must not claim original physics laws, frontier-model validation, statistical significance or empirical results without reproducible evidence.
