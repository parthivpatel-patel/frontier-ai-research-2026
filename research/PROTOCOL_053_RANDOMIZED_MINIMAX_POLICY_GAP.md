# Protocol 053 — Randomized minimax actions and the deterministic-policy gap

Status: analytical correction and falsifiable design, **not** a novel theorem, executed experiment, or evidence of AI-model improvement. 2026-11-13 (US Eastern).

## Correction to Protocol 052

Protocol 052 minimizes the maximum conditional loss **among three pure actions** (accept, reject, abstain). This does not necessarily minimize worst-case loss over **randomized policies**. The distinction matters whenever a paper uses the phrase “minimax optimal”: the original result is optimal only in the deterministic action class. Randomization is a classical decision-theoretic device and is not claimed as novel here.

Let p=P(Y=1 | V1=V2=1) lie in [L,U]. Let q_A,q_R,q_X be nonnegative probabilities summing to one for accept, reject, and abstain. With false-accept cost a>0, false-reject cost b>0 and abstention cost c>=0, the risk at truth probability p is

R(p;q)=q_A a(1-p)+q_R b p+q_X c.

Since this is affine in p, its worst case on [L,U] occurs at L or U. The randomized minimax program is

minimize t over (q_A,q_R,q_X,t), subject to
q_A+q_R+q_X=1; q_A,q_R,q_X>=0;
t >= q_A a(1-L)+q_R b L+q_X c;
t >= q_A a(1-U)+q_R b U+q_X c.

This is a three-action linear program with two endpoint-risk constraints. A deterministic rule is a feasible special case; therefore randomized minimax risk cannot exceed the pure-action minimax risk.

## Exact analytical counterexample

Set [L,U]=[3/4,1], a=4, b=1, c=2. Protocol 052 gives pure-action worst-case losses (accept,reject,abstain)=(1,1,2), so its deterministic minimax risk is 1.

A randomized policy q_A=1/5, q_R=4/5, q_X=0 yields:
- R(3/4)= (1/5)*1+(4/5)*(3/4)=4/5;
- R(1)= (1/5)*0+(4/5)*1=4/5.

The worst-case risk is 4/5, strictly below the deterministic optimum 1. To prove global optimality in this example, at p=4/5, accept and reject each have expected loss 4/5 and abstain has loss 2. Any randomized policy therefore has R(4/5)>=4/5; since 4/5 lies inside [3/4,1], no policy can have worst-case loss below 4/5. Thus 4/5 is the randomized minimax value.

For c=1/5 instead, pure abstention has risk 1/5 and is minimax even allowing randomization: at every p, abstention is cheaper than or equal to the randomized minimax lower bound of 4/5 for accept/reject mixtures. This latter statement uses the same interval and error costs.

## Operational interpretation

A randomized recommendation for whether to accept a **single scientific claim** may be operationally unacceptable even if it lowers average loss across repeated claims. A deployed safety-critical verifier may require deterministic outputs, an explicit human review channel, or additional constraints on false-accept probability. Thus both policy classes should be reported, without conflating randomized minimax *expected loss* with per-claim guarantees.

If randomization is evaluated, pre-register the policy seed, report seed-to-seed variability, and separately estimate false-accept rates, coverage, and loss. Never market randomized acceptance as improved factual certainty.

## Falsification and comparison plan

1. Verify exact endpoint risks and the analytical lower-bound certificate using rational arithmetic; test c=2 and c=1/5.
2. Compare pure-action minimax against randomized minimax on a pre-registered rational grid, including L=U and L=0,U=1.
3. Add strong baselines: calibrated point estimates, selective classification, and decision-theoretic reject options. Attribute gains to action-class expansion rather than a new uncertainty estimator.
4. Under claim-disjoint real evaluations, compare expected loss and false-accept risk with uncertainty intervals clustered by claim/evidence lineage. Reject any improvement claim if it vanishes under cost-matched baselines, dependence shift, or conservative uncertainty estimates.
5. Check that the randomization is ethically and operationally admissible before any deployment discussion.

## Prior art and novelty limits

Randomized statistical decision rules, minimax games, robust Bayes decision-making, reject-option classification, and partial identification are established research areas. This counterexample corrects the scope of Protocol 052; it is **not** a discovery of a new AI algorithm. Before claiming novelty, review primary work on minimax randomized decision rules, robust classification with abstention, imprecise probabilities, and selective risk under shift. A physics-inspired framing requires its own independently testable physical model, not an analogy.

## Execution and cost controls

This document is a pencil-and-paper analytical result only. No tests, cloud jobs, models, or benchmarks are reported as run. The user's laptop must remain browser-only. Do not execute any GitHub Actions workflow until account-specific runner availability, billing safeguards, free quota, and zero-cost eligibility are verified. Never use paid or larger runners; never incur a charge without explicit authorization.

The November 22, 2026 publication date remains a conditional internal target. Report this as a methodological correction, not empirical progress.
