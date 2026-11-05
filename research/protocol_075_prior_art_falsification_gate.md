# Protocol 075 — Closest-prior-art and falsification gate (2026-11-05)

Status: literature triage, **not** a systematic review; no new empirical result. This document is independent of all other projects.

## Claim boundary

The project studies whether explicit assumptions and independently checkable physics certificates improve the safety of accepting AI-generated scientific claims at *matched acceptance coverage*. Mathematical validity of a certificate, empirical physical truth, source provenance, and statistical identification are distinct properties. No novel theorem or superiority claim is established.

## Closest prior art requiring direct comparison

1. **DeepSciVerify** (Sadeghi et al., 2026), https://arxiv.org/abs/2605.27710 — scientific claim/citation verification with selective evidence escalation; reported SCitance results. This challenges any broad novelty claim about staged evidence verification. Its claim–citation alignment task is not identical to independent physical truth adjudication.
2. **CURE / Think Through Uncertainty** (Liu and Wang, 2026), https://arxiv.org/abs/2604.12046 — atomic claim-level confidence, calibration, and abstention. This challenges novelty claims about decomposing claims or selective acceptance.
3. **Selective classification / risk–coverage** (Geifman and El-Yaniv, 2017), https://arxiv.org/abs/1705.08500 — compare error at fixed coverage; abstention alone is not a contribution.
4. **Conformal risk control** (Angelopoulos et al., 2022), https://arxiv.org/abs/2208.02814 — distributional risk guarantees under assumptions; compare guarantee assumptions and failure under distribution shift.
5. **Partial identification** (Manski, 2003, *Partial Identification of Probability Distributions*) and **missing-data mechanisms** (Little and Rubin, *Statistical Analysis with Missing Data*) — unknown physical labels require bounds or explicit identifying assumptions; paired bounds are not new.
6. **Scientific verification with formal tools**: compare against symbolic/unit checking and independently executable numerical or analytic checks. A certificate's syntax is not physical evidence.

These references are candidate closest prior art, not an exhaustive novelty audit. Check version dates, datasets, licenses, and benchmark compatibility before manuscript claims.

## Precommitted falsification criteria

- Reject a superiority claim if a baseline has equal or lower unsafe acceptance at the same acceptance coverage on source-disjoint, independently adjudicated cases.
- Report *not identified*, rather than a win, if sharp missing-truth bounds include zero for the paired unsafe-acceptance difference.
- Reject a certificate-specific benefit if improvements disappear when comparing against a baseline with the same information, adjudication budget, and evidence retrieval.
- Report leakage if test claims share source families, near-duplicates, or answer-bearing derivations with training or prompt-development data.
- Report calibration failures and subgroup heterogeneity; do not hide them in an aggregate.
- Never substitute synthetic labels, placeholder adjudicators, or LLM self-grading for independently checkable physical truth.

## Next executable design

Construct a small, license-compatible, provenance-tracked set of physics claims from public-domain or appropriately licensed sources. Each record must include the proposition, explicit physical assumptions, units, derivation or falsifying counterexample, independent adjudication evidence, source-family ID, and adjudicator provenance. Freeze source-family splits before any model evaluation. Compare (a) direct answer confidence, (b) atomic-claim uncertainty and abstention, (c) retrieval/evidence escalation, (d) symbolic/unit checking, and (e) assumption-explicit certificates, all at matched coverage and evidence budgets. Publish exact prompts, model/version IDs, seeds, refusal rates, costs, and uncertainty bounds. Do not run model inference until its provider and account-specific $0 eligibility are verified.

## Compute and integrity gate

GitHub's published billing documentation says standard GitHub-hosted runners are free for **public** repositories, but larger runners are billed and artifact/cache storage can incur charges outside allowances: https://docs.github.com/en/billing/concepts/product-billing/github-actions . GitHub Free lists included allowances, but account-specific billing settings, current quotas, runner access and spending controls have **not** been inspected. Therefore this protocol does not initiate any run or assert account-specific eligibility. Use only standard public-repository hosted runners, no artifacts/cache, short timeout, and no paid API, after confirming the account configuration. No laptop workloads.

## Publication gate

The 2026-11-22 target is internal only. A methods/preregistration manuscript is permissible if experiments are absent; an empirical improvement paper is not. Disclose AI assistance according to the selected venue's policies and accurately identify human adjudication.
