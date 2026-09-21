from Agents.Contracts.research import ResearchStatus
from Agents.Contracts.research_input import ResearchInput
from Agents.Research.pipeline import ResearchPipeline


PRODUCT_NAME = "ChatGPT"
PRODUCT_URL = "https://chatgpt.com"


def main():
    print("=" * 60)
    print("RESEARCH PIPELINE TEST")
    print("=" * 60)

    research_input = ResearchInput(
        product_name=PRODUCT_NAME,
        url=PRODUCT_URL,
    )

    pipeline = ResearchPipeline()

    output = pipeline.run(research_input)

    print(f"Product: {output.product_name}")
    print(f"URL: {output.product_url}")
    print(f"Status: {output.status}")
    print(f"Sources found: {len(output.sources)}")

    if output.status != ResearchStatus.COMPLETED:
        raise RuntimeError(
            "Research pipeline did not complete successfully."
        )

    if not output.sources:
        raise RuntimeError(
            "Research pipeline returned no sources."
        )

    for index, source in enumerate(
        output.sources,
        start=1,
    ):
        print()
        print(f"Source {index}")
        print(f"Title: {source.title}")
        print(f"URL: {source.url}")
        print(f"Type: {source.source_type}")

    print()
    print("=" * 60)
    print("RESEARCH PIPELINE TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()