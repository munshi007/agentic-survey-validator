"""Pipeline script to execute order-swapped judging and merge metrics."""

from typing import List, Dict, Any
from ..llm.judge import score_pair
from ..metrics.lexical_metrics import evaluate_lexical_metrics
from ..config import MODEL_CONFIG, RUBRIC
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
        factual = (score_fwd.factual_alignment.score + score_bwd.factual_alignment.score) / 2
        rationale = (score_fwd.rationale_alignment.score + score_bwd.rationale_alignment.score) / 2
        specificity = (score_fwd.specificity_calibration.score + score_bwd.specificity_calibration.score) / 2
        tone = (score_fwd.tone_persona_match.score + score_bwd.tone_persona_match.score) / 2
        contradiction = (score_fwd.contradiction_hallucination.score + score_bwd.contradiction_hallucination.score) / 2

        # 5. Extract weights from rubric and compute 1-100 score
        weights = RUBRIC['overall_score']['formula']
        # Scores are 1-5, so we calculate out of 5, then multiply by 20 to get out of 100.
        avg_score_out_of_5 = (
            factual * weights['factual_alignment'] +
            rationale * weights['rationale_alignment'] +
            specificity * weights['specificity_calibration'] +
            tone * weights['tone_persona_match'] +
            contradiction * weights['contradiction_hallucination']
        )
        final_overall_score = avg_score_out_of_5 * 20
        
        # Calculate Forward and Backward specific totals to catch instability
        fwd_score_out_of_5 = (
            score_fwd.factual_alignment.score * weights['factual_alignment'] +
            score_fwd.rationale_alignment.score * weights['rationale_alignment'] +
            score_fwd.specificity_calibration.score * weights['specificity_calibration'] +
            score_fwd.tone_persona_match.score * weights['tone_persona_match'] +
            score_fwd.contradiction_hallucination.score * weights['contradiction_hallucination']
        )
        bwd_score_out_of_5 = (
            score_bwd.factual_alignment.score * weights['factual_alignment'] +
            score_bwd.rationale_alignment.score * weights['rationale_alignment'] +
            score_bwd.specificity_calibration.score * weights['specificity_calibration'] +
            score_bwd.tone_persona_match.score * weights['tone_persona_match'] +
            score_bwd.contradiction_hallucination.score * weights['contradiction_hallucination']
        )
        
        fwd_score_100 = fwd_score_out_of_5 * 20
        bwd_score_100 = bwd_score_out_of_5 * 20
        absolute_delta = abs(fwd_score_100 - bwd_score_100)
        instability_flag = absolute_delta > 15.0 # Mark unstable if it swung by more than 15 points
        
        # We'll rely on the forward pass for explanations/tags to avoid merging text.
        
        final_results.append({
            "id": pair.id,
            "person_id": pair.person_id,
            "category": pair.question_category,
            "question_text": pair.question_text,
            "human_answer": pair.human_answer,
            "ai_answer": pair.ai_answer,
            
            "length_ratio": lexical['length_ratio'],
            "bert_score_f1": lexical['bert_score_f1'],
            
            "overall_score": final_overall_score,
            "forward_score": fwd_score_100,
            "swapped_score": bwd_score_100,
            "absolute_delta": absolute_delta,
            "instability_flag": instability_flag,
            
            "factual_score": factual,
            "rationale_score": rationale,
            "specificity_score": specificity,
            "tone_score": tone,
            "contradiction_score": contradiction,
            
            "error_tags": ", ".join(score_fwd.error_tags),
            "is_acceptable": score_fwd.directional_insight_acceptable,
            "judge_explanation": score_fwd.executive_summary
        })
        
    return final_results
