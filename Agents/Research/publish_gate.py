from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from Agents.Contracts.research import (
    ResearchStatus,
    ReviewStatus,
)

from .review_store import ReviewStore


class PublishGate:
    """
    Final safety gate before publication.

    Publishing requires:
    - an existing research record
    - approved review status
    - completed research
    - a product URL
    - at least one source
    """

    name = "publish_gate"
    version = "2.0.0"

    def __init__(
        self,
        store: ReviewStore | None = None,
    ) -> None:
        self.store = store or ReviewStore()

    def _get_file(
        self,
        product_name: str,
    ) -> Path:
        return (
            self.store.directory
            / f"{self.store._safe_filename(product_name)}.json"
        )

    def _load(
        self,
        file_path: Path,
    ) -> dict[str, Any]:
        with file_path.open(
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    def can_publish(
        self,
        product_name: str,
    ) -> bool:
        file_path = self._get_file(product_name)

        if not file_path.exists():
            return False

        data = self._load(file_path)

        if (
            data.get("review_status")
            != ReviewStatus.APPROVED.value
        ):
            return False

        if (
            data.get("status")
            != ResearchStatus.COMPLETED.value
        ):
            return False

        if not data.get("product_url"):
            return False

        sources = data.get("sources", [])

        if not isinstance(
            sources,
            list,
        ):
            return False

        if not sources:
            return False

        return True