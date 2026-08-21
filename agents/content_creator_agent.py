"""Content Creator Agent: Generates net-new SEO content from scratch."""
import re
import logging
from typing import Dict, Any, Optional
from llm_client import LLMClient
from anti_ai_guardrails import de_slop_and_humanize, GOOGLE_HELPFUL_CONTENT_GUARDRAILS

logger = logging.getLogger("content_creator_agent")


YATRADHAM_ECOSYSTEM_KNOWLEDGE = """
OFFICIAL YATRADHAM.ORG ECOSYSTEM DIRECTORY & INTERNAL LINKING GUIDELINES:
You MUST naturally cite, reference, and link to these official YatraDham portals wherever contextually relevant:
1. Main Stays & Accommodations: [YatraDham.Org](https://yatradham.org/) — Verified dharamshalas, ashrams, hotels, and guest houses across 700+ pilgrimage sites.
2. Online Temple Pujas & Sevas: [YatraDham Temple Pujas](https://temple.yatradham.org/pujas) — Authentic Vedic ritual bookings, Sankalp Pujas, and Temple Sevas performed by verified temple priests.
3. Yatra Travel & Tour Packages: [YatraDham Travel Packages](https://travel.yatradham.org/) — Custom and fixed pilgrimage tour packages, tempo travelers, buses, and private car rentals.
4. Verified Pandit Ji Bookings: [YatraDham Pandit Ji](https://temple.yatradham.org/pandit-ji) — Book verified, experienced Vedic Pandit Ji for rituals (Hawan, Pind Daan, Abhishek, Rudrabhishek).
5. Wellness & Ayurveda Retreats: [YatraDham Wellness](https://wellness.yatradham.org/) — Verified Ayurveda centers, Yoga ashrams, Naturopathy, and Panchakarma retreats across Rishikesh, Haridwar, Kerala, and Himachal.
6. Chardham Packages & Bookings: [YatraDham Chardham Packages](https://yatradham.org/chardham-package) — Dedicated Char Dham Yatra booking packages, registration guidance, helicopter passes, and stays for Yamunotri, Gangotri, Kedarnath, and Badrinath.
7. Kumbh Mela Stays & Guidance: [YatraDham Kumbh Mela Nashik](https://yatradham.org/kumbh-mela-nashik/) — Kumbh Mela tent cities, dharamshalas, and Shahi Snan dates.
"""

