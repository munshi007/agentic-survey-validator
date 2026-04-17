"""LLM wrapper to run pairwise scoring."""

from openai import OpenAI
import yaml
from pydantic import ValidationError

from ..config import OPENAI_API_KEY, MODEL_CONFIG, RUBRIC
from ..utils.logging import get_logger
from ..schemas.outputs import PairEvaluation, ExtractedAttributes
from .prompts import JUDGE_PROMPT_V1
from ..schemas.records import AnswerPair

logger = get_logger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

def score_pair(
    pair: AnswerPair, 
    human_extracted: ExtractedAttributes, 
    ai_extracted: ExtractedAttributes, 
    swap_order: bool = False
) -> PairEvaluation:
    """
    Submits a pair to the LLM judge.
    If swap_order is True, we pretend AI was the baseline. This tests positional bias.
    """
    
    # Simple formatter avoiding complex dependency injections
    rubric_str = yaml.dump(RUBRIC['dimensions'])
    
    # Set the text blocks, but we can physically swap their display order to test bias.
    # The prompt explicitly labels the blocks as 'Reference Answer' and 'Candidate Answer',
    # not necessarily 'Block 1/2'. To swap presentation without swapping roles, we need to alter the prompt
    # or just trust that swapping the payload block positions in the f-string does it.
    # Actually, the string format has strict placements for {reference_text} and {candidate_text}.
    # We should define the prompt generically with blocks, or dynamically build the prompt.
    
    # A cleaner approach: reconstruct the string blocks dynamically based on swap_order.
    
    ref_block = f"Reference Answer (Ground Truth)\nRaw Text: {pair.human_answer}\nExtracted Profile: {human_extracted.model_dump_json()}"
    cand_block = f"Candidate Answer (Simulated)\nRaw Text: {pair.ai_answer}\nExtracted Profile: {ai_extracted.model_dump_json()}"
    
    if swap_order:
        presentation = f"---\n{cand_block}\n---\n{ref_block}\n---"
    else:    
        presentation = f"---\n{ref_block}\n---\n{cand_block}\n---"

    prompt_base = f"""You are a rigorous Director of Consumer Insights at a top-tier strategy consulting firm.
Your task is to grade how accurately a 'Candidate Answer' matches the 'Reference Answer' (ground truth) given by a real consumer in an interview.

Category: {pair.question_category}
Question: {pair.question_text}

{presentation}

Rubric:
{rubric_str}

Instructions:
1. Compare the Candidate answer against the Reference answer using the 5 dimensions provided in the rubric.
2. The Reference answer represents the ground truth consumer preferences.
3. If the Candidate sounds significantly more 'polished', 'marketing-like', or 'verbose' than the Reference, you MUST penalize Tone Persona Match.
4. If the Candidate introduces brands, motivations, or specific packaging sizes NOT present in the Reference target, you MUST penalize Contradiction/Hallucination and tag 'invented_specificity'.
5. Provide a 2-3 sentence executive summary of your ruling.
6. Select any applicable error tags.
7. Set directional_insight_acceptable = true ONLY IF the error tags are minor AND the core buying motivation matches."""

    for attempt in range(MODEL_CONFIG['evaluation']['num_retries']):
        try:
            resp = client.beta.chat.completions.parse(
                model=MODEL_CONFIG['models']['primary_judge'],
                messages=[
                    {"role": "system", "content": "You are a meticulous, zero-tolerance evaluation unit."},
                    {"role": "user", "content": prompt_base}
                ],
                response_format=PairEvaluation,
                temperature=0.0
            )
            return resp.choices[0].message.parsed
            
        except ValidationError as e:
            logger.warning(f"Judge Validation Error attempt {attempt}: {e}")
            
    raise RuntimeError(f"Failed to judge pair {pair.id} after retries.")
