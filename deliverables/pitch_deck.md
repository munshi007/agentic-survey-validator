---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #fff
style: |
  section {
    font-size: 26px;
  }
  h1 {
    font-size: 45px;
    color: #1a4d7d;
  }
  h2 {
    font-size: 38px;
    color: #2c3e50;
  }
  table {
    font-size: 18px;
  }
---

# Evaluating Simulated Human Fidelity
### An Assessment of Generative Agent Architecture
**Roland Berger Technical Review**

---

## 1. Core Evaluation Approach
**Bridging the gap between Lexical Strings and Consumer Intent**

- **The Challenge:** Open-ended consumer responses are fragmented and colloquial. Standard NLP metrics (BLEU/Word-Overlap) fail to reward valid paraphrasing and penalize AI "brand ambassador" verbosity.
- **Our Solution:** A **Hybrid Fidelity Framework** inspired by Park et al. (2024).
  - **Structured Extraction:** AI answers are parsed into clean preference schemas (Brands, Rationale, Constraints) before comparison.
  - **LLM-as-a-Judge:** A consumer insights "Director" agent scores the pair across 5 dimensions using an explicit 100-point weighted rubric.
  - **Debiasing:** Uses **Order-Swapped** passes to eliminate position bias.
- **Why it works:** It verifies *semantic mapping* rather than string matching.

---

## 2. Findings: Key Simulation Drifts
**Directionally Useful, but Structurally "Over-Authored"**

**Fidelity Score: 43.8/100** *(Weighted average of 30 test pairs)*

| Simulation Drift Mode | Frequency | Mitigation Priority |
| :--- | :--- | :--- |
| **Invented Specificity** | 30/30 (100%) | **High:** Hallucinating exact sizes/brands. |
| **Tone Mismatch** | 18/30 (60%) | **High:** AI sounds too polished/professional. |
| **Rationale Drift** | 17/30 (57%) | **Med:** AI invents ethical defenses for casual buys. |

- **Top Insight:** The simulation is **directionally useful** for capturing broad market trend exploration (e.g. channel preference), but fails at granular loyalty modeling due to the LLM's bias toward "helpful correctness."

---

## 3. Strategic Recommendations
**Deploying Simulations with Confidence**

- **Correct Use-Case:** Use for **broad market exploration** and directional campaign resonance.
- **High-Risk Area:** Avoid using current agents for granular "packaging testing" or "copy testing" where the AI’s over-polished persona will yield false positives.
- **Strategic Fixes for the Pipeline:**
  1. **Constraint Memories:** Anchor all generation to verified persona interactions.
  2. **Trait Calibration:** Pass "Apathy" or "Skepticism" as core prompt parameters.
  3. **Style Transfer Layer:** Apply a secondary filter to down-sample "marketing speech" into realistic human fragmentation/hedging.

---

## Appendix: Methodology Choices

- **GPT-4o Judge:** Chosen for superior zero-shot reasoning and structured output adherence.
- **Prompt-Based Judge vs. Fine-Tuning:** The judge approach is more auditable and robust for behavioral evaluation, whereas fine-tuning often masks hallucinations behind better style.
- **BERTScore Anchor:** Provides a deterministic, mathematical semantic check to complement the qualitative LLM judgment.
- **Persona Consistency Layer:** Tracked as a separate diagnostic (scoring 75–85) to ensure persona stability without polluting the single-answer fidelity metric.
