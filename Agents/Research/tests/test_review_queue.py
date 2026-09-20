from Agents.Research.review import ResearchReview
from Agents.Research.review_queue import ReviewQueue
from Agents.Research.review_store import ReviewStore
from Agents.Research.schema import (
    ResearchResult,
    ResearchStatus,
)


def main():
    store = ReviewStore()
    review = ResearchReview()
    queue = ReviewQueue()

    test_products = [
        "queue_test_one",
        "queue_test_two",
        "queue_test_three",
    ]

    files = []

    for product in test_products:
        result = ResearchResult(
            product_name=product,
            url="https://example.com",
            status=ResearchStatus.COMPLETED,
            sources=[],
        )

        files.append(store.save(result))

    review.approve(
        "queue_test_two",
        note="Approved test",
    )

    review.reject(
        "queue_test_three",
        note="Rejected test",
    )

    pending = queue.list_pending()
    approved = queue.list_approved()
    rejected = queue.list_rejected()

    pending_names = {
        item["product_name"]
        for item in pending
    }

    approved_names = {
        item["product_name"]
        for item in approved
    }

    rejected_names = {
        item["product_name"]
        for item in rejected
    }

    print("Pending:", pending_names)
    print("Approved:", approved_names)
    print("Rejected:", rejected_names)

    if "queue_test_one" not in pending_names:
        raise RuntimeError(
            "Pending queue test failed."
        )

    if "queue_test_two" not in approved_names:
        raise RuntimeError(
            "Approved queue test failed."
        )

    if "queue_test_three" not in rejected_names:
        raise RuntimeError(
            "Rejected queue test failed."
        )

    for file_path in files:
        file_path.unlink()

    print()
    print("Review Queue test: PASSED")


if __name__ == "__main__":
    main()
