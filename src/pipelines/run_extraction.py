"""Pipeline script to run extraction against parsed records."""

from typing import List
from ..schemas.records import AnswerPair
from ..llm.extraction import extract_attributes
from ..utils.logging import get_logger

logger = get_logger(__name__)

def run_extraction_pass(records: List[AnswerPair]) -> List[dict]:
    """Iterates records and runs Structured LLM extraction on both answers."""
    results = []
    logger.info(f"Running extraction over {len(records)} records...")
    
    for idx, pair in enumerate(records):
        logger.info(f"Extracting {idx+1}/{len(records)} - {pair.id}")
        
        # 1. Parse human
        h_extract = extract_attributes(pair.human_answer, pair)
        
        # 2. Parse AI
        a_extract = extract_attributes(pair.ai_answer, pair)
        
        results.append({
            "pair": pair,
            "human_extracted": h_extract,
            "ai_extracted": a_extract
        })
        
    return results
