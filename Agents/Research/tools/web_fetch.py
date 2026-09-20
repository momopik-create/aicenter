from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class FetchResult:
    success: bool
    url: str
    content: str = ""
    status_code: Optional[int] = None
    error: Optional[str] = None


class WebFetchTool:
    name = "web_fetch"
    version = "1.0.0"

    def fetch(
        self,
        url: str,
        timeout: int = 20,
    ) -> FetchResult:

        try:
            response = requests.get(
                url,
                timeout=timeout,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "MomopikResearchBot/1.0"
                    )
                },
            )

            return FetchResult(
                success=response.ok,
                url=url,
                content=response.text,
                status_code=response.status_code,
            )

        except Exception as error:
            return FetchResult(
                success=False,
                url=url,
                error=str(error),
            )
