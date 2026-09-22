import json
from datetime import datetime, timezone

from Agents.Research.publish_gate import PublishGate

from .content_builder import ContentBuilder
from .schema import PublishResult


class PublisherAgent:
    name = "publisher"
    version = "0.4.0"

    def __init__(self):
        self.gate = PublishGate()
        self.content_builder = ContentBuilder()

    def publish(
        self,
        product_name: str,
    ) -> PublishResult:

        # --------------------------------------------------
        # 1. Find research record
        # --------------------------------------------------

        file_path = self.gate._get_file(product_name)

        if not file_path.exists():
            return PublishResult(
                success=False,
                product_name=product_name,
                error="Research record not found.",
            )

        # --------------------------------------------------
        # 2. Load research record
        # --------------------------------------------------

        try:
            data = json.loads(
                file_path.read_text(
                    encoding="utf-8"
                )
            )
        except (json.JSONDecodeError, OSError) as exc:
            return PublishResult(
                success=False,
                product_name=product_name,
                error=f"Failed to read research record: {exc}",
            )

        # --------------------------------------------------
        # 3. Prevent duplicate publication
        # --------------------------------------------------

        if data.get("published") is True:
            return PublishResult(
                success=False,
                product_name=product_name,
                published=False,
                already_published=True,
                error="Item has already been published.",
            )

        # --------------------------------------------------
        # 4. Check Publish Gate
        # --------------------------------------------------

        if not self.gate.can_publish(product_name):
            return PublishResult(
                success=False,
                product_name=product_name,
                published=False,
                error="Publish rejected by Publish Gate.",
            )

        # --------------------------------------------------
        # 5. Build Astro content
        # --------------------------------------------------

        try:
            from Agents.Contracts.research import (
                ResearchPackage,
                ResearchStatus,
                ReviewStatus,
                SourceEvidence,
            )

            sources = [
                SourceEvidence(
                    url=source.get("url", ""),
                    title=source.get("title", ""),
                    source_type=source.get(
                        "source_type",
                        "unknown",
                    ),
                    excerpt=source.get("excerpt"),
                    reliability_score=source.get(
                        "reliability_score"
                    ),
                )
                for source in data.get(
                    "sources",
                    [],
                )
                if isinstance(source, dict)
            ]

            research = ResearchPackage(
                product_name=data.get(
                    "product_name",
                    product_name,
                ),
                product_url=data.get(
                    "product_url",
                    "",
                ),
                status=ResearchStatus(
                    data.get(
                        "status",
                        ResearchStatus.COMPLETED.value,
                    )
                ),
                sources=sources,
                facts=data.get(
                    "facts",
                    [],
                ),
                pricing=data.get(
                    "pricing",
                    [],
                ),
                pros=data.get(
                    "pros",
                    [],
                ),
                cons=data.get(
                    "cons",
                    [],
                ),
                review_status=ReviewStatus(
                    data.get(
                        "review_status",
                        ReviewStatus.APPROVED.value,
                    )
                ),
                review_note=data.get(
                    "review_note"
                ),
            )

            content_file = self.content_builder.build(
                research
            )

        except Exception as exc:
            return PublishResult(
                success=False,
                product_name=product_name,
                published=False,
                error=(
                    "Content generation failed: "
                    f"{exc}"
                ),
            )

        # --------------------------------------------------
        # 6. Generate publication metadata
        # --------------------------------------------------

        published_at = datetime.now(
            timezone.utc
        ).isoformat()

        publication_id = (
            f"{product_name.lower().replace(' ', '-')}"
            f"-"
            f"{int(datetime.now(timezone.utc).timestamp())}"
        )

        # --------------------------------------------------
        # 7. Mark research record as published
        # --------------------------------------------------

        data["published"] = True
        data["published_at"] = published_at
        data["publication_id"] = publication_id
        data["publisher"] = self.name
        data["publisher_version"] = self.version
        data["content_file"] = str(content_file)

        file_path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        # --------------------------------------------------
        # 8. Return successful result
        # --------------------------------------------------

        return PublishResult(
            success=True,
            product_name=product_name,
            published=True,
            publication_id=publication_id,
            published_at=published_at,
        )
