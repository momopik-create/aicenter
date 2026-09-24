from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class ValidationResult:
    valid: bool
    source_type: str
    reason: str = ""


class SourceValidator:
    name = "source_validator"
    version = "2.0.0"

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

            hostname = (
                parsed.hostname or ""
            ).lower()

            if not hostname:
                return ValidationResult(
                    valid=False,
                    source_type="unknown",
                    reason="Missing hostname",
                )

            source_type = self._classify(
                hostname,
                parsed.path,
            )

            return ValidationResult(
                valid=True,
                source_type=source_type,
            )

        except Exception as error:
            return ValidationResult(
                valid=False,
                source_type="unknown",
                reason=str(error),
            )

    @staticmethod
    def _classify(
        hostname: str,
        path: str,
    ) -> str:

        path_lower = path.lower()

        if any(
            marker in path_lower
            for marker in (
                "pricing",
                "plans",
                "price",
            )
        ):
            return "pricing"

        if any(
            marker in path_lower
            for marker in (
                "docs",
                "documentation",
                "help",
            )
        ):
            return "documentation"

        if hostname.startswith(
            (
                "www.",
                "app.",
                "blog.",
            )
        ):
            return "website"

        return "website"