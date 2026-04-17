# Evaluating Generative Agent Simulation Performance
## Technical Evaluation Report for Roland Berger

**Executive Summary**
This report evaluates the behavioral fidelity of simulated consumers generated via generative agent architecture (following the methodologies in *Generative Agent Simulations of 1,000 People*, Park et al., 2024). Analysing 30 paired open-ended responses spanning shopping behavior and product preferences, our finding is that while the simulations accurately estimate the **directional preferences** of the target demographic, they suffer from significant **behavioral over-authoring**. 

Our hybrid LLM-as-a-judge framework, tracking factual, rationale, and stylized linguistic metrics, produced an overall **Simulation Fidelity Score of 43.8/100** (weighted from five rubric dimensions). The agents are highly reliable for broad market trend aggregation but require strict stylistic debiasing before replacing deep qualitative human interviews.

---

### 1. Methodology: Why Classic Similarity Fails
Traditional NLP evaluation metrics (like BLEU or ROUGE) are inadequate for open-ended consumer answers. A consumer can express a valid preference in terse, fragmented language, while an LLM might express the exact same preference using verbose, polished marketing language. To address this, we developed a **Hybrid Fidelity Framework**:

1. **Structured Extraction Pass:** Responses are first mapped into explicit attributes (Brands, Budget Signals, Ingredient Salience, Channel).
2. **LLM Rubric Scoring (The Judge):** A rigorously prompted AI agent acting as a Consumer Insights Director evaluates differences in Factual Alignment, Specificity Calibration, and Rationale Drift.
3. **Person-Level Consistency (Separate Diagnostic):** We aggregate all answers per respondent to detect underlying "persona drift" across the full interview. This layer is reported separately and is not factored into the headline fidelity score.
4. **Order-Swapped Debiasing:** To mitigate LLM positional bias, human and AI answers were swapped, and final rubrics were averaged.

### 2. Key Findings & The "Over-authoring" Problem
While the AI captured broad topic alignment (e.g., recognizing an affinity for Korean skincare), it consistently broke character. 

**Top Error Modes Observed:**
- **Invented Specificity (100% of rows exhibited this):** The simulation frequently appended detailed constraints not found in human answers. For instance, when a human vaguely expressed a desire for a "big glass bottle", the AI hallucinated an exact volumetric constraint ("250-300ml"). 
- **Tone Mismatch (66% of rows):** Simulated respondents sound hyper-articulate and polished, adopting the cadence of a brand ambassador rather than a stressed business professional.
- **Rationale Drift (60% of rows):** When human respondents noted they "don't really know the brands," indicating low brand loyalty, the AI generated a highly-logic driven rationale defending its product choices based on "sustainable packaging" or "trusted formulations."

**Consistency Level Assessment (Separate Diagnostic, Not Included in Headline Score):**
When scoring consistency across the survey for a single respondent, the AI scored highly (75–85/100). The models successfully remember what persona they are emulating. The failure mode resides not in memory, but in *calibration*. The AI profile often distorts slight user apathies into passionate brand philosophies.

### 3. Implications and Recommendations
Based on these diagnostics, we propose the following strategic implementations for the Roland Berger GenAI pipeline:

1. **Use for Directional Exploration, not Granular Insight:**
   The current simulation architecture is exceptionally useful for rapid, top-down strategy hypothesis testing. However, relying on these agents for granular packaging details or copy-testing will result in false positives driven by the LLM's bias toward "helpful correctness."
2. **Deploy "Constraint Prompts" to Prevent Unsupported Elaboration:**
   Future architectures must include strict generation rules: *"Do not invent brands, ingredient sensitivities, or packaging sizes unless grounded strictly in the source persona's memory stream."*
3. **Calibrate Idiosyncrasy vs. Polish:**
   Implement a "Style Transfer" generation step that forces the LLM to adopt the exact verbosity, hedging, and colloquial roughness of the source participant to prevent "brand-marketing" tone creep. 
