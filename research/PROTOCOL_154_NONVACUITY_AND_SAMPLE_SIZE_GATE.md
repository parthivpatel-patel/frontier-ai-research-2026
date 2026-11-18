# Protocol 154 — Non-vacuity and sample-size feasibility gate (2026-11-17)

## Scope and evidence status
Pre-experimental mathematical feasibility audit, **not** a model result, original concentration theorem, or validated statistical-coverage claim. Follows Protocols 147–153. No compute, data collection, or spending is authorized by this note.

## Precommitted finite-family source-level certificate
Let independent source clusters \(S_1,\dots,S_n\) be sampled from the target source distribution. For each of \(M\) **fixed before inspecting these evaluation labels** verifier/abstention policies \(h\), compute a source-level loss \(L_i(h)\in[0,B]\), where a source with many paraphrases contributes **one** prespecified aggregated loss. Dependence within a source is unrestricted. For \(\delta\in(0,1)\), Hoeffding plus a union bound yields, simultaneously for all \(M\) policies,

\[
R(h) \le \widehat R_n(h) + B\sqrt{\frac{\log(M/\delta)}{2n}}
\]

with probability at least \(1-\delta\). Here \(R(h)\) is target-population expected source-level loss. This statement requires independent identically distributed sources, bounded loss, fixed policies, valid labels, and a prespecified source aggregation rule. It does **not** protect against choosing new policies after reading the evaluation labels, selecting favorable sources, temporal shift, or optional stopping. No independence of prompts within a source is assumed.

## Explicit feasibility threshold
If the desired additive certificate radius is at most \(\epsilon\), then a sufficient independent-source count is

\[
n \ge \left\lceil \frac{B^2\log(M/\delta)}{2\epsilon^2} \right\rceil.
\]

With \(B=2\), \(\delta=0.05\), and \(M=10\), the required number of independent source clusters is:
- radius 0.25: at least 170 clusters;
- radius 0.10: at least 1,060 clusters;
- radius 0.05: at least 4,239 clusters.

These are **calculated theoretical thresholds**, not data sizes already available. They are conservative sufficient counts, not a statistical power analysis for detecting improvement against a baseline. A zero-width-looking certificate obtained by counting duplicated prompts as sources is invalid.

For comparisons against a prespecified baseline on the *same* sources, use a bounded paired source-level difference and a prespecified inference procedure; report the comparison's uncertainty separately. A non-vacuous upper bound on absolute risk alone does not establish a statistically significant improvement.

## Pre-experiment go/no-go
1. Inventory genuinely independent, legally usable source IDs separately for NLP, mathematics, and physics. Do not equate question count with source count.
2. Freeze source sampling, domain weighting, label adjudication, abstention cost, inference budget, baseline policies, and candidate family before revealing test labels.
3. Calculate the attainable confidence radius **before** running model inference. If too wide to support the intended claim, downgrade the experiment to exploratory or negative-feasibility reporting; do not silently relax confidence targets.
4. Use source-disjoint development, calibration, and final test splits. Audit near duplicates and common upstream documents; record unresolved provenance.
5. Verify free cloud inference availability, account-specific quotas, card/billing requirements, license restrictions, and data terms independently before any invocation. Standard public-repository GitHub Actions CPU runners may execute small deterministic tests but are not evidence of free GPU/model hosting.
6. Publish raw source identifiers where licenses permit, frozen code, model versions, run logs, failures, and all uncertainty estimates. Disclose AI assistance according to venue rules.

## Falsification and collision checks
- **Falsify calibration assumptions** if source dependence or nonrepresentative selection makes the claimed independent-source sampling model untenable.
- **Falsify performance improvement** if a cost-matched baseline is not outperformed under the prespecified paired source-level test or if the direction reverses on independently sampled sources.
- **Falsify broad cross-domain generality** if improvements do not replicate independently in each claimed domain.
- **Reject novelty framing** if the contribution reduces to the standard Hoeffding/union-bound certificate, selective classification, conformal risk control, or established verifier ensembles. Candidate novelty must lie in a clearly differentiated and reproducible empirical finding or a genuinely new result proven against closest prior art.

## Publication status
**NO-GO for an empirical novelty claim.** The Nov 22 date is a conditional internal checkpoint, not a deadline that overrides validity. Next evidence priority: obtain current CI logs for Protocol 152 and perform full-text theorem-level prior-art comparison, then assess independent-source inventory and free-cloud inference feasibility. No laptop workloads or paid resources.
