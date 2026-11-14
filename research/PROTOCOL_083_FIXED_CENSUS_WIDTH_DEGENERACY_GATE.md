# Protocol 083 — Fixed-census identification-width degeneracy and research pivot

Date: 2026-11-14. Status: analytical audit only; no empirical results or novelty claim.

## Critical finding

Protocol 081 proposes, as a possible novelty target, a provenance-aware adjudication allocation policy that reduces worst-case false-release bound width at equal adjudication cost. Under Protocols 081–082's **fixed released-claim census**, unrestricted binary missing-truth assumptions, and successful complete adjudication of exactly one previously unresolved claim per unit cost, that target is mathematically **degenerate**.

Let K>0 be the fixed number of released claims, F the number of resolved false claims, and U the number unresolved. The sharp interval is [F/K,(F+U)/K] with width W=U/K. After resolving any one unresolved label, either F increases by one (if false) or stays unchanged (if true), while U decreases by one. In both cases the width becomes (U-1)/K, an improvement of exactly 1/K **regardless of which claim is selected, its domain, its provenance family, or its true label**. After b successful resolutions (0<=b<=U), W_b=(U-b)/K. Thus no adaptive selection method can beat random selection on this width metric at the same number of successful resolutions. Reporting an improvement under this setting would indicate a mismatch in the experimental design, denominator, or comparator.

The same degeneracy holds for a predeclared positive-weight aggregate of domain false rates R_w=sum_d w_d T_d/K_d, where sum_d w_d=1 and K_d>0: resolving a claim in domain d reduces interval width by w_d/K_d. Selecting the largest weight-per-claim can improve width but is a deterministic known-weight allocation, **not** an ML innovation. Inverse-probability or clustered sampling uncertainty is not addressed by this census identity.

## When nontrivial allocation may remain possible

A useful policy question requires explicit heterogeneous verification *costs*, probabilistic *success or abstention*, a predeclared loss function, or an estimand with varying claim importance. For example, if claim i has verified adjudication probability p_i and fixed cost c_i, the expected one-attempt reduction in unrestricted census width is p_i/K (assuming a successful resolution and no other change). With equal costs, maximizing expected width reduction is equivalent to maximizing p_i; a learned policy must beat a strong calibrated success-probability baseline and account for its own training and evaluation costs. If p_i is unknown or varies with unobserved truth, unbiasedness and identification claims require additional assumptions. Do not conflate improved adjudication yield with improved truth accuracy.

For variable costs and sequential decisions, benchmark against transparent cost-aware scheduling, a greedy estimated-success-per-cost rule, uniform random selection, and an oracle upper bound available only in simulation. Evaluate under fixed *total* cost, not just equal numbers of attempts. Domain and provenance stratification must be frozen before seeing outcomes. Include worst-case unresolved-label completions and within-family dependence in uncertainty analyses.

## Falsification gate

1. For every fixed-census synthetic record set with K>0 and U>0, adjudicating any single unresolved claim must reduce unrestricted width by exactly 1/K.
2. For any two allocation policies completing the same b unresolved claims, final width must be identical; reject a reported difference.
3. A policy claiming benefit under heterogeneous cost must report attempted adjudications, successful resolutions, unresolved counts, actual cost, and the frozen denominator.
4. Run a negative control with identical success probabilities and costs across claims: no policy should show systematic advantage beyond sampling noise.
5. Run an adversarial case where difficult/false claims are less likely to resolve: disclose that optimizing resolution yield may worsen selective-label bias in naive resolved-only error rates, even while shrinking logical bounds.
6. Compare against prior art in active testing, selective labels, verification bias, and budgeted active learning before claiming novelty. An improved yield is not itself evidence of novel methodology.
7. Predeclare failure criteria: no material improvement against strong calibrated cost-aware baselines, poor cross-domain transfer, unstable uncertainty under provenance clustering, or insufficient adjudication evidence means **no positive novelty claim**.

## Minimal exact fixture specification

Use Python standard-library fractions and unittest on a verified free public GitHub-hosted standard runner. Enumerate binary completions for U<=8; for each selected unresolved claim verify both true and false resolutions yield width reduction 1/K. Verify b-step policy invariance for different selection orders. Add a domain-weighted counterexample demonstrating known weight-per-claim, not learned novelty. Store logs, workflow SHA, Python version, and negative results. No local laptop execution.

## Publication implication

This audit rules out the proposed *equal-successful-adjudications, unrestricted-bound-width* novelty claim before costly experiments. A narrower study of **cost- and success-aware scientific truth adjudication** may be testable, but its originality remains unverified. Treat the November 22 target as conditional; prefer a transparent negative/methodological paper over manufactured positive results. Cite established partial identification (Manski), active testing, selective-label/verification-bias, and budgeted active-learning literature in the manuscript after source-level review.

No cloud workload, GPU, payment, or user-laptop compute is required to state or check this algebra.
