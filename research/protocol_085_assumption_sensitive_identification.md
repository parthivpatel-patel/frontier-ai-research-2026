# Protocol 085 — Assumption-sensitive verification: identification and locked evaluation plan

Status: research design only. No model results, independent adjudication, or novel empirical effects are claimed.
Date: 2026-11-05

## Scientific question
Does a verifier that explicitly checks physical assumptions reduce unsafe acceptance of scientific claims relative to a verifier that checks equations alone, when both are compared at equal claim coverage and equal evidence/compute budget?

The distinction is crucial: an equation can be algebraically valid while its applicability is unsupported. A missing premise is not proof that a physical conclusion is false. The output taxonomy is **supported**, **refuted**, **underdetermined**, or **out of model scope**. Abstention is separately recorded as a decision action, not treated as a truth label.

## Experimental unit and pairing
Each unit is a claim with a specified physical system, units, premises, question, and reference derivation. Construct a paired counterfactual by changing exactly one premise while keeping the claim text and numerical parameters fixed where physically coherent. Record whether the perturbation changes (a) applicability, (b) mathematical truth conditional on assumptions, or (c) both. Never assume that an inapplicable formula entails a false claim.

Group by source problem and underlying equation family. Split whole groups across development and evaluation; prevent paraphrases, generated siblings, and near-duplicates from crossing splits. Keep original source, license, transformation recipe, and adjudication provenance. Lock evaluation records and hash manifests before model selection.

## Primary estimand
Let A_v(i,t) indicate that verifier v accepts claim i at threshold t, and U(i) indicate an independently adjudicated unsafe claim (refuted, or asserted as supported despite an unverified necessary premise under the prespecified policy). At matched acceptance coverage c, compare:
R_v(c) = sum_i w_i A_v(i,t_v(c)) U(i) / sum_i w_i A_v(i,t_v(c)).
Thresholds are tuned on development data only; ties require a prespecified deterministic policy. Report risk–coverage curves and the difference R_certificate(c)-R_baseline(c) with paired, source-cluster bootstrap intervals. Separate refuted claims from underdetermined premises in every report; do not conflate them.

The estimand is not identified on a fully observed population if ground truth is missing nonrandomly. Report worst-case bounds over unresolved cases and a sensitivity curve varying unresolved unsafe prevalence. Never use constructed hidden labels as observed truth.

## Minimum comparison matrix
1. Equation-only deterministic oracle.
2. Assumption-aware deterministic oracle (mechanism sanity check, not a model).
3. Direct language-model verifier if and only if genuinely free cloud inference is available.
4. Evidence-retrieval verifier under the same evidence budget, if feasible.
5. Proposed certificate method with identical input and adjudication policy.

For stochastic baselines, prespecify model versions, prompts, seeds where supported, decoding settings, latency, token usage, and repetitions. Do not treat a deterministic oracle comparison as evidence of superiority over frontier models.

## Adversarial falsification tests
- **Premise removal:** a necessary assumption disappears; the method should not continue issuing a supported certificate without justification.
- **Unit perturbation:** incompatible units appear; the system must flag the mismatch.
- **Non-identifiability:** multiple physical states satisfy the observations but imply different answers; the verifier must not force a unique answer.
- **Equation memorization:** familiar formula is paired with an explicitly non-ideal system; accepting by pattern match counts against the method.
- **Source leakage:** evaluate unseen equation/source families and hold out paraphrase siblings.
- **Selective truth:** compare fully observed constructed controls against missing-not-at-random adjudication; risk bounds must contain the feasible true risk.

## Failure and publication rules
Reject the superiority hypothesis if matched-coverage confidence intervals fail to support a lower unsafe-acceptance risk, if benefits disappear under source-family holdout, if the method uses more evidence without a budget-matched advantage, or if independent adjudicators cannot reliably agree on the labels. Report negative results. Claims of novelty require a dated prior-art table with exact overlap and a documented difference in mechanism and evidence, not just terminology.

## Adjudication protocol
Two independent adjudicators work blind to verifier identity. Require explicit assumptions, dimensional checks, derivation, applicability decision, source URL or textbook citation, and uncertainty notes. Resolve disagreement through a separately recorded third adjudication, not silent majority rewriting. Elementary numerical fixtures are candidate controls only until this procedure is completed.

## Cloud and cost gate
No cloud job is authorized by this document. Before any run, verify the specific repository is public, GitHub Actions is enabled, the workflow uses a standard GitHub-hosted runner, account billing settings and limits preclude charges, no paid marketplace actions or larger runners are involved, and artifacts/storage remain inside verified free limits. Public-repository standard runner pricing alone does not verify account-specific safeguards. Do not run on the user's laptop.

## Immediate next implementation
Add a schema validator for claim, premise, units, applicability, adjudication status, source family, and manifest hash. Then test the four-way truth taxonomy, including counterexamples where inapplicability does not imply falsehood. Run tests only after the cloud cost gate is verified.

This protocol is independent of all other projects and is intended for reproducible, disclosure-compliant research.
