from .search_models import SearchResponse
from .tavily_provider import TavilyProvider


class WebSearchTool:
    name = "web_search"
    version = "2.0.0"

    def __init__(self):
        self.provider = TavilyProvider()

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> SearchResponse:

        if not query.strip():
            return SearchResponse(
                query=query,
                success=False,
                results=[],
                error="Search query cannot be empty.",
            )

        return self.provider.search(
            query=query,
            max_results=max_results,
        )