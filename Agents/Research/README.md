# Research Agent v2

The Research Agent collects evidence for products listed in `affiliates.json`. It does not publish content.

Production flow:

1. Tavily search collects candidate sources.
2. Source validation removes malformed URLs and classifies sources.
3. A `ResearchPackage` is stored under `data/research_reviews/`.
4. New packages remain `pending` until reviewed.
5. GitHub Actions `Review Approval` changes the review status.
6. `PublisherAgent` can publish only approved, completed packages with the configured minimum number of sources.

The stored JSON is intentionally reviewable and committed to Git so approval survives between GitHub Actions runs.
