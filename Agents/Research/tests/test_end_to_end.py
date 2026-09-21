from Agents.Research.pipeline import ResearchPipeline
from Agents.Research.input import ResearchInput
from Agents.Research.review_store import ReviewStore
from Agents.Research.publish_gate import PublishGate
from Agents.Contracts.research import ReviewStatus


def main():
    print("=" * 60)
    print("RESEARCH AGENT END-TO-END TEST")
    print("=" * 60)

    product_name = "ChatGPT"
    product_url = "https://chatgpt.com"

    # ---------------------------------------------------------
    # 1. Create research input
    # ---------------------------------------------------------

    print("\n[1/7] Creating research input")

    research_input = ResearchInput(
        product_name=product_name,
        url=product_url,
    )

    print(f"Product: {research_input.product_name}")
    print(f"URL: {research_input.url}")

    # ---------------------------------------------------------
    # 2. Run research pipeline
    # ---------------------------------------------------------

    print("\n[2/7] Running research pipeline")

    pipeline = ResearchPipeline()

    result = pipeline.run(research_input)

    if result is None:
        raise RuntimeError(
            "Research pipeline returned no result."
        )

    print("Research pipeline completed.")
    print(f"Result type: {type(result).__name__}")

    # ---------------------------------------------------------
    # 3. Inspect research result
    # ---------------------------------------------------------

    print("\n[3/7] Inspecting research result")

    if not hasattr(result, "product_name"):
        raise RuntimeError(
            "Research result has no product_name."
        )

    if not hasattr(result, "status"):
        raise RuntimeError(
            "Research result has no status."
        )

    if not hasattr(result, "sources"):
        raise RuntimeError(
            "Research result has no sources."
        )

    print(f"Product: {result.product_name}")
    print(f"Status: {result.status}")
    print(f"Sources: {len(result.sources)}")

    if result.product_name != product_name:
        raise RuntimeError(
            "Research result product_name does not match input."
        )

    # ---------------------------------------------------------
    # 4. Save result to ReviewStore
    # ---------------------------------------------------------

    print("\n[4/7] Saving research result")

    store = ReviewStore()

    file_path = store.save(result)

    print(f"Review saved: {file_path}")

    if not file_path.exists():
        raise RuntimeError(
            "ReviewStore did not create the review file."
        )

    # ---------------------------------------------------------
    # 5. Verify stored review
    # ---------------------------------------------------------

    print("\n[5/7] Verifying stored review")

    import json

    data = json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )

    print(
        "Stored product:",
        data.get("product_name"),
    )

    print(
        "Stored status:",
        data.get("status"),
    )

    print(
        "Stored review status:",
        data.get("review_status"),
    )

    print(
        "Stored sources:",
        len(data.get("sources", [])),
    )

    if data.get("product_name") != product_name:
        raise RuntimeError(
            "Stored product_name is incorrect."
        )

    if not data.get("sources"):
        raise RuntimeError(
            "Stored research contains no sources."
        )

    # ---------------------------------------------------------
    # 6. Approve research
    # ---------------------------------------------------------

    print("\n[6/7] Approving research")

    store.update_status(
        product_name,
        ReviewStatus.APPROVED,
        note="End-to-end test approval",
    )

    updated_data = json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )

    print(
        "Updated review status:",
        updated_data.get("review_status"),
    )

    if (
        updated_data.get("review_status")
        != ReviewStatus.APPROVED.value
    ):
        raise RuntimeError(
            "Research approval was not stored correctly."
        )

    # ---------------------------------------------------------
    # 7. Publish Gate
    # ---------------------------------------------------------

    print("\n[7/7] Checking Publish Gate")

    gate = PublishGate(store)

    can_publish = gate.can_publish(
        product_name
    )

    print(
        f"Publish allowed: {can_publish}"
    )

    if not can_publish:
        raise RuntimeError(
            "Publish Gate rejected a valid "
            "approved research item."
        )

    print("\n" + "=" * 60)
    print("RESEARCH AGENT END-TO-END TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()