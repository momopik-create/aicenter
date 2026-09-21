from typing import Any, Dict

from ..provider import PublishProvider


class DisabledProvider(PublishProvider):
    name = "disabled"
    version = "0.1.0"

    def publish(
        self,
        product_name: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {
            "success": False,
            "published": False,
            "provider": self.name,
            "error": "Publishing provider is disabled.",
        }
