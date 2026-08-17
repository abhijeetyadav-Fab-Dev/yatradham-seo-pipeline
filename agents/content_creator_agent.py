"""Content Creator Agent: Generates net-new SEO content from scratch."""
import re
from typing import Dict, Any, Optional
from llm_client import LLMClient


SYSTEM_PROMPT = """You are an expert SEO Content Writer and Marketer for Yatradham.org.

ABOUT YATRADHAM.ORG:
- Yatradham is India's first dedicated religious tourism platform (launched in 2016).
- Services: Verified accommodation bookings and Puja services across 700+ pilgrimage destinations.
- Mission: Support pilgrims in their spiritual journey by taking care of stay and logistics.
- Brand Voice: Respectful, devout, helpful, informative, trustworthy, and welcoming.

Your goal is to generate high-quality, engaging, and SEO-optimized content based on the user's request.
CRITICAL RULE: You MUST format your response EXACTLY using the markdown headings requested. Do NOT output JSON. Do NOT output code blocks. Just plain markdown text.
"""


CONTENT_TYPE_PROMPTS = {
    "blog_post": SYSTEM_PROMPT + """Write a comprehensive, engaging, and SEO-optimized blog post.

Rules:
- Use the target keyword naturally 3-5 times.
- Structure with H2 and H3 subheadings.
- Write in an informative yet warm tone.
- Include practical tips and actionable advice.
- End with a compelling call-to-action mentioning Yatradham.

Format your response EXACTLY like this:
# TITLE
[Your Title Here]

# META DESCRIPTION
[Your Meta Description Here]

# SUGGESTED TAGS
[Tag 1, Tag 2, Tag 3]

# CONTENT
[Your Blog Content Here]""",

    "landing_page": SYSTEM_PROMPT + """Write a high-converting landing page for a new travel/wellness package.

Rules:
- Start with a powerful headline and subheadline.
- Write persuasive, benefit-focused language.
- Keep sentences short and clear.

Format your response EXACTLY like this:
# HEADLINE
[Your Headline]

# SUBHEADLINE
[Your Subheadline]

# META DESCRIPTION
[Your Meta Description]

# HERO TEXT
[Your Hero Text]

# WHY CHOOSE
- [Reason 1]
- [Reason 2]

# WHATS INCLUDED
- [Item 1]
- [Item 2]

# IDEAL FOR
- [Audience 1]
- [Audience 2]

# PRICING CTA
[Your CTA Text]

# FAQ
Q: [Question 1]
A: [Answer 1]

Q: [Question 2]
A: [Answer 2]""",

    "destination_guide": SYSTEM_PROMPT + """Write a comprehensive destination guide for spiritual/wellness tourism.

Rules:
- Cover: Overview, Best Time to Visit, How to Reach, Top Temples, Accommodation Options.
- Include practical details (distances, costs, timings).

Format your response EXACTLY like this:
# TITLE
[Your Title Here]

# META DESCRIPTION
[Your Meta Description Here]

# SUGGESTED TAGS
[Tag 1, Tag 2]

# KEY HIGHLIGHTS
- [Highlight 1]
- [Highlight 2]

# CONTENT
[Your Destination Guide Content Here]""",

    "social_media": SYSTEM_PROMPT + """Generate engaging social media captions for Instagram and Facebook.

Rules:
- Create 3-5 different caption variations.
- Include relevant hashtags.
- Use emojis strategically.

Format your response EXACTLY like this:
# CAPTION 1
Platform: Instagram
Text: [Caption Text]
Hashtags: [#tag1 #tag2]

# CAPTION 2
Platform: Facebook
Text: [Caption Text]
Hashtags: [#tag1 #tag2]"""
}


