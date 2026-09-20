from .schema import ResearchResult, ResearchStatus


class ResearchAgent:
    name = "research"
    version = "0.1.0"

    def run(self, product_name: str, url: str) -> ResearchResult:
        """
        Create a research result for a product.

        The agent does not publish anything.
        Actual research is performed by the Research Pipeline
        and its tools.
        """

        return ResearchResult(
            product_name=product_name,
            url=url,
            status=ResearchStatus.IN_PROGRESS,
        )
