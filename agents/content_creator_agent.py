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
    """Parse a markdown string into a dictionary based on H1 headings and H2 transitions."""
    sections = {}
    current_heading = None
    current_content = []

    for line in text.split('\n'):
        if line.startswith('# '):
            if current_heading:
                sections[current_heading] = '\n'.join(current_content).strip()
            current_heading = line[2:].strip()
            current_content = []
        elif line.startswith('## ') and current_heading in ['SUGGESTED TAGS', 'TAGS', 'META DESCRIPTION', 'TITLE', None]:
            # Transitioned into main content without an explicit # CONTENT H1 header
            if current_heading:
                sections[current_heading] = '\n'.join(current_content).strip()
            current_heading = 'CONTENT'
            current_content = [line]
        elif current_heading:
            current_content.append(line)

    if current_heading:
        sections[current_heading] = '\n'.join(current_content).strip()

    return sections


def _sanitize_repetition(text: str) -> str:
    """Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks."""
    if not text:
        return ""
    
    # 1. Clean catastrophic loops (characters and single words)
    text = re.sub(r'(.)\1{4,}', r'\1', text)
    text = re.sub(r'(.{2,6}?)\1{4,}', r'\1', text)
    text = re.sub(r'\b(\w+)(?:\s+\1\b){3,}', r'\1', text, flags=re.IGNORECASE)
    
    # 2. Clean multi-line loops (LLM gets stuck repeating identical blocks)
    blocks = re.split(r'\n\s*\n', text)
    cleaned_blocks = []
    for block in blocks:
        if not cleaned_blocks or cleaned_blocks[-1].strip() != block.strip():
            cleaned_blocks.append(block)
    text = '\n\n'.join(cleaned_blocks)
    
    # 3. Clean consecutive identical lines
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if not cleaned_lines or cleaned_lines[-1].strip() != line.strip():
            cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)

    # 4. AI "Slop" Word Replacements (Beats Copyleaks Word-Frequency detection)
    ai_phrases = {
        r'\bDelve into\b': 'Discover',
        r'\bdelve into\b': 'discover',
        r'\bEmbark on\b': 'Start',
        r'\bembark on\b': 'start',
        r'\bLeverage\b': 'Use',
        r'\bleverage\b': 'use',
        r'\bUtilize\b': 'Use',
        r'\butilize\b': 'use',
        r'\bTapestry of\b': 'Blend of',
        r'\btapestry of\b': 'blend of',
        r'\bSeamless(ly)?\b': r'Smooth\1',
        r'\bseamless(ly)?\b': r'smooth\1',
        r'\bRobust\b': 'Reliable',
        r'\brobust\b': 'reliable',
        r'\bFoster(ing)?\b': r'Build\1',
        r'\bfoster(ing)?\b': r'build\1',
        r'\bCutting-edge\b': 'Excellent',
        r'\bcutting-edge\b': 'excellent',
        r'\bTestament to\b': 'Proof of',
        r'\btestament to\b': 'proof of',
        r'\bMoreover,?\b': 'Also,',
        r'\bmoreover,?\b': 'also,',
        r'\bFurthermore,?\b': 'In addition,',
        r'\bfurthermore,?\b': 'in addition,',
        r'\bUltimately,?\b': 'In the end,',
        r'\bultimately,?\b': 'in the end,',
        r'\bIt is important to note that\b': 'Remember that',
        r'\bit is important to note that\b': 'remember that',
        r'\bBeacon of\b': 'Center of',
        r'\bbeacon of\b': 'center of',
        r'\bNestled\b': 'Located',
        r'\bnestled\b': 'located',
        r'\bVibrant\b': 'Lively',
        r'\bvibrant\b': 'lively'
    }
    
    for pattern, replacement in ai_phrases.items():
        text = re.sub(pattern, replacement, text)
        
    return text.strip()


def _strip_thinking_tags(text: str) -> str:
    """Remove LLM chain-of-thought / reasoning blocks that leak into output.
    
    Models like DeepSeek, Gemini Thinking, and QwQ wrap internal reasoning
    in <think>...</think>, <reasoning>...</reasoning>, etc.
    """
    if not text:
        return ""
    # 1. Strip all closed reasoning tag pairs
    for tag in ("think", "thinking", "reasoning", "reflection", "inner_monologue", "scratchpad"):
        text = re.sub(
            rf"<{tag}>.*?</{tag}>",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )
    # 2. Handle unclosed reasoning tags (e.g. model drafted inside <think> and got cut off or didn't close)
    for tag in ("think", "thinking", "reasoning", "reflection"):
        pattern = rf"<{tag}>"
        while re.search(pattern, text, flags=re.IGNORECASE):
            m = re.search(pattern, text, flags=re.IGNORECASE)
            start_pos = m.start()
            rest = text[m.end():]
            # Look for where actual markdown content or headers start after <think>
            header_match = re.search(r'(?:\n|^)(#{1,3}\s+[^\n]+)', rest)
            if header_match:
                text = text[:start_pos] + rest[header_match.start():]
            else:
                text = text[:start_pos]
                break
    return text.strip()


