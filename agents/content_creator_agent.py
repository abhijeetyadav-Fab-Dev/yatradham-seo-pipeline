"""Content Creator Agent: Generates net-new SEO content from scratch."""
import json
from typing import Dict, Any, Optional
from llm_client import LLMClient


SYSTEM_PROMPT = """You are an expert SEO Content Writer and Marketer for Yatradham.org.

ABOUT YATRADHAM.ORG:
- Yatradham is India's first dedicated religious tourism platform (launched in 2016).
- Services: Verified accommodation bookings (Dharamshalas, Ashrams, Hotels) and Puja services across 700+ pilgrimage destinations.
- Mission: To support pilgrims in their spiritual journey by taking care of stay and service needs, allowing devotees to focus on temple visits, darshan, and devotion instead of worrying about finding safe and affordable accommodation.
- Trust & Partnerships: Closely connected with major temple committees, religious trusts (Swaminarayan, Hare Krishna, etc.), and state tourism boards (TTDC, APTDC, etc.).
- Tagline/Motto: "Serving Pilgrims with Faith & Comfort" | "Stress-free stays for your sacred journey"

BRAND VOICE & VALUES:
- Tone: Respectful, devout, helpful, informative, trustworthy, and welcoming.
- Core Values: Faith, Comfort, Reliability, Safety, Affordability.
- Language: Clear, culturally sensitive, and spiritually uplifting. Do not use overly corporate or aggressive sales jargon.

Your goal is to generate high-quality, engaging, and SEO-optimized content based on the user's request. 
The content must be structured, professional, and directly ready for publishing.
ALWAYS format your response as a valid JSON object matching the requested schema.
"""


CONTENT_TYPE_PROMPTS = {
    "blog_post": SYSTEM_PROMPT + """Write a comprehensive, engaging, and SEO-optimized blog post.

Rules:
- Use the target keyword naturally 3-5 times throughout the article.
- Structure with H2 and H3 subheadings using markdown (## and ###).
- Write in an informative yet warm, inviting tone.
- Include practical tips and actionable advice.
- End with a compelling call-to-action mentioning Yatradham.
- Use short paragraphs (2-3 sentences max).
- Include bullet points and numbered lists where appropriate.
- Naturally mention related Yatradham packages where relevant.

Output valid JSON: {"title": "...", "meta_description": "...", "content": "...", "suggested_tags": ["...", "..."]}""",

    "landing_page": SYSTEM_PROMPT + """Write a high-converting landing page for a new travel/wellness package.

Rules:
- Start with a powerful headline and subheadline.
- Include a compelling hero section description.
- Write "Why Choose This" section with 5-6 bullet points.
- Create a "What's Included" section.
- Write an "Ideal For" section describing the target audience.
- Include a pricing/CTA section.
- Add 3-4 FAQ items.
- Use persuasive, benefit-focused language.
- Keep sentences under 20 words.

Output valid JSON: {"headline": "...", "subheadline": "...", "meta_description": "...", "hero_text": "...", "why_choose": ["..."], "whats_included": ["..."], "ideal_for": ["..."], "pricing_cta": "...", "faq": [{"q": "...", "a": "..."}], "full_content": "..."}""",

    "destination_guide": SYSTEM_PROMPT + """Write a comprehensive destination guide for spiritual/wellness tourism.

Rules:
- Cover: Overview, Best Time to Visit, How to Reach, Top Temples/Sites, Local Cuisine, Accommodation Options, Travel Tips, Nearby Destinations.
- Use H2/H3 markdown headings for structure.
- Include practical details (distances, costs in INR, timings).
- Write in an authoritative yet friendly tone.
- Mention Yatradham packages available for this destination.
- Include insider tips that only experienced travelers would know.

Output valid JSON: {"title": "...", "meta_description": "...", "content": "...", "key_highlights": ["..."], "suggested_tags": ["..."]}""",

    "social_media": SYSTEM_PROMPT + """Generate engaging social media captions for Instagram and Facebook.

Rules:
- Create 5 different caption variations (mix of short/long).
- Include relevant hashtags (10-15 per post).
- Use emojis strategically (not excessively).
- Include a clear call-to-action in each caption.
- Mix tones: inspirational, informational, promotional, storytelling.
- Keep Instagram captions under 2200 characters.
- Make them shareable and engaging.

Output valid JSON: {"captions": [{"platform": "instagram|facebook", "caption": "...", "hashtags": ["..."], "cta": "..."}]}"""
}


def run(
    content_type: str,
    topic: str,
    client: LLMClient,
    target_keyword: Optional[str] = None,
    audience: Optional[str] = None,
    tone: Optional[str] = None,
    word_count: Optional[int] = None,
    additional_instructions: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate net-new content based on user requirements."""
    
    system_prompt = CONTENT_TYPE_PROMPTS.get(content_type, CONTENT_TYPE_PROMPTS["blog_post"])
    
    # Build the user message with all available context
    parts = [f"Topic: {topic}"]
    if target_keyword:
        parts.append(f"Target SEO Keyword: {target_keyword}")
    if audience:
        parts.append(f"Target Audience: {audience}")
    if tone:
        parts.append(f"Writing Tone: {tone}")
    if word_count:
        parts.append(f"Target Word Count: {word_count} words")
    if additional_instructions:
        parts.append(f"Additional Instructions: {additional_instructions}")
    
    user_msg = "\n".join(parts) + "\n\nGenerate the content now. Output ONLY valid JSON."
    
    # Use higher max_tokens for content generation
    max_tokens = 4000
    if content_type == "destination_guide":
        max_tokens = 6000
    elif content_type == "social_media":
        max_tokens = 3000
    
    content = client.chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=max_tokens,
        temperature=0.7,
        response_format={"type": "json_object"},
    )
    
    try:
        # Clean the response content before parsing
        clean_content = content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content[7:]
        elif clean_content.startswith("```"):
            clean_content = clean_content[3:]
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3]
        clean_content = clean_content.strip()
        
        # If there's extra conversational text, try to extract just the JSON block
        if "{" in clean_content and "}" in clean_content:
            start_idx = clean_content.find("{")
            end_idx = clean_content.rfind("}") + 1
            clean_content = clean_content[start_idx:end_idx]

        result = json.loads(clean_content)
    except json.JSONDecodeError:
        # Return the raw text wrapped in a simple structure
        result = {
            "title": topic,
            "content": content,
            "error": "AI returned non-JSON content. Raw text is included above."
        }
    
    result["content_type"] = content_type
    result["topic"] = topic
    result["target_keyword"] = target_keyword or ""
    
    return result
