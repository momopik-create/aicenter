import json

from Agents.Research.review import ResearchReview
from Agents.Research.review_store import ReviewStore
from Agents.Research.schema import ResearchResult, ResearchStatus


def main():
    store = ReviewStore()

    result = ResearchResult(
        product_name="__review_test__",
        url="https://example.com",
        status=ResearchStatus.COMPLETED,
        sources=[],
    )

    store.save(result)

    review = ResearchReview()

    review.approve(
        "__review_test__",
        note="Test approval",
    )

    file_path = (
        store.directory / "__review_test__.json"
    )

    data = json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )

    print("After approval:")
    print("Status:", data["review_status"])
    print("Note:", data["review_note"])

    if data["review_status"] != "approved":
        raise RuntimeError(
            "Approval test failed."
        )

    review.reject(
        "__review_test__",
        note="Test rejection",
    )

    data = json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )

    print()
    print("After rejection:")
    print("Status:", data["review_status"])
    print("Note:", data["review_note"])

    if data["review_status"] != "rejected":
        raise RuntimeError(
            "Rejection test failed."
        )

    file_path.unlink()

    print()
    print("Research Review test: PASSED")


if __name__ == "__main__":
    main()
