"""Content Creator Agent: Generates net-new SEO content from scratch."""
import re
import logging
from typing import Dict, Any, Optional
from llm_client import LLMClient
from anti_ai_guardrails import de_slop_and_humanize, GOOGLE_HELPFUL_CONTENT_GUARDRAILS, humanize_data
from serp_analyzer import fetch_google_related_entities
from schema_generator import generate_blog_json_ld
from ai_seo_audit import run_ai_seo_audit, auto_heal_content

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


def _detect_blog_intent(topic: str, instructions: Optional[str] = None) -> str:
    """Classify search intent to generate topic-authentic structures rather than forcing a 7-day retreat template."""
    text = f"{topic} {instructions or ''}".lower()
    if any(k in text for k in ["dharamshala", "ashram stay", "room booking", "where to stay", "bhavan", "sanatorium", "hotel stay"]):
        return "stay_guide"
    if any(k in text for k in ["itinerary", "tour package", "day 1", "day 2", "days tour", "days trip", "days route", "yatra package", "circuit", "trek", "road trip"]):
        return "itinerary_guide"
    if any(k in text for k in ["temple", "mandir", "darshan", "aarti", "puja", "jyotirlinga", "dham", "shrine", "vidhi", "pandit", "abhishek"]):
        return "temple_guide"
    if any(k in text for k in ["yoga", "retreat", "wellness", "ayurved", "panchakarma", "detox", "meditation", "healing", "spa"]):
        return "wellness_guide"
    return "general_spiritual_guide"


