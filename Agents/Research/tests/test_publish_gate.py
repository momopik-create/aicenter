import json

from Agents.Contracts.research import (
    ResearchStatus,
    ReviewStatus,
)

from .review_store import ReviewStore


class PublishGate:
    name = "publish_gate"
    version = "1.0.0"

    def __init__(self):
        self.store = ReviewStore()

    def can_publish(
        self,
        product_name: str,
    ) -> bool:

        file_path = self._get_file(
            product_name
        )

        if not file_path.exists():
            return False

        data = self._load(file_path)

        if data.get("status") != (
            ResearchStatus.COMPLETED.value
        ):
            return False

        if data.get("review_status") != (
            ReviewStatus.APPROVED.value
        ):
            return False

        if not data.get("product_url"):
            return False

        sources = data.get(
            "sources",
            [],
        )

        if not sources:
            return False

        return True

    def _get_file(
        self,
        product_name: str,
    ):
        file_name = self.store._safe_filename(
            product_name
        )

        return (
            self.store.directory
            / f"{file_name}.json"
        )

    @staticmethod
    def _load(file_path):
        return json.loads(
            file_path.read_text(
                encoding="utf-8",
            )
        )