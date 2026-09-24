from __future__ import annotations

import json
from datetime import datetime, timezone

from Agents.Contracts.research import ResearchPackage, ResearchStatus, ReviewStatus, SourceEvidence
from Agents.Research.publish_gate import PublishGate
from Agents.Research.review_queue import ReviewQueue
from Agents.Research.review_store import ReviewStore

from .content_builder import ContentBuilder
from .schema import PublishResult


class PublisherAgent:
    name = "publisher"
    version = "1.0.0"

    def __init__(self, store=None, output_directory=None):
        self.store = store or ReviewStore()
        self.gate = PublishGate(self.store)
        self.queue = ReviewQueue(self.store)
        self.content_builder = ContentBuilder(output_directory=output_directory)

    def publish(self, product_name: str) -> PublishResult:
        try:
            data = self.store.load(product_name)
        except FileNotFoundError:
            return PublishResult(False, product_name, error="Research record not found.")

        if data.get("published") is True:
            return PublishResult(
                False,
                product_name,
                already_published=True,
                error="Item has already been published.",
            )

        if not self.gate.can_publish(product_name):
            return PublishResult(False, product_name, error="Publish rejected by Publish Gate.")

        try:
            research = self._to_package(data)
            content_file = self.content_builder.build(research)
            published_at = datetime.now(timezone.utc).isoformat()
            publication_id = (
                f"{self.store._safe_filename(product_name)}-"
                f"{int(datetime.now(timezone.utc).timestamp())}"
            )

            data.update(
                {
                    "published": True,
                    "published_at": published_at,
                    "publication_id": publication_id,
                    "publisher": self.name,
                    "publisher_version": self.version,
                    "content_file": str(content_file),
                }
            )
            self.store._file_path(product_name).write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            return PublishResult(
                success=True,
                product_name=product_name,
                published=True,
                publication_id=publication_id,
                published_at=published_at,
            )
        except Exception as exc:
            return PublishResult(False, product_name, error=f"Content generation failed: {exc}")

    def publish_approved(self) -> list[PublishResult]:
        results = []
        for record in self.queue.list_approved():
            product_name = record.get("product_name")
            if product_name:
                results.append(self.publish(product_name))
        return results

    @staticmethod
    def _to_package(data: dict) -> ResearchPackage:
        sources = [
            SourceEvidence(
                url=source.get("url", ""),
                title=source.get("title", ""),
                source_type=source.get("source_type", "unknown"),
                excerpt=source.get("excerpt"),
                reliability_score=source.get("reliability_score"),
            )
            for source in data.get("sources", [])
            if isinstance(source, dict)
        ]
        return ResearchPackage(
            product_name=data.get("product_name", ""),
            product_url=data.get("product_url", ""),
            status=ResearchStatus(data.get("status", ResearchStatus.COMPLETED.value)),
            sources=sources,
            facts=data.get("facts", []),
            pricing=data.get("pricing", []),
            pros=data.get("pros", []),
            cons=data.get("cons", []),
            review_status=ReviewStatus(data.get("review_status", ReviewStatus.APPROVED.value)),
            review_note=data.get("review_note"),
        )