def _parse_markdown_sections(text: str) -> Dict[str, str]:
    """Parse a markdown string into a dictionary based on H1 headings."""
    sections = {}
    current_heading = None
    current_content = []

    for line in text.split('\n'):
        if line.startswith('# '):
            if current_heading:
                sections[current_heading] = '\n'.join(current_content).strip()
            current_heading = line[2:].strip()
            current_content = []
        elif current_heading:
            current_content.append(line)

    if current_heading:
        sections[current_heading] = '\n'.join(current_content).strip()

    return sections


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
    """Generate net-new content based on user requirements using robust markdown parsing."""
    
    system_prompt = CONTENT_TYPE_PROMPTS.get(content_type, CONTENT_TYPE_PROMPTS["blog_post"])
    
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
    
    user_msg = "\n".join(parts) + "\n\nGenerate the content now. Output ONLY the requested markdown format."
    
    # Generate content (without JSON format constraint)
    content = client.chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=4000,
        temperature=0.7,
    )

    # Clean markdown blocks if LLM still includes them
    if content.startswith("```markdown"):
        content = content[11:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
        
    sections = _parse_markdown_sections(content.strip())
    
    # Map markdown sections to the expected JSON schema for the frontend
    result = {}
    
    if content_type in ["blog_post", "destination_guide"]:
        result["title"] = sections.get("TITLE", topic)
        result["meta_description"] = sections.get("META DESCRIPTION", "")
        result["content"] = sections.get("CONTENT", content) # fallback to full content if parsing fails
        
        tags_str = sections.get("SUGGESTED TAGS", "")
        result["suggested_tags"] = [t.strip() for t in tags_str.split(",")] if tags_str else []
        
        if content_type == "destination_guide":
            hl_str = sections.get("KEY HIGHLIGHTS", "")
            result["key_highlights"] = [h.replace("- ", "").strip() for h in hl_str.split("\n") if h.strip()]
            
    elif content_type == "landing_page":
        result["headline"] = sections.get("HEADLINE", topic)
        result["subheadline"] = sections.get("SUBHEADLINE", "")
        result["meta_description"] = sections.get("META DESCRIPTION", "")
        result["hero_text"] = sections.get("HERO TEXT", "")
        
        for key, out_key in [("WHY CHOOSE", "why_choose"), ("WHATS INCLUDED", "whats_included"), ("IDEAL FOR", "ideal_for")]:
            val = sections.get(key, "")
            result[out_key] = [i.replace("- ", "").strip() for i in val.split("\n") if i.strip()]
            
        result["pricing_cta"] = sections.get("PRICING CTA", "")
        
        # Parse FAQ
        faq_raw = sections.get("FAQ", "")
        faqs = []
        current_q, current_a = "", ""
        for line in faq_raw.split("\n"):
            if line.startswith("Q:"):
                if current_q: faqs.append({"q": current_q, "a": current_a.strip()})
                current_q = line[2:].strip()
                current_a = ""
            elif line.startswith("A:"):
                current_a = line[2:].strip()
            elif current_a != "":
                current_a += " " + line.strip()
        if current_q:
            faqs.append({"q": current_q, "a": current_a.strip()})
        result["faq"] = faqs
        
    elif content_type == "social_media":
        captions = []
        for key, text in sections.items():
            if "CAPTION" in key:
                lines = text.split("\n")
                platform = "social"
                caption_text = []
                hashtags = []
                for line in lines:
                    if line.startswith("Platform:"):
                        platform = line.split(":", 1)[1].strip().lower()
                    elif line.startswith("Hashtags:"):
                        tags = line.split(":", 1)[1].strip()
                        hashtags = [t.strip() for t in tags.split(" ") if t.strip()]
                    elif line.startswith("Text:"):
                        caption_text.append(line.split(":", 1)[1].strip())
                    else:
                        caption_text.append(line.strip())
                
                captions.append({
                    "platform": platform,
                    "caption": "\n".join(caption_text).strip(),
                    "hashtags": hashtags
                })
        result["captions"] = captions if captions else [{"platform": "social", "caption": content, "hashtags": []}]

    # Always ensure content_type and topic are set
    result["content_type"] = content_type
    result["topic"] = topic
    result["target_keyword"] = target_keyword or ""
    
    return result
