# Free-cloud execution gate — 2026-11-21

Status: feasibility assessment, **not** experimental results or approval to spend.

## Verified provider rules (official documentation, checked 2026-11-21)

1. GitHub Actions standard GitHub-hosted runners are free for **public** repositories. This does not extend to larger runners or imply unlimited usage. Source: https://docs.github.com/en/actions/concepts/billing-and-usage . Use standard `ubuntu-latest` only, with bounded timeout and concurrency. Confirm the repository is public, the workflow is enabled, and the specific run is accepted before claiming usable capacity.
2. Hugging Face lists CPU Basic at $0/hour, **but creating a new Gradio or Docker compute Space requires a paid plan**; static Spaces remain free. Thus the zero hourly price does not establish that a new compute Space is accessible to this project without subscription. Sources: https://huggingface.co/docs/hub/spaces-overview and https://huggingface.co/docs/huggingface_hub/main/guides/manage-spaces .
3. Hugging Face GPU upgrades require a payment method and prepaid credits or a community grant; not approved for this project. Source: https://huggingface.co/docs/huggingface_hub/main/guides/manage-spaces . An awarded free grant could be reconsidered only after verifying its terms and availability.

No provider-specific account entitlements, card status, or remaining quota have been verified. Do not provision or upgrade resources based solely on advertised pricing.

## Executable zero-spend plan

**Stage A — CI and deterministic data checks (standard public GitHub-hosted runner only):**
- Run unit tests, type/format checks, schema validation, timestamp chronology checks, and contamination/leakage checks.
- Pin Python and dependency versions, data hashes and random seeds. Use a hard job timeout, fail-fast and a single concurrency group. Do not enable paid larger runners or external APIs.
- Produce machine-readable provenance and aggregate test reports; do not imply that passing tests establishes the research hypothesis.

**Stage B — small public-data pilot, only after source licensing and provenance are verified:**
- Curate independently adjudicated, temporally indexed examples from each of NLP, mathematics and physics, retaining source-family IDs and original evidence timestamps.
- For mathematics and physics, distinguish source publication/update chronology from problem-solving time: timestamps must be causally meaningful, not synthetic labels added after the fact.
- Freeze calibration thresholds before opening the held-out domain; evaluate temporal, strong non-temporal and timestamp-shuffled controls on identical examples. Match actual token, latency and compute costs, not token budgets alone.
- Cluster uncertainty by independent source family; include leave-one-family-out sensitivity and coverage noninferiority. Declare no result when data are insufficient.

**Stage C — model inference:** blocked until a genuinely accessible, card-free, no-charge hosted inference or GPU allocation is confirmed. Standard GitHub Actions is appropriate for bounded CI, not assumed to be a general free GPU service. Never offload this to the user's laptop.

## Falsification and publication gates

A temporal-specific claim fails if shuffled timestamps perform comparably, if improvement disappears against a strong non-temporal baseline, if family-cluster uncertainty is inconclusive, if chronology leaks labels, or if cost/coverage constraints are violated. A cross-domain claim additionally fails if transfer is not supported in the prespecified domains. Do not equate a null result with a failed project: it can support an accurately labeled negative or methods report.

Before publication, complete a systematic nearest-prior-art table, preregistration and disclosure of AI assistance; publish code/data only where redistribution rights permit. November 22 is a conditional checkpoint, not a scientific evidence deadline.
