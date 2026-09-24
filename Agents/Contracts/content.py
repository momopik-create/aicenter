from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ContentStatus(str, Enum):
    DRAFT = "draft"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ContentPackage:
    product_name: str

    title: str

    slug: str

    content: str

    status: ContentStatus

    summary: Optional[str] = None

    pros: List[str] = field(
        default_factory=list
    )

    cons: List[str] = field(
        default_factory=list
    )

    faq: List[dict] = field(
        default_factory=list
    )

    source_urls: List[str] = field(
        default_factory=list
    )

    review_status: str = "pending"