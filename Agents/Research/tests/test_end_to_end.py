from Agents.Research.pipeline import ResearchPipeline
from Agents.Research.input import ResearchInput
from Agents.Research.review_store import ReviewStore
from Agents.Research.publish_gate import PublishGate
from Agents.Research.review import ReviewStatus


def main():
    print("=" * 60)
    print("RESEARCH AGENT END-TO-END TEST")
    print("=" * 60)

    product_name = "ChatGPT"
    product_url = "https://chatgpt.com"

    # ---------------------------------------------------------
    # 1. Create research input
    # ---------------------------------------------------------

    research_input = ResearchInput(
        product_name=product_name,
        url=product_url,
    )

    print("\n[1/7] Research input created")
    print(f"Product: {product_name}")
    print(f"URL: {product_url}")

    # ---------------------------------------------------------
    # 2. Run research pipeline
    # ---------------------------------------------------------

    pipeline = ResearchPipeline()

    print("\n[2/7] Running research pipeline...")

    result = pipeline.run(research_input)

    if result is None:
        raise RuntimeError("Research pipeline returned no result.")

    print("Research pipeline completed.")
    print(f"Result type: {type(result).__name__}")

    # ---------------------------------------------------------
    # 3. Inspect research result
    # ---------------------------------------------------------

    print("\n[3/7] Inspecting research result")

    if hasattr(result, "status"):
        print(f"Status: {result.status}")

    if hasattr(result, "product_name"):
        print(f"Product: {result.product_name}")

    if hasattr(result, "sources"):
        print(f"Sources: {len(result.sources)}")

    # ---------------------------------------------------------
    # 4. Store review
    # ---------------------------------------------------------

    print("\n[4/7] Saving review item")

    store = ReviewStore()

    store.save(result)

    print("Review item saved.")

    # ---------------------------------------------------------
    # 5. Verify pending state
    # ---------------------------------------------------------

    print("\n[5/7] Checking initial review state")

    pending_item = store.get(product_name)

    if pending_item is None:
        raise RuntimeError("Review item was not saved.")

    print(
        "Review status:",
        pending_item.get("review_status")
        if isinstance(pending_item, dict)
        else getattr(pending_item, "review_status", None),
    )

    # ---------------------------------------------------------
    # 6. Approve item
    # ---------------------------------------------------------

    print("\n[6/7] Approving research item")

    store.update_status(
        product_name,
        ReviewStatus.APPROVED,
        note="End-to-end test approval",
    )

    print("Approval recorded.")

    # ---------------------------------------------------------
    # 7. Publish Gate
    # ---------------------------------------------------------

    print("\n[7/7] Checking Publish Gate")

    gate = PublishGate(store)

    can_publish = gate.can_publish(product_name)

    print(f"Publish allowed: {can_publish}")

    if not can_publish:
        raise RuntimeError(
            "End-to-end test failed: "
            "Publish Gate rejected the approved research item."
        )

    print("\n" + "=" * 60)
    print("RESEARCH AGENT END-TO-END TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()