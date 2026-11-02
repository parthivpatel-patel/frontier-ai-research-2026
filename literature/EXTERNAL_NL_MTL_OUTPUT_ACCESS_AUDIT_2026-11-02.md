# External NL-to-MTL output access and rights audit — 2026-11-02

**Status: candidate found; NOT cleared as an independent semantic ground truth or redistribution source.** This is an access/provenance review, not a model-accuracy result.

## New candidate: Barrientos, Winter and Rinderle-Ma, NL2MTL (EDOC 2024 / published February 6, 2025)

- Paper: *Automatic Extraction and Formalization of Temporal Requirements from Text: A Survey*, DOI https://doi.org/10.1007/978-3-031-78338-8_14 ; institutional bibliographic record https://research.tue.nl/en/publications/automatic-extraction-andformalization-oftemporal-requirements-fro/ .
- Public upstream repository: https://github.com/marisol-barrientos/nl2mtl ; reviewed `main` commit `c8cd92f7f46da57848cf9f6af494219f8683d1b3`.
- Inspected `data/input`: **four named input text files**, `article_78.txt`, `article_80.txt`, `cara_pump_requirements.txt`, `harvesting_process.txt`.
- Inspected `data/test_1/output` through `data/test_5/output`: each contains four paired `.json` and `.html` output files. This gives **20 visible JSON output files**, grouped as five tests per input document. The same source text is reused across tests: **four documents, not 20 independent source documents**. Individual extracted requirement counts have not been exhaustively checked.
- The JSON samples contain `context`, `MTL_expressions`, `propositions`, `assumptions`, `ambiguities`, and `MTL_expression` fields. A single input can yield a variable number of formulas across tests; therefore one-to-one alignment of predicted formulas cannot be assumed. No strict model correctness or equivalence score is established.
- `config.json` sets `model_name: "gpt-4"` and a placeholder API key; `src/main.py` calls a GPT-4 handler. This supports an **upstream-attributed GPT-4 pipeline**, but does **not authenticate** the historical model identity, generation conditions, or the origin of each stored output. Do not claim independent GPT-4 provenance.
- GitHub repository metadata reports `GPL-3.0`, and a GPLv3 `LICENSE` exists. This is evidence for the repository's software licensing; **do not assume every source document, model output, survey dataset or third-party input has unencumbered redistribution rights**. In particular, legal texts and reused external materials may have distinct rights. We did not copy any input/output text into our repository.
- There is **no independent human-intent adjudication** or physical model annotation in the inspected artifacts. It is MTL, not necessarily the LTL offset family in our current toy code.

**Scientific disposition:** promising source for a later *read-only, aggregate-only* schema and ambiguity/provenance audit if file-level rights are clarified. It is insufficient for the preregistered >=30 independently authored requirements until the individual requirements, provenance, rights and independent adjudication are established. Do not equate five test folders with five source authors or twenty independent requirements.

## Additional relevant prior art, checked November 2, 2026

1. Wang et al., *SCP-NL2TL* (2026-08-05), https://arxiv.org/abs/2608.05439 : back-translation fidelity, repeated-output semantic agreement, selective conformal risk control, OOD screening and abstention on LTL/STL/SpaTiaL. **Disqualifies novelty claims based solely on uncertainty-aware acceptance/abstention or repeat agreement.**
2. Newcomb and Ochoa, *Automatic Translation of Unstructured Requirements into Linear Temporal Logic through Large Language Models* (2026-08-06), https://arxiv.org/abs/2608.06287 : 15 requirements, six models, five generations each, 450 candidates, manual semantic evaluation. **Disqualifies novelty claims based solely on repeated real-model generations and manual checking.**
3. Quansah, Rivas and Bonnah, *VERIFY* (ICLR 2026), https://proceedings.iclr.cc/paper_files/paper/2026/hash/8b078da44614b6e249dc9e9474dc8d11-Abstract-Conference.html : >200k logic/intermediate-language/NL triplets, contextual domains, and verification. **Disqualifies generic multi-domain grounded NL-to-LTL dataset claims.**
4. English et al., *VLTL-Bench* (2025), https://arxiv.org/abs/2507.00877 : grounded state spaces and trace-based verification. **Disqualifies generic trace-grounded model-checking novelty claims.**
5. Barrientos et al. (2025), above: already addresses extraction and formalization from legal/industrial texts with NL2MTL; the present project must not claim that domain coverage alone is new.

## Existing alternative: Danso et al. SecDev 2026

https://github.com/ochowdhu/NL2LTL-SecDev26 at reviewed `main-branch` commit `35b2b28069531f3ca5cea938182f652bacd4922a` has an apparent licensing conflict: GitHub repository metadata/`LICENSE` indicates GPL-3.0, while its README explicitly describes **CC BY-NC-ND 4.0**. We do not treat this as a clear permission to redistribute transformed benchmark or model-output data. Previous inspection did not identify the required matched NL-to-LTL prediction files in the examined output folders. This remains **rights/provenance blocked**.

## Decision and next gate

**No model-accuracy claim or external dataset ingestion yet.** A future cloud-only, pinned read-only audit could inventory the 20 NL2MTL JSON files and report aggregate structure without reproducing source texts; a separate, independent intent-annotation protocol would still be necessary. Before any public reproduction or derived dataset distribution, establish file-specific rights. The source-disjoint evaluation gate remains >=30 independently authored requirements, with independent semantic adjudication and matched baselines. Without this evidence, publish a transparent replication/limitations paper instead of claiming novelty.

## Cost and privacy

No new inference, training, cloud bill, local laptop workload, paid API, credentials, copied external texts, or public redistribution. GitHub's documentation (accessed 2026-11-02), https://docs.github.com/en/billing/concepts/product-billing/github-actions , says standard GitHub-hosted runners on **public** repositories are free; larger runners are billed. The project uses standard `ubuntu-latest`, five-minute timeout, read-only permissions, and no artifact or cache storage.
