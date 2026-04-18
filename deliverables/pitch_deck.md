---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #fff
style: |
  h1 { color: #1a4d7d; }
  h2 { color: #2c3e50; }
  section { font-size: 24px; }
  footer { font-size: 15px; }
---

# Evaluating Simulated Human Fidelity
### An Assessment of Generative Agent Architecture
**Roland Berger Technical Review**

---

## 1. The Approach: Hybrid Evaluation Framework
**Why standard metrics (BLEU/ROUGE) fail:** They ignore semantic intent. A human saying "I like glass" is a 100% match for intent to "I prefer glass packaging", but a 0% lexical match.

**Our Business-Ready Solution:**
- **Answer Fidelity:** Extracts preference structures (Brands, Reasons) over strings.
- **Tone Fidelity:** Identifies and penalizes artificial verbal polish.
- **Consistency Diagnostic:** Monitors persona preservation throughout the survey. 
- **Debiasing:** Order-swapped judging (GPT-4o) to remove positional bias.

---

## 2. Findings: Directionally Sound but "Over-Authored"
**Headline Fidelity Score: 43.8/100** (Python-weighted average)

**Top Simulation Drifts Identifed:**
| Issue | Human Target | LLM Simulation |
| :--- | :--- | :--- |
| **Specificity** | *"I want a big glass bottle."* | *"Prefer 250-300ml glass with pump."* |
| **Rationale** | *"I don't know the brands."* | *Passionate defense of transparency.* |
| **Tone** | *"Buy what works/is cheap."* | *"I stick to simple, effective routines."* |

**Audit Trail:** 30/30 rows showed invented specificity; 18/30 showed tone mismatch.

---

## 3. Strategic Recommendations for Management
The agents are **useful for broad market exploration**, but granular packaging or copy-testing will yield false positives driven by the LLM's "helpful correctness" bias.

**Proposed Implementation Fixes:**
- **Constraint Memories:** Anchor all generation strictly to past user memories. 
- **Trait Calibration:** Pass "Apathy" and "Skepticism" scores to prevent over-expertise.
- **Style Filtering:** Apply a secondary filter to reduce "ambassador vernacular" into simple, human-like responses.

*Persona consistency is maintained as a separate advisory diagnostic.*

---

## Appendix: Methodology & Architecture
- **GPT-4o Judge:** Selected for superior zero-shot reasoning and JSON output reliability.
- **Python-Based Weighting:** Final scores are computed deterministically from rubric weights in `configs/rubric.yaml` to prevent LLM scoring hallucinations.
- **BERTScore Inclusion:** Used as a non-hallucinating mathematical anchor to track semantic embedding similarity alongside qualitative judge notes.
- **Consistency Separation:** Keeping consistency separate avoids muddying the signal of whether an agent failed on a *single fact* vs. a *long-term memory*.

---
