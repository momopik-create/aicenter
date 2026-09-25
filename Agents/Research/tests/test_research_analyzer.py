import json

from Agents.Contracts.research import SourceEvidence
from Agents.Research.tools.research_analyzer import ResearchAnalyzer


class FakeResponse:
    text = json.dumps(
        {
            "facts": [
                {"text": "The product offers cloud compute.", "source_ids": ["S1"]}
            ],
            "pricing": [
                {
                    "plan": "Basic",
                    "price": "$5",
                    "currency": "USD",
                    "billing_period": "monthly",
                    "details": "Entry plan.",
                    "source_ids": ["S2"],
                }
            ],
            "features": [
                {"text": "Cloud compute", "source_ids": ["S1"]}
            ],
            "pros": [
                {"text": "Broad infrastructure options.", "source_ids": ["S1"]}
            ],
            "cons": [
                {"text": "Pricing varies by resource.", "source_ids": ["S2"]}
            ],
        }
    )


class FakeModels:
    def generate_content(self, **kwargs):
        return FakeResponse()


class FakeClient:
    models = FakeModels()


def main():
    analyzer = ResearchAnalyzer(client=FakeClient())
    result = analyzer.analyze(
        "Vultr",
        "https://www.vultr.com",
        [
            SourceEvidence(
                url="https://example.com/official",
                title="Official",
                source_type="website",
                excerpt="Cloud compute and infrastructure.",
            ),
            SourceEvidence(
                url="https://example.com/pricing",
                title="Pricing",
                source_type="pricing",
                excerpt="Basic plan $5 monthly.",
            ),
            SourceEvidence(
                url="https://example.com/docs",
                title="Docs",
                source_type="documentation",
                excerpt="Documentation.",
            ),
        ],
    )

    assert len(result["facts"]) == 1
    assert len(result["pricing"]) == 1
    assert result["pricing"][0]["price"] == "$5"
    assert len(result["pros"]) == 1
    assert len(result["cons"]) == 1
    print("Research Analyzer test: PASSED")


if __name__ == "__main__":
    main()
