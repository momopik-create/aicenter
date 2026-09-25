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
from .tools.research_analyzer import ResearchAnalyzer
from .tools.source_validator import SourceValidator
from .tools.web_search import WebSearchTool


class ResearchPipeline:
    name = "research_pipeline"
    version = "2.2.0"

    def __init__(
        self,
        search_tool=None,
        validator=None,
        store=None,
        analyzer=None,
    ):
        self.agent = ResearchAgent()
        self.search_tool = search_tool or WebSearchTool()
        self.validator = validator or SourceValidator()
        self.store = store or ReviewStore()
        self.analyzer = analyzer or ResearchAnalyzer()

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
                package.review_note = search.error or "Search failed."
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
                if len(package.sources) >= ResearchConfig.MAX_FETCHED_SOURCES:
                    break

            if len(package.sources) < ResearchConfig.MIN_SOURCES:
                package.status = ResearchStatus.FAILED
                package.review_note = (
                    f"Only {len(package.sources)} validated sources found; "
                    f"{ResearchConfig.MIN_SOURCES} required."
                )
                self.store.save(package)
                return package

            analysis = self.analyzer.analyze(
                product_name=research_input.product_name,
                product_url=research_input.url,
                sources=package.sources,
            )
            package.facts = analysis["facts"]
            package.pricing = analysis["pricing"]
            package.pros = analysis["pros"]
            package.cons = analysis["cons"]

            package.status = ResearchStatus.COMPLETED
            package.review_note = (
                f"Extracted {len(package.facts)} facts, "
                f"{len(package.pricing)} pricing records, "
                f"{len(analysis.get('features', []))} features."
            )
            self.store.save(package)
            return package

        except Exception as exc:
            package.status = ResearchStatus.FAILED
            package.review_note = str(exc)
            self.store.save(package)
            return package
