from Agents.Decision.agent import DecisionAgent

from .agent import ResearchAgent
from .input import ResearchInput
from .output import ResearchOutput
from .schema import ResearchStatus
from .source import ResearchSource
from .tools.source_validator import SourceValidator
from .tools.web_fetch import WebFetchTool
from .tools.web_search import WebSearchTool
from .review_store import ReviewStore

class ResearchPipeline:
    name = "research_pipeline"
    version = "0.4.0"

    def __init__(self):
        self.agent = ResearchAgent()
        self.decision_agent = DecisionAgent()
        self.search_tool = WebSearchTool()
        self.fetch_tool = WebFetchTool()
        self.source_validator = SourceValidator()

    def run(
        self,
        research_input: ResearchInput,
    ) -> ResearchOutput:

        try:
            result = self.agent.run(
                product_name=research_input.product_name,
                url=research_input.url,
            )

            search_response = self.search_tool.search(
                research_input.product_name,
                max_results=10,
            )

            if not search_response.success:
                result.status = ResearchStatus.FAILED

                return ResearchOutput(
                    success=False,
                    result=result,
                    error=search_response.error,
                )

            for search_result in search_response.results:

                validation = self.source_validator.validate(
                    search_result.url
                )

                if not validation.valid:
                    continue

                source = ResearchSource(
                    url=search_result.url,
                    title=search_result.title,
                    source_type=validation.source_type,
                    checked_at=None,
                )

                result.sources.append(source)

            self.decision_agent.decide(
                state="research_sources",
                questions={
                    "product_name": research_input.product_name,
                    "source_count": len(result.sources),
                },
            )

            result.status = ResearchStatus.COMPLETED

            self.review_store.save(result)

            return ResearchOutput(
                success=True,
                result=result,
            )

        except Exception as error:
            return ResearchOutput(
                success=False,
                error=str(error),
            )
