from .schema import ResearchResult, ResearchStatus


class ResearchAgent:
    name = "research"
    version = "0.1.0"

    def run(self, product_name: str, url: str) -> ResearchResult:
        """
        Run research for a product.

        This version only prepares the research task.
        It does not access the web or publish anything.
        """

        return ResearchResult(
            product_name=product_name,
            url=url,
            status=ResearchStatus.IN_PROGRESS,
        )
