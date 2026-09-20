from dataclasses import dataclass, field
from typing import List


@dataclass
class ResearchResult:
    product_name: str
    url: str
    summary: str = ""
    sources: List[str] = field(default_factory=list)
