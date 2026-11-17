# Protocol 135 — Randomized minimax and empirical-evidence gate

Status: mathematical research specification; no experiments executed; no novelty or performance claim. 2026-11-17.

## Why this is needed

Protocols 129–134 enumerate 144 deterministic sequential policies for two heterogeneous binary verifiers. A deterministic minimax optimum is not necessarily optimal among randomized policies. Publishing a claim of optimal robust verification without testing mixed strategies would be unjustified.

## Formal problem

Let P be the 144 policies and C the four feasible extreme dependence configurations, computed independently for the true and false states. For each policy p and corner c define the exact-rational expected loss L[p,c], including asymmetric false-accept / false-reject losses, abstention and *conditional* second-verifier acquisition fees.

A randomized policy is a probability vector x over P. Solve

    minimize t
    subject to sum_p x[p] L[p,c] <= t for every c in C
               sum_p x[p] = 1
               x[p] >= 0 for all p.

Compare its objective with the deterministic benchmark min_p max_c L[p,c]. The mixed optimum cannot be worse, but strict improvement is a hypothesis, not a guaranteed result.

Dual diagnostic: find a distribution y over C maximizing min_p sum_c y[c] L[p,c]. Strong duality should hold for the finite zero-sum game. Primal/dual objective agreement and nonnegative weights are required checks. For an independently known toy matrix [[0,1],[1,0]], deterministic minimax loss is 1 and randomized minimax loss is 1/2; this is an algorithmic sanity check, not an AI result.

## Important distinctions

- Randomization occurs over **complete, nonanticipatory policies**, before evidence is observed. It must not access an unseen second-verifier response.
- The adversary chooses a conditional dependence model in the prespecified uncertainty set, not a different model after observing each realized policy draw. Otherwise the game changes.
- A shared random seed and full policy-mixture weights are necessary for reproduction.
- Corner sufficiency follows from affine expected risk over the rectangular dependence set; test it on off-diagonal interior grid points as well.
- The 144-policy class assumes two binary verifier outputs, three terminal actions and optional one-time acquisition. Do not extrapolate it to arbitrary LLM agents or longer verification chains.

## Independent implementation acceptance

1. Build L twice using distinct probability enumeration paths; compare every cell exactly against Protocol 134.
2. Solve the finite LP using a pinned, license-compatible package only after confirming a genuinely zero-charge hosted runner. If no package is available, retain the specification without claiming an executed result.
3. Verify simplex constraints, corner constraints, primal-dual gap within declared solver tolerance, deterministic upper bound, and the 2x2 toy case.
4. Test sensitivity to asymmetric costs, prior, verifier marginal accuracies, dependence interval widths, and acquisition fee. Preserve exact-rational input matrices even if the LP solver uses floats.
5. Save commit SHA, runner OS/image, package versions, full logs, RNG seeds, and a hash of each output artifact.

## Empirical novelty and falsification gate

The paper's candidate contribution is an **evaluated combination** of dependence-robust sequential verification, calibrated acquisition and source-disjoint cross-domain tests; it is *not* the Fréchet bounds, finite minimax LP, selective prediction, or value of information individually.

Prior-art audit must directly compare at least: selective prediction / classification with reject option (Chow, 1970); conformal risk control (Angelopoulos et al., 2024); self-consistency reasoning (Wang et al., 2023); SelfCheckGPT (Manakul et al., 2023); chain-of-verification (Dhuliawala et al., 2024); and verifier-guided reasoning / process supervision (Lightman et al., 2023). Confirm exact bibliographic metadata and any closer 2025–2026 work before claiming novelty. This is a **candidate reading list**, not a completed exhaustive literature review.

Pre-register datasets with independent ground truth for NLP factuality, math and physics reasoning; stratify by domain, difficulty and verifier pair. Keep calibration, policy-selection and held-out test examples disjoint by source/problem family. Compare: no verification, single verifier, always acquire, deterministic sequential, randomized sequential, calibrated selective prediction, and matched-budget self-consistency. Measure false-accept risk, abstention, second-verifier calls, token/compute cost and worst-domain outcomes; report confidence intervals with paired bootstrap clustered by source and multiple-comparison correction.

Falsify any claim of advantage if held-out gains disappear against matched-budget baselines, depend on shared-source leakage, reverse across domains, vanish under reasonable cost or dependence sensitivity, or are smaller than uncertainty intervals. Report negative outcomes and do not reinterpret synthetic probability results as observed model behavior.

## Compute and safety gate

No laptop training, inference, large downloads or simulations. Before *any* cloud run, verify current free-tier quota, actual account eligibility, card/billing requirements, storage/egress conditions, runner-minute allowance and whether automatic charges can occur. Never activate paid billing or incur costs without explicit approval. Until verified, work is limited to source inspection, mathematical analysis and publication of non-executed protocols.

## Publication gate

The November 22, 2026 date is a conditional internal checkpoint. Do not submit a performance paper without executed CI evidence, traceable empirical measurements, source-disjoint evaluation, complete prior-art review, limitations, and accurate AI-assistance disclosures.
