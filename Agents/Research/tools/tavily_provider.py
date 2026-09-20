import os
from dataclasses import dataclass

import requests

from .web_search import SearchResult, SearchResponse


@dataclass
class TavilyConfig:
    api_key: str
    base_url: str = "https://api.tavily.com/search"


class TavilyProvider:
    name = "tavily"
    version = "0.2.0"

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

        payload = {
            "api_key": self.config.api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": "basic",
        }

        try:
            response = requests.post(
                self.config.base_url,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            results = []

            for item in data.get("results", []):
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        snippet=item.get("content", ""),
                        source="tavily",
                    )
                )

            return SearchResponse(
                query=query,
                results=results,
                success=True,
            )

        except requests.RequestException as error:
            return SearchResponse(
                query=query,
                results=[],
                success=False,
                error=str(error),
            )
