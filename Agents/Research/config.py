import os


class ResearchConfig:
    name = "research_config"
    version = "1.0.0"

    MAX_SEARCH_RESULTS = int(
        os.getenv(
            "RESEARCH_MAX_SEARCH_RESULTS",
            "10",
        )
    )

    REQUEST_TIMEOUT = int(
        os.getenv(
            "RESEARCH_REQUEST_TIMEOUT",
            "20",
        )
    )

    MIN_SOURCES = int(
        os.getenv(
            "RESEARCH_MIN_SOURCES",
            "3",
        )
    )
