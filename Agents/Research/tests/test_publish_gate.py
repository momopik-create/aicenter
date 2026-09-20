from Agents.Research.publish_gate import PublishGate
from Agents.Research.review import ResearchReview
from Agents.Research.review_store import ReviewStore
from Agents.Research.schema import (
    ResearchResult,
    ResearchStatus,
)
from Agents.Research.source import ResearchSource


PRODUCT_NAME = "publish_gate_test"


def main():
    store = ReviewStore()
    review = ResearchReview()
    gate = PublishGate()

    source = ResearchSource(
        url="https://example.com",
        title="Example",
        source_type="website",
        checked_at=None,
    )

    result = ResearchResult(
        product_name=PRODUCT_NAME,
        url="https://example.com",
        status=ResearchStatus.COMPLETED,
        sources=[source],
    )

    file_path = store.save(result)

    print(
        "Before approval:",
        gate.can_publish(PRODUCT_NAME),
    )

    if gate.can_publish(PRODUCT_NAME):
        raise RuntimeError(
            "Publish Gate allowed an unapproved item."
        )

    review.approve(
        PRODUCT_NAME,
        note="Publish gate test approval",
    )

    print(
        "After approval:",
        gate.can_publish(PRODUCT_NAME),
    )

    if not gate.can_publish(PRODUCT_NAME):
        raise RuntimeError(
            "Publish Gate rejected a valid approved item."
        )

    review.reject(
        PRODUCT_NAME,
        note="Publish gate rejection test",
    )

    print(
        "After rejection:",
        gate.can_publish(PRODUCT_NAME),
    )

    if gate.can_publish(PRODUCT_NAME):
        raise RuntimeError(
            "Publish Gate allowed a rejected item."
        )

    file_path.unlink()

    print()
    print("Publish Gate test: PASSED")


if __name__ == "__main__":
    main()
