# Direct-source novelty collision audit: partial identification and budgeted robustness
Date: 2026-11-23
Status: literature-screening evidence, not a systematic review or novelty certification.

## Verified primary references

1. Charles F. Manski (2005), "Partial identification with missing data: concepts and findings," *International Journal of Approximate Reasoning* 39(2–3):151–165. DOI: https://doi.org/10.1016/j.ijar.2004.10.006 . The publisher abstract explicitly frames missing data as a set of admissible distributions and evaluates how credible assumptions narrow identification regions.
2. Dimitris Bertsimas and Melvyn Sim (2004), "The Price of Robustness," *Operations Research* 52(1):35–53. DOI: https://doi.org/10.1287/opre.1030.0065 . The publisher abstract explicitly describes tunable robustness budgets and uncertainty/constraint-violation tradeoffs in optimization. This is a conceptual collision, **not** evidence that its uncertainty-set construction is identical to our source-cluster parity oracle.

## Claim-by-claim novelty boundary

- **Not novel by itself:** bounding missing outcomes over feasible completions. Manski already develops partial identification with missing data.
- **Not novel by itself:** controlling conservatism by a finite budget of uncertain components. Bertsimas–Sim is prior art; our source-cluster violation budget is not asserted equivalent to their model.
- **Not established as novel:** exhaustive enumeration of binary assignments under parity constraints; source-grouped relaxations; interval nesting under constraint relaxation; merging-source monotonicity. These are elementary consequences of feasible-set inclusion and may be known in constraint satisfaction and robust optimization.
- **Candidate application contribution only:** preregistered, independently adjudicated AI-verification evaluation with incomplete labels, authenticated evidence provenance, source-level assumption sensitivity, and misleading-narrowing stress tests across NLP, mathematics, and physics. No priority or superiority claim until a broader review and held-out evidence.

## Explicit model and estimand

For binary missing labels z in {0,1}^m and observed hard labels H, let E be parity assertions e=(i,j,b,s) claiming z_i XOR z_j=b with provenance source s. Define the violated-source set V(z)={s: some e with source s fails under z}. For budget k, the admissible set is F_k={z: z satisfies H and |V(z)|<=k}. For any estimand T(z) defined on F_k, sharp finite-frame bounds are [min T(z), max T(z)] over assignments with defined denominators. This is an identification interval conditional on H, E, provenance partition and k, **not** a confidence interval.

## Pre-registered falsification and comparison gates

1. Compare F_k bounds against no-parity Manski-style unrestricted completion bounds; report width and whether independently adjudicated held-out truth lies inside, separately. Tightening without validity is not success.
2. Compare record-budget and source-budget bounds at matched numerical k, with an explicit warning that k counts different units.
3. Freeze provenance clusters before observing held-out labels; rerun under plausible externally specified alternative partitions and report worst-case bounds.
4. Inject false parity assertions by source cluster, including duplicates, and report whether narrower bounds wrongly exclude independently adjudicated truth.
5. Compare against a simple source-dropping baseline: enumerate every subset of at most k sources, remove their assertions, solve remaining parity constraints and hard labels, and union feasible assignments. This is an independent reference formulation, not a new method.
6. Distinguish infeasible frames, undefined denominators, finite-frame identification and repeated-sample coverage; do not silently omit any.
7. Require separate physics-task ground truth derived independently of the evaluated model; mathematical consistency of parity assertions is not physical validation.
8. Publish seeds, sample selection, adjudication rubric, source hashes, exclusions, and negative findings. Any AI-assistance disclosure must comply with venue rules.

## Feasibility / zero-dollar boundary

GitHub documentation checked 2026-11-23: standard GitHub-hosted runners for public repositories are free; larger runners are charged, and storage allowances differ by plan. Sources: https://docs.github.com/en/actions/concepts/billing-and-usage and https://docs.github.com/en/billing/concepts/product-billing/github-actions . Public-repo status verified through the connected GitHub repository metadata. Do not assume a specific account's billing configuration or that Actions is suitable for sustained model training. No new paid service, cloud inference, local workload, or download is authorized.

## Outstanding literature search

Directly inspect Max-2-LIN / unique-games approximations, grouped constraint deletion / MaxSAT, selective prediction, conformal risk control, dataset auditing and evidence-dependence literature. Add bibliographic details and claim-level comparisons before manuscript novelty language. The two verified references above are only the first directly sourced collision checks.
