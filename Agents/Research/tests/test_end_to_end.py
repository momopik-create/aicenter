import json

from Agents.Research.pipeline import ResearchPipeline
from Agents.Research.input import ResearchInput
from Agents.Research.review_store import ReviewStore
from Agents.Research.publish_gate import PublishGate
from Agents.Contracts.research import ReviewStatus
from Agents.Publisher.agent import PublisherAgent


def main():
    print("=" * 60)
    print("RESEARCH → PUBLISH END-TO-END TEST")
    print("=" * 60)

    product_name = "ChatGPT"
    product_url = "https://chatgpt.com"

    # ---------------------------------------------------------
    # 1. Create research input
    # ---------------------------------------------------------

    print("\n[1/9] Creating research input")

    research_input = ResearchInput(
        product_name=product_name,
        url=product_url,
    )

    print(f"Product: {research_input.product_name}")
    print(f"URL: {research_input.url}")

    # ---------------------------------------------------------
    # 2. Run research pipeline
    # ---------------------------------------------------------

    print("\n[2/9] Running research pipeline")

    pipeline = ResearchPipeline()

    result = pipeline.run(research_input)

    if result is None:
        raise RuntimeError(
            "Research pipeline returned no result."
        )

    print("Research pipeline completed.")
    print(f"Result type: {type(result).__name__}")
    print(f"Status: {result.status}")
    print(f"Sources: {len(result.sources)}")

    if result.product_name != product_name:
        raise RuntimeError(
            "Research result product_name does not match input."
        )

    if not result.sources:
        raise RuntimeError(
            "Research result contains no sources."
        )

    # ---------------------------------------------------------
    # 3. Save research result
    # ---------------------------------------------------------

    print("\n[3/9] Saving research result")

    store = ReviewStore()

    file_path = store.save(result)

    print(f"Review saved: {file_path}")

    if not file_path.exists():
        raise RuntimeError(
            "ReviewStore did not create the review file."
        )

    # ---------------------------------------------------------
    # 4. Verify stored research
    # ---------------------------------------------------------

    print("\n[4/9] Verifying stored research")

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

    if data.get("status") != "completed":
        raise RuntimeError(
            "Research was not completed successfully."
        )

    if not data.get("sources"):
        raise RuntimeError(
            "Stored research contains no sources."
        )

    # ---------------------------------------------------------
    # 5. Approve research
    # ---------------------------------------------------------

    print("\n[5/9] Approving research")

    store.update_status(
        product_name,
        ReviewStatus.APPROVED,
        note="End-to-end publication test approval",
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
    # 6. Check Publish Gate
    # ---------------------------------------------------------

    print("\n[6/9] Checking Publish Gate")

    gate = PublishGate(store)

    can_publish = gate.can_publish(
        product_name
    )

    print(
        f"Publish allowed: {can_publish}"
    )

    if not can_publish:
        raise RuntimeError(
            "Publish Gate rejected a valid approved "
            "research item."
        )

    # ---------------------------------------------------------
    # 7. Run Publisher
    # ---------------------------------------------------------

    print("\n[7/9] Publishing research result")

    publisher = PublisherAgent()

    publish_result = publisher.publish(
        product_name
    )

    print(
        "Success:",
        publish_result.success,
    )

    print(
        "Published:",
        publish_result.published,
    )

    print(
        "Publication ID:",
        publish_result.publication_id,
    )

    print(
        "Published at:",
        publish_result.published_at,
    )

    print(
        "Error:",
        publish_result.error,
    )

    if not publish_result.success:
        raise RuntimeError(
            "Publisher rejected a valid approved item."
        )

    if not publish_result.published:
        raise RuntimeError(
            "Publisher did not mark the item as published."
        )

    if not publish_result.publication_id:
        raise RuntimeError(
            "Publisher did not create a publication ID."
        )

    # ---------------------------------------------------------
    # 8. Verify publication metadata
    # ---------------------------------------------------------

    print("\n[8/9] Verifying publication metadata")

    published_data = json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )

    print(
        "Stored published:",
        published_data.get("published"),
    )

    print(
        "Stored publication ID:",
        published_data.get("publication_id"),
    )

    print(
        "Stored published at:",
        published_data.get("published_at"),
    )

    print(
        "Stored publisher:",
        published_data.get("publisher"),
    )

    if published_data.get("published") is not True:
        raise RuntimeError(
            "Publication status was not stored correctly."
        )

    if (
        published_data.get("publication_id")
        != publish_result.publication_id
    ):
        raise RuntimeError(
            "Stored publication ID does not match result."
        )

    if not published_data.get("published_at"):
        raise RuntimeError(
            "Published timestamp was not stored."
        )

    if published_data.get("publisher") != "publisher":
        raise RuntimeError(
            "Publisher metadata is incorrect."
        )

    # ---------------------------------------------------------
    # 9. Test duplicate publication protection
    # ---------------------------------------------------------

    print("\n[9/9] Testing duplicate publish protection")

    duplicate_result = publisher.publish(
        product_name
    )

    print(
        "Success:",
        duplicate_result.success,
    )

    print(
        "Published:",
        duplicate_result.published,
    )

    print(
        "Already published:",
        duplicate_result.already_published,
    )

    print(
        "Error:",
        duplicate_result.error,
    )

    if duplicate_result.success:
        raise RuntimeError(
            "Publisher allowed duplicate publication."
        )

    if not duplicate_result.already_published:
        raise RuntimeError(
            "Publisher did not detect already published item."
        )

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------

    print("\nCleaning up test publication")

    if file_path.exists():
        file_path.unlink()

    print("Temporary test file removed.")

    print("\n" + "=" * 60)
    print(
        "RESEARCH → PUBLISH END-TO-END TEST: PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()