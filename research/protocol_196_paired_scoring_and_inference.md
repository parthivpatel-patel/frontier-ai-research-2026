# Protocol 196 — Paired outcome scoring, uncertainty, and decision gates

Date: 2026-11-11. Status: preregistration design only. No model outputs or statistical findings.

## Correction to the Protocol 195 estimand

Let T_i(z)=1 mean the model says the specified provenance relation is **valid**. In the original condition z=0 the relation is adjudicated valid; in the corrupted condition z=1 it is adjudicated invalid. Therefore raw acceptance difference E[T_i(1)-T_i(0)] measures **acceptance shift**, not accuracy change. If Y_i(z) denotes *accuracy against condition-specific labels*, then Y_i(0)=T_i(0) and Y_i(1)=1-T_i(1). These are different estimands and must not be conflated. In particular, a competent detector should have low T(1), high T(0), and high accuracy in both conditions; accuracy difference may be near zero despite excellent discrimination.

Primary diagnostic contrast proposed for preregistration: D=E[T_i(0)-T_i(1)] on the eligible, preselected population. D>0 means less acceptance of corrupted than original support, but is not by itself proof of scientific provenance reasoning. Also report sensitivity Se=P(T(1)=0), specificity Sp=P(T(0)=1), balanced accuracy (Se+Sp)/2, and unconditional abstention rate. If abstentions occur, retain a third response category and report both conservative scoring (abstention not correct) and a clearly labeled conditional answered-only analysis. Never silently exclude abstentions.

## Pairwise table and uncertainty

For each source problem record the 2x2 table of (T(0),T(1)): (1,0) is correct discrimination, (0,1) is reversed discrimination, (1,1) is indiscriminate acceptance, and (0,0) is indiscriminate rejection. D=(n_10-n_01)/N. A paired confidence interval should be computed from problem-level resampling, not by pretending the two conditions are independent. With multiple graph instances/templates per problem, predefine a problem-level average and resample problems as clusters. For a single pair per independent problem, the sample variance of d_i=T_i(0)-T_i(1) yields a transparent standard error sqrt(s_d^2/N); a preregistered percentile cluster bootstrap may be a sensitivity analysis, but report its assumptions and small-N limitations.

The sham contrast D_sham=E[T(original)-T(presentation-sham)] and the valid-reassignment false-alarm contrast must be reported alongside D. A difference D-D_sham alone is not an identified mechanistic effect if the interventions differ in surface salience, complexity, or adjudication uncertainty. Predefine equivalence tolerances and minimum practically important discrimination before data collection; do not choose thresholds after seeing outcomes.

## Randomization and leakage protection

Freeze physics source problems, permitted/admissible edge labels, adjudicator disagreements, graph intervention certificate, prompt versions, model versions, randomization seed, analysis script hash, and exclusion rules before querying. Randomize original/corrupted/sham presentation order within source problem and counterbalance source identifiers. Prevent model response from informing semantic labels. Use separate pilot problems for prompt debugging and never include them in confirmatory estimates. Record any unavailable model/version and failed requests as missing, not negative outcomes.

## Falsification / stop rules

Do not claim provenance-specific scientific reasoning if: D is indistinguishable from sham under preregistered margin; valid-reassignment graphs receive similar invalidity judgments; label agreement is inadequate; identifier permutations reverse conclusions; or the experiment relies on selective exclusions. No model-effect claims until execution logs, frozen labels, complete query inventory, and a public reproducibility package exist. A null or failed-identification result must remain reportable.

## Closest prior art and differentiation questions

- Turpin et al., 2023, *Language Models Don't Always Say What They Think* (https://arxiv.org/abs/2305.04388): counterfactual perturbations and explanation faithfulness. Does the proposed study isolate a different causal object?
- Lightman et al., 2023, *Let's Verify Step by Step* (https://arxiv.org/abs/2305.20050): process supervision. Does provenance-link verification go beyond step correctness?
- Gao et al., 2023, *Enabling Large Language Models to Generate Text with Citations* (https://arxiv.org/abs/2305.14627): citation support evaluation. Are graph constraints and adjudicated physics links genuinely distinct from attribution checking?
- Jacovi and Goldberg, 2020, *Towards Faithfully Interpretable NLP Systems* (https://arxiv.org/abs/2004.03685): faithfulness definitions and causal evidence. Does the intervention support the claimed interpretation?

These are starting references, **not a completed full-text novelty audit**. Before claiming novelty, compare experimental units, intervention granularity, semantic oracle, matched controls, failure cases, and the actual contribution; graph matching and max-flow are established methods.

## Execution and cost status

No test, model inference, cloud runner, or external API was invoked for this document. Before any GitHub Actions dispatch, obtain account-specific evidence of public-repo free eligibility, remaining runner quota, billing/spending guardrails, and runner availability. Published free allowances alone are insufficient. User laptop must remain browser-only. No paid fallback. November 22 remains a conditional manuscript milestone.
