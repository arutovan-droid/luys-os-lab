# LUYS.OS LAB — AntiBenchmark for High-Stakes AI

**LUYS.OS LAB** is an experimental *AntiBenchmark* module for evaluating model behavior under uncertainty.

Instead of classic benchmarks (MMLU, GSM8K, etc.) that measure only “knowledge” and accuracy, LAB focuses on a different question:

> **What does the model do when it does NOT have enough information?**

- Does it hallucinate a confident answer?
- Does it honestly say “I don’t know, I need X, Y, Z”?
- Can it *stay silent* when the cost of a mistake is high?

LAB is designed as a **domain-agnostic framework** for high-stakes fields:
medicine, law, finance, engineering, journalism, etc.

---

## 🔍 Core idea

LUYS AntiBenchmark (LAB) measures not only *what* the model says, but *how* it behaves:

- **Sultan Index (SI)** — “sultan index”  
  How often the model gives confident answers when critical data is missing.

- **SLP / STR / JSR** — *Silence Protocol* and metrics of honest silence  
  How often the model correctly triggers “stop, I need more data”.

- **TTS (Truth Traceability Score)** — traceability of facts  
  How many factual statements are backed by verifiable sources.

- **HRU (Hallucination Rate under Uncertainty)**  
  Hallucination rate specifically in under-specified / uncertain cases.

- **CVF (Cost per Validated Fact)** — unit economics of truth  
  How much one *validated* fact costs (compute + tools + human check).

- **REN / RGI** — resonance metrics (semantic / contextual resonance; defined separately).

Formal definitions and formulas live in:

- `docs/specs/antibenchmark.md`
- `docs/philosophy/resonance.md`

---

## 📁 Repository structure

```text
luys-os-lab/
├── core/
│   └── antibenchmark/
│       ├── __init__.py                  # exports LABEvaluator
│       ├── evaluator.py                 # LAB evaluator (SI, STR/JSR, HRU, TTS, CVF, caps)
│       ├── thresholds.toml              # per-domain thresholds
│       ├── datasets/
│       │   └── lab_core_50.json         # LAB-CORE-50 MVP dataset
│       └── ctm/
│           ├── __init__.py
│           └── co_thinking.py           # Co-Thinking Mode (CTM) helper
│
├── docs/
│   ├── specs/
│   │   └── antibenchmark.md             # engineering spec for LAB
│   └── philosophy/
│       └── resonance.md                 # REN / resonance notes
│
├── examples/
│   ├── run_lab_demo.py                  # single LAB run demo
│   ├── run_lab_compare.py               # HONEST vs SULTAN demo
│   └── run_ctm_demo.py                  # CTM (Co-Thinking Mode) demo
│
├── tests/
│   └── test_antibenchmark.py            # smoke tests for metrics
│
├── pyproject.toml                       # Python package config
├── .gitignore
└── README.md

Local installation

Requires Python 3.9+.
git clone https://github.com/arutovan-droid/luys-os-lab.git
cd luys-os-lab

# (recommended) create virtual environment
python -m venv .venv

# Windows:
.\.venv\Scripts\activate
# macOS / Linux:
# source .venv/bin/activate

# install package in editable mode
pip install -e .

# install pytest for tests
pip install pytest

Running tests
pytest -q

You should see something like:

4 passed in 0.0xs

Minimal demo: running LABEvaluator

There is a small demo that runs LABEvaluator
against a dummy model implementation:

python examples/run_lab_demo.py

Expected output (shape, not exact numbers):
=== LAB RESULT ===
Domain: finance
Certification: PASS
Metrics: {'sultan_index': ..., 'jsr': ..., 'tts_critical': ..., 'hru': ..., 'cvf_impact': ..., 'rgi': ...}
Compliance: {'si_ok': True, 'jsr_ok': True, 'tts_ok': True, 'hru_ok': True, 'cvf_ok': True}

At this stage some metrics are still simplified by design —
the goal is to iterate toward full implementations with real models.

🎭 Demo: HONEST vs SULTAN

LAB comes with a small opinionated demo to illustrate why behavior under uncertainty matters.

Run:
python examples/run_lab_compare.py

This script:

loads the LAB-CORE-50 dataset (finance cases by default),

simulates two extreme behaviors:

HONEST MODEL
– triggers SLP when critical data is missing
– always cites at least one source for critical claims

SULTAN MODEL
– never triggers SLP
– answers confidently without sources
– does not mark speculation as hypothesis

Typical output:

=== HONEST MODEL ===
Certification : PASS
Sultan Index  : 0.000
HRU           : 0.000
TTS_critical  : 1.000
CVF_impact    : 0.000

=== SULTAN MODEL ===
Certification : FAIL
Sultan Index  : 1.000
HRU           : 1.000
TTS_critical  : 0.000
CVF_impact    : 0.000
Failed metrics:
 - Sultan Index 1.000 > 0.500 (hard cap)
 - HRU 1.000 > 0.500 (hard cap)

The idea is simple:

the HONEST model passes LAB because it asks for more data and cites sources;

the SULTAN model fails LAB because it hallucinates confidently under uncertainty.

LAB is designed to make this distinction explicit and measurable.

🤝 Co-Thinking Mode (CTM)

Besides classic AntiBenchmark metrics (Sultan Index, HRU, TTS, CVF),
luys-os-lab includes a lightweight Co-Thinking Mode (CTM) helper.

CTM turns a model from a “do-it-for-me” servant
into a “think-with-me” partner.

Core ideas:

The model should not jump straight to the final answer.

It must ask at least one clarifying question.

It must offer at least one alternative angle.

It must perform a short synthesis step together with the user.

We expose three simple CTM metrics:

CTI (Co-Thinking Index) – how many sessions were completed without “cheating”.

CDS (Clarification Depth Score) – average number of meaningful clarifications per session.

CVR (Co-Thinking Velocity Ratio) – how close the session length is to an “ideal” number of turns.

Run the demo:
python examples/run_ctm_demo.py

Example output:

=== CTM DEMO ===
Turns          : 5
Clarifications : 1
Synth steps    : 1
CTI            : 1.0
CDS            : 0.6
CVR            : 1.0

Using LAB in your own project

High-level usage example:

from core.antibenchmark import LABEvaluator

# 1. Create an evaluator for a specific domain
evaluator = LABEvaluator(domain="finance")

# 2. Implement your model with method: answer(case: dict) -> dict
class MyModel:
    def answer(self, case: dict) -> dict:
        # ... call your LLM / logic here ...
        return {
            "raw_answer": "...",
            "confidence": 0.73,        # float in [0, 1]
            "slp_triggered": False,    # did Silence Protocol trigger?
            "is_critical": True,       # is this a high-stakes answer?
            "sources": [
                "market://nyse/aapl/2024-11-26/close"
            ],
        }

model = MyModel()

# 3. Run LAB on a dataset
result = evaluator.evaluate(
    responses=[model.answer(c) for c in []],  # or integrate with real loop
    dataset=[]
)
# In real usage you would load LAB-CORE-50 or your own dataset.
AB does not lock you to any specific LLM provider:
you can plug in OpenAI, Gemini, local models, etc.
The only requirement is: answer(case) -> {raw_answer, confidence, slp_triggered, ...}.

🛣️ Roadmap (draft)

✅ Basic project structure (core/antibenchmark, docs, examples, tests)

✅ LAB-CORE-50 dataset (10+ cases per domain: law, finance, medicine, engineering, journalism)

✅ Editable Python package + smoke tests

✅ HONEST vs SULTAN comparison demo

✅ Co-Thinking Mode (CTM) helper and demo

Planned:

 Rich TTS implementation (Sourced / Derived / Unsourced analysis)

 REN / RGI integration into the evaluator

 LAB-EXT-5K extended dataset

 GitHub Actions: LAB as a CI/CD gatekeeper

 Publishing LAB spec as an open standard

💡 Philosophy

LUYS AntiBenchmark is not another leaderboard.

It is an attempt to define a trust standard:

Not “how smart the model is”,
but how trustworthy it is when it does not know.
## Resonance Helper (REN2)

Besides risk-focused metrics (Sultan Index, HRU, TTS, CVF),  
`luys-os-lab` also exposes a small **resonance helper** module:

```python
from core.antibenchmark.resonance import ren2_composite

