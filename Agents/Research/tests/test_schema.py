from Agents.Contracts.research import ResearchPackage, ResearchStatus


def test_research_package_defaults():
    result = ResearchPackage(
        product_name="Test Product",
        product_url="https://example.com",
        status=ResearchStatus.IN_PROGRESS,
    )

    assert result.product_name == "Test Product"
    assert result.product_url == "https://example.com"
    assert result.status == ResearchStatus.IN_PROGRESS
    assert result.sources == []
    assert result.facts == []


if __name__ == "__main__":
    test_research_package_defaults()
    print("Research contract test passed.")
