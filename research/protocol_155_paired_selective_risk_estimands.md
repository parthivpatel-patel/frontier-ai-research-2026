# Protocol 155 — Paired selective-risk estimands and non-inferiority gates (9 November 2026)

Status: mathematical experimental specification; no model runs, statistical findings, or novelty claim.

## Why Protocol 154 needs another control

A comparison at matched *aggregate* return rate is insufficient when the two methods return answers on different examples. A method can appear more accurate simply by selecting easier examples. In addition, a method that improves conditional accuracy may lower the total number of correct responses. Pre-register both quantities and evaluate the same held-out cases.

For fixed held-out cases i=1,...,n, define S_{mi}=1 if method m returns a usable answer and Y_{mi}=1 if that returned answer is correct under a frozen, independently specified adjudication rule; set S_{mi}Y_{mi}=0 on abstention. Then

- Return rate: r_m = n^{-1} sum_i S_{mi}.
- Selective accuracy: a_m = sum_i S_{mi}Y_{mi} / sum_i S_{mi}, undefined when no answers are returned.
- Unconditional correct-answer yield: u_m = n^{-1} sum_i S_{mi}Y_{mi} = r_m a_m when r_m > 0.
- Selective error: e_m = 1-a_m, conditional on return.
- Incorrect-answer rate over all cases: b_m = n^{-1} sum_i S_{mi}(1-Y_{mi}).

These are different estimands. Abstention is neither an incorrect answer nor a correct one; report b_m and 1-r_m alongside u_m. For numeric confidence intervals, replace Y with an indicator that the interval covers a prespecified true parameter; do not conflate interval coverage with factual-answer correctness.

## Matched random abstention control

Fix a baseline's answers and their correctness before drawing random abstentions. If an independent random mask selects exactly k of n cases uniformly without replacement, expected correct-answer yield is (k/n) times the baseline's original unconditional correctness, and expected selective accuracy equals the baseline's original accuracy (when the baseline answered every case). These are design expectations, not empirical measurements. Use multiple prespecified random-mask seeds, not a favorable mask chosen after inspection.

If the baseline itself abstains, restrict random masking to its returned cases and separately report the induced total return rate. Never compare a mask of all n cases with a mask of only the baseline's accepted subset as though they were equivalent.

## Paired statistical analysis

For two frozen systems A and B on the same n independent test *units*, define d_i = S_{Ai}Y_{Ai} - S_{Bi}Y_{Bi}; estimate yield difference as mean(d_i). Construct uncertainty using paired units; do not treat the two systems' samples as independent. If prompts are paraphrases or multiple interventions from one physics problem, the independent unit is the underlying problem or physics-family cluster, not each paraphrase. Use a prespecified cluster bootstrap or an appropriate cluster-robust alternative, with enough independent clusters to support inference. Report uncertainty on both yield and return-rate difference. Do not bootstrap individual model tokens, inner resampling draws, or correlated paraphrases as independent examples.

At matched observed return rates, also compare selective errors on the *same returned intersection* as a diagnostic, while retaining the primary whole-population yield comparison. Intersection conditioning changes the population and must not replace the primary estimand.

## Preregistered falsification and safety gates

1. Reject an unconditional-reliability improvement claim if the paired yield difference is not positive under the prespecified uncertainty criterion.
2. Reject a useful selective-risk improvement claim if conditional error only improves through reduced return rate without a favorable risk–coverage curve.
3. Reject a physics-generalization claim if effects vanish on untouched physics families or perturbations that preserve physical meaning.
4. Reject a language-robustness claim if results fail under independently written semantic paraphrases or leakage-resistant splits.
5. Reject a calibration claim if the nominal coverage target is missed beyond the prespecified tolerance, accounting for abstentions.
6. Reject a novelty claim if primary literature already establishes a substantially equivalent approach.
7. Report null, negative, undefined, and failed-run outcomes without selective deletion.

## Minimal reproducible cloud plan

First run the existing standard-library Protocol 153 unit tests in a hosted runner **only after** verifying account-specific zero-cost execution, billing settings, remaining minutes, and current runner availability. Next freeze an evaluation manifest with problem IDs, family IDs, paraphrase grouping, answer keys, acceptance policy, seeds, model versions, and a manifest digest. Execute tiny deterministic reference cases before model inference. The full experiment requires independently validated physics tasks and a frozen NLP scoring rubric; these are not yet available as validated experimental results.

## Closest methodological precedents to compare

Selective classification/risk–coverage (Geifman and El-Yaniv, 2017); conformal prediction and risk control (Angelopoulos and Bates, 2023, and subsequent conformal risk-control work); process and outcome verification for reasoning (Lightman et al., 2023); and clustered resampling for dependent observations. These are literature comparison targets, not a completed novelty review. The proposed estimands and matched controls are standard statistical design principles, not new theorems.

## Resource and publication boundary

No compute was launched in preparing this protocol. Do not infer GitHub Actions free availability from repository visibility; verify actual account billing and quota before dispatch. Strict $0 spending, cloud-only compute, no laptop-heavy workloads, no unverified novelty, no fabricated results, and accurate disclosure of assistance remain mandatory. November 22 is an internal target conditional on evidence.
