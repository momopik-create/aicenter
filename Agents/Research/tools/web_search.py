from .search_models import SearchResponse
from .tavily_provider import TavilyProvider


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
