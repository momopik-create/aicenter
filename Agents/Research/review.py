from .review_store import ReviewStore
from .schema import ReviewStatus


class ResearchReview:
    name = "research_review"
    version = "0.1.0"

    def __init__(self):
        self.store = ReviewStore()

    def approve(
        self,
        product_name: str,
        note: str = None,
    ):
        return self.store.update_status(
            product_name=product_name,
            status=ReviewStatus.APPROVED,
            note=note,
        )

    def reject(
        self,
        product_name: str,
        note: str = None,
    ):
        return self.store.update_status(
            product_name=product_name,
            status=ReviewStatus.REJECTED,
            note=note,
        )
