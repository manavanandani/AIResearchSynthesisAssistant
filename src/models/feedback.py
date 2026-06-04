"""Qualitative user feedback data models."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class FeedbackSource(str, Enum):
    CSAT_SURVEY = "CSAT Survey"
    SUPPORT_TICKET = "Support Ticket"
    APP_STORE_REVIEW = "App Store Review"
    USER_INTERVIEW = "User Interview"
    SALES_OBJECTION = "Sales Objection"


class UserSegment(str, Enum):
    ENTERPRISE_ADMIN = "Enterprise Admin"
    TEAM_LEAD = "Team Lead"
    INDIVIDUAL_CONTRIBUTOR = "Individual Contributor"
    NEW_TRIAL_USER = "New Trial User"


class FeedbackItem(BaseModel):
    """Raw qualitative user feedback response."""
    feedback_id: str = Field(..., description="Unique alphanumeric identifier (e.g. RESP-001)")
    source: FeedbackSource
    user_segment: UserSegment
    text: str = Field(..., description="Open-ended verbatim feedback text")
    nps_score: Optional[int] = Field(default=None, ge=0, le=10, description="Associated NPS score if present")
    timestamp: Optional[str] = None
