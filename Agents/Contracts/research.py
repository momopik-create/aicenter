from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ResearchStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


@dataclass
class SourceEvidence:
    url: str
    title: str
    source_type: str
    excerpt: Optional[str] = None
    reliability_score: Optional[float] = None


@dataclass
class ResearchPackage:
    product_name: str
    product_url: str
    status: ResearchStatus

    sources: list[SourceEvidence] = field(
        default_factory=list
    )

    facts: list[str] = field(
        default_factory=list
    )

    pricing: list[dict] = field(
        default_factory=list
    )

    pros: list[str] = field(
        default_factory=list
    )

    cons: list[str] = field(
        default_factory=list
    )

    review_status: ReviewStatus = (
        ReviewStatus.PENDING
    )

    review_note: Optional[str] = None
    