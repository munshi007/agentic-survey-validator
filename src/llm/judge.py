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
    
    if swap_order:
        prompt = JUDGE_PROMPT_V1.format(
            category=pair.question_category,
            question=pair.question_text,
            human_text=pair.ai_answer,
            human_extracted=ai_extracted.model_dump_json(),
            ai_text=pair.human_answer,
            ai_extracted=human_extracted.model_dump_json(),
            rubric=rubric_str
        )
    else:    
        prompt = JUDGE_PROMPT_V1.format(
            category=pair.question_category,
            question=pair.question_text,
            human_text=pair.human_answer,
            human_extracted=human_extracted.model_dump_json(),
            ai_text=pair.ai_answer,
            ai_extracted=ai_extracted.model_dump_json(),
            rubric=rubric_str
        )

    for attempt in range(MODEL_CONFIG['evaluation']['num_retries']):
        try:
            resp = client.beta.chat.completions.parse(
                model=MODEL_CONFIG['models']['primary_judge'],
                messages=[
                    {"role": "system", "content": "You are a meticulous, zero-tolerance evaluation unit."},
                    {"role": "user", "content": prompt}
                ],
                response_format=PairEvaluation,
                temperature=0.0
            )
            return resp.choices[0].message.parsed
            
        except ValidationError as e:
            logger.warning(f"Judge Validation Error attempt {attempt}: {e}")
            
    raise RuntimeError(f"Failed to judge pair {pair.id} after retries.")
