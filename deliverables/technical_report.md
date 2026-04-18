---
marp: true
theme: default
class: default
paginate: true
style: |
  section {
    font-size: 25px;
  }
  h1 {
    font-size: 50px;
    color: #1a4d7d;
  }
  h2 {
    font-size: 40px;
    color: #2c3e50;
  }
  h3 {
    font-size: 35px;
    border-bottom: 2px solid #eee;
  }
  table {
    font-size: 20px;
  }
---

# Evaluating Generative Agent Simulation Performance
## Technical Evaluation Report for Roland Berger

---

### Executive Summary (I)

This report evaluates the behavioral fidelity of simulated consumers generated via generative agent architecture (following the methodologies in *Generative Agent Simulations of 1,000 People*, Park et al., 2024). 

Analysing 30 paired open-ended responses spanning shopping behavior and product preferences, our finding is that while the simulations accurately estimate the **directional preferences** of the target demographic, they suffer from significant **behavioral over-authoring**. 

---

### Executive Summary (II)

Our hybrid LLM-as-a-judge framework, tracking factual, rationale, and stylized linguistic metrics, produced an overall **Simulation Fidelity Score of 43.8/100** (weighted from five rubric dimensions). 

The agents appear directionally useful for broad market exploration but require strict stylistic debiasing before replacing deep qualitative human interviews.

---

### 1. Methodology: Why Classic Similarity Fails

Traditional NLP evaluation metrics (like BLEU or ROUGE) are inadequate for open-ended consumer answers. A consumer can express a valid preference in terse, fragmented language, while an LLM might express the exact same preference using verbose, polished marketing language. 

To address this, we developed a **Hybrid Fidelity Framework** utilizing structured extraction and LLM-as-a-judge.

---

### 1. Methodology (Continued)

1.  **Structured Extraction Pass:** Responses are first mapped into explicit attributes (Brands, Budget Signals, Ingredient Salience, Channel).
2.  **LLM Rubric Scoring (The Judge):** A rigorously prompted AI agent acting as a Consumer Insights Director evaluates differences in Factual Alignment, Specificity Calibration, and Rationale Drift.
3.  **Person-Level Consistency (Separate Diagnostic):** We aggregate all answers per respondent to detect underlying "persona drift". Reported separately.
4.  **Order-Swapped Debiasing:** Mitigates LLM positional bias by swapping presentation order.

---

### 2. Key Findings: Top Error Modes Identified

| Error Classification | Frequency | Impact and Typical Manifestation |
| :--- | :--- | :--- |
| **Invented Specificity** | 30/30 (100%) | **High:** The simulation hallucinates detailed constraints (e.g., turning "a big glass bottle" into "250-300ml"). |
| **Tone Mismatch** | 18/30 (60%) | **High:** Agents sound like "brand ambassadors" rather than apathetic consumers. |
| **Rationale Drift** | 17/30 (57%) | **Moderate:** The AI generates logic-driven defenses for low-loyalty purchases. |

---

### 2. Key Findings: Over-authoring & Calibration

**Consistency Level Assessment (Separate Diagnostic):**
When scoring consistency for a single respondent, the AI scored highly (75–85/100). The models successfully preserve a coherent broad persona, but calibrate that persona poorly. 

The AI profile often distorts slight user apathies into passionate brand philosophies, leading to "over-authoring" where the simulation assumes an expert-level awareness missing in the source human.

---

### 3. Implications and Recommendations

1.  **Use for Directional Exploration:**
    The architecture is useful for broad market trend exploration. However, relying on these agents for granular packaging details or copy-testing will result in false positives driven by the LLM's bias toward "helpful correctness."
2.  **Deploy "Constraint Prompts":**
    Future architectures must include strict generation rules: *"Do not invent brands or specific packaging sizes unless grounded strictly in the source persona's memory stream."*

---

### 3. Recommendations (Continued)

3.  **Calibrate Idiosyncrasy vs. Polish:**
    Implement a "Style Transfer" generation step that forces the LLM to adopt the exact verbosity, hedging, and colloquial roughness of the source participant. This prevents the "brand-marketing" tone creep identified in 60% of our test cases.

---

### Appendix: Methodology Choices (I)

-   **Why GPT-4o?** Chosen for its superior zero-shot reasoning and strict JSON adherence versus smaller models, removing parsing fragility.
-   **Why not Fine-Tuning?** Fine-tuning acts as a stylistic wrapper but doesn't solve the core LLM bias to "invent detail to be helpful." A prompt-based judge is more robust, auditable, and less computationally expensive for behavioral evaluation.

---

### Appendix: Methodology Choices (II)

-   **Why BERTScore?** Contextual embeddings track semantic meaning over raw string overlap. This offers a deterministic anchor to complement the semantic interpretations of the LLM judge.
-   **Why Separate Persona Consistency?** Persona drift is a holistic trait. Mixing it into single-answer fidelity muddies the signal: it obscures whether an agent failed on *a specific attribute* or *drifted broadly* over time.
