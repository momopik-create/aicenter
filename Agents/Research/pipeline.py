from .agent import ResearchAgent
from .input import ResearchInput
from .output import ResearchOutput
from .schema import ResearchStatus
from .tools.web_search import WebSearchTool
from .tools.web_fetch import WebFetchTool
from .tools.source_validator import SourceValidator


class ResearchPipeline:
    name = "research_pipeline"
    version = "0.1.0"

    def __init__(self):
        self.agent = ResearchAgent()
        self.search_tool = WebSearchTool()
        self.fetch_tool = WebFetchTool()
        self.source_validator = SourceValidator()

    def run(self, research_input: ResearchInput) -> ResearchOutput:
        try:
            result = self.agent.run(
                product_name=research_input.product_name,
                url=research_input.url,
            )

            search_results = self.search_tool.search(
                research_input.product_name
            )

            for search_result in search_results:
                validation = self.source_validator.validate(
                    search_result.url
                )

                if not validation.valid:
                    continue

                fetched = self.fetch_tool.fetch(
                    search_result.url
                )

                if not fetched.success:
                    continue

            result.status = ResearchStatus.COMPLETED

            return ResearchOutput(
                success=True,
                result=result,
            )

        except Exception as error:
            return ResearchOutput(
                success=False,
                error=str(error),
            )
