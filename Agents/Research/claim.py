from dataclasses import dataclass
from typing import Optional


@dataclass
class ResearchClaim:
    claim: str
    source_url: str
    source_type: str
    checked_at: str
    confidence: Optional[str] = None
    notes: str = ""
