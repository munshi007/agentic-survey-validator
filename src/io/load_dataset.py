"""Strictly handles dataset loading and normalization for the Roland Berger GenAI Test."""

import os
from pathlib import Path
import pandas as pd
from typing import List, Dict, Any

from ..schemas.records import AnswerPair
from ..config import DATA_DIR

RAW_FILE = DATA_DIR / "raw" / "RB_GenAI_Datatest.xlsx"
PROCESSED_FILE = DATA_DIR / "processed" / "dataset.json"

def load_and_validate_dataset() -> List[AnswerPair]:
    """Reads from Excel, validates headers, and returns strict objects."""
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Raw data not found at {RAW_FILE}")

    try:
        df = pd.read_excel(RAW_FILE)

        # Normalize input columns broadly
        df.rename(columns=lambda x: str(x).strip().lower().replace(" ", "_").replace("question_text", "question"), inplace=True)

        # Map whatever variation we get into strict output fields
        expected_columns = {
            'question_category': 'question_category',
            'question': 'question_text',
            'person_id': 'person_id',
            'human_answer': 'human_answer',
            'human_answers': 'human_answer',
            'ai_answer': 'ai_answer',
            'ai_answers': 'ai_answer'
        }
        
        # Rename to clean snake_case variables
        df = df.rename(columns=expected_columns)
        
        # Check that we have exactly what we expect using final canonical names
        required = ['question_category', 'question_text', 'person_id', 'human_answer', 'ai_answer']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise KeyError(f"Dataset missing required columns. Normalization resulted in {list(df.columns)}, but need: {missing}")

        # Add synthetic IDs for easier tracing
        df['id'] = range(1, len(df) + 1)
        
        # Convert to records
        records = df.to_dict(orient="records")
        
        valid_records: List[AnswerPair] = []
        for rec in records:
            # Pydantic validation kicks in here!
            valid_records.append(AnswerPair(**rec))
            
        print(f"Successfully loaded and validated {len(valid_records)} rows.")
        return valid_records
        
    except Exception as e:
        raise ValueError(f"Failed to load dataset strictly: {e}")

def save_processed(records: List[AnswerPair]) -> None:
    """Stores a deterministic JSON copy."""
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([rec.model_dump() for rec in records])
    df.to_json(PROCESSED_FILE, orient="records", indent=4)
