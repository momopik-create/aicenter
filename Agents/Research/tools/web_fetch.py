from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class FetchResult:
    url: str
    content: str
    title: str = ""
    success: bool = True
    error: Optional[str] = None


class WebFetchTool:
    name = "web_fetch"
    version = "0.2.0"

    def fetch(self, url: str) -> FetchResult:
        if not url or not url.strip():
            return FetchResult(
                url=url,
                content="",
                success=False,
                error="URL is empty.",
            )

        try:
            response = requests.get(
                url,
                timeout=20,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(compatible; MomopikResearchBot/1.0)"
                    )
                },
            )

            response.raise_for_status()

            return FetchResult(
                url=url,
                content=response.text,
                success=True,
            )

        except requests.RequestException as error:
            return FetchResult(
                url=url,
                content="",
                success=False,
                error=str(error),
            )
