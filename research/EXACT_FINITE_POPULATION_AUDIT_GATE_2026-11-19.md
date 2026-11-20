# Exact finite-population audit gate for zero observed errors (2026-11-19)

Status: preregistration and mathematical verification target. **No empirical model result, original theorem, or verified CI run is claimed.**

## Why this matters
The randomized-audit design note gives an unbiased estimator under known inclusion probabilities. But a frequent reporting failure is to call a verifier reliable when a small audit detects zero errors. Zero detections are not a guarantee of zero underlying accepted-answer errors. This supplement provides an exact, assumption-explicit audit planning and reporting gate for a **simple random sample without replacement** (SRSWOR) from a frozen set of accepted answers.

## Exact finite-population inversion
Let N >= 1 be the fixed number of accepted answers, K in {0,...,N} the unknown count of incorrect accepted answers, and n in {1,...,N} the number selected uniformly without replacement for independent correctness adjudication. Let X be the observed number of errors in the audit.

Conditional on fixed N,K,n and valid SRSWOR,

    P_K(X=x) = C(K,x) C(N-K,n-x) / C(N,n)

with impossible binomial coefficients defined as zero. In particular,

    P_K(X=0) = C(N-K,n) / C(N,n).

If X=0, a one-sided exact (1-alpha) upper confidence limit for K is

    U(N,n,alpha) = max { k in {0,...,N}: C(N-k,n)/C(N,n) >= alpha }.

The corresponding upper bound on the **fixed accepted population's** error fraction is U/N. The inversion is conservative because K is discrete. At n=N and X=0, U=0. If n<N, U can be positive even when X=0. This does not establish future-domain generalization or a risk guarantee after distribution shift.

For numerical stability, compute the zero-error probability as a product

    P_K(X=0) = product_{j=0}^{n-1} (N-K-j)/(N-j)

with zero when N-K<n, or use log-gamma arithmetic for large N. This formula is monotone nonincreasing in K; integer binary search gives an exact threshold up to numerical comparison tolerance. Near the alpha boundary, use integer arithmetic or exact rational comparisons.

## Concrete audit planning, not measured outcomes
To preregister a target accepted-error ceiling r0, define K0=floor(N*r0)+1, the smallest **unacceptable** number of errors. A zero-error audit can exclude all K>=K0 at one-sided significance alpha only if

    C(N-K0,n) / C(N,n) < alpha.

Choose the smallest n meeting this criterion, subject to the available independent adjudication budget. This is a prospective design calculation, not evidence that the verifier meets r0. For large N and small sampling fraction, the familiar approximation is (1-r0)^n; it is not the exact finite-population result. The audit must actually observe zero errors for the zero-error release gate to apply.

## Nonzero errors and multiple families
For x>0, invert the appropriate hypergeometric lower tail P_K(X<=x) to obtain an exact upper confidence bound on K; do not reuse the zero-error formula. Preregister simultaneous family-wise coverage (NLP, mathematics, physics), e.g. allocate alpha/3 per family by Bonferroni, if all three family-level statements are required simultaneously. Report each N_f, n_f, x_f and upper bound, not only the pooled total.

## Failure conditions and applicability
- Audit selection is not uniform SRSWOR, inclusion probabilities are unknown, or audits are chosen after seeing correctness: the formula is invalid.
- Some selected answers lack independent adjudication: zero *observed* errors among respondents is not zero errors in the randomized audit. Resolve nonresponse or use explicitly justified conservative bounds.
- Generated answers, verifier scores, thresholds or accepted sets change after sampling: the frozen-population interpretation breaks.
- Confidence intervals are misrepresented as deterministic guarantees, causal effects, or distribution-shift guarantees.
- The target error ceiling, alpha, families, and audit stopping rule are chosen after seeing results: nominal coverage can fail.
- Repeated peeking or optional stopping without a valid sequential method invalidates the fixed-n inversion.
- Exact correctness labels in physics and NLP may be disputed; use blind independent adjudication and disagreement sensitivity.

## Testable implementation requirements
1. Enumerate small N,K,n and compare exact rational hypergeometric zero probabilities against combinatorial counts.
2. Check monotonicity in K, U=0 for n=N with X=0, and upper-bound behavior when n is small.
3. Exhaustively enumerate all samples for small finite populations to verify at-least-nominal frequentist coverage of the inverted bound, including x>0 before implementing a general reporting tool.
4. Fail closed on missing adjudications, non-SRS sampling, post-selection tuning, and undefined N or n.
5. Record the frozen accepted population, random seed, draw indices, label provenance, and any exclusions in cloud CI artifacts.

## Scientific positioning
This is standard hypergeometric sampling and exact confidence-interval inversion, not novel mathematics. It supplies an auditable *falsification and reporting gate* for the proposed cross-domain AI verifier study. It is not evidence of a distinctive verifier, model capability, or advantage over selective-classification/conformal baselines. The project's scientific novelty remains unverified.

## Compute and publication policy
The note requires no model inference, downloads, or laptop computation. Any subsequent execution must use verified no-charge cloud resources with billing disabled or otherwise assured $0; no paid runner, account upgrade, or card enrollment is authorized. The November 22 checkpoint should release a methods/preregistration manuscript rather than claim a discovery if held-out cross-domain evidence is absent.
