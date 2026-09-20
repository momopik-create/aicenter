from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PublishStatus(str, Enum):
    BLOCKED = "blocked"
    READY = "ready"
    PUBLISHED = "published"
    FAILED = "failed"


@dataclass
class PublishRequest:
    product_name: str

    slug: str

    content: str

    approved: bool

    seo_ready: bool

    factcheck_passed: bool


@dataclass
class PublishResult:
    status: PublishStatus

    product_name: str

    path: Optional[str] = None

    commit_sha: Optional[str] = None

    error: Optional[str] = None
