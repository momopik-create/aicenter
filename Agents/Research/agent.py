from Agents.Contracts.research import (
    ResearchPackage,
    ResearchStatus,
)


class ResearchAgent:
    name = "research_agent"
    version = "2.0.0"

    def run(
        self,
        product_name: str,
        url: str,
    ) -> ResearchPackage:

        return ResearchPackage(
            product_name=product_name,
            product_url=url,
            status=ResearchStatus.IN_PROGRESS,
        )