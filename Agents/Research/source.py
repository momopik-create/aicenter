from dataclasses import dataclass
from typing import Optional


@dataclass
class ResearchSource:
    url: str
    title: str = ""
    source_type: str = "unknown"
    publisher: str = ""
    published_at: Optional[str] = None
    checked_at: Optional[str] = None
