# Protocol 172: Replication invariance and cluster estimand audit

Date: 2026-11-09
Status: mathematical analysis; no empirical results or execution claimed.

## Question
Does evaluation of a physics-grounded verifier change merely because a dataset curator adds NLP paraphrases of an existing source problem?

Let source problems be indexed by g=1,...,G and paraphrases within a source by j=1,...,n_g. Let y_gj(m,t) be a bounded outcome for method m under a frozen threshold t. The equal-source estimand is

T(m,t) = (1/G) sum_g [(1/n_g) sum_j y_gj(m,t)].

The case-weighted estimand is

C(m,t) = [sum_g sum_j y_gj(m,t)] / [sum_g n_g].

These target different populations. Neither is universally correct.

## Exact replication theorem
If every observation in one source cluster g is duplicated exactly k times (including all method scores, labels, and decisions), its within-source mean is unchanged. Therefore T is unchanged, provided G and all other clusters are unchanged. By contrast C generally changes whenever that source mean differs from the existing case-weighted mean.

Proof: The duplicated cluster numerator and denominator both multiply by k, so their ratio is unchanged. The case-weighted numerator and denominator instead receive additional weight (k-1)n_g from one source.

## Counterexample
Two sources have constant outcomes: source A has outcome 1, source B has outcome 0. Initially each has one paraphrase, so T=C=0.5. Duplicating A nine additional times leaves T=0.5 but changes C to 10/11. This is a constructed mathematical example, not experimental evidence.

## Crucial limitation
Adding *new, non-identical* paraphrases can change a source's within-cluster mean. Equal-source weighting protects against literal replication, not against a shift in the paraphrase sampling distribution. Therefore a claim of 'paraphrase invariance' must be restricted to exact replication or supported by a prespecified paraphrase-generating distribution.

## Paired method comparison
For two methods A and B, define d_g as the within-source mean of y_gj(A,t_A)-y_gj(B,t_B), with thresholds frozen on separate calibration sources. The target contrast is Delta=(1/G)sum_g d_g. Inference must resample source clusters, not individual paraphrases. If physics families are few or highly imbalanced, also report equal-family sensitivity and avoid assuming asymptotic cluster-bootstrap validity.

## Pre-registered tests to implement
1. Exact replication of one source changes case-weighted results but not equal-source results.
2. Adding a genuinely different paraphrase may change the equal-source result; the implementation must not falsely promise otherwise.
3. A method ranking reversal between case-weighted and equal-source estimands must be surfaced, not averaged away.
4. All method comparisons use identical source membership, with missing predictions rejected or separately accounted for.
5. Calibration and test source identifiers remain disjoint; no test labels enter threshold selection.
6. A source assigned to multiple physics families is rejected.

## Scientific decision gate
This theorem is an elementary property of weighted means, **not** a novel AI contribution. The proposed research requires an independently demonstrated gain against strong physics verification baselines under the declared source-level estimand, with honest coverage matching, uncertainty and prior-art analysis. Failure to show that gain means no positive performance claim.

## Infrastructure gate
No CI run, GPU job, or model inference is authorized here. The previously observed missing pytest dependency remains unresolved. Verify runner eligibility, quotas, billing/card requirements, and the actual workflow before cloud execution. No laptop computation or paid resources.
