from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from .review import ReviewStatus
from .review_store import ReviewStore
from .schema import ResearchStatus


class PublishGate:
    """
    Final safety gate before a research result can be published.

    Publishing is allowed only when:
    - a review record exists
    - the review is approved
    - research completed successfully
    - a product URL exists
    - at least one research source exists
    """

    def __init__(self, store: ReviewStore | None = None) -> None:
        self.store = store or ReviewStore()

    def _get_file(self, product_name: str) -> Path:
        return (
            self.store.directory
            / f"{self.store._safe_filename(product_name)}.json"
        )

    def _load(self, file_path: Path) -> dict[str, Any]:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def can_publish(self, product_name: str) -> bool:
        file_path = self._get_file(product_name)

        # 1. A review record must exist.
        if not file_path.exists():
            return False

        data = self._load(file_path)

        # 2. Human/Review approval is mandatory.
        if (
            data.get("review_status")
            != ReviewStatus.APPROVED.value
        ):
            return False

        # 3. Research itself must have completed successfully.
        if (
            data.get("status")
            != ResearchStatus.COMPLETED.value
        ):
            return False

        # 4. Product URL is mandatory.
        # The canonical field in Research is "product_url".
        if not data.get("product_url"):
            return False

        # 5. At least one research source is mandatory.
        sources = data.get("sources", [])

        if not sources:
            return False

        return True