"""LLM wrapper to run attribute extraction."""

from openai import OpenAI
from pydantic import ValidationError

from ..config import OPENAI_API_KEY, MODEL_CONFIG
from ..utils.logging import get_logger
from ..schemas.outputs import ExtractedAttributes
from .prompts import EXTRACTION_PROMPT_V1
from ..schemas.records import AnswerPair

logger = get_logger(__name__)

# Reusing a persistent client
client = OpenAI(api_key=OPENAI_API_KEY)

def extract_attributes(answer: str, pair: AnswerPair) -> ExtractedAttributes:
    """Uses Structured Outputs to strictly parse free text."""
    prompt = EXTRACTION_PROMPT_V1.format(
        category=pair.question_category,
        question=pair.question_text,
        answer=answer
    )
    
    retries = MODEL_CONFIG['evaluation']['num_retries']
    model_name = MODEL_CONFIG['models']['extractor']
    
    for attempt in range(retries):
        try:
            response = client.beta.chat.completions.parse(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a precise data extractor. Only output JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format=ExtractedAttributes,
                temperature=0.0
            )
            return response.choices[0].message.parsed
            
        except ValidationError as e:
            logger.warning(f"Validation Error in extraction attempt {attempt}. {e}")
        except Exception as e:
            logger.error(f"Fallback Exception during extract: {e}")
            break
            
    # Absolute fallback to fail gracefully
    logger.error(f"Failed to extract attributes for {answer[:30]} after {retries} retries. Returning empty profile.")
    return ExtractedAttributes(
        preferred_brands=[],
        channel_preference="Unknown",
        packaging_size_preference="Unknown",
        budget_value_signal="Unknown",
        ingredient_salience="Unknown",
        convenience_signal="Unknown",
        decision_criteria=[],
        sentiment_confidence="Unknown",
        quoted_anchors=[]
    )
