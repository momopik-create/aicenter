import os


class ResearchConfig:
    name = "research_config"
    version = "2.0.0"

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

    MAX_FETCHED_SOURCES = int(
        os.getenv(
            "RESEARCH_MAX_FETCHED_SOURCES",
            "5",
        )
    )

    MAX_EXCERPT_LENGTH = int(
        os.getenv(
            "RESEARCH_MAX_EXCERPT_LENGTH",
            "2000",
        )
    )