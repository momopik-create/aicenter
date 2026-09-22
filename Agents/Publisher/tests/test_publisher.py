```python
import json

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

    print("\n[1/7] Creating test research record")

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
                "reliability_score": 1.0,
            }
        ],
        "facts": [
            "Example product used for Publisher Agent testing."
        ],
        "pricing": [
            {
                "name": "Pro",
                "price": "$19/month",
                "description": "Example paid plan",
            }
        ],
        "pros": [
            "Easy to use",
            "Useful for testing",
        ],
        "cons": [
            "Test data only",
        ],
        "review_status": ReviewStatus.PENDING.value,
        "review_note": None,
    }

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

    print("\n[2/7] Testing pending research")

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
    # 3. Approve research and publish
    # ---------------------------------------------------------

    print("\n[3/7] Approving research")

    store.update_status(
        product_name,
        ReviewStatus.APPROVED,
        note="Publisher test approval",
    )

    result = agent.publish(product_name)

    print("Success:", result.success)
    print("Published:", result.published)
    print("Publication ID:", result.publication_id)
    print("Published at:", result.published_at)
    print("Error:", result.error)

    if not result.success:
        raise RuntimeError(
            f"Publisher rejected a valid approved item: {result.error}"
        )

    if not result.published:
        raise RuntimeError(
            "Publisher did not mark approved item as published."
        )

    if not result.publication_id:
        raise RuntimeError(
            "Publisher did not return a publication ID."
        )

    if not result.published_at:
        raise RuntimeError(
            "Publisher did not return a publication timestamp."
        )

    # ---------------------------------------------------------
    # 4. Verify publication metadata
    # ---------------------------------------------------------

    print("\n[4/7] Verifying publication metadata")

    stored_data = json.loads(
        test_file.read_text(
            encoding="utf-8"
        )
    )

    print(
        "Stored published:",
        stored_data.get("published"),
    )

    print(
        "Stored publication ID:",
        stored_data.get("publication_id"),
    )

    print(
        "Stored published at:",
        stored_data.get("published_at"),
    )

    print(
        "Stored publisher:",
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

    # ---------------------------------------------------------
    # 5. Verify generated Astro content
    # ---------------------------------------------------------

    print("\n[5/7] Verifying generated Astro content")

    content_file_value = stored_data.get("content_file")

    if not content_file_value:
        raise RuntimeError(
            "Publisher did not store the generated content file path."
        )

    content_file = agent.content_builder.output_directory / (
        "publisher-test.md"
    )

    print("Expected content file:", content_file)
    print("Stored content path:", content_file_value)

    if not content_file.exists():
        raise RuntimeError(
            "ContentBuilder did not generate the expected Markdown file."
        )

    content = content_file.read_text(
        encoding="utf-8"
    )

    required_fields = [
        "title:",
        "description:",
        "rating:",
        "date:",
        "pricing_tier:",
    ]

    for field in required_fields:
        if field not in content:
            raise RuntimeError(
                f"Generated content is missing frontmatter field: {field}"
            )

    if "Publisher Test Review" not in content:
        raise RuntimeError(
            "Generated article title is incorrect."
        )

    if "## Key Facts" not in content:
        raise RuntimeError(
            "Generated article is missing Key Facts section."
        )

    if "## Pricing" not in content:
        raise RuntimeError(
            "Generated article is missing Pricing section."
        )

    if "## Pros" not in content:
        raise RuntimeError(
            "Generated article is missing Pros section."
        )

    if "## Cons" not in content:
        raise RuntimeError(
            "Generated article is missing Cons section."
        )

    if "## Sources" not in content:
        raise RuntimeError(
            "Generated article is missing Sources section."
        )

    print("Generated content verified successfully.")
    print("Content length:", len(content))

    # ---------------------------------------------------------
    # 6. Verify duplicate publishing is blocked
    # ---------------------------------------------------------

    print("\n[6/7] Testing duplicate publish protection")

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
    # 7. Cleanup
    # ---------------------------------------------------------

    print("\n[7/7] Cleaning up")

    if test_file.exists():
        test_file.unlink()

    if content_file.exists():
        content_file.unlink()

    print("Temporary test files removed.")

    print()
    print("=" * 60)
    print("PUBLISHER AGENT TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
```
