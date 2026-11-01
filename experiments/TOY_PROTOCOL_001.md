# Toy protocol 001: observational agreement versus intervention failure

**Status:** pre-registered deterministic sanity check. Not a paper result, not an original contribution, not evidence about actual LLMs.

## Physical system and abstraction

One-dimensional position x in [0,1], velocity v, controllable impulse a, one-step time increment 1, at most one wall reflection.

Let z = x + v + a. Ground truth is T(x,v,a) = z if 0 <= z <= 1; 2-z if z>1; and -z if z<0. Candidate abstraction omits the wall: A(x,v,a)=z.

For the regime z>1, the error is |A-T| = 2(z-1). For 0<=z<=1 the two models agree exactly. This is an elementary identity, not a novel theorem.

## Decision witness

Initial x=0.9, v=0.2, available impulses a in {-0.2, 0, +0.2}, and objective minimize (x_next - 0.7)^2. The wall-omitting abstraction selects -0.2, while the true system prefers +0.2. Regret under the true dynamics is 0.04 (squared-position units). This is a deliberately constructed witness, not a population estimate.

## Sampling and expected checks

Three proposal regimes (256 independent seeded draws each, seed 20261101):
- ordinary: x in [0.25,0.65], v in [-0.08,0.08], a in [-0.05,0.05]. No impacts are possible.
- uniform: x in [0.1,0.9], v in [-0.2,0.2], a in [-0.1,0.1]. Some impacts are possible.
- boundary: x in [0.88,0.98], v in [0.14,0.28], a in [0,0.08]. All draws impact the right wall.

Metrics: mean absolute one-step error, fraction of draws with error > 1e-12, maximum absolute error, and single constructed decision regret.

**Selection-bias warning:** The boundary regime is intentionally enriched for failure cases; it must not be used to claim improved population detection performance over random sampling. Future method comparisons require matched query budgets, pre-specified test distributions, independent seeds, and held-out physics families.

## Reproduce in cloud

Use the standard public-repository GitHub Actions workflow `toy-falsification.yml`. It runs Python standard-library tests and prints the JSON sanity check to the job log, with no downloaded models, paid services, external packages, or stored artifacts. The workflow may be triggered by pushing code or manually.

Equivalent commands inside the cloud runner:

```bash
python -m unittest discover -s tests -v
python -m src.toy_falsification --count 256 --seed 20261101
```

No local laptop execution is requested.

## Novelty gate

Prior work already studies rare pivotal transition errors, planning regret, intervention-aware world models, and multimodal physical misalignment. This toy example is ONLY a correctness scaffold for future research, not an argument that the gap is new.