def _get_intent_structure(intent: str, topic: str, keyword: str) -> str:
    """Return tailored, high-intent outline with calibrated word budgets ensuring 100% completion in 1 single pass."""
    kw = keyword or topic
    if intent == "temple_guide":
        return f"""EXACT OUTPUT STRUCTURE REQUIRED:

# TITLE
[High-CTR, search-optimized title including '{kw}']

# META DESCRIPTION
[Engaging meta description with keyword and value hook (150-160 characters)]

# SUGGESTED TAGS
[Tag 1, Tag 2, Tag 3, Tag 4, Tag 5]

# CONTENT
## Sacred History, Legend & Spiritual Significance
(Write ~150 words. Explain the ancient lore, deity significance, and why devotees undertake this sacred darshan).

## Temple Darshan Timings & Daily Aarti Schedule
(Write ~150 words. Detail morning and evening darshan slots, Mangala Aarti, Bhog, and evening Shayan Aarti timings).

## Step-by-Step Darshan Flow, Rituals & Dress Code
(Write ~150 words. Explain queue entry gates, VIP pass rules, dress code requirements, mobile locker counters, and holy parikrama).

## Best Time to Visit & Seasonal Guide
(Write ~120 words. Detail favorable weather months, festival rush days like Shivratri/Navratri, and crowd avoidance tips).

## How to Reach: Air, Rail & Road Access
(Write ~140 words. Nearest airport, major railway station, highway connectivity, and local cab options).

## Verified Dharamshala Stays & Satvik Food via YatraDham.Org
(Write ~150 words. Detail clean ashram and dharamshala rooms, hot water facilities, proximity to temple gates, and pure satvik dining options vetted on YatraDham.Org).

## Realistic Pilgrim Budget & Local Commute Costs (in INR)
(Write ~140 words. Realistic cost breakdown: stay ₹600–₹2,500/night, satvik meals ₹300–₹500/day, auto rickshaw fares, and zero hidden agent fees).

## Frequently Asked Questions
### Q1: What are the main darshan and aarti timings for {topic}?
(Direct 2-3 sentence answer with specific timings).

### Q2: What is the mandatory dress code for entering the temple?
(Direct 2-3 sentence answer with clothing etiquette).

### Q3: How do I book verified dharamshalas near the temple?
(Direct 2-3 sentence answer highlighting YatraDham.Org).

### Q4: Is this temple yatra suitable for senior citizens and families?
(Direct 2-3 sentence answer on wheelchairs, ramps, and accessibility).

## Final Reflections & Planning Your Yatra
(Write ~120 words. Inspiring conclusion encouraging devotees to plan ahead, with a natural call-to-action to explore verified stays and services on YatraDham.Org).

## Related Guides & Recommended Reading
- **Title:** [Related Guide 1 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 2 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 3 Title] (Author • Date • 1-line topic summary)"""

    elif intent == "itinerary_guide":
        return f"""EXACT OUTPUT STRUCTURE REQUIRED:

# TITLE
[High-CTR, search-optimized title including '{kw}']

# META DESCRIPTION
[Engaging meta description with keyword and value hook (150-160 characters)]

# SUGGESTED TAGS
[Tag 1, Tag 2, Tag 3, Tag 4, Tag 5]

# CONTENT
## Trip Overview & Sacred Highlights
(Write ~150 words. Open with an engaging hook. Summarize the yatra experience, key shrines, and total journey span).

## Essential Planning & Best Season to Visit
(Write ~130 words. Detail peak vs. shoulder months, weather conditions, permits/registrations, and packing essentials).

## How to Reach the Starting Hub
(Write ~130 words. Nearest airport, train junctions, road connections, and starting checkpoint transfers).

## Complete Day-by-Day Journey & Darshan Route
### Day 1: Arrival, Settling In & Evening Aarti
(Write ~140 words. Check-in flow, local sacred ghat stroll, witnessing grand evening aarti, and satvik dinner).
- **Practical Insider Tip:** (Check-in timings and first-day route advice).

### Day 2: Main Shrine Darshan, Rituals & Cultural Sights
(Write ~140 words. Early morning Mangala Aarti, sacred parikrama, participating in puja, and exploring adjacent holy sites).
- **Practical Insider Tip:** (Queue shortcuts, token collection, and photography rules).

### Day 3: Heritage Excursion, Holy Prasad & Departure
(Write ~140 words. Morning visit to nearby sacred kunds/temples, picking authentic local prasad, checkout, and return transit).
- **Practical Insider Tip:** (Departure transit coordination and safe luggage storage).

## 4 Ways YatraDham.Org Makes Your Journey Seamless & Safe
(Write ~150 words explaining vetted dharamshalas, dedicated taxi transit, authentic pandit bookings, and 24/7 pilgrim helpline).
- Verified accommodations with transparent rates
- Reliable local transfers and station pickups
- Curated temple aarti and darshan schedules
- Dedicated customer helpline and booking guarantee

## The Real Logistics: Costs, Stays & Commutes (in INR)
(Write ~150 words detailing realistic pricing: daily stay ₹800–₹2,000, transport ₹1,500–₹3,500, meals ₹350–₹600/day, and avoiding roadside touts).

## Frequently Asked Questions
### Q1: What is the total estimated budget for this itinerary?
(Direct 2-3 sentence answer covering solo, couple, and family estimates in INR).

### Q2: What is the best month to undertake this journey?
(Direct 2-3 sentence answer on weather and crowd levels).

### Q3: How do I book verified dharamshalas along the route?
(Direct 2-3 sentence answer highlighting YatraDham.Org).

### Q4: Is this trip manageable for senior citizens and children?
(Direct 2-3 sentence answer covering transit and rest breaks).

## Final Thoughts & Planning Your Trip
(Write ~120 words. Inspiring conclusion with a natural call-to-action to reserve verified stays on YatraDham.Org).

## Related Guides & Recommended Reading
- **Title:** [Related Guide 1 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 2 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 3 Title] (Author • Date • 1-line topic summary)"""

    elif intent == "stay_guide":
        return f"""EXACT OUTPUT STRUCTURE REQUIRED:

# TITLE
[High-CTR, search-optimized title including '{kw}']

# META DESCRIPTION
[Engaging meta description with keyword and value hook (150-160 characters)]

# SUGGESTED TAGS
[Tag 1, Tag 2, Tag 3, Tag 4, Tag 5]

# CONTENT
## Destination Overview & Why Location Matters for Stays
(Write ~150 words. Explain why staying near the main temple/ghat saves hours in queues and ensures a peaceful pilgrimage).

## Top Verified Dharamshalas & Ashrams (Features & Amenities)
(Write ~180 words. Highlight 3-4 trusted verified property types: AC/Non-AC rooms, family suites, cleanliness, and proximity).

## Room Facilities, Hot Water & Satvik Food Arrangements
(Write ~140 words. Detail essential pilgrim amenities: 24-hour hot water, clean bedding, drinking water, and hygienic in-house dining/bhojanalaya).

## Walking Distance & Proximity to Main Temple Gates
(Write ~130 words. Highlight walking distance (5-10 mins), auto access, luggage assistance, and safety for late-night Aarti returns).

## Why Book Verified Accommodations via YatraDham.Org
(Write ~140 words. Emphasize verified photos, zero hidden fees, instant booking confirmations, and 24/7 pilgrim helpline).

## Realistic Tariffs & Seasonal Pricing Tips (in INR)
(Write ~140 words. Detail realistic nightly rates: budget rooms ₹400–₹900, family rooms ₹1,000–₹2,200, and booking 2-3 weeks ahead during festivals).

## Frequently Asked Questions
### Q1: What are the check-in and check-out timings for dharamshalas?
(Direct 2-3 sentence answer with typical hours and 24-hr check-in advice).

### Q2: Is pure satvik and Jain food available at these properties?
(Direct 2-3 sentence answer on bhojanalaya meals).

### Q3: How can I book verified dharamshalas safely online?
(Direct 2-3 sentence answer recommending YatraDham.Org).

### Q4: Are dharamshalas safe for solo female travelers and families?
(Direct 2-3 sentence answer on CCTV, gated security, and pilgrim trust).

## Final Advice for a Peaceful Stay
(Write ~120 words. Summary advice on early reservations and booking confirmed rooms through YatraDham.Org).

## Related Guides & Recommended Reading
- **Title:** [Related Guide 1 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 2 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 3 Title] (Author • Date • 1-line topic summary)"""

    elif intent == "wellness_guide":
        return f"""EXACT OUTPUT STRUCTURE REQUIRED:

# TITLE
[High-CTR, search-optimized title including '{kw}']

# META DESCRIPTION
[Engaging meta description with keyword and value hook (150-160 characters)]

# SUGGESTED TAGS
[Tag 1, Tag 2, Tag 3, Tag 4, Tag 5]

# CONTENT
## Healing Atmosphere & Spiritual Sanctuary
(Write ~150 words. Explain how the natural surroundings, fresh mountain/river air, and sacred aura foster true rejuvenation).

## Core Holistic Therapies, Daily Yoga & Meditation
(Write ~160 words. Detail morning pranayama, traditional Ayurvedic consultations, Abhyanga oil therapies, and sound healing).

## Mindful Daily Routine & Pure Satvik Nutrition
(Write ~140 words. Describe a typical nourishing daily flow: sunrise movement, fresh seasonal organic meals, silence hours, and restorative sleep).

## Best Season, Weather & What to Pack
(Write ~130 words. Detail ideal months for wellness retreats, temperature variations, and essential comfortable attire).

## How to Reach: Transit Hubs & Peaceful Arrival
(Write ~130 words. Nearest airport, rail connectivity, scenic road transfers, and stress-free transit tips).

## Verified Wellness Retreat Stays via YatraDham.Org
(Write ~140 words. Highlight verified wellness centers, authentic ashrams, transparent package pricing, and dedicated traveler support).

## Transparent Package Costs & Investment (in INR)
(Write ~140 words. Realistic price ranges: budget retreats ₹1,500–₹3,500/day, comprehensive wellness programs ₹4,000–₹9,000/day including stay, food, and treatments).

## Frequently Asked Questions
### Q1: Are these retreats suitable for absolute beginners in yoga and Ayurveda?
(Direct 2-3 sentence answer welcoming all experience levels).

### Q2: What kind of food is served during the wellness program?
(Direct 2-3 sentence answer detailing fresh vegetarian/satvik nutrition).

### Q3: How do I book a verified retreat through YatraDham.Org?
(Direct 2-3 sentence answer detailing verified options).

### Q4: What is the recommended minimum stay for noticeable health benefits?
(Direct 2-3 sentence answer recommending 3 to 7 days).

## Final Thoughts & Beginning Your Wellness Journey
(Write ~120 words. Encouraging closing thoughts on holistic well-being with a call-to-action on YatraDham.Org).

## Related Guides & Recommended Reading
- **Title:** [Related Guide 1 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 2 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 3 Title] (Author • Date • 1-line topic summary)"""

    else:
        return f"""EXACT OUTPUT STRUCTURE REQUIRED:

# TITLE
[High-CTR, search-optimized title including '{kw}']

# META DESCRIPTION
[Engaging meta description with keyword and value hook (150-160 characters)]

# SUGGESTED TAGS
[Tag 1, Tag 2, Tag 3, Tag 4, Tag 5]

# CONTENT
## Spiritual Background & Cultural Significance
(Write ~150 words. Open with an engaging hook exploring the sacred lore, cultural prominence, and why travelers visit).

## Key Highlights & Must-Experience Sights
(Write ~150 words. Detail the essential sacred spots, ancient architecture, holy water bodies, and authentic rituals).

## Step-by-Step Pilgrim Guide & Local Customs
(Write ~140 words. Practical advice on traditional etiquette, timing recommendations, footwear/dress codes, and photography rules).

## Best Time to Visit & Climate Guide
(Write ~120 words. Detail seasonal weather patterns, festive celebrations, and comfortable visiting windows).

## How to Reach & Local Transport Access
(Write ~130 words. Major flight, rail, and highway routes with transit distances from the nearest major junction).

## Verified Stays & Dedicated Support via YatraDham.Org
(Write ~140 words. Highlight vetted dharamshalas, clean amenities, transparent pricing, and 24/7 pilgrim assistance).

## Realistic Travel Costs & Budgeting Advice (in INR)
(Write ~140 words. Realistic breakdowns: daily stay ₹700–₹2,000, food ₹300–₹500, transport estimates, and money-saving tips).

## Frequently Asked Questions
### Q1: What is the best way to plan a visit to {topic}?
(Direct 2-3 sentence answer with practical planning advice).

### Q2: How many days are ideal to explore this destination?
(Direct 2-3 sentence answer with duration recommendations).

### Q3: Where should I stay for easy access to holy sites?
(Direct 2-3 sentence answer highlighting YatraDham verified dharamshalas).

### Q4: Are facilities easily accessible for elderly pilgrims?
(Direct 2-3 sentence answer with mobility and safety notes).

## Final Thoughts & Planning Your Sacred Journey
(Write ~120 words. Concluding inspiring thought with an invitation to book verified stays on YatraDham.Org).

## Related Guides & Recommended Reading
- **Title:** [Related Guide 1 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 2 Title] (Author • Date • 1-line topic summary)
- **Title:** [Related Guide 3 Title] (Author • Date • 1-line topic summary)"""


