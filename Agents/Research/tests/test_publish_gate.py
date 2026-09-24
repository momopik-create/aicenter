from Agents.Contracts.research import ResearchPackage, ResearchStatus, ReviewStatus, SourceEvidence
from Agents.Research.publish_gate import PublishGate
from Agents.Research.review import ResearchReview
from Agents.Research.review_store import ReviewStore

PRODUCT_NAME = "publish_gate_test"


def main():
    store = ReviewStore(directory="/tmp/aicenter-publish-gate")
    review = ResearchReview(store)
    gate = PublishGate(store)

    sources = [
        SourceEvidence("https://example.com/1", "Example 1", "website"),
        SourceEvidence("https://example.com/2", "Example 2", "documentation"),
        SourceEvidence("https://example.com/3", "Example 3", "pricing"),
    ]
    package = ResearchPackage(
        product_name=PRODUCT_NAME,
        product_url="https://example.com",
        status=ResearchStatus.COMPLETED,
        sources=sources,
        review_status=ReviewStatus.PENDING,
    )
    file_path = store.save(package)

    assert not gate.can_publish(PRODUCT_NAME)
    review.approve(PRODUCT_NAME, "test approval")
    assert gate.can_publish(PRODUCT_NAME)
    review.reject(PRODUCT_NAME, "test rejection")
    assert not gate.can_publish(PRODUCT_NAME)

    if file_path.exists():
        file_path.unlink()
    print("Publish Gate test: PASSED")


if __name__ == "__main__":
    main()
