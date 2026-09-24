from __future__ import annotations

import json
import os
from pathlib import Path

from Agents.Contracts.research import ResearchStatus
from Agents.Contracts.research_input import ResearchInput
from Agents.Research.pipeline import ResearchPipeline
from Agents.Research.review_store import ReviewStore


ROOT = Path(__file__).resolve().parents[1]
AFFILIATES_FILE = ROOT / "affiliates.json"


def load_affiliates() -> dict[str, str]:
    data = json.loads(AFFILIATES_FILE.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if k != "default" and isinstance(v, str) and v.strip()}


def main() -> None:
    affiliates = load_affiliates()
    store = ReviewStore()
    force = os.getenv("FORCE_RESEARCH", "false").lower() == "true"

    for name, url in affiliates.items():
        try:
            existing = store.load(name)
            if not force:
                status = existing.get("review_status", "pending")
                if existing.get("published") is True:
                    print(f"SKIP published: {name}")
                else:
                    print(f"SKIP existing ({status}): {name}")
                continue
        except FileNotFoundError:
            # Existing live content is treated as already launched.
            # Do not replace it with a newly generated draft on the first v2 run.
            slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-")
            existing_content = ROOT / "src" / "content" / "products" / f"{slug}.md"
            if existing_content.exists() and not force:
                print(f"SKIP existing site content: {name}")
                continue

        print(f"Researching: {name}")
        result = ResearchPipeline().run(
            ResearchInput(product_name=name, url=url)
        )
        print(f"  status={result.status.value}, sources={len(result.sources)}")
        if result.status != ResearchStatus.COMPLETED:
            print(f"  note={result.review_note or 'research failed'}")


if __name__ == "__main__":
    main()
