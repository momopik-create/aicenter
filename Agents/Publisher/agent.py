from Agents.Research.publish_gate import PublishGate

from .schema import PublishResult


class PublisherAgent:
    name = "publisher"
    version = "0.1.0"

    def __init__(self):
        self.gate = PublishGate()

    def publish(
        self,
        product_name: str,
    ) -> PublishResult:

        if not self.gate.can_publish(product_name):
            return PublishResult(
                success=False,
                product_name=product_name,
                published=False,
                error=(
                    "Publish rejected by Publish Gate."
                ),
            )

        return PublishResult(
            success=True,
            product_name=product_name,
            published=True,
        )
