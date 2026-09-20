import json

from .review_store import ReviewStore


class ReviewQueue:
    name = "review_queue"
    version = "0.1.0"

    def __init__(self):
        self.store = ReviewStore()

    def list_pending(self):
        return self._list_by_status("pending")

    def list_approved(self):
        return self._list_by_status("approved")

    def list_rejected(self):
        return self._list_by_status("rejected")

    def _list_by_status(self, status: str):
        items = []

        for file_path in sorted(
            self.store.directory.glob("*.json")
        ):
            try:
                data = json.loads(
                    file_path.read_text(
                        encoding="utf-8"
                    )
                )

                if data.get("review_status") == status:
                    items.append(data)

            except (OSError, json.JSONDecodeError):
                continue

        return items
