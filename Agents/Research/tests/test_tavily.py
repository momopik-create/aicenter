import os

from Agents.Research.tools.web_search import WebSearchTool


def main():
    if not os.getenv("TAVILY_API_KEY"):
        print("Tavily smoke test skipped: TAVILY_API_KEY is not configured.")
        return

    search = WebSearchTool()

    response = search.search(
        query="best AI coding tools",
        max_results=5,
    )

    if not response.success:
        raise RuntimeError(
            f"Search failed: {response.error}"
        )

    print(f"Query: {response.query}")
    print(f"Results: {len(response.results)}")
    print()

    for index, result in enumerate(response.results, start=1):
        print(f"{index}. {result.title}")
        print(f"   {result.url}")
        print()


if __name__ == "__main__":
    main()
