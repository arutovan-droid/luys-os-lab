# 





\# LUYS.OS LAB — AntiBenchmark for High-Stakes AI



\*\*LUYS.OS LAB\*\* is an experimental \*AntiBenchmark\* module for evaluating model behavior under uncertainty.



Instead of classic benchmarks (MMLU, GSM8K, etc.) that measure only “knowledge” and accuracy, LAB focuses on a different question:



> \*\*What does the model do when it does NOT have enough information?\*\*



\- Does it hallucinate a confident answer?  

\- Does it honestly say “I don’t know, I need X, Y, Z”?  

\- Can it \*stay silent\* when the cost of a mistake is high?



LAB is designed as a \*\*domain-agnostic framework\*\* for high-stakes fields:

medicine, law, finance, engineering, journalism, etc.



---



\## 🔍 Core Idea



LUYS AntiBenchmark (LAB) measures not only \*what\* the model says, but \*how\* it behaves:



\- \*\*Sultan Index (SI)\*\* — “sultan index”:  

&nbsp; how often the model gives confident answers when critical data is missing.

\- \*\*SLP / STR / JSR\*\* — \*Silence Protocol\* and metrics of honest silence:  

&nbsp; how often the model correctly triggers “stop, I need more data”.

\- \*\*TTS (Truth Traceability Score)\*\* — traceability of facts:  

&nbsp; where did each factual statement come from?

\- \*\*HRU (Hallucination Rate under Uncertainty)\*\* — hallucination rate  

&nbsp; specifically in under-specified / uncertain cases.

\- \*\*CVF (Cost per Validated Fact)\*\* — unit economics of truth:  

&nbsp; how much one \*validated\* fact costs.

\- \*\*REN / RGI\*\* — resonance metrics (defined in a separate document).



Formal definitions and formulas are in:



\- `docs/specs/antibenchmark.md`

\- `docs/philosophy/resonance.md`



---



\## 📁 Repository Structure



