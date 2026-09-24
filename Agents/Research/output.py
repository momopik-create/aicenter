from dataclasses import dataclass
from typing import Optional

from Agents.Contracts.research import ResearchPackage


@dataclass
class ResearchOutput:
    """Compatibility wrapper for callers expecting a success envelope."""

    success: bool
    result: Optional[ResearchPackage] = None
    error: Optional[str] = None
