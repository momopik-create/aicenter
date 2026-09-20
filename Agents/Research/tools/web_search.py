from .provider_factory import SearchProviderFactory
from .search_models import SearchResponse


class WebSearchTool:
    name = "web_search"
    version = "0.4.0"

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
                error="Search query is empty.",
            )

        return self.provider.search(
            query=query,
            max_results=max_results,
        )
