# External model-output and licensing feasibility audit — 2026-11-02

**Decision:** **Do not ingest or redistribute** the newly inspected external repository as a baseline until rights and relevant outputs are clarified. Metadata inspection only; no dataset, weights, or binaries downloaded.

## Candidate: Danso et al., *Syntax Is Easy, Semantics Is Hard: Evaluating LLMs for LTL Translation* (ACM SecDev 2026)
- Paper DOI: https://doi.org/10.1145/3805773.3806005
- Public repository: https://github.com/ochowdhu/NL2LTL-SecDev26
- Default branch at inspection: `main-branch`. Public, GitHub reports read access.
- Repository README describes six tasks, including NL2FutureLTL, and claims datasets, prompts, code and experiment outputs. It uses GPT, Claude and Gemini model families in its original experiments; **we did not run any of these models**.
- The small `input_data/nl2ltl_finalized.csv` file is present (39,432 bytes). Its header is `Natural Language,Ground Truth,Atomic Proposition`. Sampled rows contain natural-language instructions and LTL formulas, **not model predictions**. Authorship, independence and reference adjudication are not yet established.
- The visible `output_data/minimal` tree has only a `wff` subfolder; `output_data/detailed` has `wff` and `nl2pl`; `output_data/python` contains no experiment-output files in the inspected listing. The detailed NL2PL result file is one byte. **No released NL2FutureLTL prediction output was located in these paths**. This is an observation about the inspected repository tree, not proof that no output exists elsewhere or in external archives.
- A `wff_raw_results.csv` file exists (1,251 bytes) with model names and raw well-formedness judgments; these are **not NL-to-LTL generated formula predictions** suitable for our proposed translation-error experiment.
- **License conflict:** README advertises **CC BY-NC-ND 4.0**, while repository root `LICENSE` is **GNU GPL v3**. Scope of each license over code, dataset and outputs is not clear from the inspected metadata. Neither label is permission to assume unrestricted redistribution of modified benchmark data. Do not copy data into our public repository or release derivatives until scope and rights are clarified.
- The README includes examples of API-key configuration. **No credentials were accessed or used**, and no paid API calls are planned.

## Scientific feasibility conclusion
This source is valuable **prior art** for evaluating LLM syntax versus semantics, but it does not yet provide a verified, lawful, ready-to-use, source-disjoint collection of released NL2FutureLTL model predictions. We should not claim that such predictions are available merely because a README describes experiments. It also strengthens the novelty collision: syntactic-versus-semantic LTL evaluation is already a substantial research topic.

## Next non-billable checks
1. Search other explicitly linked archival supplements or author-provided repositories for model prediction files, without downloading large artifacts.
2. Confirm applicable dataset license and whether the authors permit independent noncommercial evaluation and publication of aggregate results.
3. Audit source authorship, exact duplicate/paraphrase clusters, and model outputs **before** using the dataset for generalization.
4. If none of the above can be resolved, keep this as a literature comparator only and look for another openly licensed dataset with real model outputs.

## Research integrity
This was metadata/short-text inspection through the public GitHub interface, not model inference or an experimental replication. No local laptop compute, no external compute charges, no downloads, no paid services. No findings about OpenAI/Anthropic/Google model quality are asserted.
