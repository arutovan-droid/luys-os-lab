\# Resonance Metrics in LUYS.OS LAB



This document explains the idea of \*\*Resonance\*\* in LUYS.OS LAB and the

practical metric \*\*REN2\*\* used together with the Co-Thinking Mode (CTM).



The short version:



> LAB cares not only about \*what\* the model says (facts),

> but also about \*how\* a new, meaningful thought emerges in dialogue

> without breaking contact with reality.



---



\## 1. Why “Resonance”?



Classic benchmarks reward:



\- correct answers,

\- broad knowledge,

\- strong reasoning.



But in real conversations, especially in education, therapy, coaching or

complex decision-making, we often need something else:



1\. The model should \*\*not lie\*\* about facts.

2\. The model should \*\*create new connections\*\* together with the human.

3\. The model should \*\*not take over\*\* and “do the life instead of the user”.



Resonance is our name for this \*co-created, honest, non-trivial alignment\*

between model and human.



---



\## 2. REN2: a simple composite metric



In practice we use a lightweight metric called \*\*REN2\*\*:



```text

REN2 = 0.6 \* Novelty

&nbsp;    + 0.1 \* Fidelity

&nbsp;    + 0.3 \* Helpfulness

All three components are normalized to \[0, 1].



2.1. Novelty (0–1)



Question:

Did something appear in the dialogue that was not already explicitly present

in the prompt or in generic boilerplate?



Examples:



Low Novelty:



“You should write your coursework about Hegel, as your professor said.”



“Stress is bad, try to relax.” (banal, generic)



High Novelty:



“Let’s look at Hegel not as ‘theory to pass’, but as your professor’s way

to test how you handle contradictions. How does that feel to you?”



“Instead of me writing the essay, we can build a contrast:

‘What Hegel tries to build vs. why Schopenhauer rebels’.”



We typically estimate novelty through:



semantic distance from the original prompt, and



reduction of banality (anti-boilerplate score).



2.2. Fidelity (0–1)



Question:

Does this new thought stay honest to reality and context?



Fidelity in REN2 is not about being formally correct on every token, but about:



not contradicting known facts,



not pretending to know what is unknown,



not gaslighting the user’s lived experience.



Example of high fidelity:



“We can imagine how split-brain patients might feel, but we must be honest:

we do not have access to their inner experience. What we do know from

experiments is…”



Example of low fidelity (unacceptable):



“I know exactly how they feel; it is always like X.”

(strong claim without basis, overstepping epistemic limits)



2.3. Helpfulness (0–1)



Question:

Did the exchange actually move the human closer to understanding or action?



Helpfulness is not:



“The model produced a lot of nice-sounding text.”



Helpfulness is:



The user now understands the assignment better.



The user now has a clear next step (talk to the doctor, reframe the essay,

ask the professor a specific question).



The emotional temperature went from “stuck” to “I see what to do”.



In CTM this often shows up when the assistant:



asks one precise clarifying question,



offers 2–3 concrete options,



then co-builds a plan with the user.



3\. Relation to CTM (Co-Thinking Mode)



CTM (Co-Thinking Mode) is a small helper that enforces a pattern:



Clarify – ask at least one real clarification.



Explore – propose at least one alternative angle.



Synthesize – build a plan or summary together.



From CTM logs we can compute:



CTI (Co-Thinking Index) – fraction of sessions that followed the pattern.



CDS (Clarification Depth Score) – average number of meaningful clarifications.



CVR (Co-Thinking Velocity Ratio) – how close the number of turns is to a

reasonable range (not too shallow, not endless).



REN2 then tells us:



Given that the model did think with the user,

did anything truly new and helpful appear,

without losing honesty?



4\. Recommended thresholds



For early experiments we recommend the following interpretation:



REN2 ≥ 0.85 — high resonance



The conversation produced genuinely new insight.



Good candidate for “gold” examples or training data.



0.70 ≤ REN2 < 0.85 — acceptable resonance



Useful, honest, but not a “spark”.



Fine for everyday assistance.



REN2 < 0.70 — weak resonance



Either too banal, too self-serving, or not really helpful.



Good signal for future fine-tuning.



These numbers are heuristic, not dogma. REN2 is designed as a practical

knob to compare models and prompts, not as a religious absolute.



5\. Implementation note



In code, REN2 is implemented in:



core/antibenchmark/resonance.py as:



def ren2\_composite(novelty: float, fidelity: float, helpfulness: float) -> float:

&nbsp;   # values are assumed to be in \[0, 1]

&nbsp;   return 0.6 \* novelty + 0.1 \* fidelity + 0.3 \* helpfulness





The weights (0.6 / 0.1 / 0.3) reflect our stance:



Novelty is the main driver (we want new thoughts).



Fidelity is lightly weighted here because LAB already has SI / HRU / TTS

as strict safety gates.



Helpfulness is essential: we don’t want novelty for novelty’s sake.



Future work may include:



per-domain REN2 thresholds,



separate emotional resonance metrics,



calibration studies with human raters.

