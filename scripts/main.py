import os
import json
import random
import datetime
import time
from google import genai

def get_active_affiliate_tools():
    """فقط ابزارهایی را برمی‌گرداند که لینک واقعی آن‌ها در affiliates.json ثبت شده است"""
    json_path = "affiliates.json"
    if not os.path.exists(json_path):
        raise FileNotFoundError("affiliates.json not found!")
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    active_tools = [key for key in data.keys() if key != "default"]
    return active_tools

def generate_review():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing!")

    tools_list = get_active_affiliate_tools()
    
    if not tools_list:
        print("No active affiliate tools found in affiliates.json. Skipping generation.")
        return

    client = genai.Client(api_key=api_key)
    selected_tool = random.choice(tools_list)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = selected_tool.lower().replace(" ", "-").replace(".", "")

    prompt = f"""
    You are an expert tech reviewer and affiliate marketer. Write a comprehensive, SEO-optimized, highly engaging review for the AI tool or platform: "{selected_tool}".
    
    CRITICAL INSTRUCTIONS:
    1. Output strictly valid Markdown with YAML frontmatter at the top.
    2. Frontmatter fields must include:
       title: "{selected_tool.title()} Review (2026): Features, Pricing & Alternatives"
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

    # به‌روزرسانی مدل به gemini-3.6-flash طبق اعلام رسمی گوگل
    model_name = 'gemini-3.6-flash'
    content = None
    
    print(f"Attempting generation for '{selected_tool}' using {model_name}...")
    for attempt in range(1, 4):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            content = response.text.strip()
            print(f"Successfully generated review with {model_name}.")
            break
        except Exception as e:
            wait_time = attempt * 10
            print(f"Attempt {attempt} failed: {e}")
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)

    if not content:
        raise ValueError(f"Failed to generate content using {model_name}.")

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
