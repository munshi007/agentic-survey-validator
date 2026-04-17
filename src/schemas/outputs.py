"""Pydantic schemas used for strict LLM Structured Outputs."""

from pydantic import BaseModel, Field
from typing import Optional, Literal

class ExtractedAttributes(BaseModel):
    """Structured extraction of preferences from a single open-text answer."""
    preferred_brands: list[str] = Field(description="Explicit brands mentioned")
    channel_preference: Optional[str] = Field(None, description="Where they shop e.g. online, supermarket")
    packaging_size_preference: Optional[str] = Field(None, description="Preferred packaging or size")
    budget_value_signal: Optional[str] = Field(None, description="Hints about budget vs premium priorities")
    ingredient_salience: Optional[str] = Field(None, description="Do they care about ingredients? Which ones?")
    convenience_signal: Optional[str] = Field(None, description="Do they prioritize convenience/routine?")
    decision_criteria: list[str] = Field(description="Main factors for buying the product")
    sentiment_confidence: str = Field(description="How certain or passionate the speaker sounds")
    quoted_anchors: list[str] = Field(description="2-3 exact phrases capturing the core vibe")

class DimensionScore(BaseModel):
    """Score for a specific rubric dimension."""
    score: int = Field(ge=1, le=5, description="1-5 score")
    justification: str = Field(description="1 sentence explaining why")

class PairEvaluation(BaseModel):
    """The final Judge output evaluating Human vs AI."""
    factual_alignment: DimensionScore
    rationale_alignment: DimensionScore
    specificity_calibration: DimensionScore
    tone_persona_match: DimensionScore
    contradiction_hallucination: DimensionScore
    
    error_tags: list[Literal[
        "invented_specificity", 
        "preference_distortion", 
        "rationale_drift", 
        "tone_mismatch", 
        "generic_overpolish", 
        "contradiction", 
        "omission_of_key_detail"
    ]] = Field(description="Any error tags that apply to the AI answer")
    
    directional_insight_acceptable: bool = Field(description="Is this good enough for directional market research?")
    executive_summary: str = Field(description="2-3 sentence final verdict on simulation fidelity")