SYSTEM_PROMPT = f"""You are an expert SEO Content Writer and Travel Strategist for Yatradham.org.

ABOUT YATRADHAM.ORG:
- Yatradham is India's first dedicated religious tourism platform (launched in 2016).
- Services: Verified accommodation bookings, Tour packages, and Puja services across 700+ pilgrimage destinations.
- Mission: Support pilgrims in their spiritual journey by taking care of stay, transit, and puja logistics.
- Brand Voice: Respectful, devout, helpful, practical, trustworthy, and welcoming.

{YATRADHAM_ECOSYSTEM_KNOWLEDGE}

{GOOGLE_HELPFUL_CONTENT_GUARDRAILS}

EDITORIAL & AUTHENTIC WRITING GUARDRAILS (SECOND-LAYER QUALITY STANDARDS):
1. HIGH BURSTINESS & SENTENCE VARIETY:
   - Vary sentence lengths noticeably. Mix short, punchy 4-to-7 word observations with longer, descriptive explanations.
   - Avoid uniform rhythm or symmetrical paragraph structures. Write natural paragraphs ranging from 2 to 5 sentences.
2. ZERO ROBOTIC CLICHÉS OR FILLER TRANSITIONS:
   - STRICTLY FORBIDDEN FILLER: "Moreover", "Furthermore", "In conclusion", "It is important to note", "A testament to", "Needless to say", "In today's fast-paced world", "Look no further".
   - STRICTLY FORBIDDEN BUZZWORDS: "tapestry", "beacon", "delve", "foster", "holistic", "embark", "leverage", "utilize", "seamlessly", "nestled", "unravel", "transformative journey".
   - Use direct, everyday English verbs (e.g., "use", "start", "visit", "explore", "walk", "learn", "book").
3. CONCRETE REAL-WORLD DETAILS & LOGISTICS:
   - Ground every section in real numbers, exact INR prices (e.g., ₹500–₹1,200/night for ashrams), specific route advice, meal timings, and local etiquette.
   - Give practical, no-nonsense travel tips instead of abstract generalizations.
4. ACTIVE VOICE & DIRECT EXPERIENTIAL ADDRESS:
   - Speak directly to the reader like an experienced local guide ("When you reach Haridwar...", "Take an auto to Ram Jhula...", "Pack breathable cottons...").
   - Avoid passive academic phrasing (e.g., replace "It is recommended that one should book" with "Book your room 2 weeks early").
5. MANDATORY USER INSTRUCTIONS PRIORITY:
   - If the user provides any specific URLs, links, pricing constraints, or special notes in Additional Instructions, you MUST strictly include and honor them in the body of the generated content.

Your goal is to generate rich, engaging, highly informative, and authoritative content.
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

CORE SEO & EDITORIAL GUARDRAILS (SECOND-LAYER AUTHENTIC WRITING STANDARDS):
1. SEARCH INTENT & PRACTICAL VALUE FIRST:
   - Answer real pilgrim and traveler questions with practical, high-value, actionable advice—never fluffy filler.
2. HIGH BURSTINESS & VARIED SYNTAX:
   - Mix short, punchy 4-to-7 word observations with longer, descriptive explanations.
   - Avoid symmetric paragraph rhythms. Write organic paragraphs ranging from 2 to 5 sentences.
3. ZERO ROBOTIC CLICHÉS OR FILLER TRANSITIONS:
   - STRICTLY FORBIDDEN FILLER: "Moreover", "Furthermore", "In conclusion", "It is important to note", "A testament to", "Needless to say", "In today's fast-paced world", "Look no further".
   - STRICTLY FORBIDDEN BUZZWORDS: "tapestry", "beacon", "delve into", "foster", "holistic", "embark on", "leverage", "utilize", "seamlessly", "nestled in", "unravel", "transformative journey".
   - Use plain, active English verbs (e.g., "use", "start", "visit", "explore", "walk", "learn", "book").
4. DEEP E-E-A-T & PRACTICAL SPECIFICITY:
   - Provide exact timings (e.g., 5:30 AM Ganga Aarti, 6:00 AM Yoga), realistic pricing in INR (e.g., ₹600–₹1,500/night for ashrams), route comparisons, verified dharamshala advice, and local customs.
5. ACTIVE VOICE & DIRECT EXPERIENTIAL ADDRESS:
   - Speak directly to the reader like an experienced local guide ("When you reach Haridwar...", "Take an auto to Ram Jhula...", "Pack breathable cottons...").
   - Avoid passive academic phrasing (e.g., replace "It is recommended that one should book" with "Book your room 2 weeks early").
6. STRATEGIC BRAND INTEGRATION:
   - Naturally highlight Yatradham.Org as the trusted platform for verified bookings, clean dharamshalas, and transparent pricing without sounding like a hard sales pitch.
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
- Write in rich, descriptive narrative detail across all sections with full paragraphs.
- For EVERY single day (Day 1 through Day 7), provide the complete breakdown: Morning, Afternoon, Evening, and a Practical Insider Tip.
- Do NOT skip any days or compress them into single short paragraphs. Each day must be rich with practical advice, timings, and local context.
- Follow the exact structure below once from top to bottom.

EXACT OUTPUT STRUCTURE REQUIRED:

# TITLE
[Search-optimized, high CTR title with target keyword]

# META DESCRIPTION
[Engaging meta description with keyword and value hook (150-160 characters)]

# SUGGESTED TAGS
[Tag 1, Tag 2, Tag 3, Tag 4, Tag 5]

# CONTENT
## Introduction: The Sacred Energy & Spiritual Allure
(Write ~300 words. Open with an engaging hook. Explain the history, spiritual allure, and why this journey resets your body and mind).

## Essential Planning & Preparation Before You Go
(Write ~350 words covering Best Time to Visit, How to Reach with airport/train routes, Verified Stay Advice via Yatradham.Org, and a quick bulleted packing checklist).

## Day 1: Arrival, Settling In & Gentle Immersion
- **Morning & Afternoon:** (Write ~150 words. Arrival flow, checking into your Yatradham-verified stay, exploring the serene surroundings, and settling in).
- **Evening:** (Write ~150 words. First stroll along the sacred river/ghats, witnessing evening rituals/aarti, and enjoying a light sattvic welcome dinner).
- **Practical Insider Tip:** (Specific timings, route notes, and check-in guidance).

## Day 2: Awakening the Body & Mindful Movement
- **Morning:** (Write ~150 words. Sunrise yoga/darshan session, pranayama breathwork, and nourishing breakfast).
- **Afternoon & Evening:** (Write ~150 words. Introduction to Ayurvedic wellness, restorative self-care workshop, mindful walking, and peaceful dinner).
- **Practical Insider Tip:** (Hydration, yoga/temple recommendations, and meal advice).

## Day 3: Nature Trails, Waterfalls & Sacred Spaces
- **Morning:** (Write ~150 words. Scenic nature walk, hill trail or waterfall trek, forest bathing, and panoramic views).
- **Afternoon & Evening:** (Write ~150 words. Local herbal tea tasting, cultural interaction, sunset meditation by the riverbank, and fire ceremony).
- **Practical Insider Tip:** (Trek difficulty, footwear tips, and local guide advice).

## Day 4: Deep Detox, Healing Therapies & Rejuvenation
- **Morning:** (Write ~150 words. Traditional Ayurvedic consultation, herbal oil therapy/Abhyanga, and dosha balancing).
- **Afternoon & Evening:** (Write ~150 words. Sattvic cooking workshop, restorative yoga nidra relaxation, and calming herbal infusions).
- **Practical Insider Tip:** (Therapy cost ranges in INR and booking verified centers).

## Day 5: Ancient Temples, Sacred Shrines & Living Culture
- **Morning:** (Write ~150 words. Early temple darshan, understanding sacred rituals, and participating in seva/selfless service).
- **Afternoon & Evening:** (Write ~150 words. Cultural walk through historic ashrams/bazaars, attending grand evening Aarti, and group reflection).
- **Practical Insider Tip:** (Temple etiquette, photography guidelines, and aarti timings).

## Day 6: Sound Healing, Silence & Deep Stillness
- **Morning:** (Write ~150 words. Silent walking meditation along the riverbank, guided breath awareness, and wholesome breakfast).
- **Afternoon & Evening:** (Write ~150 words. Singing bowl sound healing session, quiet journaling, and evening campfire reflection).
- **Practical Insider Tip:** (Sound bath preparation and mental stillness practices).

## Day 7: Integration, Departure & Carrying the Peace Home
- **Morning:** (Write ~150 words. Closing gratitude ritual, building a sustainable home wellness routine, and picking up authentic local herbs/souvenirs).
- **Afternoon & Evening:** (Write ~150 words. Mindful checkout, luggage assistance via Yatradham stay, departure transit, and final reflections).
- **Practical Insider Tip:** (Late checkout advice and maintaining daily habits at home).

## 3 Key Takeaways From This 7-Day Journey
### 1. Pacing Drives True Rejuvenation
(Write 2-3 paragraphs. Explain why rushing ruins a spiritual wellness trip and how allocating 2-3 hours per practice creates long-lasting benefits).

### 2. High-Value Experiences Win Over Crowded Sightseeing
(Write 2-3 paragraphs. Explain why personalized Ayurveda, quiet meditation, and authentic ashram stays deliver 10x more value than tourist traps).

### 3. Local Etiquette & Trust Build the Connection
(Write 2-3 paragraphs. Detail temple customs, sacred river protocols, and respecting local culture).

## 4 Ways Yatradham.Org Makes Your Journey Seamless & Safe
### 1. Verified Accommodations & Transparent Pricing
(Explain how Yatradham vets dharamshalas, ashrams, and wellness retreats for hygiene, transparent rates with zero hidden broker fees).
- Zero surprise checkout charges
- Verified photos and guest reviews
- Prime locations near sacred ghats

### 2. Dedicated Yatra & Transport Coordination
(Explain how Yatradham assists with reliable local transfers, station pickups, and transparent taxi rates).
- Pre-negotiated fares from Dehradun and Haridwar
- Trusted, background-verified drivers
- Direct helpline for route updates

### 3. Tailored Spiritual & Wellness Itineraries
(Explain how Yatradham guides travelers to authentic ashram schedules, certified Ayurvedic doctors, and genuine meditation halls).
- Curated daily routines for beginners and seasoned seekers
- Direct access to authentic temple aarti timings
- Guidance on sattvic dining options

### 4. 24/7 Pilgrim Support & Flexible Booking
(Explain Yatradham's dedicated customer support for seamless date adjustments and on-ground help).
- Round-the-clock helpline
- Flexible cancellation on select partner properties
- Real-time WhatsApp assistance

## 3 Actionable Tips to Plan Your Journey Today
### 1. Plan Around Search & Seasonal Intent
(Explain how choosing shoulder months like October-November or February-March maximizes weather comfort and avoids peak holiday surges).

### 2. Book Your Verified Stay in Advance
(Explain why booking verified ashrams and dharamshalas early prevents last-minute scams and ensures clean rooms near the ghats).

### 3. Maintain Consistency With Daily Routines
(Explain how keeping simple morning and evening habits built during the trip anchors your wellness routine when returning home).

## The Real Logistics: Costs, Stays & Commutes
(Write ~400 words detailing flight/train connections with fares in INR, realistic daily budget breakdowns from budget to luxury, local commute rates, and why booking verified dharamshalas and wellness stays through Yatradham.Org guarantees transparent pricing and safety).

## Frequently Asked Questions
(Provide exactly 6 distinct, search-focused FAQs with thorough, direct answers covering budget, beginner friendliness, solo female safety, packing, sattvic meals, and best booking seasons).

## Final Thoughts & Planning Your Trip
(Write ~200 words. An inspiring conclusion encouraging the reader to take the first step, with a natural call-to-action to explore verified accommodations and packages on Yatradham.Org).

## Related Articles & Recommended Reading
(Provide 3 formatted internal article suggestions for readers planning spiritual/wellness travel):
- **Title:** [Related Guide 1 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 2 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 3 Title] (Author • Date • 1-line topic summary)

CRITICAL: Output ONLY markdown text starting with `# TITLE`. Follow the structure completely."""

    raw_response = client.chat_completion(
        messages=[
            {"role": "system", "content": brand_context},
            {"role": "user", "content": master_prompt}
        ],
        max_tokens=4000,
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

    # Ensure ALL closing sections are 100% completed and not cut off mid-way
    has_faqs = "## Frequently Asked Questions" in full_content or "## FAQs" in full_content
    has_final_thoughts = "## Final Thoughts" in full_content or "## Conclusion" in full_content
    has_related_articles = "## Related Articles" in full_content
    is_cut_off = full_content.strip().endswith(("-", "•", "–", ":", "and", "or", "the", "with", "to", "in", "of", "a", "..."))

    if not (has_faqs and has_final_thoughts and has_related_articles) or is_cut_off:
        logger.info("Detecting incomplete or truncated sections in long-form blog. Running intelligent completion pass...")
        
        # If cut off inside an incomplete section, trim back to the last complete H2 header
        last_h2_idx = full_content.rfind("\n## ")
        if is_cut_off and last_h2_idx != -1:
            last_sec_text = full_content[last_h2_idx:]
            if not has_faqs and ("## The Real Logistics" in last_sec_text or "## 3 Actionable Tips" in last_sec_text or "## 4 Ways Yatradham" in last_sec_text or "## 3 Key Takeaways" in last_sec_text):
                full_content = full_content[:last_h2_idx].strip()

        missing_requirements = []
        if "## 3 Key Takeaways" not in full_content and "## Key Takeaways" not in full_content:
            missing_requirements.append("## 3 Key Takeaways From This 7-Day Journey\n(Write 3 detailed takeaway subsections: 1. Pacing Drives True Rejuvenation, 2. High-Value Experiences Win Over Crowded Sightseeing, 3. Local Etiquette & Trust Build the Connection)")
        if "## 4 Ways Yatradham" not in full_content and "## Ways Yatradham" not in full_content:
            missing_requirements.append("## 4 Ways Yatradham.Org Makes Your Journey Seamless & Safe\n(Write 4 subsections with bullet points: 1. Verified Accommodations & Transparent Pricing, 2. Dedicated Yatra & Transport Coordination, 3. Tailored Spiritual & Wellness Itineraries, 4. 24/7 Pilgrim Support & Flexible Booking)")
        if "## 3 Actionable Tips" not in full_content and "## Actionable Tips" not in full_content:
            missing_requirements.append("## 3 Actionable Tips to Plan Your Journey Today\n(Write 3 subsections: 1. Plan Around Search & Seasonal Intent, 2. Book Your Verified Stay in Advance, 3. Maintain Consistency With Daily Routines)")
        if "## The Real Logistics" not in full_content and "## Real Logistics" not in full_content:
            missing_requirements.append("## The Real Logistics: Costs, Stays & Commutes\n(Write ~400 words detailing flight/train connections with exact fares in INR, realistic daily budget breakdowns from budget to luxury, local commute rates, and Yatradham stay benefits)")
        if not has_faqs:
            missing_requirements.append("## Frequently Asked Questions\n(Provide exactly 6 distinct, search-focused FAQs with thorough, direct answers covering budget, beginner friendliness, solo female safety, packing, meals, and best booking seasons)")
        if not has_final_thoughts:
            missing_requirements.append("## Final Thoughts & Planning Your Trip\n(Write ~200 words. An inspiring conclusion encouraging the reader to take the first step, with a natural call-to-action to explore verified accommodations and packages on Yatradham.Org)")
        if not has_related_articles:
            missing_requirements.append("## Related Articles & Recommended Reading\n(Provide 3 formatted internal article suggestions with Title, Author, Date, and 1-line topic summary)")

        if missing_requirements:
            reqs_str = "\n\n".join(missing_requirements)
            finale_prompt = f"""You have written the preceding part of the guide for: "{topic}".

Now generate ONLY the remaining missing closing sections below to complete the full 3,000-word authoritative blog post:

{reqs_str}

CRITICAL: Output ONLY markdown text starting with the first missing section heading. Follow all editorial standards and do not repeat anything already written above."""

            finale_raw = client.chat_completion(
                messages=[
                    {"role": "system", "content": brand_context},
                    {"role": "user", "content": master_prompt},
                    {"role": "assistant", "content": full_content},
                    {"role": "user", "content": finale_prompt}
                ],
                max_tokens=3000,
                temperature=0.6,
            )
            cleaned_finale = _clean_markdown(finale_raw)
            if cleaned_finale:
                full_content = f"{full_content}\n\n{_sanitize_repetition(cleaned_finale)}"

    # Apply automatic Google Helpful Content & Copyleaks de-slopping to ensure 95%+ Human score
    clean_human_content = de_slop_and_humanize(full_content)

    return {
        "title": title,
        "meta_description": meta_desc,
        "suggested_tags": tags,
        "content": clean_human_content,
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

    # Automatically de-slop and humanize before returning
    if "content" in result and isinstance(result["content"], str):
        result["content"] = de_slop_and_humanize(result["content"])

    # Always ensure content_type and topic are set
    result["content_type"] = content_type
    result["topic"] = topic
    result["target_keyword"] = target_keyword or ""
    
    return result
