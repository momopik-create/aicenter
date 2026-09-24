import json

from Agents.Research.review import ResearchReview
from Agents.Research.review_store import ReviewStore
from Agents.Contracts.research import ResearchPackage, ResearchStatus


PRODUCT_NAME = "review_test_product"


def main():
    store = ReviewStore()

    result = ResearchPackage(
        product_name=PRODUCT_NAME,
        product_url="https://example.com",
        status=ResearchStatus.COMPLETED,
        sources=[],
    )

    file_path = store.save(result)

    print("Review file:")
    print(file_path)

    review = ResearchReview()

    review.approve(
        PRODUCT_NAME,
        note="Test approval",
    )

    data = json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )

    print()
    print("After approval:")
    print("Status:", data["review_status"])
    print("Note:", data["review_note"])

    if data["review_status"] != "approved":
        raise RuntimeError(
            "Approval test failed."
        )

    review.reject(
        PRODUCT_NAME,
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
