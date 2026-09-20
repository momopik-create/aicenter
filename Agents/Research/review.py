from .audit import AuditLog
from .review_store import ReviewStore
from .schema import ReviewStatus


class ResearchReview:
    name = "research_review"
    version = "0.2.0"

    def __init__(self):
        self.store = ReviewStore()
        self.audit = AuditLog()

    def approve(
        self,
        product_name: str,
        note: str = None,
    ):
        result = self.store.update_status(
            product_name=product_name,
            status=ReviewStatus.APPROVED,
            note=note,
        )

        self.audit.record(
            product_name=product_name,
            action="approved",
            note=note,
        )

        return result

    def reject(
        self,
        product_name: str,
        note: str = None,
    ):
        result = self.store.update_status(
            product_name=product_name,
            status=ReviewStatus.REJECTED,
            note=note,
        )

        self.audit.record(
            product_name=product_name,
            action="rejected",
            note=note,
        )

        return result
