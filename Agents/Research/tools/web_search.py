from dataclasses import dataclass, field
from typing import List, Optional


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
    version = "0.2.0"

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> SearchResponse:
        """
        Search the web for reliable information.

        The actual search provider will be connected later.
        """

        if not query.strip():
            return SearchResponse(
                query=query,
                success=False,
                error="Search query is empty.",
            )

        return SearchResponse(
            query=query,
            results=[],
            success=False,
            error="Search provider is not configured.",
        )
