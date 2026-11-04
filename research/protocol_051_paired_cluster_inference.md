# Protocol 051 — Paired cluster inference with frozen operating points

Status: prospective analysis specification; **no experimental results**. Prepared 2026-11-04. Independent frontier AI research only.

## Research question
At validation-selected operating points, does an independently checked physical certificate reduce the probability of accepting an incorrect language-derived scientific claim, relative to a competitive baseline, without hiding a large loss of coverage?

## Units and estimands
Let i index held-out claims and g(i) the source family (e.g., original document, physical system, or generative template). A method m produces a binary acceptance A_mi from a threshold fixed *before* test inspection, and a binary independently adjudicated correctness Y_i. Define W_mi = A_mi(1-Y_i). For N test claims, report (i) accepted fraction C_m = sum A_mi/N, (ii) unconditional unsafe acceptance U_m = sum W_mi/N, and (iii) conditional selective risk R_m = sum W_mi/sum A_mi when the denominator is positive. Empty acceptance has undefined R, never zero risk. Primary paired effect: D_U = U_certificate - U_baseline, with D_C also reported. The unconditional effect is deployment-relevant but cannot by itself demonstrate improvement at matched coverage.

## Prespecified procedure
1. Freeze source-disjoint train/validation/test partitions, adjudication rules, model versions, prompts, scoring, and all random seeds. Detect duplicate or near-duplicate claims across partitions and audit grouping manually.
2. For each method and target validation coverage in {0.25, 0.50, 0.75}, select a score threshold on validation only. Accept score ties together. Store threshold and its hash in an immutable manifest before inspecting test labels.
3. Evaluate both methods on the *same* test claims, including abstentions, failures, and timeouts. Treat missing model outputs as non-acceptance but report their frequency. Keep ambiguous ground truth in a separate stratum and never silently assign it to correctness.
4. Report paired D_U and D_C, plus each method's C, U, R and accepted counts. Report risk-coverage curves only as secondary retrospective descriptions; do not present test-tuned operating points as deployment results.
5. Bootstrap *source clusters* with replacement using the same sampled cluster indices for both methods (paired bootstrap). Preserve all claims within each sampled cluster. Predeclare B=2000 replicates and RNG seed 51051. Report percentile 95% intervals and cluster count; interpret cautiously with few clusters. No per-claim independent bootstrap when source clustering exists.
6. As a sensitivity analysis, report source-macro averages (equal weight per source), leave-one-source-out estimates, and separate physics families. If source clusters are too few for credible uncertainty, report descriptive results and withhold inferential superiority claims.
7. Compare with direct-answer confidence selection, grounded NL-to-logic plus verifier, selective semantic verification, certificate method without independent model audit, and a physics oracle upper-bound control where feasible. Match datasets, compute budgets, and adjudication.

## Falsification and failure conditions
- Reject superiority if paired cluster uncertainty does not support D_U < 0 at a prespecified operating point, or if any improvement is explained solely by substantially reduced coverage.
- Reject a physical-validity claim when independently adjudicated physical assumptions fail, even if the formal checker accepts a certificate.
- Report as inconclusive if test leakage, non-independent labels, insufficient clusters, or competitive baseline implementation gaps invalidate comparison.
- Do not claim novelty for selective classification, formal verification, model checking, abstention, or clustered bootstrap themselves.
- Do not claim safety for unmodeled continuous systems from finite-state checks.

## Audit requirements and artifacts
Publish versioned dataset provenance, rights/licensing, source IDs, frozen threshold manifest, adjudication disagreements, raw method predictions, all failure cases, exact dependency lock, cloud runner identification, billing safeguards, command lines, checksums, and unedited test logs. Redact private information and follow benchmark licenses. Include AI-assistance disclosure wherever required.

## Literature collisions to audit before manuscript
Review original full texts and contemporaneous versions of CEGAR (Clarke et al., 2000), selective classification / risk-coverage literature, language-to-temporal-logic grounding benchmarks, VLTL-Bench, SCP-NL2TL, SENTINEL and GinSign. Record exact tasks, physics assumptions, independence of verifier, abstention definitions, and evaluation splits in a side-by-side table. Similarity of a title or abstract alone does not establish a novel gap.

## Execution gate
Do not start cloud runs until the actual repository Actions permissions, public-repo standard-runner eligibility, storage retention, account billing settings and any required payment-card conditions are verified. No paid or larger runners, GPU instances, local training, local inference or laptop workloads. This protocol is documentation, not executed evidence.
