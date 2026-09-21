import os


AGENT_NAME = "publisher"
AGENT_VERSION = "0.1.0"

PUBLISH_PROVIDER = os.getenv(
    "PUBLISH_PROVIDER",
    "disabled",
).lower()
