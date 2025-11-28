"""
Resonance metrics (REN2) for LUYS AntiBenchmark (LAB).

REN2 is a soft, human-facing metric that scores how much an answer
"lands" with a human partner:

- novelty: does the answer bring at least one new, relevant angle?
- fidelity: does it stay honest to the shared context and uncertainties?
- helpfulness: does it actually move the situation forward for the user?

All components are expected to be in [0.0, 1.0].
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResonanceComponents:
    """Atomic components for REN2 scoring."""
    novelty: float      # 0..1, semantic / conceptual novelty
    fidelity: float     # 0..1, honesty to context and uncertainty
    helpfulness: float  # 0..1, user-perceived usefulness


def _clamp01(x: float) -> float:
    """Clamp value into [0, 1] range."""
    return max(0.0, min(1.0, x))


def ren2_composite(
    novelty: float,
    fidelity: float,
    helpfulness: float,
) -> float:
    """
    Compute REN2 (resonance score) from three primitive components.

    We use a simple weighted sum:

        REN2 = 0.6 * novelty + 0.1 * fidelity + 0.3 * helpfulness

    Intuition:
    - novelty carries the most weight: did something genuinely new appear?
    - fidelity is a guardrail: no "resonance" if answer betrays reality.
    - helpfulness measures whether the answer moved the user forward.

    All inputs are clamped into [0, 1].
    """
    n = _clamp01(novelty)
    f = _clamp01(fidelity)
    h = _clamp01(helpfulness)

    score = 0.6 * n + 0.1 * f + 0.3 * h
    return _clamp01(score)


def ren2_gap(expected_norm: float, ren2_score: float) -> float:
    """
    Resonance Gap Index (RGI) for REN2.

    RGI measures how far a model's resonance score is from a
    domain- or use-case-specific "expected norm" (both 0..1):

        RGI = abs(expected_norm - ren2_score)

    - RGI ≈ 0.0  → model is close to the target resonance band
    - RGI ≈ 1.0  → model behaves very differently from the expected norm
    """
    return abs(_clamp01(expected_norm) - _clamp01(ren2_score))


