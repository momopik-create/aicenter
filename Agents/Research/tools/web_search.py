from dataclasses import dataclass
from typing import List


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""


class WebSearchTool:
    name = "web_search"
    version = "0.1.0"

    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """
        Search for information related to a query.

        This is currently a placeholder.
        The real search provider will be connected later.
        """

        if not query.strip():
            return []

        return []
