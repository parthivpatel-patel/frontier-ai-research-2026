# Prior-art collision and falsification gate (2026-11-20)

Status: targeted literature audit, not exhaustive systematic review. No empirical discovery is claimed. This note is intended to constrain claims before the November 22 checkpoint.

## Direct collisions

1. Allein et al. (2023), *Implicit Temporal Reasoning for Evidence-Based Fact-Checking*, https://arxiv.org/abs/2302.12569. Temporal alignment and temporal cues already improve evidence-based fact-checking. **Therefore neither temporal verification nor improvements from timestamps are novel by themselves.**
2. Barik et al. (IJCAI 2025), *ChronoFact: Timeline-based Temporal Fact Verification*, https://ijcai.org/proceedings/2025/893. Event-level and time-level timeline verification already exist. **Therefore constructing timelines is not a new mechanism.**
3. Strong and Vlachos (EMNLP 2025), *TSVer: A Benchmark for Fact Verification Against Time-Series Evidence*, https://aclanthology.org/2025.emnlp-main.1519/. Real-world claims and structured numerical time-series evidence are established evaluation territory. **Therefore time-series verification is not new.**
4. Chu et al. (ACL 2024), *TimeBench*, https://aclanthology.org/2024.acl-long.66/; Luo et al. (ACL 2025), *ETRQA*, https://aclanthology.org/2025.findings-acl.1198/; Wei et al. (NeurIPS 2025), *TimE*, https://proceedings.neurips.cc/paper_files/paper/2025/hash/84f1e188c2be52f89f6e206bc37d092d-Abstract-Datasets_and_Benchmarks_Track.html. Temporal reasoning benchmarks and multi-level temporal evaluation are established.
5. Uddin et al. (ACL 2025), *UnSeenTimeQA*, https://aclanthology.org/2025.acl-long.94/. Synthetic scenarios that avoid memorized answers are already an established contamination control.

## Narrower hypothesis worth testing, not claiming as novel

Whether **temporally grounded evidence selection with frozen cross-domain calibration** reduces selective error, compared with strong non-temporal and shuffled-time controls, at matched acceptance coverage and measured resource use, *simultaneously* across NLP, mathematics and physics. The intersection of these conditions is a proposed experimental contribution, not verified novelty. Search for prior selective-prediction, abstention, conformal risk control, retrieval and tool-use papers before asserting distinctiveness. Mathematics/physics need genuine timestamp-sensitive evidence tasks; merely adding dates to timeless questions is not a meaningful cross-domain test.

## Confirmatory falsification gates

- No improvement over a conventional verifier under comparable accepted coverage and matched total compute: reject performance hypothesis.
- Shuffled, reversed or irrelevant timestamps perform similarly: reject evidence for a distinctive temporal mechanism.
- Gain appears only in one domain or disappears under source-family-held-out evaluation: reject robust cross-domain transfer claim.
- Held-out thresholds tuned after seeing outcomes, shared source families between splits, unresolved correctness labels, or hidden cost differences: declare experiment non-confirmatory.
- Gains disappear under time-validity checks, source-publication cutoffs, and answer-contamination controls: reject temporal grounding interpretation.
- A selective error improvement without evidence of mechanistic mediation: report predictive association, not causal mechanism.

## Minimum reproducible evidence package

Versioned question IDs, source-family IDs, timestamp provenance, claim/reference dates, immutable calibration/held-out splits, independent correctness labels, exact verifier outputs, deterministic tie rules, per-arm accepted masks, measured input/output tokens and wall time, frozen analysis script, bootstrap units, all exclusions and negative-control results. Report both per-domain effects and aggregate effects with uncertainty, including unfavorable results.

## Decision at November 22 checkpoint

If these gates lack independent held-out results, release a **methods/preregistration** manuscript with explicit negative-space novelty discussion, not a result paper. A software test suite passing is not evidence for the research hypothesis.

## Research integrity

Disclose AI assistance as required by the publication venue; never represent generated or simulated examples as empirical observations. This note does not establish complete coverage of literature through 2026.
