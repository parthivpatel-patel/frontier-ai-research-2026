# Protocol 145 — Identifiability and Robustness-Certificate Audit (2026-11-17)

## Purpose and claim boundary
This memo tests what can and cannot be inferred from the synthetic coupled-verifier model in Protocols 139–141. It is a mathematical specification and falsification plan, not an empirical result, a novel theorem, or an assertion that AI verifier outputs follow this model.

## Exact state model
Let Y ∈ {0,1}, P(Y=1)=p, and V1,V2 ∈ {0,1}. Conditional on Y=y, let
P(V1=0,V2=0|Y=y)=P(V1=1,V2=1|Y=y)=t_y,
P(V1=0,V2=1|Y=y)=P(V1=1,V2=0|Y=y)=1/2-t_y,
where 0 ≤ t_y ≤ 1/2.

Each verifier has conditional positive rate 1/2 for either Y. Thus each is *individually uninformative* about Y in this construction. Dependence can nevertheless differ by Y; their joint output may be informative. This assumption is central and is not a realistic default for actual AI verifiers.

For the decision rule 'accept only if V1=V2=1', with loss 2 on a false acceptance and loss 1 on abstention, the risk is

R(t0,t1,p) = 1 + (1-p)t0 - p t1.

Derivation: starting from loss 1 for all cases, an acceptance changes loss by +1 when Y=0 and by -1 when Y=1. The probabilities of (V1,V2)=(1,1) in the two truth strata are t0 and t1.

## Identifiability obstruction (important)
From unlabeled verifier pairs alone, the observable probability of (1,1) is q=(1-p)t0+p t1, and the other diagonal cell has the same probability q. Consequently (p,t0,t1) cannot generally be identified from unlabeled outputs. Different latent truth/dependence configurations can induce *identical observable verifier distributions* but different decision risks.

Exact witness at p=1/2, q=1/4:
- Model A: t0=0, t1=1/2. Risk R=3/4.
- Model B: t0=1/2, t1=0. Risk R=5/4.
Both yield P(00)=P(11)=1/4 and P(01)=P(10)=1/4. Yet the risks differ by 1/2.

Therefore, no distribution-free, nontrivial risk certificate for this policy can be learned from unlabeled verifier agreement alone under this model. Ground-truth labels, externally justified structural restrictions, or a conservative uncertainty set are indispensable. This is a direct counterexample, not a novel impossibility theorem.

## A valid uncertainty-set certificate
For a declared feasible set U ⊆ [0,1]×[0,1/2]^2, define B(U)=sup_(p,t0,t1 in U) [1+(1-p)t0-p t1]. A claimed bound B must state:
1. whether U is fixed independently of the evaluation sample;
2. how label sampling, uncertainty calibration, and distribution shift affect coverage;
3. whether policy selection reuses the calibration data;
4. whether the adversary observes the policy randomization;
5. whether loss and verification costs are bounded as modeled.

For the rectangular set p ∈ [1/4,3/4], t0,t1 ∈ [0,1/2], the maximum is 1+(3/4)(1/2)=11/8, attained at p=1/4, t0=1/2, t1=0. For the coupled set t0=t1=t, p ∈ [1/4,3/4], t ∈ [0,1/2], the maximum is 5/4. The difference is a relaxation gap, not evidence of a better deployed policy.

## Required exact-rational regression witnesses
1. Enumerate the eight joint states and verify normalization and conditional marginals.
2. Verify Model A and B have exactly the same four unlabeled verifier-pair probabilities.
3. Verify R_A=3/4 and R_B=5/4.
4. Verify the rectangular bound 11/8 and coupled bound 5/4 at their stated extrema.
5. Verify any proposed estimator based *only* on unlabeled pair frequencies cannot distinguish A from B; prohibit claims of certified risk from agreement statistics alone.
6. Cross-check the algebraic risk formula against independently enumerated losses, rather than a shared helper.
7. Record an explicit failed test if an implementation silently treats the coupled set as rectangular or claims equality of the two maxima.

## Experimental preregistration implications
For NLP, mathematics, and physics evaluation, obtain independently adjudicated truth labels and record the provenance of each label. Split sources (not just near-duplicate prompts) between calibration, policy tuning, and final testing. Fix verifier identities, prompts, latency/cost measurement, abstention rule, uncertainty-set construction, and primary loss *before* held-out evaluation. Compare to single verifier, fixed two-verifier, selective/conformal, and cost-matched sequential baselines. Report coverage, selective error, total verification cost, source-clustered uncertainty, and violations of nominal risk bounds. A claimed advantage fails if it disappears under matched budget/coverage, label leakage is detected, or the uncertainty set misses held-out frequencies.

## Prior-art collision
The impossibility witness is an instance of latent-variable nonidentifiability; minimax optimization, robust uncertainty sets, and abstention are established topics. Compare with classical partial identification, Dawid–Skene label aggregation, correlated annotator models, robust sequential decision-making, and conformal/selective risk control before making methodological novelty claims. Protocol 144 lists initial papers; theorem-level overlap is still outstanding.

## Execution and integrity
No test, training, inference, download, cloud job, or paid service was executed for this memo. No laptop computation is needed. Any GitHub Actions or other cloud execution remains blocked until account-specific billing, quotas, and zero-charge safeguards are verified. November 22 is a conditional checkpoint.
