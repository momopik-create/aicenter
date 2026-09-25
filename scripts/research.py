from __future__ import annotations

import argparse
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
    return {
        key: value
        for key, value in data.items()
        if key != "default" and isinstance(value, str) and value.strip()
    }


def slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run product research.")
    parser.add_argument(
        "--product",
        default=os.getenv("RESEARCH_PRODUCT", "").strip(),
        help="Affiliate product key. If omitted, process the normal batch.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=os.getenv("FORCE_RESEARCH", "false").lower() == "true",
        help="Research even when a review or live content already exists.",
    )
    return parser.parse_args()


def should_skip(name: str, store: ReviewStore, force: bool, explicit_product: bool) -> bool:
    # An explicitly requested product is always allowed to run. This is what
    # makes the manual GitHub Actions test useful for already-published seeds.
    if force or explicit_product:
        return False

    try:
        existing = store.load(name)
    except FileNotFoundError:
        existing_content = ROOT / "src" / "content" / "products" / f"{slugify(name)}.md"
        if existing_content.exists():
            print(f"SKIP existing site content: {name}")
            return True
        return False

    status = existing.get("review_status", "pending")
    if existing.get("published") is True:
        print(f"SKIP published: {name}")
    else:
        print(f"SKIP existing ({status}): {name}")
    return True


def main() -> None:
    args = parse_args()
    affiliates = load_affiliates()
    store = ReviewStore()

    if args.product:
        if args.product not in affiliates:
            available = ", ".join(sorted(affiliates))
            raise SystemExit(
                f"Unknown product '{args.product}'. Available products: {available}"
            )
        targets = {args.product: affiliates[args.product]}
    else:
        targets = affiliates

    failures = 0
    for name, url in targets.items():
        if should_skip(name, store, args.force, bool(args.product)):
            continue

        print(f"Researching: {name}")
        result = ResearchPipeline().run(
            ResearchInput(product_name=name, url=url)
        )
        print(
            f"  status={result.status.value}, "
            f"sources={len(result.sources)}, "
            f"facts={len(result.facts)}, "
            f"pricing={len(result.pricing)}"
        )

        if result.status != ResearchStatus.COMPLETED:
            failures += 1
            print(f"  note={result.review_note or 'research failed'}")
        else:
            print(f"  review_status={result.review_status.value}")

    if failures:
        raise SystemExit(f"Research failed for {failures} product(s).")


if __name__ == "__main__":
    main()
