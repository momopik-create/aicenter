from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class DecisionStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    UNCERTAIN = "uncertain"
    NEEDS_REVIEW = "needs_review"


@dataclass
class DecisionResult:
    decision: DecisionStatus

    confidence: float

    reason: str

    provider: str

    model: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )