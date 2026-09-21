from Agents.Publisher.agent import PublisherAgent
from Agents.Research.review_store import ReviewStore
from Agents.Contracts.research import ReviewStatus


def main():
    print("=" * 60)
    print("PUBLISHER AGENT TEST")
    print("=" * 60)

    product_name = "publisher_test"

    store = ReviewStore()
    agent = PublisherAgent()

    # ---------------------------------------------------------
    # 1. Create a valid research record
    # ---------------------------------------------------------

    print("\n[1/4] Creating test research record")

    test_file = store.directory / "publisher_test.json"

    data = {
        "product_name": product_name,
        "product_url": "https://example.com",
        "status": "completed",
        "sources": [
            {
                "url": "https://example.com",
                "title": "Example",
                "source_type": "official",
                "excerpt": "Test source",
            }
        ],
        "review_status": ReviewStatus.PENDING.value,
        "review_note": None,
    }

    import json

    test_file.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Test file: {test_file}")

    # ---------------------------------------------------------
    # 2. Verify pending research cannot be published
    # ---------------------------------------------------------

    print("\n[2/4] Testing pending research")

    result = agent.publish(product_name)

    print("Success:", result.success)
    print("Published:", result.published)
    print("Error:", result.error)

    if result.success:
        raise RuntimeError(
            "Publisher allowed publishing before approval."
        )

    if result.published:
        raise RuntimeError(
            "Publisher marked an unapproved item as published."
        )

    # ---------------------------------------------------------
    # 3. Approve research
    # ---------------------------------------------------------

    print("\n[3/4] Approving research")

    store.update_status(
        product_name,
        ReviewStatus.APPROVED,
        note="Publisher test approval",
    )

    result = agent.publish(product_name)

    print("Success:", result.success)
    print("Published:", result.published)
    print("Error:", result.error)

    if not result.success:
        raise RuntimeError(
            "Publisher rejected a valid approved item."
    # ---------------------------------------------------------
    # 4. Verify publication metadata
    # ---------------------------------------------------------

    print("\n[4/5] Verifying publication metadata")

    stored_data = json.loads(
        test_file.read_text(
            encoding="utf-8"
        )
    )

    print(
        "Published:",
        stored_data.get("published"),
    )

    print(
        "Publication ID:",
        stored_data.get("publication_id"),
    )

    print(
        "Published at:",
        stored_data.get("published_at"),
    )

    print(
        "Publisher:",
        stored_data.get("publisher"),
    )

    if stored_data.get("published") is not True:
        raise RuntimeError(
            "Published flag was not stored correctly."
        )

    if not stored_data.get("publication_id"):
        raise RuntimeError(
            "Publication ID was not stored."
        )

    if not stored_data.get("published_at"):
        raise RuntimeError(
            "Published timestamp was not stored."
        )

    if stored_data.get("publisher") != "publisher":
        raise RuntimeError(
            "Publisher name was not stored correctly."
        )
        )

    if not result.published:
        raise RuntimeError(
            "Publisher did not mark approved item as published."
        )
    # ---------------------------------------------------------
    # 5. Verify duplicate publishing is blocked
    # ---------------------------------------------------------

    print("\n[5/6] Testing duplicate publish protection")

    duplicate_result = agent.publish(product_name)

    print("Success:", duplicate_result.success)
    print("Published:", duplicate_result.published)
    print(
        "Already published:",
        duplicate_result.already_published,
    )
    print("Error:", duplicate_result.error)

    if duplicate_result.success:
        raise RuntimeError(
            "Publisher allowed duplicate publishing."
        )

    if not duplicate_result.already_published:
        raise RuntimeError(
            "Publisher did not detect already published item."
        )

    if duplicate_result.published:
        raise RuntimeError(
            "Duplicate publish was incorrectly marked as published."
        )
    # ---------------------------------------------------------
    # 6. Cleanup
    # ---------------------------------------------------------

    print("\n[6/6] Cleaning up")

    if test_file.exists():
        test_file.unlink()

    print("Temporary test file removed.")

    print("\n" + "=" * 60)
    print("PUBLISHER AGENT TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
