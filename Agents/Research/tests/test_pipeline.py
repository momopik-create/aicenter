from Agents.Research.input import ResearchInput
from Agents.Research.pipeline import ResearchPipeline


def main():
    research_input = ResearchInput(
        product_name="ChatGPT",
        url="https://chatgpt.com",
    )

    pipeline = ResearchPipeline()

    output = pipeline.run(research_input)

    print("=" * 60)
    print("RESEARCH PIPELINE TEST")
    print("=" * 60)

    print(f"Success: {output.success}")

    if output.error:
        print(f"Error: {output.error}")

    if not output.result:
        raise RuntimeError(
            "Pipeline returned no research result."
        )

    print(f"Product: {output.result.product_name}")
    print(f"URL: {output.result.url}")
    print(f"Status: {output.result.status}")

    print()
    print(f"Sources found: {len(output.result.sources)}")

    for index, source in enumerate(
        output.result.sources,
        start=1,
    ):
        print()
        print(f"Source {index}")
        print(f"Title: {source.title}")
        print(f"URL: {source.url}")
        print(f"Type: {source.source_type}")

    print()
    print("=" * 60)
    print("PIPELINE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
