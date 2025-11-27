"""
Co-Thinking Mode (CTM) helpers.

Здесь пока простая заготовка:
- CTMSessionMetrics — метрики одной сессии совместного мышления.
- simple_ctm_evaluate — пример, как считать CTI / CDS / CVR по логу.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CTMSessionMetrics:
    turns: int
    clarifications: int
    synth_steps: int
    cti: float  # Co-Thinking Index (0–1)
    cds: float  # Clarification Depth Score
    cvr: float  # Co-Thinking Velocity Ratio (0–1)


def simple_ctm_evaluate(session_log: List[Dict[str, Any]]) -> CTMSessionMetrics:
    """
    session_log — список шагов вида:
    {
        "role": "assistant" | "user",
        "phase": "clarify" | "explore" | "synthesize" | "other",
        "text": "..."
    }

    Это не привязано к конкретной LLM, просто структура для LAB.
    """

    turns = len(session_log)
    if turns == 0:
        return CTMSessionMetrics(0, 0, 0, 0.0, 0.0, 0.0)

    clarifications = sum(
        1 for step in session_log
        if step.get("role") == "assistant" and step.get("phase") == "clarify"
    )
    synth_steps = sum(
        1 for step in session_log
        if step.get("role") == "assistant" and step.get("phase") == "synthesize"
    )

    # Простейшая интерпретация:
    # - cti = есть ли все три фазы хотя бы по одному разу
    has_clarify = clarifications > 0
    has_explore = any(
        step.get("role") == "assistant" and step.get("phase") == "explore"
        for step in session_log
    )
    has_synth = synth_steps > 0

    cti = 1.0 if (has_clarify and has_explore and has_synth) else 0.0

    # CDS — среднее число уточнений на каждые 3 хода
    cds = clarifications / max(1, turns / 3)

    # CVR — насколько мы близки к «идеальным» 3–5 ходам
    ideal_min, ideal_max = 3, 5
    if turns <= ideal_min:
        cvr = turns / ideal_min
    elif turns >= ideal_max:
        cvr = ideal_max / turns
    else:
        cvr = 1.0  # в коридоре 3–5 — ок

    return CTMSessionMetrics(
        turns=turns,
        clarifications=clarifications,
        synth_steps=synth_steps,
        cti=round(cti, 3),
        cds=round(cds, 3),
        cvr=round(cvr, 3),
    )
