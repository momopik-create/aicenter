import os
import json
import random
import datetime
import time

from google import genai


def get_active_affiliate_tools():
    """Return only affiliate tools registered in affiliates.json."""

    json_path = "affiliates.json"

    if not os.path.exists(json_path):
        raise FileNotFoundError(
            "affiliates.json not found!"
        )

    with open(
        json_path,
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    active_tools = [
        key
        for key in data.keys()
        if key != "default"
    ]

    return active_tools


def generate_review():

    api_key = os.environ.get(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is missing!"
        )

    tools_list = get_active_affiliate_tools()

    if not tools_list:
        print(
            "No active affiliate tools found "
            "in affiliates.json. Skipping generation."
        )
        return

    client = genai.Client(
        api_key=api_key
    )

    selected_tool = random.choice(
        tools_list
    )

    date_str = (
        datetime.datetime.now()
        .strftime("%Y-%m-%d")
    )

    slug = (
        selected_tool
        .lower()
        .replace(" ", "-")
        .replace(".", "")
    )

    prompt = f"""
You are an expert technology researcher
and affiliate content writer.

Write a comprehensive, factual,
SEO-friendly review for:

"{selected_tool}"

IMPORTANT RULES:

1. Output strictly valid Markdown.
2. Output YAML frontmatter at the top.
3. Do NOT use Markdown code fences around
   the complete response.
4. Do NOT invent facts, pricing,
   features, traffic numbers, guarantees,
   ratings, or claims.
5. If a fact is unknown, say that it is
   unknown rather than guessing.
6. Do NOT assign an overall rating.
7. The rating must be exactly 0 because
   the Decision Agent is responsible for
   future scoring.

Required frontmatter:

---
title: "{selected_tool.title()} Review (2026): Features, Pricing & Alternatives"
description: "A concise factual summary of {selected_tool}."
rating: 0
date: "{date_str}"
pricing_tier: "Unknown"
---

The article must contain:

# {selected_tool.title()} Review

## Executive Summary

Provide a concise factual overview.

## Key Facts

List important verifiable facts.

## Pros & Cons

### Pros

Use clear bullet points.

### Cons

Use clear bullet points.

## Key Features

Describe important features without
inventing unsupported capabilities.

## Pricing Breakdown

Provide a Markdown table.

If reliable pricing information is unavailable,
explicitly state that pricing could not be
verified.

## Alternatives

List relevant alternatives and explain
the factual differences where known.

## Verdict & Recommendation

Do NOT assign a numerical score.

Instead explain:

- Who may benefit from the product.
- Who may not benefit from it.
- Important limitations.
- What should be verified before purchasing.

Return content starting directly with ---.
"""

    # Models are tried in order.
    # The first model is the preferred model.
    models = [
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
    ]

    content = None
    successful_model = None

    for model_name in models:

        print(
            f"Attempting generation for "
            f"'{selected_tool}' using "
            f"{model_name}..."
        )

        for attempt in range(1, 4):

            try:

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )

                if not response.text:
                    raise ValueError(
                        "Model returned empty content."
                    )

                content = response.text.strip()
                successful_model = model_name

                print(
                    f"Successfully generated review "
                    f"with {model_name}."
                )

                break

            except Exception as e:

                print(
                    f"Attempt {attempt} failed "
                    f"for {model_name}: {e}"
                )

                if attempt < 3:

                    wait_time = attempt * 10

                    print(
                        f"Waiting {wait_time} seconds "
                        f"before retrying..."
                    )

                    time.sleep(wait_time)

        if content:
            break

        print(
            f"Model {model_name} failed. "
            f"Trying next fallback model."
        )

    if not content:
        raise ValueError(
            "Failed to generate content using "
            "all configured Gemini models."
        )

    # Remove accidental Markdown fences.
    if content.startswith(
        "```markdown"
    ):
        content = content[
            len("```markdown"):
        ]

    elif content.startswith(
        "```"
    ):
        content = content[
            len("```"):
        ]

    if content.endswith(
        "```"
    ):
        content = content[
            :-len("```")
        ]

    content = content.strip()

    # Safety check:
    # prevent the model from publishing
    # a fabricated rating.
    lines = content.splitlines()

    for index, line in enumerate(lines):

        if line.strip().startswith(
            "rating:"
        ):
            lines[index] = "rating: 0"

    content = "\n".join(lines).strip()

    # Ensure output directory exists.
    output_directory = (
        "src/content/products"
    )

    os.makedirs(
        output_directory,
        exist_ok=True,
    )

    file_path = (
        f"{output_directory}/{slug}.md"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(content)

    print(
        f"Successfully saved review at: "
        f"{file_path}"
    )

    print(
        f"Generation model: "
        f"{successful_model}"
    )


if __name__ == "__main__":
    generate_review()
