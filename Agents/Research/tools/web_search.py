from dataclasses import dataclass
from typing import List

from .tavily_provider import TavilyProvider


@dataclass
class SearchResult:
    title: str
    url: str
    content: str = ""


@dataclass
class SearchResponse:
    success: bool
    results: List[SearchResult]
    error: str | None = None


class WebSearchTool:
    name = "web_search"
    version = "1.0.0"

    def __init__(self):
        self.provider = TavilyProvider()

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> SearchResponse:

        return self.provider.search(
            query=query,
            max_results=max_results,
        )
