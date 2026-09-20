import os
from typing import List

from tavily import TavilyClient

from .search_models import (
    SearchResponse,
    SearchResult,
)


class TavilyProvider:
    name = "tavily"
    version = "1.0.0"

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise RuntimeError(
                "TAVILY_API_KEY is not configured."
            )

        self.client = TavilyClient(
            api_key=api_key
        )

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> SearchResponse:

        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
            )

            results: List[SearchResult] = []

            for item in response.get(
                "results",
                [],
            ):
                results.append(
                    SearchResult(
                        title=item.get(
                            "title",
                            "",
                        ),
                        url=item.get(
                            "url",
                            "",
                        ),
                        content=item.get(
                            "content",
                            "",
                        ),
                    )
                )

            return SearchResponse(
                success=True,
                results=results,
            )

        except Exception as error:
            return SearchResponse(
                success=False,
                results=[],
                error=str(error),
            )
