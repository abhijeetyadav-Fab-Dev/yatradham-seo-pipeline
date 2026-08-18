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

ANTI-AI DETECTION CRITICAL RULES:
- DO NOT use common AI transition words or filler (e.g., "Moreover", "Furthermore", "In conclusion", "It's important to note", "A testament to").
- DO NOT use overused corporate/AI verbs (e.g., "leverage", "utilize", "streamline", "foster", "delve", "embark"). Use simple, plain English (e.g., "use", "make easier", "build", "explore", "start").
- DO NOT use hollow intensifiers (e.g., "cutting-edge", "seamless", "robust", "game-changing", "tapestry").
- Vary your sentence lengths. Write some very short sentences. Write some longer, conversational sentences. Avoid perfect symmetry.
- Write in the active voice. Speak directly to the reader like a knowledgeable friend, not a textbook.

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


def _sanitize_repetition(text: str) -> str:
    """Strip LLM repetition loops (repeated single characters, phrases, or unicode loops)."""
    if not text:
        return ""
    # Remove repeated single characters (e.g. 琪琪琪... or aaaaa...)
    text = re.sub(r'(.)\1{4,}', r'\1', text)
    # Remove repeated 2-5 character patterns (e.g. abcabcabc...)
    text = re.sub(r'(.{2,6}?)\1{4,}', r'\1', text)
    # Remove repeated word loops (e.g. "word word word word word")
    text = re.sub(r'\b(\w+)(?:\s+\1\b){3,}', r'\1', text, flags=re.IGNORECASE)
    return text.strip()


