from dataclasses import dataclass
from typing import Optional


@dataclass
class ResearchInput:
    product_name: str
    url: Optional[str] = None
