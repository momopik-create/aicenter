from .search_models import SearchResponse
from .provider_factory import SearchProviderFactory


class WebSearchTool:
    name = "web_search"
    version = "2.1.0"

    def __init__(self, provider=None):
        self.provider = provider or SearchProviderFactory.create()

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
