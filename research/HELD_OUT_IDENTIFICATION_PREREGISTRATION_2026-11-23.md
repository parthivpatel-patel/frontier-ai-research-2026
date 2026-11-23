# Held-out identification study: preregistered protocol (2026-11-23)

Status: **design only**. No held-out AI results, novelty claim, or external annotation is implied.

## Unit, target and missingness

The unit is a frozen claim instance (prompt, model response, atomic proposition, timestamp, domain). Let Y_i in {0,1} denote adjudicated correctness, A_i^p in {0,1} the accept decision of policy p, and V_i in {0,1} whether its label is observed. Record provenance for every label and for every proposed parity edge. Do not treat abstentions as incorrect claims.

For a fixed policy p, define selective error R_p = sum_i A_i^p (1-Y_i) / sum_i A_i^p when the denominator is positive. For comparing policies, the primary contrast is R_p - R_q, with both policies evaluated on the **same frozen claim frame**. When a denominator is zero, mark that policy's risk undefined; never silently replace it with zero. Report coverage/acceptance separately.

## Identified sets and sensitivity

Let F_k be the binary-label assignments consistent with observed labels and violating at most k *recorded* parity assertions. The sharp finite-frame contrast interval, conditional on the frozen frame and these assumptions, is [min_{y in F_k}(R_p(y)-R_q(y)), max_{y in F_k}(R_p(y)-R_q(y))]. If F_k is empty, return **infeasible** rather than an interval. Nested F_k imply nested identified sets; this is a mathematical check, not a calibration guarantee.

Record-level k is sensitive to duplicated evidence records: report both raw-record and independently deduplicated-source budgets. A graph of asserted equivalences is not ground truth; if labels and edges come from the same model, call the result model-conditional rather than independently verified.

## Split and adjudication firewall

1. Freeze the evaluation claims, timestamps, model/version hashes, and policy decisions before opening reference labels.
2. Select the audit/verification subset using a declared seed and sampling design independent of correctness, or explicitly report and adjust known selection probabilities. Never imply random missingness from convenience auditing.
3. Two independent adjudicators should inspect the original source, not policy predictions. Record disagreements, unresolvable claims, source freshness, and adjudication dates; adjudicators of parity edges should be blinded to which policy benefits.
4. Split edge-development examples from held-out evaluation. A post-hoc edge chosen after seeing errors is not eligible for the confirmatory analysis.
5. Publish an immutable manifest of included/excluded claims and edge provenance, with licenses and personal information screened.

## Predeclared comparisons

B0: unrestricted unknown-label bounds; B1: independently authenticated zero-violation parity bounds; B2: bounded-violation sets at k in {1,2} and at prespecified fractions of *unique* edge sources (when feasible); B3: fully observed reference subset with known labels, clearly separated from the missing-label target. Include random-edge and corrupted-edge stress tests as **negative controls**, not evidence of genuine constraints.

Report interval width, inclusion of fully adjudicated contrast on stress-test fixtures, infeasibility rate, undefined-denominator rate, number of genuinely independent constraints, sensitivity to duplicate removal, and runtime. Narrower intervals alone do not establish better truth recovery or statistical coverage.

## Cross-domain claim rules

NLP: preserve quoted claim spans, source URLs, retrieval dates, and semantic equivalence adjudication. Mathematics: identify exact formal assumptions and provide proofs or counterexamples for asserted equivalence. Physics: include units, measurement uncertainties, regimes, and boundary conditions; textual similarity does not establish physical equivalence. No cross-domain aggregation before domain-specific error analyses.

## Falsification and stop rules

Reject the empirical usefulness claim if authenticated constraints routinely exclude independently known truth under declared corruption rates, if narrowing disappears after provenance deduplication, if the policy ranking reverses under small plausible k without being disclosed, or if labels/edges were selected using held-out policy errors. Treat missing verification labels under nonrandom selection as a separate identification problem; parity constraints do not fix selection bias automatically.

## Novelty boundary and publication integrity

Binary parity constraints, bounded disagreement, exact enumeration, and partial identification overlap established work. A possible contribution is the auditable combination of provenance-controlled logical constraints, selective-risk contrasts, and sensitivity reporting for partially labeled AI verification. This is a **hypothesis about contribution**, pending a source-by-source prior-art comparison and real held-out results. Record all AI assistance as required by venue rules. Never describe synthetic fixtures as real model performance.

## Cloud execution gate

Run only small CPU tests in a standard public-repository GitHub-hosted workflow after checking current runner eligibility, account spending limits and any billing policy changes. No paid runner, GPU, local model execution, large download, credit-card enrollment or external service is authorized. If eligibility cannot be established, keep this protocol executable on paper and do not launch experiments.
