from pathlib import Path
from tempfile import TemporaryDirectory

from Agents.Contracts.research import (
    ResearchPackage,
    ResearchStatus,
    ReviewStatus,
    SourceEvidence,
)
from Agents.Publisher.content_builder import ContentBuilder


def main():
    print("=" * 60)
    print("CONTENT BUILDER TEST")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Create temporary output directory
    # ---------------------------------------------------------

    print("\n[1/4] Preparing temporary output directory")

    with TemporaryDirectory() as temp_directory:

        builder = ContentBuilder(
            output_directory=temp_directory
        )

        # -----------------------------------------------------
        # 2. Create research package
        # -----------------------------------------------------

        print("\n[2/4] Creating test research package")

        research = ResearchPackage(
            product_name="Publisher Content Test",
            product_url="https://example.com",
            status=ResearchStatus.COMPLETED,
            facts=[
                "A test product used to verify Astro content generation."
            ],
            pricing=[
                {
                    "name": "Pro",
                    "price": "$19/month",
                    "description": "Example paid plan",
                }
            ],
            pros=[
                "Easy to use",
                "Useful for testing",
            ],
            cons=[
                "Test data only",
            ],
            sources=[
                SourceEvidence(
                    url="https://example.com",
                    title="Example Source",
                    source_type="official",
                    excerpt="Example evidence",
                    reliability_score=1.0,
                )
            ],
            review_status=ReviewStatus.APPROVED,
        )

        # -----------------------------------------------------
        # 3. Build Astro Markdown
        # -----------------------------------------------------

        print("\n[3/4] Building Astro content")

        output_file = builder.build(research)

        print("Output file:", output_file)

        if not output_file.exists():
            raise RuntimeError(
                "ContentBuilder did not create a Markdown file."
            )

        if output_file.name != "publisher-content-test.md":
            raise RuntimeError(
                "Generated slug/file name is incorrect."
            )

        content = output_file.read_text(
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
                    f"Missing frontmatter field: {field}"
                )

        if "Publisher Content Test Review" not in content:
            raise RuntimeError(
                "Generated article title is incorrect."
            )

        if "## Pros" not in content:
            raise RuntimeError(
                "Pros section was not generated."
            )

        if "## Cons" not in content:
            raise RuntimeError(
                "Cons section was not generated."
            )

        if "## Pricing" not in content:
            raise RuntimeError(
                "Pricing section was not generated."
            )

        if "## Sources" not in content:
            raise RuntimeError(
                "Sources section was not generated."
            )

        # -----------------------------------------------------
        # 4. Finish
        # -----------------------------------------------------

        print("\n[4/4] Verification complete")
        print("Generated file:", Path(output_file).name)
        print("Content length:", len(content))

    print()
    print("=" * 60)
    print("CONTENT BUILDER TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()