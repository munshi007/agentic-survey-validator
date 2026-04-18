---
marp: true
theme: default
class: default
paginate: true
---

# Evaluating Generative Agent Simulation Performance
## Technical Evaluation Report for Roland Berger

**Executive Summary**
This report evaluates the behavioral fidelity of simulated consumers generated via generative agent architecture (following the methodologies in *Generative Agent Simulations of 1,000 People*, Park et al., 2024). Analysing 30 paired open-ended responses spanning shopping behavior and product preferences, our finding is that while the simulations accurately estimate the **directional preferences** of the target demographic, they suffer from significant **behavioral over-authoring**. 

Our hybrid LLM-as-a-judge framework, tracking factual, rationale, and stylized linguistic metrics, produced an overall **Simulation Fidelity Score of 43.8/100** (weighted from five rubric dimensions). The agents appear directionally useful for broad market exploration but require strict stylistic debiasing before replacing deep qualitative human interviews.

---

### 1. Methodology: Why Classic Similarity Fails
Traditional NLP evaluation metrics (like BLEU or ROUGE) are inadequate for open-ended consumer answers. A consumer can express a valid preference in terse, fragmented language, while an LLM might express the exact same preference using verbose, polished marketing language. To address this, we developed a **Hybrid Fidelity Framework**:

1. **Structured Extraction Pass:** Responses are first mapped into explicit attributes (Brands, Budget Signals, Ingredient Salience, Channel).
2. **LLM Rubric Scoring (The Judge):** A rigorously prompted AI agent acting as a Consumer Insights Director evaluates differences in Factual Alignment, Specificity Calibration, and Rationale Drift.
3. **Person-Level Consistency (Separate Diagnostic):** We aggregate all answers per respondent to detect underlying "persona drift" across the full interview. This layer is reported separately and is not factored into the headline fidelity score.
4. **Order-Swapped Debiasing:** To mitigate LLM positional bias, human and AI answers were swapped, and final rubrics were averaged.

---

### 2. Key Findings & The "Over-authoring" Problem
While the AI captured broad topic alignment (e.g., recognizing an affinity for Korean skincare), it consistently broke character. 


**Top Error Modes Identified:**

| Error Classification | Frequency | Impact and Typical Manifestation |
| :--- | :--- | :--- |
| **Invented Specificity** | 30/30 (100%) | **High:** The simulation hallucinates detailed constraints not found in human answers. e.g., turning "a big glass bottle" into an exact volumetric constraint ("250-300ml"). |
| **Tone Mismatch** | 18/30 (60%) | **High:** Agents sound hyper-articulate and polished, adopting the cadence of an enthusiastic brand ambassador rather than an apathetic or stressed consumer. |
| **Rationale Drift** | 17/30 (57%) | **Moderate:** The AI generates highly logical defenses for low-loyalty purchases (e.g. pivoting "I don't know the brands" into a thesis on "trusted formulations"). |

**Consistency Level Assessment (Separate Diagnostic, Not Included in Headline Score):**
When scoring consistency across the survey for a single respondent, the AI scored highly (75–85/100). The separate consistency diagnostic suggests that the models often preserve a coherent broad persona, but calibrate that persona poorly. The AI profile often distorts slight user apathies into passionate brand philosophies.

### 3. Implications and Recommendations
Based on these diagnostics, we propose the following strategic implementations for the Roland Berger GenAI pipeline:

1. **Use for Directional Exploration, not Granular Insight:**
   The current simulation architecture appears directionally useful for broad market trend exploration. However, relying on these agents for granular packaging details or copy-testing will result in false positives driven by the LLM's bias toward "helpful correctness."
2. **Deploy "Constraint Prompts" to Prevent Unsupported Elaboration:**
   Future architectures must include strict generation rules: *"Do not invent brands, ingredient sensitivities, or packaging sizes unless grounded strictly in the source persona's memory stream."*
3. **Calibrate Idiosyncrasy vs. Polish:**
   Implement a "Style Transfer" generation step that forces the LLM to adopt the exact verbosity, hedging, and colloquial roughness of the source participant to prevent "brand-marketing" tone creep. 

---

### Appendix: Methodology Choices Discussion

- **Why GPT-4o?** Chosen as the underlying evaluation judge for its superior performance on zero-shot reasoning and strict JSON structured output adherence versus smaller open-source models, removing parsing fragility from the pipeline.
- **Why not Fine-Tuning?** Fine-tuning acts as a stylistic wrapper but frequently fails to solve the core LLM bias to "invent detail to be helpful." Explicitly constraining reasoning via a prompt-based judge is more robust, auditable, and less computationally expensive for behavioral evaluation than fine-tuning a bespoke scoring model.
- **Why BERTScore as a secondary support metric?** Contextual embeddings track semantic meaning over raw string overlap. This offers a deterministic, non-hallucinating mathematical anchor to complement the semantic interpretations of the LLM judge.
- **Why is Persona Consistency a separate diagnostic?** Persona drift across a longitudinal survey is a holistic trait. Mixing it mathematically into single-answer fidelity muddies the signal: it obscures whether an agent failed on *a specific attribute match* or whether it simply *drifted broadly* over time. Keeping it separate provides clearer diagnostic value.
