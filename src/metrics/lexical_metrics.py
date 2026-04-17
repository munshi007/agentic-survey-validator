"""Deterministic non-LLM support metrics."""

import math
from bert_score import score as bert_score_fn
from ..schemas.records import AnswerPair

def compute_length_ratio(human_text: str, ai_text: str) -> float:
    """Returns AI length / Human length based on approximate word count."""
    h_len = len(human_text.split())
    a_len = len(ai_text.split())
    
    if h_len == 0:
        return 0.0
    return round(float(a_len) / float(h_len), 2)

def compute_bert_score(human_text: str, ai_text: str) -> float:
    """Minimal wrapper around BERTScore."""
    P, R, F1 = bert_score_fn([ai_text], [human_text], lang="en", verbose=False)
    # Using F1 since it captures both precision and recall
    return round(float(F1[0]), 3)

def evaluate_lexical_metrics(pair: AnswerPair) -> dict:
    """Bundles all string-based metrics."""
    return {
        "id": pair.id,
        "person_id": pair.person_id,
        "human_length": len(pair.human_answer.split()),
        "ai_length": len(pair.ai_answer.split()),
        "length_ratio": compute_length_ratio(pair.human_answer, pair.ai_answer),
        "bert_score_f1": compute_bert_score(pair.human_answer, pair.ai_answer)
    }
