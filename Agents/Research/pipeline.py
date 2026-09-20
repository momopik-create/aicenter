from Agents.Contracts.research import (
    ResearchPackage,
    ResearchStatus,
    SourceEvidence,
)
from Agents.Contracts.research_input import ResearchInput

from .agent import ResearchAgent
from .config import ResearchConfig
from .review_store import ReviewStore
from .tools.source_validator import SourceValidator
from .tools.web_fetch import WebFetchTool
from .tools.web_search import WebSearchTool


class ResearchPipeline:
    name = "research_pipeline"
    version = "1.0.0"

    def __init__(self):
        self.agent = ResearchAgent()
        self.search_tool = WebSearchTool()
        self.fetch_tool = WebFetchTool()
        self.validator = SourceValidator()
        self.store = ReviewStore()

    def run(
        self,
        research_input: ResearchInput,
    ) -> ResearchPackage:

        package = self.agent.run(
            product_name=research_input.product_name,
            url=research_input.product_url,
        )

        try:
            search = self.search_tool.search(
                query=research_input.product_name,
                max_results=(
                    ResearchConfig.MAX_SEARCH_RESULTS
                ),
            )

            if not search.success:
                package.status = ResearchStatus.FAILED
                self.store.save(package)
                return package

            for item in search.results:
                validation = self.validator.validate(
                    item.url
                )

                if not validation.valid:
                    continue

                package.sources.append(
                    SourceEvidence(
                        url=item.url,
                        title=item.title,
                        source_type=validation.source_type,
                        excerpt=item.content,
                    )
                )

            if len(package.sources) < (
                ResearchConfig.MIN_SOURCES
            ):
                package.status = ResearchStatus.FAILED
            else:
                package.status = (
                    ResearchStatus.COMPLETED
                )

            self.store.save(package)

            return package

        except Exception:
            package.status = ResearchStatus.FAILED
            self.store.save(package)
            return package
