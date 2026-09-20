from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ResearchStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class ResearchResult:
    product_name: str
    url: str
    status: ResearchStatus
    sources: List = field(default_factory=list)
    review_status: ReviewStatus = ReviewStatus.PENDING
    review_note: Optional[str] = None
