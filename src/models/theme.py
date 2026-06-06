"""Synthesized theme clusters and actionable PRD requirements."""

from typing import List, Dict
from pydantic import BaseModel, Field


class ActionableRequirement(BaseModel):
    """PRD-ready actionable product requirement derived from feedback theme."""
    requirement_id: str
    priority: str = Field(..., description="P0 (Blocker), P1 (High), P2 (Medium)")
    user_story: str = Field(..., description="As a <user>, I want <goal> so that <benefit>")
    acceptance_criteria: List[str]
    estimated_impact: str


class ThemeCluster(BaseModel):
    """Semantic cluster grouping of user feedback entries."""
    cluster_id: int
    theme_title: str
    primary_sentiment: str = Field(..., description="Negative, Neutral, or Positive")
    response_count: int
    sentiment_distribution: Dict[str, int]
    representative_quotes: List[str]
    root_cause_analysis: str
    requirements: List[ActionableRequirement]


class SynthesisResult(BaseModel):
    """End-to-end synthesis run summary."""
    run_id: str
    total_responses_processed: int
    cluster_count: int
    themes: List[ThemeCluster]
    executive_summary: str
