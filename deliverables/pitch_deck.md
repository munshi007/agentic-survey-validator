---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #fff
---

# Evaluating Simulated Human Fidelity
### An Assessment of Generative Agent Architecture
**Roland Berger Technical Review**

---

## 1. The Evaluation Challenge

**Why standard metrics fail for open-ended consumer responses:**

*   **Humans:** Use fragmented language, hedge, and paraphrase.
*   **LLM Simulations:** Default to polished, verbose "marketing speech."
*   **Classic NLP (e.g., BLEU):** Fails because it measures exactly matched words, not intent.

**Our Hybrid Solution:** We adopted Park et al. (2024)'s methodology but adapted it for unstructured text using an LLM-as-a-Judge combined with structured extraction.

---

## 2. Methodology: A Multi-Layered Approach

1.  **Structured Extraction:** Parse messy paragraphs into clean variables (Brands, Budget, Constraints).
2.  **Rubric-Based Judging:** Evaluated across 5 strict dimensions (Factual, Rationale, Tone, Specificity, Contradiction).
3.  **Order-Swapped Debiasing:** Mitigates the "Position 1 Bias" of LLM judges by swapping presentation order while preserving ground-truth mapping.
4.  **Cross-Question Consistency:** A separate diagnostic measuring how well the persona limits drift across the entire interview. *(Not mixed into the headline score).*

---

## 3. What We Found

**Directionally Sound, but Structurally "Over-Authored"**

**Fidelity Scoreboard (43.8/100, weighted):**
*   **Factual Alignment:** *Weak-to-Fair.* General topic intent matches, but exact preferences diverge.
*   **Specificity Calibration:** *Poor.* AI regularly invents constraints.
*   **Tone & Persona Match:** *Poor.* Artificially hyper-articulate.

**Quantifying the Errors:**
*   Invented Specificity: **30/30 rows**
*   Tone Mismatch: **18/30 rows**
*   Rationale Drift: **17/30 rows**

---

## 4. Illustrative "Simulation Drifts"

| Metric | Human Target | LLM Simulation |
| :--- | :--- | :--- |
| **Invented Specificity** | *"I want a big glass bottle."* | *"I prefer a 250-300 ml glass bottle with a pump dispenser."* |
| **Rationale Shift** | *"I don't really know the brands."* | *Passionate defense of transparency and ethical sourcing.* |
| **Tone Mismatch** | *"Buy whatever gets the job done and is affordable."* | *"I stick to simple, effective routines with non-harmful ingredients."* |

---

## 5. Strategic Recommendations

**How to deploy simulations with confidence:**

1.  **Immediate Value:** The current agent framework is useful for **directional exploration** (e.g., testing the broad resonance of a campaign).
2.  **High-Risk Blindness:** Using these agents to determine precise brand loyalty or specific packaging dimensions yields false positives skewed toward sustainability and high eloquence.
3.  **Pipeline Fixes:**
    *   **Constraint Memories:** Force generation mapped securely to past interactions.
    *   **Calibrate Traits:** Pass negative traits like "Skepticism" or "Apathy."
    *   **Style Transfer:** Apply a debiasing layer to downgrade "ambassador vernacular."

---

## Appendix: Methodology Choices

*   **Why GPT-4o?** Chosen as the judge for its superior performance on zero-shot reasoning and JSON output adherence versus smaller open models.
*   **Why not Fine-Tuning?** Fine-tuning acts as a stylistic wrapper but doesn't solve the core LLM bias to "invent detail to be helpful." Explicitly constraining reasoning via a judge is more robust for evaluation.
*   **Why BERTScore as a secondary support metric?** Contextual embeddings track semantic meaning over raw string overlap, offering a deterministic non-hallucinating mathematical anchor to complement the LLM judge.
*   **Why is Consistency a separate diagnostic?** Persona drift across a survey is a holistic trait. Mixing it into single-answer fidelity mathematically muddies whether an agent failed on *this specific answer* or *drifted broadly*.

