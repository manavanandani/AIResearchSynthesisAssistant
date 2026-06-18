"""Tests for prompt orchestrator and theme synthesis."""

from src.models.feedback import FeedbackItem, FeedbackSource, UserSegment
from src.pipeline.prompt_orchestrator import PromptOrchestrator


def test_cluster_synthesis():
    orchestrator = PromptOrchestrator()
    items = [
        FeedbackItem(
            feedback_id="RESP-001",
            source=FeedbackSource.SUPPORT_TICKET,
            user_segment=UserSegment.INDIVIDUAL_CONTRIBUTOR,
            text="Search is extremely slow and laggy when looking up records.",
        ),
        FeedbackItem(
            feedback_id="RESP-002",
            source=FeedbackSource.CSAT_SURVEY,
            user_segment=UserSegment.TEAM_LEAD,
            text="Typing in search takes 5 seconds, severe query latency.",
        ),
    ]

    theme = orchestrator.synthesize_cluster(0, items)
    assert "Search Latency" in theme.theme_title
    assert theme.response_count == 2
    assert theme.primary_sentiment == "Negative"
    assert len(theme.requirements) == 1
    assert "REQ-" in theme.requirements[0].requirement_id
