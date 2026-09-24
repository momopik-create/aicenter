from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SearchResult:
    title: str
    url: str
    content: str = ""


@dataclass
class SearchResponse:
    query: str
    success: bool
    results: List[SearchResult] = field(
        default_factory=list
    )
    error: Optional[str] = None 