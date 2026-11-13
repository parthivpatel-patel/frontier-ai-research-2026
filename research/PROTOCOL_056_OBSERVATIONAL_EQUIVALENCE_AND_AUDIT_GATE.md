# Protocol 056 — Observational equivalence and the labeled-audit necessity gate

Date: 2026-11-13. Status: analytical negative result and prospective study design. No experiments executed; no novelty or AI performance claim.

## Question

Can a verifier ensemble estimate the probability that a scientific statement is true solely from the joint distribution of its verifier outputs, even when those outputs are observed without sampling error?

**Answer in the unrestricted latent-truth model: no.** This is a standard identification limitation, not a new theorem. The consequence for the proposed study is operational: a posterior confidence interval is not empirically grounded until its labeled-audit or structural assumptions are stated, tested where possible, and subjected to sensitivity analysis.

## Constructive observational-equivalence witness

Let Y in {0,1} be the unobserved truth of a scientific claim and let V=(V1,V2) in {0,1}^2 denote the outputs of two verifiers. Consider two data-generating worlds, both with P(Y=1)=1/2 and P(V=v)=1/4 for every v in {00,01,10,11}.

World I (uninformative verifiers): P(Y=1|V=v)=1/2 for every v.

World II (perfectly informative joint-positive event): P(Y=1|V=11)=1 and P(Y=1|V=00)=0; set P(Y=1|V=01)=P(Y=1|V=10)=1/2.

The total truth prevalence in World II is (1+0+1/2+1/2)/4=1/2. Thus the two worlds have exactly the same distribution of observable verifier outputs and the same prevalence, but

    P_I(Y=1|V=11)=1/2, while P_II(Y=1|V=11)=1.

Both are valid joint distributions. No procedure that uses only unlimited unlabeled samples of V (and even knows the prevalence) can distinguish these worlds. This is a counterexample to point identification, not a claim that every posterior is unrestricted under additional verified assumptions.

### Decision-theoretic consequence

Consider accepting a claim when V=11, with false-accept loss a>0. Its conditional expected loss is a/2 in World I and zero in World II. Any purportedly distribution-free numerical guarantee on this conditional risk from unlabeled V alone that is tighter than both possibilities must fail in at least one world. The conclusion does **not** rule out conservative bounds or guarantees supported by audited labels, verified physical constraints, or explicit assumptions.

## Falsification-oriented operational design

1. **Unit of independence:** a source claim family, not an individual paraphrase or a verifier call. Preserve source, domain, theorem/physical system, version, and transformation lineage.
2. **Gold truth:** for mathematics, independently checked formal proofs or counterexamples; for physics, explicitly specified equations, units, regimes, and reference calculations. Exclude ambiguous/undecidable claims rather than forcing labels. Audit any reference implementation independently.
3. **Verifier provenance:** record model identity/version, prompt, retrieval corpus, tool use, seed/temperature, shared evidence, and whether the verifier is a clone. Missing provenance is a reported limitation, not evidence of independence.
4. **Calibration:** fit error-rate and dependence sensitivity sets on training/calibration claim families only. If labels are absent or scarce, report a vacuous or assumption-conditional interval rather than inventing precision.
5. **Locked evaluation:** hold out whole source families; compare against calibrated single-verifier, majority vote, duplicate-aware aggregation, reject-option, and conformal/selective baselines at matched coverage and common loss matrices.
6. **Stress cases:** duplicate one verifier verbatim; introduce shared incorrect evidence; shift truth prevalence; swap physics regimes; introduce unit-inconsistent statements; vary the audit-label budget. Include adversarially correlated errors.
7. **Metrics:** conditional false-accept risk, risk-coverage curves, abstention rate, realized cost, interval width, and calibration. Use cluster-aware uncertainty by source family; distinguish nominal from realized guarantees.
8. **Precommitted failure conditions:** no improvement at matched coverage; benefits vanish against duplicate-aware calibration; intervals become uninformative under plausible dependence ranges; sensitivity sets systematically miss held-out audit frequencies; any data leakage or unverified label invalidates the primary claim.

## Minimal free-cloud experiment plan (not authorized to execute yet)

Stage A: run existing pure-Python exact-rational fixtures in a standard GitHub-hosted runner only after verifying account-specific free eligibility, quotas, spending controls, and runner access. Record workflow SHA, URL, logs, and zero-charge status. Stage B: construct a tiny, human-auditable, license-compatible benchmark of mathematics and elementary physics statements with preexisting verified solutions; no model inference is required for the dataset specification. Stage C: run only permitted, genuinely zero-cost hosted inference if such access can be verified independently; otherwise publish the mathematical negative result and experimental design without fabricating model comparisons.

A public repository does not by itself prove that every workflow, artifact, storage feature, or third-party service will cost $0. No laptop computation, self-hosted runner, card-backed trial, or unapproved cloud execution.

## Literature collision checklist

Compare explicitly with latent-class/noisy-annotator identifiability (Dawid and Skene, 1979), partial identification (Manski, 2003), abstention (Chow, 1970), selective classification (Geifman and El-Yaniv, 2017), conformal prediction (Angelopoulos and Bates, 2023), and recent correlated LLM-as-judge literature. The witness above is an elementary identification counterexample; do not market it as original. Verify exact bibliographic details and newer related work before manuscript submission.

## Go/no-go

The November 22 target is contingent on an identifiable estimand, credible labels, verified $0 infrastructure, and a defensible incremental contribution. If those are absent, release a clearly labeled research note or negative-result manuscript rather than claiming an empirically validated frontier-AI breakthrough.
