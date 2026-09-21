from Agents.Contracts.research import (
    ResearchPackage,
    ResearchStatus,
    ReviewStatus,
    SourceEvidence,
)
from Agents.Research.publish_gate import PublishGate
from Agents.Research.review import ResearchReview
from Agents.Research.review_store import ReviewStore


PRODUCT_NAME = "publish_gate_test"


def main():
    print("=" * 60)
    print("PUBLISH GATE TEST")
    print("=" * 60)

    store = ReviewStore()
    review = ResearchReview()
    gate = PublishGate()

    package = ResearchPackage(
        product_name=PRODUCT_NAME,
        product_url="https://example.com",
        status=ResearchStatus.COMPLETED,
        sources=[
            SourceEvidence(
                url="https://example.com",
                title="Example",
                source_type="website",
                excerpt="Example source.",
                reliability_score=1.0,
            )
        ],
        review_status=ReviewStatus.PENDING,
    )

    file_path = store.save(package)

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

    if file_path.exists():
        file_path.unlink()

    print()
    print("=" * 60)
    print("PUBLISH GATE TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()