"""Backward-compatible aliases for the v2 Research contracts.

The canonical contracts live in ``Agents.Contracts.research``.
"""

from Agents.Contracts.research import (
    ResearchPackage,
    ResearchStatus,
    ReviewStatus,
    SourceEvidence,
)

ResearchResult = ResearchPackage
ResearchSource = SourceEvidence

__all__ = [
    "ResearchPackage",
    "ResearchResult",
    "ResearchStatus",
    "ReviewStatus",
    "SourceEvidence",
    "ResearchSource",
]
