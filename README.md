# AI Center

AI Center is an Astro affiliate review site backed by a small research and publishing pipeline.

## Production flow

1. `Research Agent` researches products listed in `affiliates.json` and saves review records under `data/research_reviews/`.
2. New research remains `pending` until reviewed.
3. `Review Approval` approves or rejects a product from GitHub Actions.
4. `Publisher Agent` publishes only records that pass the Publish Gate.
5. A Git push triggers the site deployment on the hosting platform.

## Required GitHub secret

- `TAVILY_API_KEY`

The Decision Agent is intentionally disabled for the MVP and does not block publication.
