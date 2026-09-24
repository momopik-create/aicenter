from __future__ import annotations

from Agents.Publisher.agent import PublisherAgent


def main() -> None:
    agent = PublisherAgent()
    results = agent.publish_approved()

    if not results:
        print("No approved research waiting for publication.")
        return

    failures = 0
    for result in results:
        print(
            f"{result.product_name}: success={result.success} "
            f"published={result.published} error={result.error}"
        )
        if not result.success:
            failures += 1

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
