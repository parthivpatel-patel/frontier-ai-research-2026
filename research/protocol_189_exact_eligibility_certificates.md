# Protocol 189 — Exact eligibility certificates and intervention sampling audit

Date: 2026-11-11 UTC. Status: executable-design specification only; no tests, experiments or novelty claim.

## Purpose and relationship to Protocol 188

Protocol 188 defines the fixed-margin bipartite graph fiber and semantic invalidity. This protocol specifies a *checkable certificate* for an eligible intervention, distinguishes local two-switch eligibility from global eligibility, and prevents a subtle selection error: finding no qualifying **single** two-switch from the original graph does not establish that no semantically invalid graph exists elsewhere in the fiber.

## Mathematical objects

For each preregistered link-type/scope stratum k, take finite source set S_k, target set T_k, original simple edge set E0_k, and independently adjudicated admissibility relation A_k subset S_k x T_k. The degree-constrained fiber F_k consists of all simple graphs with exactly the observed source and target degree vectors. Require E0_k subset A_k and an independently preserved adjudication record before eligibility testing.

Define global eligibility G_k = 1 iff there exists E in F_k with E not subset A_k. Define one-switch eligibility L_k = 1 iff a single legal two-edge switch from E0_k produces an edge outside A_k. Always L_k <= G_k; do not silently replace G with L. A sequence of valid two-switches may reach an invalid graph even when no immediately invalid one-switch exists. Any intervening graphs must remain in the same fiber; do not imply all intermediate graphs are semantically valid.

## Certificate format

A positive certificate includes: immutable problem and stratum identifiers; digests of E0, A and the registered identifier universes; the candidate E1; sorted source and target degree vectors for both arms; exact set difference E1 minus A (at least one edge); and a deterministic verifier version. The verifier checks that E1 differs from E0, all edges are unique and registered, degrees and scope match, and no non-provenance model-visible bytes differ. The A digest alone is not an independent signature or timestamp.

For a negative **global** certificate, use exact finite search over the entire fiber or a separately reviewed mathematical proof. Exhaustion must record the number of distinct graphs visited and a verifiable enumeration method. A bounded search timeout, zero qualifying local switches, or unsuccessful random sampling is **unknown**, never ineligible. Distinguish status codes ELIGIBLE_LOCAL, ELIGIBLE_NONLOCAL, PROVEN_INELIGIBLE, UNKNOWN_TIMEOUT, INVALID_ORIGINAL and UNADJUDICATED.

## Exact small-instance oracle (design, not run)

For small strata, enumerate all 0/1 adjacency matrices row by row, pruning partial rows that exceed target degrees and remaining-capacity bounds. For each complete matrix with the required margins, test whether at least one edge lies outside A. Store a canonical sorted edge-set digest to detect duplicates. Record counts of fiber size, valid graphs, and semantically invalid graphs. This is exponential in general; set a predeclared maximum state budget and classify overflow as UNKNOWN_TIMEOUT. Do not run this on the user's laptop.

For larger strata, use degree-preserving switches to *find positive witnesses*, but never treat a failure to find one as a proof of nonexistence. A switch-chain sampler is not automatically uniform over the fiber: mixing, irreducibility under additional restrictions, and acceptance bias require analysis. If sampling only qualifying invalid graphs, specify the proposal, rejection rule, seed commitment, and intervention-distance distribution before model outcomes.

## Statistical and causal consequences

Eligibility based on the existence of an invalid graph differs from eligibility under a chosen intervention policy q_i. A global-eligible item may have effectively zero probability of selection by a local-switch policy. Report both denominators, and do not generalize the local-switch estimand to all global-eligible templates. Intervention distance (number of changed edges), number of invalid edges, and graph plausibility can affect responses; preregister them as descriptive covariates and possible effect modifiers, not post-hoc selection criteria.

## Adversarial test plan (not executed)

1. Singleton fiber: prove ineligible rather than claim timeout.
2. All admissible edges: nontrivial fiber but proven semantically ineligible.
3. One valid two-switch with an inadmissible crossed edge: eligible-local positive certificate.
4. Distinct both-valid two-switch: negative-control graph, not a positive certificate.
5. Candidate with source-degree drift or target-degree drift: reject.
6. Candidate containing a duplicate or unregistered edge: reject.
7. Search budget exhausted without witness: UNKNOWN_TIMEOUT, not PROVEN_INELIGIBLE.
8. Cross-stratum switch: reject even if pooled degrees happen to match.
9. Modified evidence text with unchanged edges: reject as non-provenance confound.
10. Construct or search for a finite graph where L=0 and G=1; until independently verified, this remains a proposed stress test, not an observed counterexample.

## Falsification and publication gate

If a primary analysis excludes UNKNOWN_TIMEOUT as though those templates were proven ineligible, the selection analysis is invalid. If the intervention sampler preferentially selects stronger semantic corruptions after observing model responses, the preregistered causal comparison is invalid. If no independently anchored adjudication, $0-only cloud eligibility verification, and independent held-out evaluation exist, publish a methods/pre-registration note rather than an empirical effectiveness or novelty claim.

## Prior art and integrity

Fixed-degree bipartite graph switching, exact contingency-table enumeration, and Markov-chain sampling are established mathematical techniques. The certificate design is a project-specific engineering specification, not a claimed new theorem. Relevant foundational literature to inspect in full before claiming a distinct contribution includes Diaconis and Sturmfels (1998), *Algebraic algorithms for sampling from conditional distributions*, and Ryser (1957), *Combinatorial properties of matrices of zeros and ones*. These citations are research leads, not a completed full-text audit.

No model inference, training, simulations, cloud jobs, local laptop workloads, or paid resources were used to create this design note. All empirical claims remain pending.
