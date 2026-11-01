"""Deterministic toy falsification protocol; NOT a novel method or validated research result.

No external dependencies, network access, model training, or local machine requirements.
Run on standard free GitHub-hosted runner for public repositories.
"""
from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class Case:
    position: float
    velocity: float
    impulse: float


def next_position(case: Case, *, wall: bool) -> float:
    """One time step, one elastic reflection maximum at walls x=0 and x=1."""
    y = case.position + case.velocity + case.impulse
    if not wall:
        return y
    if y > 1.0:
        return 2.0 - y
    if y < 0.0:
        return -y
    return y


def sample_cases(regime: str, count: int, seed: int) -> list[Case]:
    if count <= 0:
        raise ValueError("count must be positive")
    rng = random.Random(seed)
    samples = []
    for _ in range(count):
        if regime == "ordinary":
            case = Case(rng.uniform(0.25, 0.65),
                        rng.uniform(-0.08, 0.08),
                        rng.uniform(-0.05, 0.05))
        elif regime == "uniform":
            case = Case(rng.uniform(0.10, 0.90),
                        rng.uniform(-0.20, 0.20),
                        rng.uniform(-0.10, 0.10))
        elif regime == "boundary":
            case = Case(rng.uniform(0.88, 0.98),
                        rng.uniform(0.14, 0.28),
                        rng.uniform(0.0, 0.08))
        else:
            raise ValueError(f"unknown regime: {regime}")
        samples.append(case)
    return samples


def evaluate(regime: str, count: int, seed: int) -> dict:
    cases = sample_cases(regime, count, seed)
    errors = [abs(next_position(c, wall=True) - next_position(c, wall=False))
              for c in cases]
    return {
        "regime": regime,
        "count": count,
        "mean_absolute_error": mean(errors),
        "fraction_disagree": sum(e > 1e-12 for e in errors) / count,
        "max_absolute_error": max(errors),
    }


def decision_witness() -> dict:
    """Illustrative decision mismatch, not an empirical generalization."""
    options = [-0.2, 0.0, 0.2]
    target = 0.7
    cases = [Case(0.9, 0.2, a) for a in options]
    predicted = [next_position(c, wall=False) for c in cases]
    actual = [next_position(c, wall=True) for c in cases]
    predicted_losses = [(x - target) ** 2 for x in predicted]
    actual_losses = [(x - target) ** 2 for x in actual]
    chosen_index = min(range(len(options)), key=lambda i: predicted_losses[i])
    optimal_index = min(range(len(options)), key=lambda i: actual_losses[i])
    return {
        "target": target,
        "actions": options,
        "predicted_positions": predicted,
        "true_positions": actual,
        "selected_action": options[chosen_index],
        "oracle_action": options[optimal_index],
        "selected_true_loss": actual_losses[chosen_index],
        "oracle_true_loss": actual_losses[optimal_index],
        "regret": actual_losses[chosen_index] - actual_losses[optimal_index],
    }


def run(count: int = 256, seed: int = 20261101) -> dict:
    return {
        "status": "synthetic_toy_sanity_check_only",
        "model": "one-dimensional elastic-wall dynamics vs wall-omitting abstraction",
        "seed": seed,
        "evaluations": [evaluate(name, count, seed) for name in
                        ("ordinary", "uniform", "boundary")],
        "decision_witness": decision_witness(),
        "disclaimer": "No learned model, LLM, statistical significance, or novelty claim.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20261101)
    args = parser.parse_args()
    print(json.dumps(run(count=args.count, seed=args.seed), indent=2, sort_keys=True))
