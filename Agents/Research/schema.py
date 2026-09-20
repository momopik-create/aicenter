from dataclasses import dataclass, field
from enum import Enum
from typing import List

from .claim import ResearchClaim
from .source import ResearchSource


class ResearchStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"


@dataclass
class ResearchResult:
    product_name: str
    url: str

    description: str = ""
    features: List[str] = field(default_factory=list)
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)

    claims: List[ResearchClaim] = field(default_factory=list)
    sources: List[ResearchSource] = field(default_factory=list)

    status: ResearchStatus = ResearchStatus.PENDING
