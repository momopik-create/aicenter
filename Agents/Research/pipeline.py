from __future__ import annotations

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
from .tools.web_search import WebSearchTool


class ResearchPipeline:
    name = "research_pipeline"
    version = "2.1.0"

    def __init__(
        self,
        search_tool=None,
        validator=None,
        store=None,
    ):
        self.agent = ResearchAgent()
        self.search_tool = search_tool or WebSearchTool()
        self.validator = validator or SourceValidator()
        self.store = store or ReviewStore()

    def run(self, research_input: ResearchInput) -> ResearchPackage:
        package = self.agent.run(
            product_name=research_input.product_name,
            url=research_input.url,
        )

        try:
            search = self.search_tool.search(
                query=research_input.product_name,
                max_results=ResearchConfig.MAX_SEARCH_RESULTS,
            )

            if not search.success:
                package.status = ResearchStatus.FAILED
                self.store.save(package)
                return package

            seen: set[str] = set()
            for item in search.results:
                validation = self.validator.validate(item.url)
                if not validation.valid or item.url in seen:
                    continue
                seen.add(item.url)
                package.sources.append(
                    SourceEvidence(
                        url=item.url,
                        title=item.title or item.url,
                        source_type=validation.source_type,
                        excerpt=(item.content or "")[: ResearchConfig.MAX_EXCERPT_LENGTH],
                    )
                )

            package.status = (
                ResearchStatus.COMPLETED
                if len(package.sources) >= ResearchConfig.MIN_SOURCES
                else ResearchStatus.FAILED
            )
            self.store.save(package)
            return package

        except Exception as exc:
            package.status = ResearchStatus.FAILED
            package.review_note = str(exc)
            self.store.save(package)
            return package
