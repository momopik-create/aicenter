import json
from pathlib import Path

from Agents.Publisher.agent import PublisherAgent
from Agents.Research.publish_gate import PublishGate
from Agents.Research.review_store import ReviewStore
from Agents.Contracts.research import (
ResearchPackage,
ResearchStatus,
ReviewStatus,
)

def main():
print(”=” * 60)
print(“CONTENT PUBLISH TEST”)
print(”=” * 60)

product_name = "Publisher Content Test"
product_url = "https://example.com"
store = ReviewStore()
# ---------------------------------------------------------
# 1. Create approved research record
# ---------------------------------------------------------
print("\n[1/5] Creating research record")
research = ResearchPackage(
    product_name=product_name,
    product_url=product_url,
    status=ResearchStatus.COMPLETED,
    facts=[
        "Example product used for publisher integration testing."
    ],
    pricing=[
        {
            "name": "Pro",
            "price": "$19/month",
        }
    ],
    pros=[
        "Easy to use",
        "Useful for testing",
    ],
    cons=[
        "Test data only",
    ],
    review_status=ReviewStatus.APPROVED,
)
research_file = store.save(research)
print(f"Research file: {research_file}")
# ---------------------------------------------------------
# 2. Verify Publish Gate
# ---------------------------------------------------------
print("\n[2/5] Checking Publish Gate")
gate = PublishGate(store)
if not gate.can_publish(product_name):
    raise RuntimeError(
        "Publish Gate rejected valid test research."
    )
print("Publish Gate: ALLOWED")
# ---------------------------------------------------------
# 3. Publish
# ---------------------------------------------------------
print("\n[3/5] Publishing content")
publisher = PublisherAgent()
result = publisher.publish(product_name)
print("Success:", result.success)
print("Published:", result.published)
print("Error:", result.error)
if not result.success:
    raise RuntimeError(
        f"Publisher failed: {result.error}"
    )
# ---------------------------------------------------------
# 4. Verify Astro content
# ---------------------------------------------------------
print("\n[4/5] Verifying Astro content")
content_file = (
    Path(__file__).resolve().parents[2]
    .parent
    / "Content"
    / "Products"
    / "publisher-content-test.md"
)
print(f"Content file: {content_file}")
if not content_file.exists():
    raise RuntimeError(
        "Publisher did not create Astro content file."
    )
content = content_file.read_text(
    encoding="utf-8"
)
print("Content file created.")
print(f"Content length: {len(content)}")
required_fields = [
    'title:',
    'description:',
    'rating:',
    'date:',
    'pricing_tier:',
]
for field in required_fields:
    if field not in content:
        raise RuntimeError(
            f"Missing frontmatter field: {field}"
        )
if "Publisher Content Test Review" not in content:
    raise RuntimeError(
        "Generated title is incorrect."
    )
# ---------------------------------------------------------
# 5. Cleanup
# ---------------------------------------------------------
print("\n[5/5] Cleaning up")
if research_file.exists():
    research_file.unlink()
if content_file.exists():
    content_file.unlink()
print("Temporary files removed.")
print("\n" + "=" * 60)
print("CONTENT PUBLISH TEST: PASSED")
print("=" * 60)

if name == “main”:
main()