def _clean_markdown(content: str) -> str:
    content = content.strip()
    if content.startswith("```markdown"):
        content = content[11:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    return content.strip()


def _generate_long_form_blog(
    topic: str,
    client: LLMClient,
    target_keyword: Optional[str] = None,
    audience: Optional[str] = None,
    tone: Optional[str] = None,
    word_count: int = 3000,
    additional_instructions: Optional[str] = None,
) -> Dict[str, Any]:
    """3-Phase chained generation for 3,000+ word comprehensive master guides with zero cutoffs."""
    
    brand_context = """You are an expert SEO Content Writer for Yatradham.Org (India's leading spiritual & wellness tourism platform since 2016).
Tone: Warm, devout, informative, highly detailed, E-E-A-T compliant, and unmistakably human.
Rules:
- Write in rich, descriptive detail with full paragraphs. Expand every single sub-activity with practical timings, benefits, and tips.
- Do NOT use brief summaries.
- Incorporate primary and related keywords naturally without keyword stuffing.
- ANTI-AI DETECTION CRITICAL RULES:
  - DO NOT use common AI transition words or filler (e.g., "Moreover", "Furthermore", "In conclusion", "It's important to note", "A testament to").
  - DO NOT use overused corporate/AI verbs (e.g., "leverage", "utilize", "streamline", "foster", "delve", "embark"). Use simple, plain English (e.g., "use", "make easier", "build", "explore", "start").
  - DO NOT use hollow intensifiers (e.g., "cutting-edge", "seamless", "robust", "game-changing", "tapestry").
  - Vary your sentence lengths. Write some very short sentences. Write some longer, conversational sentences. Avoid perfect symmetry.
  - Write in the active voice. Speak directly to the reader like a knowledgeable friend, not a textbook.
"""
    custom_rules = []
    if target_keyword:
        custom_rules.append(f"Target Primary Keyword: '{target_keyword}' (Integrate naturally in headings and body).")
    if audience:
        custom_rules.append(f"Target Audience: {audience}.")
    if tone and tone.lower() != "auto":
        custom_rules.append(f"Tone: {tone}.")
    if additional_instructions:
        custom_rules.append(f"User Instructions:\n{additional_instructions}")
    rules_text = "\n".join(custom_rules)

    # PHASE 1: Meta, Intro, Planning Essentials, Days 1-3 (~1,000 words)
    prompt_phase1 = f"""{brand_context}
{rules_text}

TASK: Generate PHASE 1 of a 3,000-word master travel guide on: "{topic}".
Target word count: ~1,000 words.

ANTI-DETECTION INSTRUCTIONS: 
- Write with HIGH PERPLEXITY and HIGH BURSTINESS.
- Use contractions (don't, you'll, we've).
- Write conversationally, as if you actually traveled there last month. Use a few brief personal-sounding anecdotes or observations (e.g., "When you step off the train...", "I usually tell travelers to...").
- AVOID perfectly balanced paragraphs. AVOID robotic list formatting.

Structure to generate for PHASE 1:
# TITLE
[Compelling, Human-sounding Title]

# META DESCRIPTION
[Engaging Meta Description (150-160 characters)]

# SUGGESTED TAGS
[Tag 1, Tag 2, Tag 3, Tag 4, Tag 5]

# CONTENT
## Why This Place Changes You
(Write ~300 words detailing the spiritual allure in a narrative, storytelling format).

## What You Actually Need to Know Before Going
(Write ~300 words covering Best Time, How to Reach, Verified Accommodation through Yatradham, and Packing. Format casually, not like a textbook).

## Day 1: Arriving and Slowing Down
(Write ~200 words. Tell them what to do on their first day. Do NOT use strict "Morning/Evening" subheadings. Just weave it into a story).

## Day 2: Getting into the Rhythm
(Write ~200 words about early asanas, food, and reflection).

## Day 3: Stepping Off the Paved Roads
(Write ~200 words about trails, nature, and quiet moments).

CRITICAL: Output rich, narrative paragraphs. Output ONLY markdown headings specified above."""

    part1_raw = client.chat_completion(
        messages=[{"role": "system", "content": brand_context}, {"role": "user", "content": prompt_phase1}],
        max_tokens=3000,
        temperature=0.6,
    )
    
    sections_part1 = _parse_markdown_sections(_clean_markdown(part1_raw))
    title = _sanitize_repetition(sections_part1.get("TITLE", topic))
    meta_desc = _sanitize_repetition(sections_part1.get("META DESCRIPTION", ""))
    tags_str = sections_part1.get("SUGGESTED TAGS", "")
    tags = [_sanitize_repetition(t) for t in tags_str.split(",") if _sanitize_repetition(t)] if tags_str else []
    content_part1 = _sanitize_repetition(sections_part1.get("CONTENT", part1_raw))

    # PHASE 2: Days 4-7 In-Depth Journey (~1,200 words)
    prompt_phase2 = f"""{brand_context}
{rules_text}

TASK: Generate PHASE 2 (Days 4 through 7) of the 3,000-word guide on: "{topic}".
Target word count: ~1,200 words.

ANTI-DETECTION INSTRUCTIONS: 
- Write with HIGH PERPLEXITY and HIGH BURSTINESS.
- Use contractions. Write like an experienced traveler giving advice.
- AVOID perfectly balanced paragraphs. DO NOT use "Morning/Mid-Day/Evening/Night" sub-subheadings. Tell the day as a flowing narrative.

We have already completed Days 1-3.
Now generate Days 4 through 7:

## Day 4: Detox and Real Healing
(Write ~300 words. Describe the Ayurvedic therapies and Sattvic food as an experience, not a schedule).

## Day 5: The Temples and the Culture
(Write ~300 words. Talk about ancient temples, Triveni Ghat, and Seva/Selfless service in a narrative way).

## Day 6: Finding Silence
(Write ~300 words. Focus on deep meditation, sound healing, and campfire reflections).

## Day 7: Packing Up and Taking It With You
(Write ~300 words. Cover the closing flow, building a home routine, and the emotional departure).

CRITICAL: Start immediately with `## Day 4`. Output ONLY markdown text."""

    part2_raw = client.chat_completion(
        messages=[{"role": "system", "content": brand_context}, {"role": "user", "content": prompt_phase2}],
        max_tokens=3000,
        temperature=0.6,
    )
    
    content_part2 = _sanitize_repetition(_clean_markdown(part2_raw))

    # PHASE 3: Logistics, FAQs & Conclusion (~800 words)
    prompt_phase3 = f"""{brand_context}
{rules_text}

TASK: Generate PHASE 3 (the finale) of the 3,000-word guide on: "{topic}".
Target word count: ~800 words.

ANTI-DETECTION INSTRUCTIONS: 
- Write with HIGH PERPLEXITY and HIGH BURSTINESS. Use contractions.
- AVOID generic conclusions like "In conclusion" or "Ultimately".

We have completed Days 1 through 7.
Now generate the final sections:

## The Real Logistics: Costs and Commutes
(Write ~350 words detailing transport, Yatradham verified bookings, realistic budgets, and safety. Keep it conversational).

## Frequently Asked Questions
(Write 6 conversational FAQs. Answer them like a human expert, not a corporate brochure).

## Final Thoughts Before You Go
(Write ~200 words. Give an inspiring, non-generic sign-off and a natural CTA for Yatradham.Org).

CRITICAL: Start immediately with `## The Real Logistics: Costs and Commutes`. Output ONLY markdown text."""

    part3_raw = client.chat_completion(
        messages=[{"role": "system", "content": brand_context}, {"role": "user", "content": prompt_phase3}],
        max_tokens=3000,
        temperature=0.6,
    )
    
    content_part3 = _sanitize_repetition(_clean_markdown(part3_raw))

    # Stitch Phase 1, Phase 2, and Phase 3 seamlessly
    full_content = f"{content_part1}\n\n{content_part2}\n\n{content_part3}"

    return {
        "title": title,
        "meta_description": meta_desc,
        "suggested_tags": tags,
        "content": full_content,
        "content_type": "blog_post",
        "topic": topic,
        "target_keyword": target_keyword or ""
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
    """Generate net-new content based on user requirements using robust markdown parsing."""
    
    # If the user requested an exhaustive long-form blog post (2,000 - 3,500 words), use the 2-stage chained generator
    if content_type in ["blog_post", "destination_guide"] and word_count and word_count >= 2000:
        return _generate_long_form_blog(
            topic=topic,
            client=client,
            target_keyword=target_keyword,
            audience=audience,
            tone=tone,
            word_count=word_count,
            additional_instructions=additional_instructions
        )

    base_prompt = CONTENT_TYPE_PROMPTS.get(content_type, CONTENT_TYPE_PROMPTS["blog_post"])
    target_tokens = min(4000, max(2000, int((word_count or 1000) * 1.5)))

    custom_rules = []
    if target_keyword:
        custom_rules.append(f"- Primary SEO Keyword: '{target_keyword}' (Integrate naturally in Title, Meta Description, H2s, H3s, and throughout content without keyword stuffing).")
    if audience:
        custom_rules.append(f"- Target Audience: {audience} (Tailor perspective, depth, and relevance to them).")
    if tone and tone.lower() != "auto":
        custom_rules.append(f"- Desired Tone of Voice: {tone}.")
    if additional_instructions:
        custom_rules.append(f"- MANDATORY USER INSTRUCTIONS:\n{additional_instructions}")

    rules_block = "\n".join(custom_rules) if custom_rules else ""

    enhanced_system_prompt = f"""{base_prompt}

ADDITIONAL CRITICAL CONSTRAINTS:
{rules_block}
"""

    user_msg = f"""Topic: {topic}
{f"Target Keyword: {target_keyword}" if target_keyword else ""}
{f"Target Audience: {audience}" if audience else ""}
{f"Target Length: ~{word_count} words" if word_count else ""}

Please generate the complete, high-quality, comprehensive {content_type.replace('_', ' ')} for Yatradham.Org now.
Follow all formatting rules and markdown heading conventions strictly."""

    # Generate content
    content = client.chat_completion(
        messages=[
            {"role": "system", "content": enhanced_system_prompt},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=target_tokens,
        temperature=0.6,
    )

    content = _clean_markdown(content)
    sections = _parse_markdown_sections(content)
    
    # Map markdown sections to the expected JSON schema for the frontend
    result = {}
    
    if content_type in ["blog_post", "destination_guide"]:
        result["title"] = _sanitize_repetition(sections.get("TITLE", topic))
        result["meta_description"] = _sanitize_repetition(sections.get("META DESCRIPTION", ""))
        result["content"] = _sanitize_repetition(sections.get("CONTENT", content))
        
        tags_str = sections.get("SUGGESTED TAGS", "")
        result["suggested_tags"] = [_sanitize_repetition(t) for t in tags_str.split(",") if _sanitize_repetition(t)] if tags_str else []
        
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
