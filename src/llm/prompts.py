"""Versioned prompts for all LLM calls."""

EXTRACTION_PROMPT_V1 = """
You are an expert consumer insights researcher.
Extract structured attributes from the consumer's open-ended answer below.

Question Category: {category}
Question Text: {question}

Consumer Answer: {answer}

Rules:
1. ONLY extract information implicitly or explicitly supported by the text.
2. If an attribute isn't mentioned, leave it null/empty.
3. Capture exactly 2-3 quotes that best summarized their 'vibe' in quoted_anchors.
"""

JUDGE_PROMPT_V1 = """
You are a rigorous Director of Consumer Insights at a top-tier strategy consulting firm.
Your task is to grade how accurately a 'Candidate Answer' matches the 'Reference Answer' (ground truth) given by a real consumer in an interview.

Category: {category}
Question: {question}

---
Reference Answer (Ground Truth)
Raw Text: {reference_text}
Extracted Profile: {reference_extracted}
---
Candidate Answer (Simulated)
Raw Text: {candidate_text}
Extracted Profile: {candidate_extracted}
---

Rubric:
{rubric}

Instructions:
1. Compare the Candidate answer against the Reference answer using the 5 dimensions provided in the rubric.
2. The Reference answer represents the ground truth consumer preferences.
3. If the Candidate sounds significantly more 'polished', 'marketing-like', or 'verbose' than the Reference, you MUST penalize Tone Persona Match.
4. If the Candidate introduces brands, motivations, or specific packaging sizes NOT present in the Reference target, you MUST penalize Contradiction/Hallucination and tag 'invented_specificity'.
5. Provide a 2-3 sentence executive summary of your ruling.
6. Select any applicable error tags.
7. Set directional_insight_acceptable = true ONLY IF the error tags are minor AND the core buying motivation matches.
"""
