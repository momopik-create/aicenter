from __future__ import annotations

from Agents.Contracts.research import ResearchStatus, ReviewStatus

from .config import ResearchConfig
from .review_store import ReviewStore


class PublishGate:
    """Final safety gate before publication."""

    name = "publish_gate"
    version = "2.1.0"

    def __init__(self, store: ReviewStore | None = None) -> None:
        self.store = store or ReviewStore()

    def can_publish(self, product_name: str) -> bool:
        try:
            data = self.store.load(product_name)
        except FileNotFoundError:
            return False

        if data.get("published") is True:
            return False
        if data.get("review_status") != ReviewStatus.APPROVED.value:
            return False
        if data.get("status") != ResearchStatus.COMPLETED.value:
            return False
        if not str(data.get("product_url", "")).strip():
            return False

        sources = data.get("sources", [])
        if not isinstance(sources, list):
            return False

        valid_sources = [
            source
            for source in sources
            if isinstance(source, dict)
            and str(source.get("url", "")).strip()
        ]
        return len(valid_sources) >= ResearchConfig.MIN_SOURCES
