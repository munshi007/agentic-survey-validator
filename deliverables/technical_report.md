---
marp: true
theme: default
class: default
paginate: true
style: |
  section {
    font-size: 21px;
    padding: 30px;
  }
  h1 { font-size: 38px; color: #1a4d7d; margin-bottom: 10px; }
  h2 { font-size: 28px; color: #2c3e50; margin-top: 10px; }
  h3 { font-size: 24px; border-bottom: 1px solid #1a4d7d; margin-top: 5px; }
  table { font-size: 16px; margin-top: 5px; }
  p, li { line-height: 1.3; }
---

# Evaluating Generative Agent Simulation Performance
## Technical Evaluation Report for Roland Berger

**Executive Summary**
This report evaluates the behavioral fidelity of simulated consumers generated via generative agent architecture (per Park et al., 2024). Analysing 30 paired open-ended responses, we find that while simulations accurately estimate **directional preferences**, they suffer from significant **behavioral over-authoring**—inventing details to satisfy the LLM's bias toward "helpful correctness." The agents appear **directionally useful** for broad market exploration but require stylistic debiasing for granular qualitative use.

### 1. Methodology: The Hybrid Fidelity Framework
Standard lexical metrics (BLEU/ROUGE) fail as they ignore semantic intent in favor of word overlap. To address this, we deployed:
- **Structured Extraction:** Mapping raw text to discrete attributes (Brands, Budget, Constraints).
- **LLM-as-a-Judge:** A consumer-insights-tuned evaluator scoring 5 dimensions (Factual, Rationale, Tone, Specificity, Contradiction).
- **Debiasing:** Order-swapped judging averaged to mitigate positional bias.
- **Diagnostics:** Separate "Persona Consistency" layer to track drift across the full interview.

**Fidelity Score: 43.8/100** (Python-weighted average across 30 row pairs)

---

### 2. Key Findings: Top Error Modes Identified
The 43.8 score is driven primarily by consistent "character breaks" where the simulation hallucinates expertise or polish missing in the source human data.

| Error Classification | Freq | Primary Manifestation & Impact |
| :--- | :--- | :--- |
| **Invented Specificity** | 30/30 | **Hallucinating Constraints:** e.g., turning "a big glass bottle" into "250-300ml glass bottle with a pump." |
| **Tone Mismatch** | 18/30 | **Hyper-Articulation:** Agents sound like brand ambassadors/marketers rather than apathetic or stressed consumers. |
| **Rationale Drift** | 17/30 | **Artificial Logic:** Pivot from "I don't know the brands" into a thesis on "trusted formulations and packaging transparency." |

**Consistency Assessment (Advisory):** While the separate diagnostic shows high persona memory (75-85), models struggle with *calibration*, often distorting mild preferences into passionate philosophies.

### 3. Recommendations & Implementation
1. **Scope for Directional Exploration:** Useful for testing high-level campaign resonance. Do not rely on specific packaging/loyalty granularities.
2. **Deploy "Constraint Prompts":** Strictly rule out inventions: *"Do not generate brands/sizes unless grounded in the source memory stream."*
3. **Calibrate Idiosyncrasy:** Implement a Style Transfer layer to force hedging and colloquial roughness, reducing the "marketing speech" pattern observed in many simulated answers.

---
