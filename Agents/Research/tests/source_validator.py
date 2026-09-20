from dataclasses import dataclass
from typing import Optional


@dataclass
class SourceValidationResult:
    url: str
    valid: bool
    source_type: str = "unknown"
    reason: Optional[str] = None


class SourceValidator:
    name = "source_validator"
    version = "0.1.0"

    def validate(self, url: str) -> SourceValidationResult:
        """
        Validate a research source.

        The real validation logic will be added later.
        """

        if not url.strip():
            return SourceValidationResult(
                url=url,
                valid=False,
                reason="URL is empty.",
            )

        return SourceValidationResult(
            url=url,
            valid=False,
            source_type="unknown",
            reason="Source validation is not configured yet.",
        )
