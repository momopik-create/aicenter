import json
from dataclasses import asdict
from pathlib import Path


class ReviewStore:
    name = "review_store"
    version = "0.1.0"

    def __init__(self):
        self.directory = Path(__file__).parent / "reviews"
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, result):
        file_name = self._safe_filename(
            result.product_name
        )

        file_path = self.directory / f"{file_name}.json"

        data = asdict(result)

        file_path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

        return file_path

    @staticmethod
    def _safe_filename(name: str) -> str:
        return "".join(
            character.lower()
            if character.isalnum()
            else "_"
            for character in name
        ).strip("_")
