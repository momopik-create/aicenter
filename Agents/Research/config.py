import os


class ResearchConfig:
    name = "research_config"
    version = "2.1.0"

    MAX_SEARCH_RESULTS = int(os.getenv("RESEARCH_MAX_SEARCH_RESULTS", "10"))
    REQUEST_TIMEOUT = int(os.getenv("RESEARCH_REQUEST_TIMEOUT", "20"))
    MIN_SOURCES = int(os.getenv("RESEARCH_MIN_SOURCES", "3"))
    MAX_FETCHED_SOURCES = int(os.getenv("RESEARCH_MAX_FETCHED_SOURCES", "8"))
    MAX_EXCERPT_LENGTH = int(os.getenv("RESEARCH_MAX_EXCERPT_LENGTH", "4000"))

    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    GEMINI_MAX_OUTPUT_TOKENS = int(
        os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "4096")
    )
    MIN_FACTS = int(os.getenv("RESEARCH_MIN_FACTS", "3"))
    MIN_PRICING = int(os.getenv("RESEARCH_MIN_PRICING", "1"))
