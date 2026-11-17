# Protocol 148 — Source-cluster certification and evidence triage (2026-11-17)

## Scope
This is a methodological correction to Protocol 147, **not** an executed experiment, novel theorem, or empirical result. It specifies the sampling unit for cross-domain risk certification and prioritizes test execution over additional untested theoretical documents.

## Why prompt-level iid can fail
A benchmark can contain many paraphrases, continuations, or derived questions from the same source. Even when there are thousands of prompt rows, their losses can be dependent within source. Applying the iid Hoeffding radius to all rows then has no justified coverage. In particular, duplicating every item 100 times does not create 100 times as much independent information.

## Valid independent-cluster certificate
Predeclare the target distribution as a distribution over independent **source clusters** C_i, i=1,...,G, and fix a policy before observing final evaluation labels. For each cluster define a predeclared bounded aggregate W_i = (1/m_i) sum_j L_pi(Z_ij), with L in [0,M]. The within-cluster losses may be arbitrarily dependent. If the source clusters are iid and their complete aggregates are observed, W_i are iid in [0,M], so

P( E[W] > mean(W_i) + M sqrt(log(1/delta)/(2G)) ) <= delta.

This certifies the expected **equal-source-weighted** risk, not automatically the prompt-weighted risk or deployment risk. Unequal source weights, nonrandom cluster sampling, overlapping parent sources, temporal dependence, or selective missingness require a separately justified analysis. A fixed K predeclared policy family may use log(K/delta), with no license for unrestricted adaptive search.

## Numerical design implication (M=2, delta=0.05)
For 100 independent sources, radius approximately 0.2448. For 1,000 independent sources, radius approximately 0.0774. If 1,000 prompts derive from only 20 independent sources, the source-level radius is approximately 0.5473, **not** 0.0774. These are theoretical margins, not performance measurements.

## Source-disjoint cross-domain protocol
- NLP: group by originating document, event, or evidence provenance, including derivative paraphrases.
- Mathematics: group by original problem and shared solution template or generator seed; check reference solutions independently.
- Physics: group by physical scenario/model family and shared derivation, with units and assumptions independently validated.
- Freeze group identifiers, split assignments, policies, abstention penalties, verifier budgets, and evaluation scripts before final labels.
- Report number of prompts and number of independent source clusters separately. Audit cross-domain duplication and training contamination.
- For source-stratified sampling, provide domain-specific certificates or a mathematically justified weighted estimand; do not pool heterogeneous clusters and call them iid.
- Compare equal-cost and equal-coverage baselines. Report negative outcomes, abstentions, label ambiguity, and sensitivity to cluster definition.

## Falsification and operational gate
1. Verify that every derived prompt shares a source ID with its ancestor; deliberately insert a duplicate and confirm leakage checks catch it.
2. Recalculate the certificate after collapsing near-duplicates; withdraw any claim relying on inflated sample size.
3. Test an all-identical-within-source synthetic loss dataset: confidence width must depend on G, not row count.
4. Validate Protocols 140, 141, and 146 with actual runner logs, collected test counts, exact commit, and nonzero exit on failures. Confirm import portability for Protocol 141.
5. Complete theorem-level prior-art comparisons before any novelty statement. Relevant families include classical cluster sampling, concentration inequalities, partial identification, Dawid–Skene, selective classification, conformal risk control, and sequential verification.
6. Do not launch CI or cloud compute until provider and account-specific no-charge eligibility, remaining quota, billing/card conditions, and workflow safety have been checked. Never shift compute to the user's laptop.

## Publication decision
The November 22 checkpoint should yield either (a) a manuscript clearly separating analytical witnesses from validated empirical results, or (b) a transparent preprint/protocol with no unearned superiority or originality claims. This protocol is not a substitute for executed evidence.
