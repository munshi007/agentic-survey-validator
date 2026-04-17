"""Data structures representing the expected input data."""

from pydantic import BaseModel, Field

class AnswerPair(BaseModel):
    """Represents one evaluation row from the dataset."""
    id: int
    question_category: str
    question_text: str
    person_id: str
    human_answer: str
    ai_answer: str

class ProcessedDataset(BaseModel):
    """Root model for loading the entire clean set."""
    records: list[AnswerPair]
