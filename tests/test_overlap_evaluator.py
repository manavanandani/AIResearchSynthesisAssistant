"""Tests for thematic overlap evaluation."""

from src.models.theme import SynthesisResult, ThemeCluster, ActionableRequirement
from src.benchmark.overlap_evaluator import OverlapEvaluator


def test_overlap_evaluation_calculation():
    theme = ThemeCluster(
        cluster_id=0,
        theme_title="Search Latency & Platform Sluggishness",
        primary_sentiment="Negative",
        response_count=2,
        sentiment_distribution={"Negative": 2, "Neutral": 0, "Positive": 0},
        representative_quotes=["Quote 1"],
        root_cause_analysis="Latency",
        requirements=[],
    )
    synthesis = SynthesisResult(
        run_id="TEST-RUN",
        total_responses_processed=2,
        cluster_count=1,
        themes=[theme],
        executive_summary="Summary",
    )

    ground_truth = {
        "R-1": "Search Latency & Platform Sluggishness",
        "R-2": "Search Latency & Platform Sluggishness",
    }
    predicted = {
        "R-1": "Search Latency & Platform Sluggishness",
        "R-2": "Search Latency & Platform Sluggishness",
    }

    metrics = OverlapEvaluator.evaluate(synthesis, ground_truth, predicted)
    assert metrics.thematic_overlap_pct == 100.0
    assert metrics.adjusted_rand_index == 1.0
