"""Pipeline script to execute order-swapped judging and merge metrics."""

from typing import List, Dict, Any
from ..llm.judge import score_pair
from ..metrics.lexical_metrics import evaluate_lexical_metrics
from ..config import MODEL_CONFIG
from ..utils.logging import get_logger

logger = get_logger(__name__)

def run_judging_pass(extracted_data: List[Dict[str, Any]]) -> List[dict]:
    """Runs the LLM judge over the extracted data, incorporating debiasing."""
    final_results = []
    
    for item in extracted_data:
        pair = item["pair"]
        logger.info(f"Judging Pair {pair.id}")
        
        # 1. Base Score
        score_fwd = score_pair(pair, item["human_extracted"], item["ai_extracted"], swap_order=False)
        
        # 2. Re-Score (Order swapped)
        do_swap = MODEL_CONFIG['evaluation']['order_swapped']
        if do_swap:
            score_bwd = score_pair(pair, item["human_extracted"], item["ai_extracted"], swap_order=True)
        else:
            score_bwd = score_fwd
            
        # 3. Lexical Score
        lexical = evaluate_lexical_metrics(pair)
        
        # 4. Average Numerical Rubric (handling pos bias)
        avg_overall = (score_fwd.overall_score_1_to_100 + score_bwd.overall_score_1_to_100) / 2
        
        # We'll rely on the forward pass for explanations/tags to avoid merging text.
        
        final_results.append({
            "id": pair.id,
            "person_id": pair.person_id,
            "category": pair.question_category,
            "human_answer": pair.human_answer,
            "ai_answer": pair.ai_answer,
            
            "length_ratio": lexical['length_ratio'],
            "bert_score_f1": lexical['bert_score_f1'],
            
            "overall_score": avg_overall,
            "factual_score": (score_fwd.factual_alignment.score + score_bwd.factual_alignment.score) / 2,
            "rationale_score": (score_fwd.rationale_alignment.score + score_bwd.rationale_alignment.score) / 2,
            "specificity_score": (score_fwd.specificity_calibration.score + score_bwd.specificity_calibration.score) / 2,
            "tone_score": (score_fwd.tone_persona_match.score + score_bwd.tone_persona_match.score) / 2,
            "contradiction_score": (score_fwd.contradiction_hallucination.score + score_bwd.contradiction_hallucination.score) / 2,
            
            "error_tags": ", ".join(score_fwd.error_tags),
            "is_acceptable": score_fwd.directional_insight_acceptable,
            "judge_explanation": score_fwd.executive_summary
        })
        
    return final_results
