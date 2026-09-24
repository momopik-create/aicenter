from __future__ import annotations

import os
from typing import List

from .search_models import SearchResponse, SearchResult


class TavilyProvider:
    name = "tavily"
    version = "2.0.0"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self._client = None

    @classmethod
    def from_environment(cls) -> "TavilyProvider":
        return cls()

    @property
    def client(self):
        if self._client is None:
            if not self.api_key:
                raise RuntimeError(
                    "TAVILY_API_KEY is not configured."
                )
            try:
                from tavily import TavilyClient
            except ImportError as exc:
                raise RuntimeError(
                    "tavily-python is not installed."
                ) from exc
            self._client = TavilyClient(api_key=self.api_key)
        return self._client

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> SearchResponse:
        if not query.strip():
            return SearchResponse(
                query=query,
                success=False,
                error="Search query cannot be empty.",
            )

        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
            )

            results: List[SearchResult] = []
            seen_urls: set[str] = set()

            for item in response.get("results", []):
                url = str(item.get("url", "")).strip()
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                results.append(
                    SearchResult(
                        title=str(item.get("title", "")).strip(),
                        url=url,
                        content=str(item.get("content", "")).strip(),
                    )
                )

            return SearchResponse(
                query=query,
                success=bool(results),
                results=results,
                error=None if results else "No search results returned.",
            )

        except Exception as error:
            return SearchResponse(
                query=query,
                success=False,
                results=[],
                error=str(error),
            )
