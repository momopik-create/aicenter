import json

from Agents.Contracts.research import ReviewStatus

from .review_store import ReviewStore


class ResearchReview:
    name = "research_review"
    version = "1.0.0"

    def __init__(self):
        self.store = ReviewStore()

    def approve(
        self,
        product_name: str,
        note: str = None,
    ):
        return self._set_status(
            product_name=product_name,
            status=ReviewStatus.APPROVED,
            note=note,
        )

    def reject(
        self,
        product_name: str,
        note: str = None,
    ):
        return self._set_status(
            product_name=product_name,
            status=ReviewStatus.REJECTED,
            note=note,
        )

    def pending(
        self,
        product_name: str,
        note: str = None,
    ):
        return self._set_status(
            product_name=product_name,
            status=ReviewStatus.PENDING,
            note=note,
        )

    def _set_status(
        self,
        product_name: str,
        status: ReviewStatus,
        note: str = None,
    ):
        file_path = self._get_file(product_name)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Research review not found: {product_name}"
            )

        data = json.loads(
            file_path.read_text(
                encoding="utf-8",
            )
        )

        data["review_status"] = status.value
        data["review_note"] = note

        file_path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return file_path

    def _get_file(self, product_name: str):
        file_name = self.store._safe_filename(
            product_name
        )

        return (
            self.store.directory
            / f"{file_name}.json"
        )