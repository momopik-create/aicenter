import os


AGENT_NAME = "decision"
AGENT_VERSION = "0.1.0"

DECISION_PROVIDER = os.getenv(
    "DECISION_PROVIDER",
    "disabled",
).lower()

JEV_MODEL = os.getenv(
    "JEV_MODEL",
    "jev-latest",
)

JEV_ENABLED = os.getenv(
    "JEV_ENABLED",
    "false",
).lower() == "true"

DEFAULT_CONFIDENCE_THRESHOLD = float(
    os.getenv(
        "DECISION_CONFIDENCE_THRESHOLD",
        "0.90",
    )
)

DEFAULT_REVIEW_THRESHOLD = float(
    os.getenv(
        "DECISION_REVIEW_THRESHOLD",
        "0.60",
    )
)
