# Presentation: Evaluating Simulated Human Fidelity
---

## Slide 1: Evaluation Approach
**Building a Business-Ready Hybrid Evaluation Framework**

- **The Challenge:** Open-ended consumer responses cannot be evaluated with standard computational metrics (e.g., word overlap). Humans naturally paraphrase and adopt conversational tones, while simulated LLMs skew toward polished "marketing speech."
- **Our Methodology:** Adopted the core finding of *Generative Agent Simulations (Park et al., 2024)*—measuring individual-level fidelity—via a multi-layered LLM-as-a-Judge approach.
  1. **Answer Fidelity:** Extracts concrete consumer preference structures (Brands, Reasons, Sizes) over pure lexical strings.
  2. **Tone & Style Fidelity:** Identifies and penalizes verbal polish and artificial certainty.
  3. **Cross-Question Consistency (Separate Diagnostic):** Ensures the core "consumer persona" is preserved across diverse interactions. Reported separately from the headline fidelity score.
- **The Process:** 30 pairs parsed through parallel OpenAI GPT-4o extractions, order-swapped debiasing (to prevent generic favorability), and mapped to an explicit 100-point rubric.

---

## Slide 2: What We Found
**Directionally Sound, but Structurally "Over-Authored"**

- **Fidelity Scoreboard (43.8/100, weighted from five rubric dimensions):**
  - **Factual Alignment:** *Weak-to-Fair.* Broad intent matches, but explicit preferences miss.
  - **Specificity Calibration:** *Poor.* The AI frequently invents detailed constraints.
  - **Tone & Persona Match:** *Poor.* Over-polished and overly articulate responses.

- **Illustrative "Simulation Drifts":**
  1. **Invented Specificity:** *Human* says, "I want a big glass bottle." | *AI* simulates, "I prefer a 250-300 ml glass bottle with a pump dispenser."
  2. **Preference Distortion:** *Human* states they buy whatever gets the job done and are affordable. | *AI* claims they stick to "simple, effective," and value "non-harmful ingredients."
  3. **Rationale Shift:** *Human* admits they "don't know brands." | *AI* generates a fully cohesive reason about transparency and ethical sourcing. 

---

## Slide 3: Recommendations for Management
**Deploying Simulations with Confidence**

- **Immediate Value:** The current agent framework successfully captures general purchasing avenues and category aversions. It is highly capable for **Directional Exploration** (e.g. testing the resonance of a broad campaign or strategy).
- **The Risks of "High-Res" Blindness:** Using these agents to determine precise brand loyalty or specific packaging dimensions will yield false positives heavily skewed toward sustainability, organic ingredients, and high eloquence. 
- **Strategic Fixes for the Simulation Pipeline:**
  1. **Implement RAG-like "Constraint Memories":** Force the LLM simulation to only generate claims mapped securely to past interactions.
  2. **Calibrate the Persona Profile:** Do not just pass "demographics" or "shopping history" into an agent. Explicitly pass "Hedging," "Skepticism," and "Apathy" traits.
  3. **Tone-Tuning Layer:** Run simulations through a secondary debiasing filter designed to reduce "brand ambassador" vernacular into simple human text.
