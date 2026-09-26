from .review_store import ReviewStore


class ReviewQueue:
    name = "review_queue"
    version = "1.0.0"

    def __init__(self, store=None):
        self.store = store or ReviewStore()

    def list_pending(self):
        return self._list_by_status("pending")

    def list_approved(self):
        return [
            item
            for item in self._list_by_status("approved")
            if item.get("published") is not True
        ]

    def list_rejected(self):
        return self._list_by_status("rejected")

    def _list_by_status(self, status: str):
        return [item for item in self.store.list_all() if item.get("review_status") == status]
