from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class FactStatus(str, Enum):
    VERIFIED = "verified"
    UNSUPPORTED = "unsupported"
    CONTRADICTED = "contradicted"
    NEEDS_REVIEW = "needs_review"


@dataclass
class ClaimCheck:
    claim: str

    status: FactStatus

    evidence_urls: List[str] = field(
        default_factory=list
    )

    explanation: Optional[str] = None


@dataclass
class FactCheckResult:
    product_name: str

    passed: bool

    claims: List[ClaimCheck] = field(
        default_factory=list
    )

    review_status: str = "pending"
