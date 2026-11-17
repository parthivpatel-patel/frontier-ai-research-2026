# Protocol 144 — Prior-art collision and claim-narrowing audit (2026-11-17)

## Scope and evidence standard
This is a literature-screening memo, not a systematic review or proof of novelty. The current repository's protocols 135–143 specify finite randomized minimax verifier policies, dependence-set sensitivity, and abstention/risk gates. None of the synthetic probability exercises establishes a model-level advance. Only abstracts and selected accessible summaries/papers have been screened here; theorem-level overlap remains to be checked.

## Verified closest literature and collisions

1. Geifman and El-Yaniv, *Selective Classification for Deep Neural Networks* (2017), https://arxiv.org/abs/1705.08500. Reject-option risk/coverage control predates this project. **Collision:** no generic claim to invent selective verification, risk-coverage tradeoffs, or abstention.
2. Geifman and El-Yaniv, *SelectiveNet* (2019), https://arxiv.org/abs/1901.09192. Jointly learns prediction and selection. **Collision:** no generic claim that coupling prediction with a reject decision is novel.
3. Angelopoulos, Bates, Fisch, Lei, Schuster, *Conformal Risk Control* (ICLR 2024), https://proceedings.iclr.cc/paper_files/paper/2024/file/f3549ef9b5ff520a7e41ff3cc306ab2b-Paper-Conference.pdf. Controls expected monotone loss, with discussion of adversarial risk and NLP examples. **Collision:** do not claim first finite-sample risk control or first application to NLP.
4. Xu, Guo, Wei, *Selective Conformal Risk Control* (submitted 2025; revised 2026), https://arxiv.org/abs/2512.12844. Combines selection and conformal risk control. **Collision:** risk-controlled selection alone is not a novel contribution.
5. Yu and Liu, *A Joint Finite-Sample Certificate for Adaptive Selective Conformal Risk Control* (June 2026), https://arxiv.org/abs/2606.08517. Jointly certifies selected risk, acceptance, and utility under adaptive policy selection. **Major collision:** joint certification and utility/coverage gates cannot be asserted as new without exact differentiation.
6. Marcondes e Resende et al., *ReCIRC: Rectified Conformal Risk Control* (September 2026), https://arxiv.org/abs/2609.38112. Studies local-risk adaptation and worst-group risk. **Collision:** heterogeneity-aware calibration is already active prior art.

## Candidate contribution — narrow and provisional
A *task-specific empirical study* of sequential, budget-constrained, potentially correlated verifier ensembles under **explicitly separated adversary-information regimes**, coupled uncertainty sets, and calibrated abstention, across independently sourced NLP, mathematics, and physics tasks. This is a research question, **not** an established new method. Finite zero-sum games, randomized minimax strategies, and adversary-timing distinctions are classical and must not be sold as original mathematics.

## Falsification / stop rules
- If existing selective/conformal or sequential decision methods implement equivalent dependence-aware robust verifier allocation, retract the methodological novelty claim and reframe as replication/benchmark.
- If policy gains vanish against cost-, coverage-, and compute-matched baselines with source-level confidence intervals, report null results.
- If gains occur only on synthetic known probabilities, do not claim real-world verifier reliability.
- If results rely on shared answer sources, duplicated questions, or oracle leakage, invalidate the affected comparison.
- If calibrated guarantees assume exchangeability, known dependence sets, or a hidden policy draw that cannot be justified in deployment, state conditional guarantees only.
- If any domain lacks sufficiently independent ground truth, exclude it from a cross-domain headline claim.
- Do not use 'physics' to imply a physical-law discovery; here physics denotes independently checkable physics problem solving.

## Immediate next actions
1. Full-text theorem-by-theorem overlap table for items 3–6 plus classical robust MDP/POMDP, sequential hypothesis testing, and decision-theoretic value of information.
2. Verify GitHub Actions public-repository allowances, actual account billing settings, and repository workflow permissions **before** enabling fixture execution; public allowance alone is not account-level proof of zero charge.
3. Fix test discovery/import portability on a review branch only after zero-charge verification; record runner SHA, collected count, failures, and provenance.
4. Preregister fixed source-disjoint task splits, human-checkable labels, calibration protocol, verifier costs, random seeds, and primary estimand before looking at held-out outcomes.

## Execution declaration
Literature screening and documentation only. No GitHub Actions run, model inference, downloads, laptop compute, paid API, empirical outcome, or novel theorem. November 22 is a conditional checkpoint.
