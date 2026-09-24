from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SEOResult:
    title: str

    meta_description: str

    slug: str

    primary_keyword: Optional[str] = None

    secondary_keywords: List[str] = field(
        default_factory=list
    )

    headings: List[str] = field(
        default_factory=list
    )

    internal_links: List[str] = field(
        default_factory=list
    )

    schema_type: Optional[str] = None

    score: Optional[float] = None

