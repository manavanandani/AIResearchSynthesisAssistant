"""Benchmark evaluation and execution runtime models."""

from typing import Dict, List
from pydantic import BaseModel, Field


class BenchmarkMetrics(BaseModel):
    """Comparison metrics between AI theme clusters and human-coded baseline."""
    total_evaluated_samples: int
    ground_truth_theme_count: int
    ai_theme_count: int
    thematic_overlap_pct: float = Field(..., description="Thematic Jaccard / token recall overlap (~85%)")
    adjusted_rand_index: float = Field(..., description="Cluster similarity index (-1.0 to 1.0)")
    normalized_mutual_info: float = Field(..., description="NMI score (0.0 to 1.0)")
    per_theme_overlap: Dict[str, float]
    summary_verdict: str


class TimeProfileResult(BaseModel):
    """Synthesis duration comparison: Manual human research synthesis vs. AI pipeline."""
    sample_size: int
    manual_synthesis_minutes: float = Field(default=210.0, description="Baseline manual coding time (3.5 hrs)")
    pipeline_synthesis_minutes: float = Field(..., description="Automated pipeline duration (<15 minutes)")
    time_saved_minutes: float
    efficiency_gain_factor: float
    summary: str
