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
        self.models = [
            self.model,
            *[
                m for m in ResearchConfig.GEMINI_FALLBACK_MODELS
                if m != self.model
            ],
        ]
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

        try:
            response = self._generate_with_retry(prompt)

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty analysis response."
                )

            data = self._parse_json(text)
            result = self._normalize(data)

            # Pricing gets a dedicated extraction pass.
            try:
                result["pricing"] = self._extract_pricing(
                    product_name=product_name,
                    product_url=product_url,
                    evidence=evidence,
                    existing_pricing=result.get("pricing", []),
                )
            except Exception as exc:
                print(
                    f"Gemini pricing extraction unavailable; "
                    f"using deterministic fallback: {exc}"
                )
                result["pricing"] = self._deterministic_pricing(
                    evidence
                )

            return result

        except Exception as exc:
            print(
                f"Gemini analysis unavailable; "
                f"using deterministic evidence fallback: {exc}"
            )
            return self._deterministic_extract(evidence)

    def _extract_pricing(
        self,
        product_name: str,
        product_url: str,
        evidence: list[dict],
        existing_pricing: list[dict],
    ) -> list[dict]:

        if existing_pricing:
            return existing_pricing

        prompt = self._build_pricing_prompt(
            product_name,
            product_url,
            evidence,
        )

        response = self._generate_with_retry(prompt)

        text = getattr(response, "text", None)

        if not text:
            return []

        try:
            data = self._parse_json(text)
        except RuntimeError:
            return []

        return self._normalize_pricing(
            data.get("pricing", [])
        )

    @staticmethod
    def _build_pricing_prompt(
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
You are the pricing extraction stage of an affiliate research engine.

Product: {product_name}
Product URL: {product_url}

Your ONLY task is to extract pricing information explicitly supported
by the supplied source evidence.

Search carefully for:
- plan names
- starting prices
- exact prices
- currency
- monthly/yearly/hourly billing
- free tiers
- minimum charges
- relevant pricing conditions

Do NOT invent or estimate prices.

If the evidence does not contain pricing, return an empty pricing array.

Every pricing record MUST include the source_ids that support it.

Return ONLY valid JSON:

{{
  "pricing": [
    {{
      "plan": "plan name",
      "price": "exact price as stated",
      "currency": "USD",
      "billing_period": "monthly",
      "details": "important pricing condition",
      "source_ids": ["S1"]
    }}
  ]
}}

Evidence:

{evidence_text}
""".strip()

    @staticmethod
    def _normalize_pricing(items: list) -> list[dict]:

        pricing = []

        for item in items or []:

            if not isinstance(item, dict):
                continue

            plan = str(item.get("plan", "")).strip()
            price = str(item.get("price", "")).strip()

            if not plan and not price:
                continue

            source_ids = item.get("source_ids", []) or []

            if isinstance(source_ids, str):
                source_ids = [source_ids]

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
                    "source_ids": source_ids,
                }
            )

        return pricing

    @classmethod
    def _deterministic_extract(
        cls,
        evidence: list[dict],
    ) -> dict[str, Any]:
        """
        Evidence-only fallback used when Gemini is unavailable.

        No new claims are generated. Facts are copied from source
        excerpts and pricing is extracted only when an explicit price
        expression exists in the source text.
        """
        facts = []

        for item in evidence:
            source_id = item.get("id", "")
            excerpt = str(item.get("excerpt", "")).strip()

            if not excerpt:
                continue

            sentences = re.split(
                r"(?<=[.!?])\\s+",
                excerpt,
            )

            for sentence in sentences:
                sentence = sentence.strip()

                if len(sentence) < 30:
                    continue

                facts.append(
                    f"[{source_id}] {sentence}"
                )

                if len(facts) >= 8:
                    break

            if len(facts) >= 8:
                break

        return {
            "facts": facts,
            "pricing": cls._deterministic_pricing(evidence),
            "features": [],
            "pros": [],
            "cons": [],
        }

    @classmethod
    def _deterministic_pricing(
        cls,
        evidence: list[dict],
    ) -> list[dict]:
        """Extract only explicitly stated prices from source evidence."""

        results = []
        seen = set()

        price_pattern = re.compile(
            r"(?:US\$|\$|€|£)\s*\d+(?:[.,]\d+)?"
            r"|"
            r"\d+(?:[.,]\d+)?\s*(?:USD|EUR|GBP|TRY|TL)",
            re.IGNORECASE,
        )

        for item in evidence:
            source_id = item.get("id", "")
            excerpt = str(item.get("excerpt", "")).strip()

            if not excerpt:
                continue

            for sentence in re.split(r"(?<=[.!?])\s+", excerpt):
                sentence = sentence.strip()

                if not sentence:
                    continue

                match = price_pattern.search(sentence)

                if not match:
                    continue

                raw_price = match.group(0).strip()
                upper = raw_price.upper()

                if "$" in raw_price or "USD" in upper:
                    currency = "USD"
                elif "€" in raw_price or "EUR" in upper:
                    currency = "EUR"
                elif "£" in raw_price or "GBP" in upper:
                    currency = "GBP"
                elif "TRY" in upper or "TL" in upper:
                    currency = "TRY"
                else:
                    currency = ""

                lower = sentence.lower()

                if re.search(r"\b(per\s+month|monthly|month)\b", lower):
                    billing_period = "monthly"
                elif re.search(
                    r"\b(per\s+year|yearly|annual|annually|year)\b",
                    lower,
                ):
                    billing_period = "yearly"
                elif re.search(
                    r"\b(per\s+hour|hourly|hour)\b",
                    lower,
                ):
                    billing_period = "hourly"
                elif re.search(
                    r"\b(per\s+day|daily|day)\b",
                    lower,
                ):
                    billing_period = "daily"
                else:
                    billing_period = ""

                plan = ""

                plan_match = re.search(
                    r"\b(?:the\s+)?"
                    r"([A-Za-z0-9][A-Za-z0-9&+._-]{0,30})"
                    r"\s+(?:plan|tier)\b",
                    sentence,
                    re.IGNORECASE,
                )

                if plan_match:
                    plan = plan_match.group(1).strip()

                key = (source_id, raw_price, sentence)

                if key in seen:
                    continue

                seen.add(key)

                results.append(
                    {
                        "plan": plan,
                        "price": raw_price,
                        "currency": currency,
                        "billing_period": billing_period,
                        "details": sentence,
                        "source_ids": [source_id],
                    }
                )

        return results

    def _generate_with_retry(self, prompt: str):
        last_error = None

        for model in self.models:
            print(f"Trying Gemini model: {model}")

            for attempt in range(1, self.max_retries + 1):
                try:
                    return self.client.models.generate_content(
                        model=model,
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

                    if attempt < self.max_retries:
                        delay = self.base_delay * (2 ** (attempt - 1))
                        delay += random.uniform(0, 2)

                        print(
                            f"Gemini temporary error on {model}, "
                            f"attempt {attempt}/{self.max_retries}: {message}"
                        )
                        print(f"Retrying in {delay:.1f}s...")

                        time.sleep(delay)
                    else:
                        print(
                            f"Model {model} failed after "
                            f"{self.max_retries} attempts."
                        )

            if model != self.models[-1]:
                print("Trying fallback Gemini model...")

        raise RuntimeError(
            f"All Gemini models failed. Last error: {last_error}"
        )

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
