from Agents.Contracts.research import ReviewStatus

from .review_store import ReviewStore


class ResearchReview:
    name = "research_review"
    version = "2.0.0"

    def __init__(self, store=None):
        self.store = store or ReviewStore()

    def approve(self, product_name: str, note: str = None):
        return self._set_status(product_name, ReviewStatus.APPROVED, note)

    def reject(self, product_name: str, note: str = None):
        return self._set_status(product_name, ReviewStatus.REJECTED, note)

    def pending(self, product_name: str, note: str = None):
        return self._set_status(product_name, ReviewStatus.PENDING, note)

    def _set_status(self, product_name, status, note):
        return self.store.update_status(product_name, status, note)
