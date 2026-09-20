from dataclasses import dataclass
from typing import Optional

from .schema import ResearchResult


@dataclass
class ResearchOutput:
    success: bool
    result: Optional[ResearchResult] = None
    error: Optional[str] = None
