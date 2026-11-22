# Joint-feasibility implementation reconciliation — 2026-11-21

## Evidence and scope
This is a repository inventory check, not a model experiment or an empirical result. At the time of inspection, the GitHub main-branch `research/` directory contained `archival_bounds.py`, `test_archival_bounds.py`, and `PAIRED_ARCHIVAL_JOINT_FEASIBILITY_GATE_2026-11-21.md`, but **no file named `paired_archival_joint_bounds.py`**. A direct request for that proposed path returned HTTP 404. Earlier session descriptions claiming a committed joint-assignment implementation and eight regression tests therefore **must not be treated as verified main-branch artifacts** until their exact paths and commit trees are reconciled. A differently named implementation may exist; this inventory alone does not prove otherwise.

## Release gate
1. Identify the exact purported implementation and test paths from the claimed commit trees; check whether they exist on main, a branch, or only in unreachable history.
2. If missing, implement a dependency-free small-m joint oracle with immutable paired predictions and acceptance flags; enumerate shared labels once, not separately by policy.
3. For each truth assignment, compute both selective risks with fixed denominators; distinguish undefined risks and reject inconsistent input frames.
4. Test identical and opposite predictions, one-sided abstention, zero accepted counts, no unresolved cases, invalid inputs, and conservative-bound containment.
5. Obtain a successful cloud CI run tied to the **exact head SHA** containing both implementation and tests. An older successful workflow run is not evidence for newer files.
6. Verify GitHub-hosted runner eligibility, public-repository policy, quota, and any account-specific billing restrictions before starting additional compute. No self-hosted runner, paid GPU, card enrollment, or local workload.
7. Do not describe the joint oracle as validated, or include its outputs as experimental evidence, before steps 1–6 pass.

## Mathematical guardrail
For fixed accepted predictions and shared unknown binary labels, the paired difference is R_A(y)-R_B(y), with the same y used for both policies. Marginal subtraction is conservative and need not be sharp. Exact enumeration scales as 2^m and is suitable only for deliberately tiny synthetic fixtures. Identification bounds do not substitute for sampling uncertainty or establish AI model improvement.

## Publication decision
The November 22 internal checkpoint is not a deadline to manufacture results. Without a completed novelty comparison and independently adjudicated held-out evidence, release only a clearly labeled methods/preregistration manuscript, if its references and claims are audited; otherwise withhold publication. Disclose AI assistance according to the venue. This document records a verification gap rather than a negative scientific finding.
