import os
import random
import datetime
import time
from google import genai

TOOLS_LIST = [
    "ChatGPT Plus", "Midjourney v6", "Claude 3.5 Sonnet", "Jasper AI", 
    "Copy.ai", "Descript", "Runway Gen-2", "ElevenLabs", "Perplexity AI",
    "GitHub Copilot", "Canva Magic Studio", "Notion AI", "Synthesia",
    "GrammarlyGO", "Surfer SEO", "Make.com", "Zapier Central"
]

def generate_review():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing!")

    client = genai.Client(api_key=api_key)
    selected_tool = random.choice(TOOLS_LIST)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = selected_tool.lower().replace(" ", "-").replace(".", "")

    prompt = f"""
    You are an expert tech reviewer and affiliate marketer. Write a comprehensive, SEO-optimized, highly engaging review for the AI tool: "{selected_tool}".
    
    CRITICAL INSTRUCTIONS:
    1. Output strictly valid Markdown with YAML frontmatter at the top.
    2. Frontmatter fields must include:
       title: "{selected_tool} Review (2026): Features, Pricing & Alternatives"
       description: "A concise 1-2 sentence summary of {selected_tool}."
       rating: 4.8
       date: "{date_str}"
       pricing_tier: "Paid" or "Freemium" or "Free Trial"
    3. The article content MUST include:
       - **Executive Summary**: Brief overview with key takeaways.
       - **Pros & Cons**: Use clear Markdown lists with green checkmarks (✅) and red crosses (❌).
       - **Key Features**: Bullet points of top capabilities.
       - **Pricing Breakdown**: A clean Markdown table showing plans and costs.
       - **Verdict & Recommendation**: Who is this tool best for?
    
    Do NOT include extra markdown fences outside the output. Return content starting with ---.
    """

    print(f"Generating review for {selected_tool} with Gemini...")
    
    content = None
    max_retries = 4
    delay = 10  # شروع انتظار با ۱۰ ثانیه

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            content = response.text.strip()
            print("Successfully received response from Gemini API.")
            break
        except Exception as e:
            print(f"Attempt {attempt} failed with error: {e}")
            if attempt < max_retries:
                print(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)
                delay *= 2  # دو برابر کردن زمان انتظار در هر تلاش
            else:
                print("All retries exhausted.")
                raise e

    if not content:
        raise ValueError("Failed to generate content: empty response.")

    # پاک‌سازی قالب خروجی
    if content.startswith("```markdown"):
        content = content[11:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    os.makedirs("src/content/products", exist_ok=True)
    file_path = f"src/content/products/{slug}.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully generated review at: {file_path}")

if __name__ == "__main__":
    generate_review()
