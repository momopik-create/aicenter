from abc import ABC, abstractmethod
from typing import Any, Dict


class PublishProvider(ABC):
    name = "base"
    version = "0.1.0"

    @abstractmethod
    def publish(
        self,
        product_name: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Publish a research result to an external destination.
        """
        raise NotImplementedError