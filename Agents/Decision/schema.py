from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class DecisionResult:
    success: bool
    decision: Optional[Any] = None
    confidence: Optional[float] = None
    probabilities: Dict[str, float] = field(default_factory=dict)
    error: Optional[str] = None
    provider: str = ""