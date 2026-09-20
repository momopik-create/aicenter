import json
from dataclasses import asdict
from pathlib import Path

from .schema import ReviewStatus


class ReviewStore:
    name = "review_store"
    version = "0.2.0"

    def __init__(self):
        self.directory = (
            Path(__file__).parent / "reviews"
        )

        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(self, result):
        file_name = self._safe_filename(
            result.product_name
        )

        file_path = (
            self.directory / f"{file_name}.json"
        )

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

    def update_status(
        self,
        product_name: str,
        status: ReviewStatus,
        note: str = None,
    ):
        file_name = self._safe_filename(
            product_name
        )

        file_path = (
            self.directory / f"{file_name}.json"
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"Review not found: {product_name}"
            )

        data = json.loads(
            file_path.read_text(
                encoding="utf-8"
            )
        )

        data["review_status"] = status.value
        data["review_note"] = note

        file_path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
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
