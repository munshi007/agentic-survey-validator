"""Pipeline script to aggregate and synthesize outputs."""

import pandas as pd
import json
from typing import List, Dict, Any
from ..io.save_outputs import save_csv_output, save_markdown_snippet
from ..utils.logging import get_logger

logger = get_logger(__name__)

def run_aggregations(scores_list: List[Dict[str, Any]]) -> dict:
    """Takes the flat list of pair scores, aggregates metrics, and formats reports."""
    df = pd.DataFrame(scores_list)
    
    # Save the raw row-level scores
    save_csv_output(scores_list, "pair_scores.csv")
    
    # Person-level averages
    person_df = df.groupby("person_id")[["overall_score", "length_ratio", "bert_score_f1"]].mean().reset_index()
    save_csv_output(person_df.to_dict(orient="records"), "person_scores.csv")
    
    # Category-level averages
    cat_df = df.groupby("category")[["overall_score"]].mean().reset_index()
    save_csv_output(cat_df.to_dict(orient="records"), "category_scores.csv")
    
    # Error Mode Analysis
    # We joined error tags with a comma, let's split and count
    all_tags = []
    for tags in df['error_tags'].dropna():
        if tags.strip():
            all_tags.extend([t.strip() for t in tags.split(",")])
            
    error_counts = pd.Series(all_tags).value_counts().reset_index()
    error_counts.columns = ['error_type', 'count']
    save_csv_output(error_counts.to_dict(orient="records"), "error_analysis.csv")
    
    # Top/Worst Examples
    df_sorted = df.sort_values(by="overall_score", ascending=False)
    best_ex = df_sorted.head(2).to_dict(orient="records")
    worst_ex = df_sorted.tail(2).to_dict(orient="records")
    
    # Build report snippet
    overall_mean = round(df['overall_score'].mean(), 1)
    
    report_json = {
        "overall_score": overall_mean,
        "dimension_scores": {
            "factual": round(df['factual_score'].mean(), 1),
            "rationale": round(df['rationale_score'].mean(), 1),
            "specificity": round(df['specificity_score'].mean(), 1),
            "tone": round(df['tone_score'].mean(), 1),
            "contradiction": round(df['contradiction_score'].mean(), 1),
        },
        "top_failure_modes": error_counts.head(3).to_dict(orient="records"),
        "recommendation": "Use for directional exploration, not high-resolution insight generation.",
    }
    
    # Save the report to deliverables
    with open("deliverables/summary_report.json", "w") as f:
        json.dump(report_json, f, indent=2)
        
    return {
        "report_json": report_json,
        "best": best_ex,
        "worst": worst_ex
    }
