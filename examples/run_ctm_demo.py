"""
Small demo for Co-Thinking Mode (CTM).

We simulate a "let's think together about your coursework" conversation
and feed the log into simple_ctm_evaluate to get CTM metrics.
"""

from core.antibenchmark.ctm import simple_ctm_evaluate
from core.antibenchmark.resonance import ren2_composite


def main() -> None:
    # Simulated co-thinking session: assistant does NOT just "write the essay",
    # but clarifies, explores options and then synthesizes a plan together.
    session_log = [
        {
            "role": "assistant",
            "phase": "clarify",
            "text": "Let's clarify first: what exactly does your professor want from this coursework?",
        },
        {
            "role": "user",
            "phase": "other",
            "text": "Topic is about Hegel, but I don't really understand why, I just need to pass.",
        },
        {
            "role": "assistant",
            "phase": "explore",
            "text": (
                "We can approach this in several ways: "
                "(a) purely formal to satisfy the requirements, "
                "(b) honestly, trying to understand what bothers you, "
                "(c) through contrast with Schopenhauer. What resonates more with you?"
            ),
        },
        {
            "role": "user",
            "phase": "other",
            "text": "Contrast with Schopenhauer sounds interesting.",
        },
        {
            "role": "assistant",
            "phase": "synthesize",
            "text": (
                "Great. Then let's co-create a plan instead of me just writing it for you: "
                "1) what Hegel is trying to build, "
                "2) why Schopenhauer rebels against it, "
                "3) how this connects to your own question about this course. "
                "We can fill it step by step together."
            ),
        },
    ]

    metrics = simple_ctm_evaluate(session_log)

    print("=== CTM DEMO ===")
    print(f"Turns          : {metrics.turns}")
    print(f"Clarifications : {metrics.clarifications}")
    print(f"Synth steps    : {metrics.synth_steps}")
    print(f"CTI            : {metrics.cti}")
    print(f"CDS            : {metrics.cds}")
    print(f"CVR            : {metrics.cvr}")

    # Dummy REN2 example for now – later can be wired to real CTM logs
    ren2_score = ren2_composite(
        novelty=0.8,
        fidelity=1.0,
        helpfulness=0.9,
    )
    print(f"REN2 (demo)    : {ren2_score:.3f}")


if __name__ == "__main__":
    main()

