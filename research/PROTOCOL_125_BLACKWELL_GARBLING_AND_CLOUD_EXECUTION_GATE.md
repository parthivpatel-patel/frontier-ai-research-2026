# Protocol 125 — Blackwell garbling, robust information monotonicity, and zero-cost execution gate (2026-11-16)

**Status:** Literature-anchored analytical protocol. No experimental results, executed tests, or novelty claims.

## Core correction: what additional verification can and cannot guarantee

For fixed prior, fixed loss, and no acquisition fee, observing (Y1,Y2) is at least as informative in the Blackwell sense as observing Y1 alone: discard Y2 deterministically. This is true for **every fixed joint distribution**, regardless of conditional dependence. With uncertainty set Q, let X12 contain all randomized policies using both signals, and X1 its subset that ignores Y2. Then

min_{x in X12} max_{q in Q} R(x,q) <= min_{x in X1} max_{q in Q} R(x,q).

The inequality follows from set inclusion, not statistical independence, and requires the *same* uncertainty set and loss in both optimizations. The second signal's robust gross incremental value can be zero, but cannot be negative under these assumptions. This does **not** imply a fitted, misspecified, or finite-sample algorithm cannot perform worse in held-out data. Nor does it guarantee benefit after additional signal acquisition costs.

**Important distinction:** Comparing a two-signal worst-case model to a single-signal model with different ambiguity sets is not justified by this inequality. For a valid comparison, project Q to the single-signal marginal laws and use the same prior/loss. If Q permits the second signal to be a deterministic duplicate of the first, that scenario does not *by itself* prove zero robust incremental value: the maximizer and minimizer order and other feasible joint laws matter. A zero-gain claim needs direct calculation or a stronger argument.

## Conditional duplicate-verifier negative control

If Y2=Y1 almost surely conditional on either truth state, and the observation cost of Y2 is zero, every two-signal policy is equivalent in realized risk to a one-signal policy on the supported outcomes. Consequently optimal gross Bayes risk is identical. If acquiring Y2 has positive incremental cost, optional acquisition should decline it. A practical test must also check that impossible mixed-sign outcomes are excluded from posterior claims while ex-ante risk stays defined.

## Numerical falsification fixtures to implement

1. Build exact rational conditional tables for both truth states; check all four cells nonnegative and summing to one.
2. Compare optimal no-signal, Y1-only, and (Y1,Y2) policies with the same loss and prior. Assert gross risk is nonincreasing as information is added.
3. Test exact duplication, conditional independence, and opposite dependence endpoints with fixed marginals.
4. Under ambiguity Q, embed each one-signal policy as a two-signal policy that ignores Y2. Assert robust mixed optimum is no larger than robust single-signal optimum.
5. Add a strictly positive second-verifier acquisition fee and assert the *optional* optimum never exceeds the one-verifier strategy's risk, since the decision maker may skip Y2.
6. Stress asymmetric false-positive/false-negative/abstention losses and zero-probability observations.
7. Require independently checked solver output and source-disjoint held-out experiments before any empirical performance claim.

## Closest foundational prior art verified

David Blackwell, **“Equivalent Comparisons of Experiments,”** *Annals of Mathematical Statistics* 24(2), 265–272 (1953), DOI: [10.1214/aoms/1177729032](https://doi.org/10.1214/aoms/1177729032). This establishes that comparing information structures by their decision value is classical. See bibliographic record: https://cir.nii.ac.jp/crid/1362544419209410176 . The present observation/discard argument is not novel.

Additional theoretical literature remains to be audited: robust Bayesian decisions under non-rectangular uncertainty; correlation-robust information aggregation; imprecise probability; selective classification and LLM judge agreement. No claim of an exhaustive literature review.

## Remote-only, $0 cloud gate — updated from official documentation

GitHub's official Actions billing documentation (accessed 2026-11-16): https://docs.github.com/en/billing/concepts/product-billing/github-actions . It says **standard GitHub-hosted runners in public repositories are free**, independently of included compute usage; **larger runners are billed even in public repositories**. Storage and caches have separate allowances/charging rules. A public repository alone does not establish account-specific workflow permissions, billing status, or current availability.

Proposed future workflow, **not launched**: manual dispatch only; standard `ubuntu-latest`; read-only `contents: read`; `timeout-minutes: 5`; no third-party actions, containers, pip installs, models, caches, or artifact uploads; `python -m unittest` on the standard-library fixtures; report short logs in GitHub Actions job output. Before enabling, inspect repository visibility, workflow permissions, account billing/payment status and spending controls. No laptop compute. Do not use larger or self-hosted runners. No paid upgrade or card enrollment.

## Publication gate

A November 22 analytical methods draft is permissible if clearly labeled; an empirical claim about NLP, mathematics, and physics requires real independently adjudicated source-disjoint data, cloud execution logs, calibrated strong baselines, and uncertainty analysis. Record AI assistance transparently. No tests have been run under this protocol.
