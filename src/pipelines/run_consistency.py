"""Pipeline step for running cross-question consistency per person."""

from typing import List, Dict, Any
import pandas as pd
from openai import OpenAI
from pydantic import BaseModel, Field

from ..config import OPENAI_API_KEY, MODEL_CONFIG
from ..utils.logging import get_logger
from ..io.save_outputs import save_csv_output

logger = get_logger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

class ConsistencyScore(BaseModel):
    """Holistic scoring per person ID across the whole questionnaire."""
    human_profile_summary: str = Field(description="3-sentence inferred consumer profile from human answers.")
    ai_profile_summary: str = Field(description="3-sentence inferred consumer profile from AI answers.")
    consistency_score_1_to_100: int = Field(description="How well does AI maintain the core profile across all 10 responses?")
    persona_drift: bool = Field(description="True if the AI diverges significantly from the human logic structure overall.")
    drift_explanation: str = Field(description="Explanation of the drift or consistency.")

def evaluate_person(person_id: str, df: pd.DataFrame) -> dict:
    """Group level evaluation."""
    person_records = df[df['person_id'] == person_id]
    
    # Build context blocks
    human_block = "\n".join([f"Q: {r['question_text']}\nA: {r['human_answer']}" for _, r in person_records.iterrows()])
    ai_block = "\n".join([f"Q: {r['question_text']}\nA: {r['ai_answer']}" for _, r in person_records.iterrows()])
    
    prompt = f"""
    You are evaluating consumer simulation consistency across a 10-question interview.
    
    Target Person ID: {person_id}
    
    === HUMAN ANSWERS (Ground Truth) ===
    {human_block}
    
    === AI ANSWERS (Simulated) ===
    {ai_block}
    
    Task:
    1. Summarize the implicit consumer profile found in the Human Answers. (e.g. price-sensitive, loyalist, high-convenience)
    2. Summarize the implicit profile found in the AI answers.
    3. Score how consistently the AI adhered to the true human profile on a scale of 1-100.
    4. Flag if persona drift occurred.
    """
    
    logger.info(f"Evaluating consistency for {person_id}")
    
    try:
        resp = client.beta.chat.completions.parse(
            model=MODEL_CONFIG['models']['primary_judge'],
            messages=[
                {"role": "system", "content": "You are an expert consumer insights profiler."},
                {"role": "user", "content": prompt}
            ],
            response_format=ConsistencyScore,
            temperature=0.0
        )
        
        parsed = resp.choices[0].message.parsed
        return {
            "person_id": person_id,
            "consistency_score_100": parsed.consistency_score_1_to_100,
            "human_summary": parsed.human_profile_summary,
            "ai_summary": parsed.ai_profile_summary,
            "persona_drift": parsed.persona_drift,
            "drift_explanation": parsed.drift_explanation
        }
            
    except Exception as e:
        logger.error(f"Failed consistency check for {person_id}: {e}")
        raise

def run_consistency_layer(data_list: List[dict]):
    """Groups data by person and evaluates."""
    df = pd.DataFrame(data_list)
    results = []
    for pid in df['person_id'].unique():
        res = evaluate_person(str(pid), df)
        results.append(res)
        
    save_csv_output(results, "person_consistency_scores.csv")
    return results
