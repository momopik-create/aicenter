from dataclasses import dataclass
from typing import Optional


@dataclass
class FetchResult:
    url: str
    content: str
    title: str = ""
    success: bool = True
    error: Optional[str] = None


class WebFetchTool:
    name = "web_fetch"
    version = "0.1.0"

    def fetch(self, url: str) -> FetchResult:
        """
        Fetch and extract readable content from a webpage.

        This is currently a placeholder.
        The actual HTTP/browser implementation will be added later.
        """

        if not url.strip():
            return FetchResult(
                url=url,
                content="",
                success=False,
                error="URL is empty.",
            )

        return FetchResult(
            url=url,
            content="",
            success=False,
            error="Web fetch provider is not configured.",
        )
