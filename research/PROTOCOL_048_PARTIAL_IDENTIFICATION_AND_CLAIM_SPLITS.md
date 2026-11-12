# Protocol 048 — Partial-identification bounds and claim-disjoint evaluation

Date: 2026-11-12. Status: analytic design and derivation only; no experiments executed, no novelty claim.

## Correction to Protocol 047

Source-family disjointness **alone is insufficient** to prevent leakage: a claim, paraphrase, or its ground-truth adjudication can recur across train/calibration/test even when evidence originates from distinct source families. Build a bipartite graph connecting each claim to every originating observation and verifier output; union all claim-equivalent paraphrases and source-lineage descendants into connected components. Allocate **whole components** to one split. A single giant component may make the planned benchmark infeasible: report the component-size distribution and abort rather than silently split it. If all claims share one global model lineage, do not use verifier-family identity alone as a graph edge (it would trivially collapse the corpus); distinguish observation provenance from reusable model families. Fit calibration and choose thresholds without seeing held-out truth labels. For leave-one-family-out evaluation, ensure claim components are also held out.

## Analytic partial-identification benchmark

Let Y be a binary truth label with prior P(Y=1)=pi. Two positive-verdict indicators V1,V2 have symmetric class-conditional marginal sensitivity P(Vi=1|Y=1)=s and false-positive rate P(Vi=1|Y=0)=f. Without any conditional-independence assumption, Fréchet bounds imply

max(0,2s-1) <= a=P(V1=V2=1|Y=1) <= s
max(0,2f-1) <= b=P(V1=V2=1|Y=0) <= f.

When the event has nonzero probability, the posterior is P(Y=1|V1=V2=1)=pi*a/[pi*a+(1-pi)*b]. Since it increases with a and decreases with b, its sharp range, given only these marginals, is

L = pi*max(0,2s-1) / [pi*max(0,2s-1)+(1-pi)*f]
U = pi*s / [pi*s+(1-pi)*max(0,2f-1)]

subject to positive denominators and attainable joint distributions. Degenerate zero denominators require an explicit event-support check; a posterior conditioned on a probability-zero event is undefined. The endpoints can be attained by separate joint couplings in the two truth strata, hence the bounds are sharp under the stated assumptions.

**Illustrative arithmetic, not experimental evidence:** pi=0.5, s=0.8, f=0.2 gives L=0.75 and U=1.00. Conditional independence gives a=0.64,b=0.04, posterior 0.941176... . Perfectly duplicated verifier outputs give a=0.8,b=0.2, posterior 0.8. Thus an observed pair of positive votes and their individual accuracies do not identify posterior confidence. This is a known implication of dependence bounds, not a new theorem.

## Physics connection, carefully scoped

The analogy to correlated measurements in physics is methodological: repeated readouts sharing a common systematic error do not supply independent information. A provenance graph can encode *observed* shared measurement lineage, but cannot by itself recover hidden common causes. This is **not** a claim of a new physical law or a quantum-mechanical mechanism.

## Testable research contribution candidate

Compare a robust interval-valued confidence/abstention policy against (i) vote-only calibrated stacking, (ii) duplicate collapse, (iii) lineage-aware calibrated stacking, and (iv) an oracle conditional-dependence model (synthetic only). An interval policy may abstain if its worst-case lower confidence fails a preregistered threshold. To be useful, it must achieve an improvement in worst-case error or reliable coverage on **claim-and-lineage-disjoint** tests, without an unacceptable abstention penalty. If it only wins on contrived duplicate cases, is dominated by calibrated vote-only stacking, or its intervals are too broad for useful coverage, report a negative result. No claim of model-level guarantee is possible without calibrated class-conditional marginals and explicit assumptions about their shift.

## Reproducibility and feasibility gate

Implement a pure-Python standard-library validator with positive/negative tiny synthetic fixtures. Fail on (1) claim reuse, (2) paraphrase component reuse, (3) source lineage crossing splits, (4) inconsistent truth labels, (5) duplicate case IDs, and (6) degenerate conditioning events. Log deterministic seed, fixture hash, split components, Python version, commit SHA, workflow run URL and exit status. Do not label tests as passing until independently executed and logged.

GitHub's public-repository standard-hosted-runner documentation is not proof of this account's settings, billing controls, or runner availability. **No workflow should be launched** before confirming exact repository public visibility, Actions permissions, runner type, spending controls and absence of a card requirement. Never use laptop compute, paid APIs, GPU services, large downloads, or billable cloud infrastructure. A document-only commit requires no compute experiment.

## Closest prior art to audit before claiming originality

- Fréchet (1935) / Hoeffding (1940) dependence bounds and copula literature: sharp binary joint-event bounds.
- Dawid and Skene (1979): observer error-rate estimation with conditional-independence assumptions.
- Karger, Oh, Shah (2011): iterative learning from crowdsourced labels.
- Conformal factuality / risk-controlling prediction sets (including Mohri and Hashimoto 2024).
- Selective classification, ensemble calibration under correlated errors, data provenance, and dataset contamination.
- Physics: correlated observations and common-mode systematic uncertainty.

Primary sources and exact theorem scope must be checked before publication. No algorithmic novelty, empirical gain, or frontier-model applicability is yet established. AI assistance must be disclosed according to publication policy. November 22 remains conditional.
