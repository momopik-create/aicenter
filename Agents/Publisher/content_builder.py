from future import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any

class ContentBuilder:
name = “content_builder”
version = “1.0.0”

def __init__(self, output_directory: str | Path | None = None):
    if output_directory is None:
        output_directory = (
            Path(__file__).resolve().parents[2]
            / "Content"
            / "Products"
        )
    self.output_directory = Path(output_directory)
    self.output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )
def build(self, research: Any) -> Path:
    product_name = research.product_name
    slug = self._slugify(product_name)
    title = self._build_title(product_name)
    description = self._build_description(research)
    rating = self._build_rating(research)
    date = datetime.now(timezone.utc).date().isoformat()
    pricing_tier = self._build_pricing_tier(research)
    body = self._build_body(research)
    content = self._build_markdown(
        title=title,
        description=description,
        rating=rating,
        date=date,
        pricing_tier=pricing_tier,
        body=body,
    )
    file_path = self.output_directory / f"{slug}.md"
    file_path.write_text(
        content,
        encoding="utf-8",
    )
    return file_path
def _build_title(self, product_name: str) -> str:
    return f"{product_name} Review"
def _build_description(self, research: Any) -> str:
    facts = getattr(research, "facts", []) or []
    if facts:
        description = str(facts[0]).strip()
        if description:
            return description[:300]
    return (
        f"An independent review of {research.product_name}, "
        "including features, pricing, pros, cons, and alternatives."
    )
def _build_rating(self, research: Any) -> float:
    """
    Do not invent a rating.
    Until the Decision Agent is enabled and a real scoring
    mechanism exists, use a neutral default value.
    """
    existing_rating = getattr(
        research,
        "rating",
        None,
    )
    if existing_rating is not None:
        try:
            rating = float(existing_rating)
            if 0 <= rating <= 5:
                return rating
        except (TypeError, ValueError):
            pass
    return 0.0
def _build_pricing_tier(self, research: Any) -> str:
    pricing = getattr(
        research,
        "pricing",
        [],
    ) or []
    if not pricing:
        return "Unknown"
    text = " ".join(
        str(item).lower()
        for item in pricing
    )
    if "free" in text:
        return "Free"
    if "paid" in text or "$" in text or "€" in text:
        return "Paid"
    return "Unknown"
def _build_body(self, research: Any) -> str:
    sections: list[str] = []
    sections.append(
        f"# {research.product_name} Review"
    )
    facts = getattr(
        research,
        "facts",
        [],
    ) or []
    if facts:
        sections.append("## Key Facts")
        sections.extend(
            f"- {fact}"
            for fact in facts
            if str(fact).strip()
        )
    pricing = getattr(
        research,
        "pricing",
        [],
    ) or []
    if pricing:
        sections.append("## Pricing")
        for item in pricing:
            if isinstance(item, dict):
                name = item.get("name") or item.get("tier")
                price = item.get("price")
                description = item.get("description")
                parts = [
                    value
                    for value in (
                        name,
                        price,
                        description,
                    )
                    if value
                ]
                if parts:
                    sections.append(
                        "- " + " — ".join(
                            str(value)
                            for value in parts
                        )
                    )
            else:
                sections.append(
                    f"- {item}"
                )
    pros = getattr(
        research,
        "pros",
        [],
    ) or []
    if pros:
        sections.append("## Pros")
        sections.extend(
            f"- {item}"
            for item in pros
            if str(item).strip()
        )
    cons = getattr(
        research,
        "cons",
        [],
    ) or []
    if cons:
        sections.append("## Cons")
        sections.extend(
            f"- {item}"
            for item in cons
            if str(item).strip()
        )
    sources = getattr(
        research,
        "sources",
        [],
    ) or []
    if sources:
        sections.append("## Sources")
        for source in sources:
            url = getattr(
                source,
                "url",
                None,
            )
            title = getattr(
                source,
                "title",
                None,
            )
            if url:
                label = title or url
                sections.append(
                    f"- [{label}]({url})"
                )
    return "\n\n".join(sections)
def _build_markdown(
    self,
    *,
    title: str,
    description: str,
    rating: float,
    date: str,
    pricing_tier: str,
    body: str,
) -> str:
    return f"""---

title: “{self._escape_yaml(title)}”
description: “{self._escape_yaml(description)}”
rating: {rating}
date: “{date}”
pricing_tier: “{self._escape_yaml(pricing_tier)}”

{body}
“””

@staticmethod
def _escape_yaml(value: str) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
        .strip()
    )
@staticmethod
def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value,
    )
    return value.strip("-")