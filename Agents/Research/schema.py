from dataclasses import dataclass, field
from typing import List


@dataclass
class ResearchResult:
    product_name: str
    url: str

    description: str = ""
    features: List[str] = field(default_factory=list)
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)

    sources: List[str] = field(default_factory=list)

    status: str = "pending"
