import os
import re
from google import genai
from slugify import slugify

def generate_review():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    # مقداردهی صحیح بر اساس آخرین ورژن SDK
    client = genai.Client(api_key=api_key)

    prompt = """
    You are an expert digital product and software reviewer.
    Select ONE popular, trending AI tool or SaaS software from 2026.
    Write a comprehensive review in Markdown format.

    CRITICAL REQUIREMENT:
    The response MUST start with this EXACT Frontmatter format at the very top:
    ---
    title: "Product Name - Brief Tagline"
    description: "A short 1-sentence SEO summary under 150 characters."
    rating: 4.8
    affiliate_url: "https://example.com"
    date: "2026-09-17"
    ---

    After the frontmatter, structure the content as follows:
    # Overview
    # Key Features
    # Pros & Cons
    # Final Verdict
    """

    print("Generating review with Gemini...")
    response = client.models.generate_content(
    model='gemini-3.6-flash',
        contents=prompt
    )

    content = response.text

    match = re.search(r'title:\s*"([^"]+)"', content)
    if match:
        title = match.group(1).split('-')[0].strip()
        slug = slugify(title)
    else:
        slug = "review-item"

    output_dir = "src/content/products"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{slug}.md")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated: {file_path}")

if __name__ == "__main__":
    generate_review()
