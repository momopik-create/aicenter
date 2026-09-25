from Agents.Contracts.research import ResearchStatus
from Agents.Contracts.research_input import ResearchInput
from Agents.Research.pipeline import ResearchPipeline
from Agents.Research.review_store import ReviewStore
from Agents.Research.tools.search_models import SearchResponse, SearchResult


class FakeAnalyzer:
    def analyze(self, product_name, product_url, sources):
        return {
            "facts": ["Fact one", "Fact two"],
            "pricing": [{"plan": "Basic", "price": "$5"}],
            "features": ["Feature one"],
            "pros": ["Pro one"],
            "cons": ["Con one"],
        }


class FakeSearchProvider:
    def search(self, query: str, max_results: int = 10) -> SearchResponse:
        return SearchResponse(
            query=query,
            success=True,
            results=[
                SearchResult("Official", "https://example.com/official", "Official product information."),
                SearchResult("Docs", "https://example.com/docs", "Documentation and features."),
                SearchResult("Pricing", "https://example.com/pricing", "Pricing plans and billing."),
            ],
        )


def main():
    pipeline = ResearchPipeline(
        search_tool=FakeSearchProvider(),
        store=ReviewStore(directory="/tmp/aicenter-test-research"),
        analyzer=FakeAnalyzer(),
    )
    output = pipeline.run(
        ResearchInput("ChatGPT", "https://chatgpt.com")
    )

    assert output.status == ResearchStatus.COMPLETED
    assert len(output.sources) == 3
    assert output.sources[2].source_type == "pricing"
    assert len(output.facts) == 2
    assert len(output.pricing) == 1
    print("Research Pipeline test: PASSED")


if __name__ == "__main__":
    main()
