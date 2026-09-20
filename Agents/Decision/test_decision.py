from Agents.Decision.agent import DecisionAgent


def main():
    agent = DecisionAgent()

    result = agent.decide(
        state="research_sources",
        questions={
            "product_name": "ChatGPT",
            "source_count": 5,
        },
    )

    print("Provider:", result.provider)
    print("Success:", result.success)
    print("Error:", result.error)

    if result.provider != "disabled":
        raise RuntimeError(
            "Decision Agent should be disabled."
        )

    if result.success:
        raise RuntimeError(
            "Disabled Decision Agent must not return success."
        )

    print()
    print("Decision Agent disabled test: PASSED")


if __name__ == "__main__":
    main()
