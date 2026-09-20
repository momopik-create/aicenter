from .review_store import ReviewStore
from .schema import ReviewStatus


class PublishGate:
    name = "publish_gate"
    version = "0.1.0"

    def __init__(self):
        self.store = ReviewStore()

    def can_publish(self, product_name: str) -> bool:
        file_name = self.store._safe_filename(
            product_name
        )

        file_path = (
            self.store.directory
            / f"{file_name}.json"
        )

        if not file_path.exists():
            return False

        data = self._load(file_path)

        return (
            data.get("review_status")
            == ReviewStatus.APPROVED.value
        )

    @staticmethod
    def _load(file_path):
        import json

        return json.loads(
            file_path.read_text(
                encoding="utf-8"
            )
        )
