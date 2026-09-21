import json

from Agents.Research.publish_gate import PublishGate

from .schema import PublishResult


class PublisherAgent:
    name = "publisher"
    version = "0.2.0"

    def __init__(self):
        self.gate = PublishGate()

    def publish(
        self,
        product_name: str,
    ) -> PublishResult:

        file_path = self.gate._get_file(product_name)

        if not file_path.exists():
            return PublishResult(
                success=False,
                product_name=product_name,
                error="Research record not found.",
            )

        data = json.loads(
            file_path.read_text(
                encoding="utf-8"
            )
        )

        if data.get("published") is True:
            return PublishResult(
                success=False,
                product_name=product_name,
                published=False,
                already_published=True,
                error="Item has already been published.",
            )

        if not self.gate.can_publish(product_name):
            return PublishResult(
                success=False,
                product_name=product_name,
                published=False,
                error="Publish rejected by Publish Gate.",
            )

        data["published"] = True

        file_path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return PublishResult(
            success=True,
            product_name=product_name,
            published=True,
        )
