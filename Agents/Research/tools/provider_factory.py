import os

from .tavily_provider import TavilyProvider


class SearchProviderFactory:
    @staticmethod
    def create():
        provider_name = os.getenv("SEARCH_PROVIDER", "tavily").lower()

        if provider_name == "tavily":
            return TavilyProvider.from_environment()

        raise ValueError(
            f"Unsupported search provider: {provider_name}"
        )
