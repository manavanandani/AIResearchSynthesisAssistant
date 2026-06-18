"""LangChain-style prompt engineering orchestrator for qualitative theme synthesis."""

from typing import List, Dict
from ..models.feedback import FeedbackItem
from ..models.theme import ThemeCluster, ActionableRequirement, SynthesisResult


class PromptOrchestrator:
    """Simulates multi-stage LLM prompt chain for clustering synthesis and PRD generation."""

    THEME_TAXONOMY_RULES = [
        (
            ["onboard", "setup", "invite", "welcome", "modal", "tutorial", "first-run", "empty state", "activation"],
            "Onboarding & First-Run Setup Friction",
            "P0",
            "Streamline workspace creation and initial member inviting",
        ),
        (
            ["search", "latency", "slow", "lag", "sluggish", "query", "crawl", "freeze", "delay", "load"],
            "Search Latency & Platform Sluggishness",
            "P0",
            "Sub-100ms response time on search queries and page transitions",
        ),
        (
            ["bill", "invoice", "seat", "license", "charge", "subscription", "pricing", "renew", "credit card", "tax"],
            "Billing Invoicing & License Seat Transparency",
            "P1",
            "Self-serve invoice downloads and real-time seat reassignment",
        ),
        (
            ["collab", "multiplayer", "cursor", "sync", "collision", "co-editing", "presence", "overwrite", "conflict"],
            "Real-Time Collaborative Multi-User Editing",
            "P1",
            "Multi-cursor live presence and instant conflict-free operational sync",
        ),
        (
            ["integ", "slack", "webhook", "zapier", "jira", "teams", "github", "token", "delivery", "trigger"],
            "Third-Party Integration & Webhook Reliability",
            "P2",
            "Bi-directional notification reliability and resilient webhook delivery",
        ),
    ]

    def synthesize_cluster(self, cluster_id: int, items: List[FeedbackItem]) -> ThemeCluster:
        """Executes synthesis prompt chain on a group of clustered feedback items."""
        texts = [i.text.lower() for i in items]
        all_text = " ".join(texts)

        # Score matching keywords for each taxonomy theme
        best_theme = "General Usability & Workflow Navigation"
        best_prio = "P2"
        best_goal = "Improve core navigation clarity and action discoverability"
        max_matches = -1

        for keywords, title, prio, goal in self.THEME_TAXONOMY_RULES:
            matches = sum(all_text.count(kw) for kw in keywords)
            if matches > max_matches:
                max_matches = matches
                best_theme = title
                best_prio = prio
                best_goal = goal

        # Sentiment estimation
        negative_words = ["slow", "lag", "confusing", "broken", "hate", "terrible", "frustrating", "error", "lost", "fail"]
        positive_words = ["love", "great", "fast", "clean", "easy", "helpful", "good", "amazing"]

        neg_count = sum(sum(1 for w in negative_words if w in t) for t in texts)
        pos_count = sum(sum(1 for w in positive_words if w in t) for t in texts)
        neut_count = max(0, len(items) - (neg_count + pos_count))

        primary_sentiment = "Negative" if neg_count >= pos_count else "Positive"
        if abs(neg_count - pos_count) <= 2 and neut_count > neg_count:
            primary_sentiment = "Neutral"

        # Select representative quotes (top 3 informative quotes)
        sorted_by_len = sorted(items, key=lambda x: len(x.text), reverse=True)
        quotes = [item.text for item in sorted_by_len[:3]]

        # Draft actionable product requirement
        req = ActionableRequirement(
            requirement_id=f"REQ-{cluster_id+1:03d}",
            priority=best_prio,
            user_story=f"As a user, I want {best_goal.lower()} so that I can accomplish my workflows without friction.",
            acceptance_criteria=[
                f"Verify that core friction points identified in '{best_theme}' are resolved in usability testing.",
                f"Ensure average task completion time improves by at least 25% for affected user segments.",
                f"Surface contextual guidance and error mitigation states in the user interface.",
            ],
            estimated_impact="High retention upside; mitigates active user friction reported in feedback batch.",
        )

        root_cause = (
            f"User feedback highlights repeated friction around {best_theme.lower()}. "
            f"Signals indicate a gap between user expectations and system feedback latency."
        )

        return ThemeCluster(
            cluster_id=cluster_id,
            theme_title=best_theme,
            primary_sentiment=primary_sentiment,
            response_count=len(items),
            sentiment_distribution={"Negative": neg_count, "Neutral": neut_count, "Positive": pos_count},
            representative_quotes=quotes,
            root_cause_analysis=root_cause,
            requirements=[req],
        )

    def synthesize_all(self, clustered_feedback: Dict[int, List[FeedbackItem]], run_id: str = "RUN-2026-JUN") -> SynthesisResult:
        """Synthesizes all clusters into a cohesive product review."""
        themes: List[ThemeCluster] = []
        total_responses = sum(len(items) for items in clustered_feedback.values())

        for cluster_id, items in clustered_feedback.items():
            theme = self.synthesize_cluster(cluster_id, items)
            themes.append(theme)

        # Sort themes by volume (largest response count first)
        themes.sort(key=lambda t: t.response_count, reverse=True)

        exec_summary = (
            f"Successfully synthesized {total_responses} qualitative feedback items across "
            f"{len(themes)} core theme clusters. Identified key user friction patterns with "
            f"actionable PRD requirements and verbatim evidentiary support."
        )

        return SynthesisResult(
            run_id=run_id,
            total_responses_processed=total_responses,
            cluster_count=len(themes),
            themes=themes,
            executive_summary=exec_summary,
        )
