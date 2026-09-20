from Agents.Research.input import ResearchInput
from Agents.Research.pipeline import ResearchPipeline


def main():
    research_input = ResearchInput(
        product_name="ChatGPT",
        url="https://chatgpt.com",
    )

    pipeline = ResearchPipeline()

    output = pipeline.run(research_input)

    print("Success:", output.success)

    if output.error:
        print("Error:", output.error)

    if not output.success:
        raise RuntimeError(
            f"Research pipeline failed: {output.error}"
        )

    print(
        "Product:",
        output.result.product_name,
    )

    print(
        "Status:",
        output.result.status,
    )

    print(
        "Sources:",
        len(output.result.sources),
    )

    print(
        "Research + Decision integration test: PASSED"
    )


if __name__ == "__main__":
    main()
