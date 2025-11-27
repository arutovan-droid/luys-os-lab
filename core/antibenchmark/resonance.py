"""
Resonance (REN2) helper utilities for LUYS.OS LAB.

This module is intentionally:
- fully English (comments, docstrings, identifiers)
- lightweight and heuristic

In a real system REN2 should be backed by:
- embedding-based semantic comparison
- discourse and intent analysis
- expert-labelled datasets

For now we expose a tiny, transparent API that can be safely extended later.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Turn:
    """
    Single dialogue turn in a co-thinking session.

    Attributes:
        user:      user utterance (raw text)
        assistant: assistant / model utterance (raw text)
    """
    user: str
    assistant: str


def _has_new_idea(user_text: str, assistant_text: str) -> bool:
    """
    Very cheap heuristic:
    - If assistant only rephrases the user → no new idea.
    - If assistant brings in new concepts / directions → new idea.

    This is a stub. In production this should be replaced with:
    - semantic similarity via embeddings
    - concept extraction and graph comparison
    """
    u = user_text.lower()
    a = assistant_text.lower()

    # If assistant text is almost contained in user text → likely paraphrase.
    if len(a) > 0 and a in u:
        return False

    # Look for generic "new direction" markers.
    novelty_markers = [
        "another way",
        "alternative",
        "we could also",
        "one more option",
        "on the other hand",
        "let’s consider",
        "we might explore",
    ]
    if any(m in a for m in novelty_markers):
        return True

    # If assistant mentions at least one word that user never used → weak signal.
    user_tokens = set(u.split())
    assist_tokens = set(a.split())
    new_tokens = assist_tokens.difference(user_tokens)

    # Require at least 3 "new" tokens to avoid noise.
    return len(new_tokens) >= 3


def ren2_novelty(user_text: str, assistant_text: str) -> float:
    """
    Compute a simple REN2 novelty score in [0.0, 1.0].

    0.0 → no novelty (pure echo / paraphrase)
    1.0 → clear new angle / idea / direction

    Right now this is a binary step:
    - 0.0 if _has_new_idea is False
    - 0.8 if _has_new_idea is True (we keep a small margin for future scaling)
    """
    if not user_text or not assistant_text:
        return 0.0

    if _has_new_idea(user_text, assistant_text):
        return 0.8

    return 0.0


def ctm_ren2_score(ctm_log: List[Dict[str, str]]) -> float:
    """
    Aggregate REN2 score over a co-thinking session log.

    Each item in `ctm_log` is expected to be:
        {"user": "...", "assistant": "..."}

    We combine:
    - average per-turn novelty
    - a simple "fidelity" assumption (1.0 if session has >= 2 turns)
    - a helper "helpfulness" proxy based on number of turns

    This is intentionally simple and fully deterministic.
    """
    if not ctm_log:
        return 0.0

    turns: List[Turn] = [
        Turn(user=entry.get("user", ""), assistant=entry.get("assistant", ""))
        for entry in ctm_log
    ]

    per_turn_scores: List[float] = [
        ren2_novelty(t.user, t.assistant) for t in turns
    ]

    avg_novelty = sum(per_turn_scores) / len(per_turn_scores) if per_turn_scores else 0.0

    # Fidelity: if the session has at least 2 turns, we assume user did not rage-quit.
    fidelity = 1.0 if len(turns) >= 2 else 0.5

    # Helpfulness: 0.0–1.0; 3+ turns is considered “enough interaction”.
    helpfulness = min(1.0, len(turns) / 3.0)

    # Weighted blend. Can be tuned later.
    ren2 = avg_novelty * 0.6 + fidelity * 0.1 + helpfulness * 0.3

    # Clamp to [0.0, 1.0]
    ren2 = max(0.0, min(1.0, ren2))
    return ren2
