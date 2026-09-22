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

    test_file = store.directory / "publisher_test.json"

    # ---------------------------------------------------------
    # 1. Create test research record
    # ---------------------------------------------------------

    print("\n[1/7] Creating test research record")

    data = {
        "product_name": "Publisher Test",
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
            "A test product used to verify the publisher pipeline."
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

    if stored_data.get("publisher_version") != "0.4.0":
        raise RuntimeError(
            "Publisher version was not stored correctly."
        )

    content_file = stored_data.get("content_file")

    if not content_file:
        raise RuntimeError(
            "Content file path was not stored."
        )

    print("Publication metadata verified.")
    print("Content file:", content_file)

    # ---------------------------------------------------------
    # 5. Verify generated Astro content
    # ---------------------------------------------------------

    print("\n[5/7] Verifying generated Astro content")

    from pathlib import Path

    content_path = Path(content_file)

    if not content_path.exists():
        raise RuntimeError(
            f"Generated Astro content does not exist: {content_path}"
        )

    content = content_path.read_text(
        encoding="utf-8"
    )

    required_sections = [
        "Publisher Test Review",
        "## Key Facts",
        "## Pricing",
        "## Pros",
        "## Cons",
        "## Sources",
    ]

    for section in required_sections:
        if section not in content:
            raise RuntimeError(
                f"Generated article is missing: {section}"
            )

    required_frontmatter = [
        "title:",
        "description:",
        "rating:",
        "date:",
        "pricing_tier:",
    ]

    for field in required_frontmatter:
        if field not in content:
            raise RuntimeError(
                f"Generated article is missing frontmatter field: {field}"
            )

    if "Publisher Content Test" not in content:
        raise RuntimeError(
            "Generated article does not contain the expected product name."
        )

    if "Pro" not in content:
        raise RuntimeError(
            "Generated article does not contain pricing data."
        )

    if "$19/month" not in content:
        raise RuntimeError(
            "Generated article does not contain pricing value."
        )

    if "https://example.com" not in content:
        raise RuntimeError(
            "Generated article does not contain source URL."
        )

    print("Generated Astro content verified.")
    print("Generated file:", content_path)
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

    if content_path.exists():
        content_path.unlink()

    print("Temporary test files removed.")

    print()
    print("=" * 60)
    print("PUBLISHER AGENT TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
