from dataclasses import dataclass
from typing import Optional


@dataclass
class PublishResult:
    success: bool
    product_name: str
    published: bool = False
    already_published: bool = False
    publication_id: Optional[str] = None
    published_at: Optional[str] = None
    error: Optional[str] = None