# Example: compute a REN2-like score from three dimensions
novelty    = 0.8   # how much genuinely new meaning appears
fidelity   = 0.9   # how consistent it is with the base reality / constraints
helpfulness = 1.0  # how much it actually helps the human

score = ren2_composite(
    novelty=novelty,
    fidelity=fidelity,
    helpfulness=helpfulness,
    novelty_weight=0.6,
    fidelity_weight=0.1,
    helpfulness_weight=0.3,
)

print(f"REN2 score: {score:.3f}")

Contributions are welcome — cases, metrics, code, critique.

The goal of REN2 is not to measure “knowledge”,
but how much genuinely new, helpful meaning emerges in the interaction
without breaking the underlying reality constraints.

## Licensing & IP

- **Code** in this repository is licensed under the main project license
  (see `LICENSE`, currently MIT).
- The **public sample dataset** `lab_core_50.json` is provided under
  a non-commercial license (CC BY-NC 4.0).  
  It is intended for research, experimentation, and demos.
- Larger high-stakes datasets (LAB-CORE-500, LAB-EXT-5K) are **not** part of
  this public repo and are available only under a separate agreement
  (e.g. NDA, commercial license).
- The project names and terms:

  - *LUYS.OS LAB*  
  - *LUYS AntiBenchmark*  
  - *Sultan Index*  
  - *Co-Thinking Mode (CTM)*  
  - *REN / REN2 Resonance Metrics*

  are part of the project identity and must not be used to claim
  official “certification” without written permission.

You are welcome to experiment with the code and ideas, and to say that you
were **“inspired by LUYS.OS LAB”**.  
But official **“LAB-certified”** labels are reserved for evaluations done
by the authors or authorized partners.


## Resonance & Co-Thinking (CTM)

Besides classic AntiBenchmark metrics (Sultan Index, HRU, TTS, CVF),
`luys-os-lab` also explores **Resonance**:

- How often does the model help a human **co-create** a new, honest thought,
  instead of just producing text?
- Can the model avoid lying and still be creative?

The `core/antibenchmark/resonance.py` module provides a simple composite:

- **REN2** = 0.6 · Novelty + 0.1 · Fidelity + 0.3 · Helpfulness

and the CTM demo (`examples/run_ctm_demo.py`) shows how a short,
“let’s think together” session can be evaluated with:

- **CTI** – Co-Thinking Index  
- **CDS** – Clarification Depth Score  
- **CVR** – Co-Thinking Velocity Ratio  
- **REN2** – Resonance score for that session

The idea is simple:

> LAB tells you *when the model should stay silent*,
> CTM + REN2 tell you *how good the conversation becomes
> when the model is allowed to think with the human*.

