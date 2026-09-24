from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path

from Agents.Contracts.research import ReviewStatus


class ReviewStore:
    name = "review_store"
    version = "2.1.0"

    def __init__(self, directory: str | Path | None = None):
        if directory is None:
            directory = os.getenv("RESEARCH_REVIEW_DIR")
        if directory is None:
            directory = (
                Path(__file__).resolve().parents[2]
                / "data"
                / "research_reviews"
            )

        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, result):
        file_path = self._file_path(result.product_name)
        data = asdict(result)
        file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, default=self._serialize),
            encoding="utf-8",
        )
        return file_path

    def load(self, product_name: str):
        file_path = self._file_path(product_name)
        if not file_path.exists():
            raise FileNotFoundError(f"Review not found: {product_name}")
        return json.loads(file_path.read_text(encoding="utf-8"))

    def update_status(
        self,
        product_name: str,
        status: ReviewStatus,
        note: str = None,
    ):
        file_path = self._file_path(product_name)
        if not file_path.exists():
            raise FileNotFoundError(f"Review not found: {product_name}")

        data = json.loads(file_path.read_text(encoding="utf-8"))
        data["review_status"] = status.value
        data["review_note"] = note
        file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return file_path

    def list_all(self):
        records = []
        for file_path in sorted(self.directory.glob("*.json")):
            try:
                records.append(json.loads(file_path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError):
                continue
        return records

    def _file_path(self, product_name: str) -> Path:
        return self.directory / f"{self._safe_filename(product_name)}.json"

    @staticmethod
    def _serialize(value):
        if hasattr(value, "value"):
            return value.value
        return str(value)

    @staticmethod
    def _safe_filename(name: str) -> str:
        return "".join(
            character.lower() if character.isalnum() else "_"
            for character in str(name)
        ).strip("_")