def _clean_markdown(content: str) -> str:
    # First strip any leaked reasoning / thinking blocks
    content = _strip_thinking_tags(content)
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
    """Single-pass unified generation for 3,000+ word comprehensive master guides adhering to top SEO ranking guardrails."""
    
    brand_context = """You are an elite SEO Content Strategist & Travel Writer for Yatradham.Org (India's premier spiritual & wellness tourism platform since 2016).

CORE SEO & EDITORIAL GUARDRAILS (Inspired by Top-Ranking Industry Standards):
1. Search Intent First: Answer real pilgrim and traveler questions with practical, high-value, actionable advice—never fluffy filler.
2. Clear Structural Hierarchy: Use logical H2s and H3s with natural keyword inclusion. Make content scannable with bullet points for rules, checklists, and key takeaways.
3. Deep E-E-A-T & Practical Specificity: Provide exact timings, realistic pricing in INR, route comparisons, verified dharamshala/ashram advice, and local nuances.
4. Strategic Brand Integration: Seamlessly highlight Yatradham.Org as the trusted platform for verified bookings, clean dharamshalas, and transparent pricing.
5. ANTI-AI DETECTION / HUMAN WRITING STANDARDS:
   - Write with high perplexity and burstiness. Mix short, punchy statements with descriptive, narrative sentences.
   - Use active voice, contractions (you'll, don't, we've), and conversational advice.
   - STRICTLY FORBIDDEN AI SLOP: "delve into", "tapestry of", "testament to", "nestled in", "seamlessly", "moreover", "furthermore", "in conclusion", "it's important to note".
"""
    custom_rules = []
    if target_keyword:
        custom_rules.append(f"Target Primary Keyword: '{target_keyword}' (Integrate naturally in H1, H2s, and body text).")
    if audience:
        custom_rules.append(f"Target Audience: {audience}.")
    if tone and tone.lower() != "auto":
        custom_rules.append(f"Tone: {tone}.")
    if additional_instructions:
        custom_rules.append(f"User Instructions:\n{additional_instructions}")
    rules_text = "\n".join(custom_rules)

    master_prompt = f"""{brand_context}
{rules_text}

TASK: Generate a complete, exhaustive, 3,000-word master travel and wellness guide on: "{topic}".
Target word count: ~{word_count or 3000} words.

CRITICAL INSTRUCTIONS:
- Write in rich, descriptive narrative detail across all sections.
- Cover every single day (Day 1 through Day 7) with full practical depth, timings, meal details, and tips.
- Do NOT skip any days. Do NOT provide brief bullet summaries where full paragraphs are required.
- Do NOT generate multiple FAQ or Conclusion sections. Follow the exact structure below once from top to bottom.

EXACT OUTPUT STRUCTURE REQUIRED:

# TITLE
[Search-optimized, high CTR title with target keyword]

# META DESCRIPTION
[Engaging meta description with keyword and value hook (150-160 characters)]

# SUGGESTED TAGS
[Tag 1, Tag 2, Tag 3, Tag 4, Tag 5]

# CONTENT
## Why This Place Changes You
(Write ~300 words. Open with an engaging hook. Explain the unique spiritual and rejuvenating energy of the destination).

## What You Actually Need to Know Before Going
(Write ~350 words covering Best Time to Visit, How to Reach with airport/train routes, Verified Stay Advice via Yatradham.Org, and a quick bulleted packing checklist).

## Day 1: Arriving and Slowing Down
(Write ~250 words. Arrival flow, settling into your stay, first peaceful river/temple visit, and sattvic welcome meal).

## Day 2: Getting into the Rhythm
(Write ~250 words. Early sunrise practice/darshan, nourishing breakfast, mid-day reflection or workshop, and quiet evening).

## Day 3: Stepping Off the Paved Roads
(Write ~250 words. Nature trails, hidden spots, waterfall/temple walks, and local cultural interaction).

## Day 4: Detox, Healing & Deep Practices
(Write ~250 words. Focus on Ayurvedic therapies, herbal care, dosha balance, and sattvic rejuvenation).

## Day 5: Ancient Temples & Living Culture
(Write ~250 words. Sacred shrines, evening Ganga Aarti at the ghats, cultural immersion, and seva/selfless service).

## Day 6: Finding Silence & Inner Stillness
(Write ~250 words. Deep meditation, sound healing, mindful walking, and peaceful evening campfire reflection).

## Day 7: Packing Up & Taking the Peace Home
(Write ~250 words. Closing gratitude rituals, buying local herbs/souvenirs, building a home routine, and checkout).

## 3 Key Takeaways for a Seamless Journey
(Provide 3 actionable, high-impact bulleted rules for travelers covering pacing, local etiquette, and verified booking).

## The Real Logistics: Costs, Stays & Commutes
(Write ~350 words detailing flight/train connections, realistic daily budget ranges in INR, local commute tips, and the advantages of booking verified dharamshalas and wellness stays through Yatradham.Org).

## Frequently Asked Questions
(Provide exactly 6 distinct, search-focused FAQs with thorough, direct answers covering budget, beginner friendliness, solo travel safety, packing, meals, and best booking seasons).

## Final Thoughts & Planning Your Trip
(Write ~200 words. An inspiring conclusion encouraging the reader to take the first step, with a natural call-to-action to explore verified accommodations and packages on Yatradham.Org).

CRITICAL: Output ONLY markdown text starting with `# TITLE`. Follow the structure completely."""

    raw_response = client.chat_completion(
        messages=[
            {"role": "system", "content": brand_context},
            {"role": "user", "content": master_prompt}
        ],
        max_tokens=6000,
        temperature=0.6,
    )

    cleaned = _clean_markdown(raw_response)
    sections = _parse_markdown_sections(cleaned)

    title = _sanitize_repetition(sections.get("TITLE", topic))
    meta_desc = _sanitize_repetition(sections.get("META DESCRIPTION", ""))
    tags_str = sections.get("SUGGESTED TAGS", "")
    tags = [_sanitize_repetition(t) for t in tags_str.split(",") if _sanitize_repetition(t)] if tags_str else []

    part_content = sections.get("CONTENT", "")
    if not part_content:
        h2_idx = cleaned.find("## ")
        if h2_idx != -1:
            part_content = cleaned[h2_idx:]
        else:
            part_content = cleaned

    full_content = _sanitize_repetition(part_content)

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
