"""Title agent: hard 60-char limit, natural language, SEO-optimized."""
import json
from typing import Dict, Any
from llm_client import LLMClient


SYSTEM_PROMPT = """You are an elite SEO title tag specialist for Yatradham, India's leading wellness travel platform.

Given a primary keyword and package details, output a JSON object with:
- title_tag: a compelling, search-optimized title, MAXIMUM 60 characters including spaces.

STRICT Rules:
- MUST be under 60 chars total. Count every character including spaces and separators.
- MUST include the primary keyword or a close variant in the first half of the title.
- MUST include the destination/location if provided.
- End with "| Yatradham" as the brand suffix when there is room (aim for it).
- Use pipe (|) or dash (–) as separators.
- Write naturally for humans — no keyword stuffing or ALL CAPS.
- Include a benefit or differentiator when possible (e.g., "Best", "Top-Rated", duration).
- Never truncate mid-word. If the title is too long, rewrite shorter — do NOT just cut it off.

GOOD examples (follow these patterns):
- "7-Day Yoga Retreat in Rishikesh | Yatradham"
- "Panchakarma Detox in Almora – 14 Days | Yatradham"
- "Best Wellness Retreat in Rajasthan | Yatradham"
- "3-Day Ayurveda Retreat in Nepal | Yatradham"
- "Weight Loss Retreat Rishikesh – 21 Days"

BAD examples (never do these):
- "Natural Healing Program" (no location, no brand, no hook)
- "14 Days Heal" (truncated mid-thought)
- "Weight Management and" (incomplete sentence)

Output valid JSON only: {"title_tag": "your title here"}"""


def run(package_data: Dict[str, Any], primary_keyword: str, client: LLMClient) -> Dict[str, Any]:
    name = package_data.get('name', '')
    destination = package_data.get('destination', '')
    duration = package_data.get('duration', '')

    user_msg = f"""Primary Keyword: {primary_keyword}
Package Name: {name}
Destination: {destination}
Duration: {duration}

Generate ONE perfect SEO title tag under 60 characters. It must include the keyword, the destination, and ideally "| Yatradham" at the end."""

    content = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=200,
        temperature=0.4,
        response_format={"type": "json_object"},
    )
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {}

    title = result.get("title_tag", "")

    # Enforce 60 char limit — smart truncation, never mid-word
    if len(title) > 60:
        # Try to keep "| Yatradham" if possible
        if "| Yatradham" in title:
            prefix = title.split("| Yatradham")[0].strip()
            while len(prefix + " | Yatradham") > 60:
                prefix = prefix.rsplit(" ", 1)[0]
            title = prefix + " | Yatradham"
        else:
            title = title[:57].rsplit(" ", 1)[0] + "..."

    # Fallback: build a decent title from the data if LLM returned junk
    if not title or len(title) < 15:
        parts = []
        if duration:
            parts.append(duration)
        parts.append(primary_keyword or name)
        if destination:
            parts.append(f"in {destination}")
        base = " ".join(parts)
        if len(base + " | Yatradham") <= 60:
            title = base + " | Yatradham"
        else:
            title = base[:60]

    result["title_tag"] = title
    return result
