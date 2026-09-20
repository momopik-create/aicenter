from schema import ResearchResult, ResearchStatus


def test_research_result_defaults():
    result = ResearchResult(
        product_name="Test Product",
        url="https://example.com",
    )

    assert result.product_name == "Test Product"
    assert result.url == "https://example.com"
    assert result.status == ResearchStatus.PENDING
    assert result.claims == []
    assert result.sources == []


if __name__ == "__main__":
    test_research_result_defaults()
    print("Research schema test passed.")
