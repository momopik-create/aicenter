from dataclasses import dataclass
from typing import Optional


@dataclass
class ResearchSource:
    url: str
    title: str
    source_type: str
    excerpt: Optional[str] = None
    reliability_score: Optional[float] = None
