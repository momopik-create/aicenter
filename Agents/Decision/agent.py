from .config import JEV_ENABLED
from .providers.jev import JevProvider
from .schema import DecisionResult


class DecisionAgent:
    name = "decision"
    version = "0.1.0"

    def __init__(self):
        self.jev = JevProvider()

    def decide(
        self,
        state: str,
        questions: dict,
    ) -> DecisionResult:

        if not JEV_ENABLED:
            return DecisionResult(
                success=False,
                provider="disabled",
                error="Decision Agent is disabled.",
            )

        return self.jev.decide(
            state=state,
            questions=questions,
        )
