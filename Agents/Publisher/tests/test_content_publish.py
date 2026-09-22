import json
from pathlib import Path

from Agents.Publisher.content_publish import ContentPublisher


def main():
    print("=" * 60)
    print("CONTENT PUBLISH TEST")
    print("=" * 60)

    product_name = "publisher_content_test"

    print("\n[1/5] Creating test publisher")

    publisher = ContentPublisher()

    print("Publisher:", publisher.name)
    print("Version:", publisher.version)

    print("\n[2/5] Creating test content")

    content = {
        "title": "Publisher Content Test",
        "description": "Temporary content generated for testing.",
        "product_name": product_name,
        "url": "https://example.com",
    }

    print("Content created.")

    print("\n[3/5] Publishing content")

    result = publisher.publish(
        product_name=product_name,
        content=content,
    )

    print("Success:", result.success)
    print("Published:", result.published)
    print("Publication ID:", result.publication_id)
    print("Error:", result.error)

    if not result.success:
        raise RuntimeError(
            "Content Publisher failed to publish valid content."
        )

    if not result.published:
        raise RuntimeError(
            "Content Publisher returned success but published=False."
        )

    print("\n[4/5] Verifying publication")

    output_file = Path(
        publisher.output_directory
    ) / f"{product_name}.json"

    if not output_file.exists():
        raise RuntimeError(
            "Published content file was not created."
        )

    data = json.loads(
        output_file.read_text(
            encoding="utf-8"
        )
    )

    print("Stored title:", data.get("title"))
    print("Stored product:", data.get("product_name"))
    print("Stored published:", data.get("published"))

    if data.get("published") is not True:
        raise RuntimeError(
            "Stored content is not marked as published."
        )

    print("\n[5/5] Cleaning up")

    if output_file.exists():
        output_file.unlink()

    print("Temporary content file removed.")

    print()
    print("=" * 60)
    print("CONTENT PUBLISH TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
