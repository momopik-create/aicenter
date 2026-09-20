from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class ValidationResult:
    valid: bool
    source_type: str
    reason: str = ""


class SourceValidator:
    name = "source_validator"
    version = "1.0.0"

    def validate(
        self,
        url: str,
    ) -> ValidationResult:

        if not url:
            return ValidationResult(
                valid=False,
                source_type="unknown",
                reason="Empty URL",
            )

        try:
            parsed = urlparse(url)

            if parsed.scheme not in (
                "http",
                "https",
            ):
                return ValidationResult(
                    valid=False,
                    source_type="unknown",
                    reason="Invalid URL scheme",
                )

            if not parsed.netloc:
                return ValidationResult(
                    valid=False,
                    source_type="unknown",
                    reason="Missing domain",
                )

            return ValidationResult(
                valid=True,
                source_type="website",
            )

        except Exception as error:
            return ValidationResult(
                valid=False,
                source_type="unknown",
                reason=str(error),
            )
