import os
from dataclasses import dataclass
from typing import List, Optional

from .web_search import SearchResult, SearchResponse


@dataclass
class TavilyConfig:
    api_key: str
    base_url: str = "https://api.tavily.com/search"


class TavilyProvider:
    name = "tavily"
    version = "0.1.0"

    def __init__(self, config: TavilyConfig):
        self.config = config

    @classmethod
    def from_environment(cls):
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY environment variable is not configured."
            )

        return cls(
            TavilyConfig(
                api_key=api_key,
            )
        )

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

        # API request will be implemented in the next step.
        return SearchResponse(
            query=query,
            results=[],
            success=False,
            error="Tavily API request is not implemented yet.",
        )