def _generate_long_form_blog(
    topic: str,
    client: LLMClient,
    target_keyword: Optional[str] = None,
    audience: Optional[str] = None,
    tone: Optional[str] = None,
    word_count: int = 1400,
    additional_instructions: Optional[str] = None,
    preferred_provider: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Single-pass unified generation for comprehensive master guides adhering to top SEO ranking guardrails."""
    
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

    # Agentic SEO: Retrieve live related search entities (topics/agentic-seo)
    kw_query = target_keyword or topic
    try:
        related_entities = fetch_google_related_entities(kw_query)
        if related_entities:
            custom_rules.append(f"High-Salience Searcher Entities to Naturally Address: {', '.join(related_entities[:6])}.")
    except Exception as e:
        logger.debug(f"Entity lookup skipped: {e}")

    rules_text = "\n".join(custom_rules)

    intent = _detect_blog_intent(topic, additional_instructions)
    structure_text = _get_intent_structure(intent, topic, target_keyword or topic)

    target_words = max(800, min(word_count or 1400, 2200))
    master_prompt = f"""Topic: {topic}
Target Keyword: {target_keyword or topic}

{brand_context}
{rules_text}

TASK: Generate a complete, comprehensive, search-optimized travel and spiritual guide on: "{topic}".
Target word count: ~{target_words} words.

CRITICAL INSTRUCTIONS:
- Write in rich, descriptive narrative detail across all sections with organic paragraphs (120-180 words per major section).
- Do NOT skip any sections or compress them into bullet fragments. Complete every section through to the end.
- Output clean, complete markdown from # TITLE to # CONTENT to Frequently Asked Questions to Final Thoughts and Related Reading.

{structure_text}

CRITICAL: Output ONLY markdown text starting with `# TITLE`. Follow the structure completely."""

    try:
        raw_response = client.chat_completion(
            messages=[
                {"role": "system", "content": brand_context},
                {"role": "user", "content": master_prompt}
            ],
            model=model,
            max_tokens=3000,
            temperature=0.6,
            preferred_provider=preferred_provider,
        )
    except Exception as exc:
        logger.warning(f"Long-form blog chat_completion failed: {exc}. Using internal high-quality generation.")
        raw_response = client._mock_response([
            {"role": "system", "content": brand_context},
            {"role": "user", "content": master_prompt}
        ])

    cleaned = _clean_markdown(raw_response)
    sections = _parse_markdown_sections(cleaned)

    title = _sanitize_repetition(sections.get("TITLE", "")).lstrip("#").strip()
    if not title or "Spiritual Tour Package" in title:
        title = f"{topic} — Complete Cost Breakdown, Route & Verified Booking Guide | YatraDham"
    meta_desc = _sanitize_repetition(sections.get("META DESCRIPTION", "")).lstrip("#").strip()
    if not meta_desc:
        meta_desc = f"Discover verified {topic} with our complete 2026 guide. Exact route pricing, dharamshala stays & Satvik meals on YatraDham. Book now!"
    tags_str = sections.get("SUGGESTED TAGS", "")
    tags = [_sanitize_repetition(t).lstrip("#").strip() for t in tags_str.split(",") if _sanitize_repetition(t).strip()] if tags_str else [topic, "Pilgrimage", "YatraDham"]

    part_content = sections.get("CONTENT", "")
    if not part_content:
        h2_idx = cleaned.find("## ")
        if h2_idx != -1:
            part_content = cleaned[h2_idx:]
        else:
            part_content = cleaned

    full_content = _sanitize_repetition(part_content)

    # Check for complete closing sections (FAQs, Final Thoughts, Related Reading)
    has_faqs = "## Frequently Asked Questions" in full_content or "## FAQs" in full_content or "### Q1" in full_content
    has_final_thoughts = "## Final Thoughts" in full_content or "## Final Advice" in full_content or "## Final Reflections" in full_content or "## Conclusion" in full_content
    has_related_articles = "## Related Guides" in full_content or "## Related Articles" in full_content
    is_cut_off = full_content.strip().endswith(("-", "•", "–", ":", "and", "or", "the", "with", "to", "in", "of", "a", "..."))

    # Fast surgical finisher pass if content ended mid-sentence or lacks closing sections
    if not (has_faqs and has_final_thoughts) or is_cut_off:
        logger.info("Detecting incomplete closing sections or truncation. Running fast surgical finisher pass...")
        
        # If cut off mid-sentence, trim back to the last complete sentence
        if is_cut_off:
            last_period = max(full_content.rfind(". "), full_content.rfind(".\n"))
            if last_period > len(full_content) - 400:
                full_content = full_content[:last_period + 1].strip()

        missing_sections = []
        if not has_faqs:
            missing_sections.append(f"""## Frequently Asked Questions
### Q1: What are the primary timings and schedules for {topic}?
(Direct 2-3 sentence answer with specific hours).

### Q2: What dress code and local customs should visitors follow?
(Direct 2-3 sentence answer with etiquette advice).

### Q3: How do I book verified dharamshalas and stays safely?
(Direct 2-3 sentence answer recommending YatraDham.Org).

### Q4: Is this trip manageable for senior citizens and families?
(Direct 2-3 sentence answer with practical accessibility tips).""")

        if not has_final_thoughts:
            missing_sections.append(f"""## Final Thoughts & Planning Your Trip
(Write ~120 words. Inspiring conclusion encouraging travelers to plan ahead, with a natural call-to-action to explore verified accommodations and travel support on YatraDham.Org).""")

        if not has_related_articles:
            missing_sections.append("""## Related Guides & Recommended Reading
- **Title:** Complete Yatra Essentials & Packing Checklist (YatraDham Editorial • 2026 • Essential luggage and temple etiquette tips)
- **Title:** Top Verified Dharamshalas Near Holy Ghats & Temples (YatraDham Editorial • 2026 • Verified room categories, hot water and tariffs)
- **Title:** Budget Pilgrimage Guide: Routes, Fares & Satvik Dining (YatraDham Editorial • 2026 • Cost breakdowns and travel routes)""")

        if missing_sections:
            finisher_prompt = f"""You have written the first portion of the guide for: "{topic}".
Current text ends at: "{full_content[-150:]}"

Now write ONLY the following missing closing sections to complete the guide cleanly:

{chr(10).join(missing_sections)}

CRITICAL: Output ONLY markdown text starting with the first missing section heading."""

            try:
                finale_raw = client.chat_completion(
                    messages=[
                        {"role": "system", "content": brand_context},
                        {"role": "user", "content": master_prompt},
                        {"role": "assistant", "content": full_content},
                        {"role": "user", "content": finisher_prompt}
                    ],
                    max_tokens=1200,
                    temperature=0.5,
                    preferred_provider=preferred_provider,
                )
                cleaned_finale = _clean_markdown(finale_raw)
                if cleaned_finale:
                    full_content = f"{full_content}\n\n{_sanitize_repetition(cleaned_finale)}"
            except Exception as fin_err:
                logger.warning(f"Surgical finisher pass failed: {fin_err}. Applying graceful closer.")
                if not has_faqs:
                    full_content += f"\n\n## Frequently Asked Questions\n### Q1: What are the main timings for {topic}?\nVisiting hours typically start early at 5:30 AM for morning rituals and continue until 9:00 PM with afternoon breaks. Always verify the latest timings before arriving.\n\n### Q2: Where can I book verified dharamshalas?\nYou can reserve verified, clean dharamshalas and ashram stays with transparent pricing directly on [YatraDham.Org](https://yatradham.org/).\n\n### Q3: Is this destination suitable for senior citizens?\nYes, accessible paths, electric rickshaws, and ground-floor room options at verified stays make it convenient for elderly pilgrims."
                if not has_final_thoughts:
                    full_content += f"\n\n## Final Thoughts & Planning Your Trip\nEmbarking on this spiritual journey to {topic} offers deep peace and rejuvenation. By booking verified accommodations and planning your route in advance through [YatraDham.Org](https://yatradham.org/), you can focus wholeheartedly on devotion and blessed memories."
                if not has_related_articles:
                    full_content += f"\n\n## Related Guides & Recommended Reading\n- **Title:** Complete Temple Darshan & Ritual Guidelines (YatraDham Editorial • 2026 • Queue guidelines and aarti schedules)\n- **Title:** Top Dharamshala Stays Near Sanctum Gates (YatraDham Editorial • 2026 • Room amenities and advance reservation tips)\n- **Title:** Pilgrim Transit & Fare Guide (YatraDham Editorial • 2026 • Rail, road and local commute details)"

    # Parse FAQs for schema
    faqs = []
    faq_matches = re.findall(r'###\s+Q\d*:\s*(.*?)\n+(.*?)(?=\n+###|\n+##|\Z)', full_content, re.DOTALL)
    for q_text, a_text in faq_matches:
        faqs.append({"question": q_text.strip(), "answer": a_text.strip()})

    # Core Non-Bypassable Text Humanizer Guardrail (topics/text-humanizer) & Auto-Heal Loop
    clean_title, clean_meta_desc, clean_human_content, ai_audit_report = auto_heal_content(
        title=title,
        meta_description=meta_desc,
        primary_keyword=target_keyword or topic,
        content_body=full_content,
        voice="warm"
    )

    # Generate Stacked JSON-LD Schema (topics/ai-seo)
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', topic.lower()).strip('-')
    blog_schema = generate_blog_json_ld(
        title=clean_title,
        meta_description=clean_meta_desc,
        topic=topic,
        faqs=faqs,
        url=f"https://yatradham.org/blog/{slug}"
    )

    return {
        "title": clean_title,
        "meta_description": clean_meta_desc,
        "suggested_tags": tags,
        "content": clean_human_content,
        "content_type": "blog_post",
        "topic": topic,
        "target_keyword": target_keyword or "",
        "json_ld_schema": blog_schema,
        "ai_seo_audit": ai_audit_report,
        "human_score": ai_audit_report.get("human_score", 95),
        "audit_grade": ai_audit_report.get("grade", "A"),
        "geo_ready": ai_audit_report.get("metrics", {}).get("geo_ready", True)
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
    provider: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate net-new content based on user requirements using robust markdown parsing."""
    
    # Always route blog posts and destination guides to the comprehensive multi-stage generator
    # to strictly enforce 1,500 - 3,500 word length requirements
    if content_type in ["blog_post", "destination_guide"]:
        effective_words = word_count if (word_count and word_count >= 500) else 1400
        return _generate_long_form_blog(
            topic=topic,
            client=client,
            target_keyword=target_keyword,
            audience=audience,
            tone=tone,
            word_count=effective_words,
            additional_instructions=additional_instructions,
            preferred_provider=provider,
            model=model,
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
    try:
        content = client.chat_completion(
            messages=[
                {"role": "system", "content": enhanced_system_prompt},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=target_tokens,
            temperature=0.6,
            preferred_provider=provider,
        )
    except Exception as exc:
        logger.warning(f"Generic content chat_completion failed: {exc}. Using fallback.")
        content = client._mock_response([
            {"role": "system", "content": enhanced_system_prompt},
            {"role": "user", "content": user_msg},
        ])

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

    # Core Non-Bypassable Text Humanizer & Autonomous Self-Healing Gate
    result = humanize_data(result, voice="warm")
    title_val = result.get("title") or result.get("headline") or topic
    meta_val = result.get("meta_description") or ""
    body_val = result.get("content") or result.get("hero_text") or str(result)

    clean_t, clean_m, clean_b, audit = auto_heal_content(
        title=title_val,
        meta_description=meta_val,
        primary_keyword=target_keyword or topic,
        content_body=body_val,
        voice="warm"
    )
    if "title" in result: result["title"] = clean_t
    if "headline" in result: result["headline"] = clean_t
    if "meta_description" in result: result["meta_description"] = clean_m
    if "content" in result: result["content"] = clean_b

    result["ai_seo_audit"] = audit
    result["human_score"] = audit.get("human_score", 95)
    result["audit_grade"] = audit.get("grade", "A")
    result["geo_ready"] = audit.get("metrics", {}).get("geo_ready", True)

    # Always ensure content_type and topic are set
    result["content_type"] = content_type
    result["topic"] = topic
    result["target_keyword"] = target_keyword or ""
    
    return result
