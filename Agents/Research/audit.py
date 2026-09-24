import json
from datetime import datetime, timezone
from pathlib import Path


class AuditLog:
    name = "audit_log"
    version = "0.1.0"

    def __init__(self):
        self.file_path = (
            Path(__file__).parent
            / "reviews"
            / "audit.jsonl"
        )

    def record(
        self,
        product_name: str,
        action: str,
        note: str = None,
    ):
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        entry = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "product_name": product_name,
            "action": action,
            "note": note,
        }

        with self.file_path.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                json.dumps(
                    entry,
                    ensure_ascii=False,
                )
                + "\n"
            )