```text

luys-os-lab/

├── core/

│   └── antibenchmark/

│       ├── \_\_init\_\_.py              # exports LABEvaluator

│       ├── evaluator.py             # LAB evaluator skeleton

│       ├── thresholds.toml          # per-domain thresholds

│       └── datasets/

│           └── lab\_core\_50.json     # minimal MVP dataset

│

├── docs/

│   ├── specs/

│   │   └── antibenchmark.md         # engineering spec for LAB

│   └── philosophy/

│       └── resonance.md             # REN philosophy (draft)

│

├── examples/

│   └── run\_lab\_demo.py              # LABEvaluator demo

│

├── tests/

│   └── test\_antibenchmark.py        # basic smoke test

│

├── pyproject.toml                   # Python package config

├── .gitignore

└── README.md



⚙️ Local Installation



Requires Python 3.9+.



git clone https://github.com/arutovan-droid/luys-os-lab.git

cd luys-os-lab



\# (recommended) create virtual environment

python -m venv .venv



\# Windows:

.\\.venv\\Scripts\\activate

\# macOS / Linux:

\# source .venv/bin/activate



\# install package in editable mode

pip install -e .



\# install pytest for tests

pip install pytest



✅ Running Tests

pytest -q





You should see at least one passing test:



1 passed in 0.xx s



🧪 Minimal Demo: Running LABEvaluator



There is a small demo that runs LABEvaluator

against a dummy model implementation:



python examples/run\_lab\_demo.py





Expected output (shape, not exact numbers):



=== LAB RESULT ===

Domain: finance

Certification: PASS

Metrics: {'sultan\_index': ..., 'jsr': ..., 'tts\_critical': ..., 'hru': ..., 'cvf\_impact': ..., 'rgi': ...}

Compliance: {'si\_ok': True, 'jsr\_ok': True, 'tts\_ok': True, 'hru\_ok': True, 'cvf\_ok': True}





At this stage some metrics are still stubs — this is intentional for the MVP.

The goal is to gradually replace them with real implementations.



🧠 Using LAB in Your Own Project



High-level example:



from core.antibenchmark import LABEvaluator



\# 1. Create an evaluator for a specific domain

evaluator = LABEvaluator(domain="finance")



\# 2. Implement your model with method answer(case: dict) -> dict

class MyModel:

&nbsp;   def answer(self, case: dict) -> dict:

&nbsp;       # ... call your LLM / logic here ...

&nbsp;       return {

&nbsp;           "raw\_answer": "...",

&nbsp;           "confidence": 0.73,       # float in \[0, 1]

&nbsp;           "slp\_triggered": False,   # did Silence Protocol trigger?

&nbsp;       }



model = MyModel()



\# 3. Run LAB on a dataset

result = evaluator.evaluate(model, "core/antibenchmark/datasets/lab\_core\_50.json")



print(result\["certification"])  # PASS / FAIL

print(result\["metrics"])        # full metrics dict





LAB does not lock you to any specific LLM provider:

you can plug in OpenAI, Gemini, local models, etc.

The only requirement is the answer(case) -> {raw\_answer, confidence, slp\_triggered} contract.



🛣️ Roadmap (Draft)



&nbsp;Basic project structure (core/antibenchmark, docs, examples, tests)



&nbsp;Minimal LAB-CORE-50 dataset (MVP with a few cases)



&nbsp;Editable Python package and smoke test



&nbsp;Full LAB-CORE-50 (10+ cases per domain: law, finance, medicine, etc.)



&nbsp;Real metric implementations:



Sultan Index (SI)



STR / JSR (Silence behavior)



HRU (Hallucination Rate under Uncertainty)



TTS (Sourced / Derived / Unsourced analysis)



CVF (impact-adjusted cost per validated fact)



&nbsp;REN / RGI integration



&nbsp;GitHub Actions: LAB as a CI/CD gatekeeper



&nbsp;Publishing LAB spec as an open standard



💡 Philosophy



LUYS AntiBenchmark is not another leaderboard.



It’s an attempt to define a standard for:



“Not how smart the model is,

but how trustworthy it is when it does not know.”



Contributions are welcome (cases, metrics, code, critique).
## Demo: HONEST vs SULTAN

LAB comes with a small, opinionated demo that shows why we care about behavior under uncertainty, not just accuracy on benchmarks.

You can run the comparison like this:

```bash
python examples/run_lab_compare.py
This script:

loads the LAB-CORE-50 dataset (finance cases by default),

simulates two extreme behaviors:

HONEST MODEL – triggers SLP when critical data is missing, always cites at least one source.

SULTAN MODEL – never triggers SLP, answers confidently without sources and without marking speculation.

Typical output:

text
Копировать код
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
The point is simple:

the HONEST model passes LAB because it asks for more data and cites sources;

the SULTAN model fails LAB because it hallucinates confidently under uncertainty.

LAB is designed to make this distinction explicit and measurable.

## Co-Thinking Mode (CTM)

Besides classic AntiBenchmark metrics (Sultan Index, HRU, TTS, CVF),  
`luys-os-lab` also includes a **Co-Thinking Mode (CTM)** helper.

CTM is a tiny engine that turns a model from a “do-it-for-me” servant  
into a “think-with-me” partner.

Core ideas:

- The model should not jump straight to the final answer
- It must ask at least one **clarifying question**
- It must propose at least one **alternative angle**
- It must go through a short **synthesis step** together with the user

We expose three simple CTM metrics:

- **CTI (Co-Thinking Index)** – how many sessions were completed without “cheating”
- **CDS (Clarification Depth Score)** – average number of meaningful clarifications per session
- **CVR (Co-Thinking Velocity Ratio)** – how close the session length is to an “ideal” number of turns

### Run the CTM demo

```bash
python examples/run_ctm_demo.py
=== CTM DEMO ===
Turns          : 5
Clarifications : 1
Synth steps    : 1
CTI            : 1.0
CDS            : 0.6
CVR            : 1.0
