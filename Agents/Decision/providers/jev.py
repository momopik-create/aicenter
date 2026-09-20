from ..schema import DecisionResult


class JevProvider:
    name = "jev"
    version = "0.1.0"

    def decide(
        self,
        state: str,
        questions: dict,
    ) -> DecisionResult:
        """
        Placeholder for the Jev API.

        Jev is intentionally disabled at this stage.
        """

        return DecisionResult(
            success=False,
            provider=self.name,
            error="Jev provider is disabled.",
        )
