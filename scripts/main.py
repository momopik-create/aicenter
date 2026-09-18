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

# لیست مدل‌ها به ترتیب اولویت
MODELS_TO_TRY = ['gemini-3.6-flash', 'gemini-1.5-flash']

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
       pricing_tier: "Paid"
    3. The article content MUST include:
       - **Executive Summary**: Brief overview with key takeaways.
       - **Pros & Cons**: Use clear Markdown lists with green checkmarks (✅) and red crosses (❌).
       - **Key Features**: Bullet points of top capabilities.
       - **Pricing Breakdown**: A clean Markdown table showing plans and costs.
       - **Verdict & Recommendation**: Who is this tool best for?
    
    Do NOT include extra markdown fences outside the output. Return content starting with ---.
    """

    content = None
    
    for model_name in MODELS_TO_TRY:
        print(f"Attempting to generate review using {model_name}...")
        for attempt in range(1, 3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                content = response.text.strip()
                print(f"Successfully generated review with {model_name}.")
                break
            except Exception as e:
                print(f"Attempt {attempt} with {model_name} failed: {e}")
                time.sleep(5)
        if content:
            break

    if not content:
        raise ValueError("Failed to generate content: all models were unavailable.")

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
        
    print(f"Successfully saved review at: {file_path}")

if __name__ == "__main__":
    generate_review()
