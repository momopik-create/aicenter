from __future__ import annotations

import json
import os
import random
import re
import time
from typing import Any

from Agents.Contracts.research import SourceEvidence
from Agents.Research.config import ResearchConfig


class ResearchAnalyzer:
    """Extract structured, source-grounded research from collected evidence."""

    name = "research_analyzer"
    version = "2.1.1"

    RETRYABLE_MARKERS = (
        "429",
        "500",
        "502",
        "503",
        "504",
        "UNAVAILABLE",
        "RESOURCE_EXHAUSTED",
        "INTERNAL",
        "TIMEOUT",
        "timed out",
    )

    def __init__(
        self,
        client=None,
        model: str | None = None,
        max_retries: int = 3,
        base_delay: float = 5.0,
    ):
        self._client = client
        self.model = model or ResearchConfig.GEMINI_MODEL
        self.max_retries = max_retries
        self.base_delay = base_delay

    @property
    def client(self):
        if self._client is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise RuntimeError("GEMINI_API_KEY is not configured.")

            try:
                from google import genai
            except ImportError as exc:
                raise RuntimeError(
                    "google-genai is not installed."
                ) from exc

            self._client = genai.Client(api_key=api_key)

        return self._client

    def analyze(
        self,
        product_name: str,
        product_url: str,
        sources: list[SourceEvidence],
    ) -> dict[str, Any]:

        if not sources:
            raise ValueError("At least one source is required for analysis.")

        evidence = []

        for index, source in enumerate(sources, start=1):
            excerpt = (source.excerpt or "").strip()

            if not excerpt:
                continue

            evidence.append(
                {
                    "id": f"S{index}",
                    "title": source.title,
                    "url": source.url,
                    "source_type": source.source_type,
                    "excerpt": excerpt,
                }
            )

        if not evidence:
            raise ValueError(
                "No source excerpts are available for analysis."
            )

        prompt = self._build_prompt(
            product_name,
            product_url,
            evidence,
        )

        response = self._generate_with_retry(prompt)

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError(
                "Gemini returned an empty analysis response."
            )

        data = self._parse_json(text)

        return self._normalize(data)

    def _generate_with_retry(self, prompt: str):
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                return self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={
                        "temperature": 0.1,
                        "max_output_tokens": (
                            ResearchConfig.GEMINI_MAX_OUTPUT_TOKENS
                        ),
                        "response_mime_type": "application/json",
                    },
                )

            except Exception as exc:
                last_error = exc
                message = str(exc)

                if not self._is_retryable(message):
                    raise

                if attempt >= self.max_retries:
                    raise RuntimeError(
                        f"Gemini failed after {self.max_retries} attempts: "
                        f"{message}"
                    ) from exc

                delay = self.base_delay * (2 ** (attempt - 1))
                delay += random.uniform(0, 2)

                print(
                    f"Gemini temporary error on attempt "
                    f"{attempt}/{self.max_retries}: {message}"
                )
                print(f"Retrying in {delay:.1f}s...")

                time.sleep(delay)

        raise RuntimeError(str(last_error))

    @classmethod
    def _is_retryable(cls, message: str) -> bool:
        lowered = message.lower()

        return any(
            marker.lower() in lowered
            for marker in cls.RETRYABLE_MARKERS
        )

    @staticmethod
    def _build_prompt(
        product_name: str,
        product_url: str,
        evidence: list[dict],
    ) -> str:

        evidence_text = json.dumps(
            evidence,
            ensure_ascii=False,
            indent=2,
        )

        return f"""
You are the evidence extraction stage of an affiliate product research engine.

Product: {product_name}
Product URL: {product_url}

Use ONLY the supplied source evidence.

Do not invent facts, prices, features, pros, cons, or claims.

Prefer official/vendor sources for product facts and pricing.

Every fact, pricing item, feature, pro, and con must include source_ids
using the S# identifiers from the evidence.

Pricing must preserve currency and billing period exactly when available.

If a field is not supported by the evidence, leave it empty.

Return ONLY valid JSON:

{{
  "facts": [
    {{
      "text": "concise factual statement",
      "source_ids": ["S1"]
    }}
  ],

  "pricing": [
    {{
      "plan": "plan name",
      "price": "price as stated",
      "currency": "USD",
      "billing_period": "monthly",
      "details": "short relevant pricing detail",
      "source_ids": ["S2"]
    }}
  ],

  "features": [
    {{
      "text": "feature",
      "source_ids": ["S1"]
    }}
  ],

  "pros": [
    {{
      "text": "evidence-supported advantage",
      "source_ids": ["S1"]
    }}
  ],

  "cons": [
    {{
      "text": "evidence-supported limitation",
      "source_ids": ["S3"]
    }}
  ]
}}

Evidence:

{evidence_text}
""".strip()

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:

        cleaned = text.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(
                r"^```(?:json)?\s*",
                "",
                cleaned,
            )

            cleaned = re.sub(
                r"\s*```$",
                "",
                cleaned,
            )

        try:
            data = json.loads(cleaned)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON."
            ) from exc

        if not isinstance(data, dict):
            raise RuntimeError(
                "Gemini analysis must be a JSON object."
            )

        return data

    @staticmethod
    def _normalize(data: dict[str, Any]) -> dict[str, Any]:

        def text_items(key: str) -> list[str]:

            output = []

            for item in data.get(key, []) or []:

                if isinstance(item, str) and item.strip():
                    output.append(item.strip())

                elif (
                    isinstance(item, dict)
                    and str(item.get("text", "")).strip()
                ):
                    output.append(
                        str(item["text"]).strip()
                    )

            return output

        pricing = []

        for item in data.get("pricing", []) or []:

            if not isinstance(item, dict):
                continue

            plan = str(
                item.get("plan", "")
            ).strip()

            price = str(
                item.get("price", "")
            ).strip()

            if not plan and not price:
                continue

            pricing.append(
                {
                    "plan": plan,
                    "price": price,
                    "currency": str(
                        item.get("currency", "")
                    ).strip(),
                    "billing_period": str(
                        item.get("billing_period", "")
                    ).strip(),
                    "details": str(
                        item.get("details", "")
                    ).strip(),
                    "source_ids": (
                        item.get("source_ids", [])
                        or []
                    ),
                }
            )

        return {
            "facts": text_items("facts"),
            "pricing": pricing,
            "features": text_items("features"),
            "pros": text_items("pros"),
            "cons": text_items("cons"),
        }
