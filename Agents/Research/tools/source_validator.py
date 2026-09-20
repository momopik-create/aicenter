from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class SourceValidationResult:
    url: str
    valid: bool
    source_type: str = "unknown"
    reason: str = ""


class SourceValidator:
    name = "source_validator"
    version = "0.2.0"

    def validate(self, url: str) -> SourceValidationResult:
        if not url or not url.strip():
            return SourceValidationResult(
                url=url,
                valid=False,
                reason="URL is empty.",
            )

        try:
            parsed = urlparse(url)

            if parsed.scheme not in ("http", "https"):
                return SourceValidationResult(
                    url=url,
                    valid=False,
                    reason="Unsupported URL scheme.",
                )

            if not parsed.netloc:
                return SourceValidationResult(
                    url=url,
                    valid=False,
                    reason="URL has no domain.",
                )

            domain = parsed.netloc.lower()

            # Basic classification only.
            # Deeper source verification will be added later.

            if domain.startswith("www."):
                domain = domain[4:]

            if domain.endswith(".gov"):
                source_type = "government"

            elif domain.endswith(".edu"):
                source_type = "education"

            elif domain.endswith(".org"):
                source_type = "organization"

            else:
                source_type = "website"

            return SourceValidationResult(
                url=url,
                valid=True,
                source_type=source_type,
            )

        except Exception as error:
            return SourceValidationResult(
                url=url,
                valid=False,
                reason=str(error),
            )
