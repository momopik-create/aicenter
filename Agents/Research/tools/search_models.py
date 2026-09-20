from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SearchResult:
    title: str
    url: str
    content: str = ""


@dataclass
class SearchResponse:
    success: bool
    results: List[SearchResult]
    error: Optional[str] = None
