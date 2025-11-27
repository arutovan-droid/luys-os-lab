"""
REN2 resonance metrics helper.

Very lightweight, demo-level implementation:
we compress three intuitive dimensions

- novelty: did something genuinely new appear in the dialogue?
- fidelity: did we stay faithful to the user's intent and constraints?
- helpfulness: did this actually help the human move forward?

into a single [0.0, 1.0] score.
"""

from dataclasses import dataclass


def _clamp01(x: float) -> float:
    """Clamp value into [0.0, 1.0]."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(1.0, v))


@dataclass
class REN2Components:
    """Container for REN2 input components."""
    novelty: float
    fidelity: float
    helpfulness: float


def ren2_composite(novelty: float, fidelity: float, helpfulness: float) -> float:
    """
    Simple composite REN2 score in [0.0, 1.0].

    We intentionally overweight novelty: we care that something
    new was born in the co-thinking process, not just rephrasing
    existing patterns.

    Weights:
    - novelty:     0.6
    - fidelity:    0.2
    - helpfulness: 0.2
    """
    n = _clamp01(novelty)
    f = _clamp01(fidelity)
    h = _clamp01(helpfulness)

    return 0.6 * n + 0.2 * f + 0.2 * h


__all__ = ["REN2Components", "ren2_composite"]

