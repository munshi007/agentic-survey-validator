# Evaluating Generative Agent Simulation Performance
## Technical Evaluation Report for Roland Berger

**Executive Summary**
This report evaluates the behavioral fidelity of simulated consumers generated via generative agent architecture (following the methodologies in *Generative Agent Simulations of 1,000 People*, Park et al., 2024). Analysing 30 paired open-ended responses spanning shopping behavior and product preferences, our finding is that while the simulations accurately estimate the **directional preferences** of the target demographic, they suffer from significant **behavioral over-authoring**. 

Our hybrid LLM-as-a-judge framework produced an overall **Simulation Fidelity Score of 43.8/100** (weighted from five rubric dimensions). The agents appear **directionally useful for broad market exploration** but require strict stylistic debiasing before replacing deep qualitative human interviews.

---

### 1. Methodology: Why Classic Similarity Fails
Traditional NLP evaluation metrics (like BLEU or ROUGE) are inadequate for open-ended consumer answers. A consumer can express a valid preference in terse, fragmented language, while an LLM might express the exact same preference using verbose marketing language. To address this, we developed a **Hybrid Fidelity Framework**:

1.  **Structured Extraction Pass:** Responses are first mapped into explicit attributes (Preferred Brands, Budget Signals, Channel Preference, Decision Criteria) to bypass lexical "noise."
2.  **LLM Rubric Scoring (The Judge):** A rigorously prompted AI agent acting as a Consumer Insights Director evaluates differences in Factual Alignment, Specificity Calibration, and Rationale Drift.
3.  **Order-Swapped Debiasing:** To mitigate LLM positional bias, human and AI answers were swapped, and final rubrics were averaged.
4.  **Person-Level Consistency (Separate Diagnostic):** We aggregate answers per respondent to detect underlying "persona drift." This is reported separately and is **not factored** into the headline fidelity score.

---

### 2. Key Findings: The "Over-authoring" Problem
While the AI captured broad topic alignment (e.g., preference for Korean skincare), it consistently "broke character" by being too helpful and too specific.

**Top Error Modes Identified:**

| Error Classification | Frequency | Impact and Typical Manifestation |
| :--- | :--- | :--- |
| **Invented Specificity** | 30/30 (100%) | **High:** Simulation hallucinates detailed constraints (e.g., turning "a big glass bottle" into "250-300ml"). |
| **Tone Mismatch** | 18/30 (60%) | **High:** Agents sound hyper-articulate and polished, adopting a brand ambassador cadence rather than a consumer tone. |
| **Rationale Drift** | 17/30 (57%) | **Moderate:** The AI generates highly logical defenses for low-loyalty or accidental purchases. |

**Consistency Level Assessment:**
The separate consistency diagnostic suggests models preserve a coherent broad persona (scoring 75–85/100), but calibrate that persona poorly. The AI profile often distorts slight user apathies into passionate brand philosophies.

---

### 3. Implications and Recommendations
Based on these diagnostics, we propose the following strategic implementations:

1.  **Use for Directional Exploration:** The architecture is useful for broad trend exploration. However, relying on these agents for granular packaging details or copy-testing will result in false positives driven by the LLM's bias toward "helpful correctness."
2.  **Deploy "Constraint Prompts":** Future architectures must include strict generation rules: *"Do not invent brands or packaging sizes unless grounded strictly in the source persona description."*
3.  **Calibrate Idiosyncrasy vs. Polish:** Implement a "Style Transfer" generation step that forces the LLM to adopt the exact verbosity and colloquial roughness of the source participant to prevent "marketing speech" creep.

---

### Appendix: Methodology Choices
- **Why GPT-4o?** Chosen as the judge for superior zero-shot reasoning and strict JSON structured output adherence versus smaller models.
- **Why not Fine-Tuning?** Fine-tuning acts as a stylistic wrapper but doesn't solve the core LLM bias to "invent detail." Explicitly constraining reasoning via a judge is more robust and auditable for behavioral evaluation.
- **Why BERTScore?** Contextual embeddings track semantic meaning over raw string overlap, offering a mathematical anchor to complement the LLM judge.
