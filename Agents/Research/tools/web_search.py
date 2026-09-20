from dataclasses import dataclass, field
from typing import List, Optional

from .tavily_provider import TavilyProvider


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""
    source: str = ""
    published_at: Optional[str] = None
    score: Optional[float] = None


@dataclass
class SearchResponse:
    query: str
    results: List[SearchResult] = field(default_factory=list)
    success: bool = True
    error: Optional[str] = None


class WebSearchTool:
    name = "web_search"
    version = "0.3.0"

    def __init__(self, provider=None):
        self.provider = provider or TavilyProvider.from_environment()

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> SearchResponse:

        if not query.strip():
            return SearchResponse(
                query=query,
                success=False,
                error="Search query is empty.",
            )

        return self.provider.search(
            query=query,
            max_results=max_results,
        )
