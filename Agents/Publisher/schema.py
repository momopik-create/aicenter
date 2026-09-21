from dataclasses import dataclass
from typing import Optional


@dataclass
class PublishResult:
    success: bool
    product_name: str
    published: bool = False
    already_published: bool = False
    error: Optional[str] = None
