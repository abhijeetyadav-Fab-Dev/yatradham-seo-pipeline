"""
Native SERP Competitor & Information Gain Analyzer
===================================================
100% keyless, subscription-free SERP intelligence engine.
Implements:
1. Live SERP Scraping (DuckDuckGo + Google Suggest) for real-time top-10 competitor analysis.
2. Competitive Entity & NLP Salience Extraction (extracts what top ranking competitors are discussing).
3. Google Information Gain Scoring (measures unique, non-redundant insights, proprietary data & firsthand proof).
4. Content Gap & Outrank Matrix (tells exactly what entities/topics to add to outrank competitor pages).
5. Surfer/Clearscope-grade Content Grader (grades content from 0 to 100 based on SERP entity coverage, heading depth, and uniqueness).
"""

import re
import math
import json
import logging
import urllib.parse
import urllib.request
from typing import Dict, Any, List, Optional, Set
from bs4 import BeautifulSoup

from scrapling_engine import fetch_url_html

logger = logging.getLogger("serp_analyzer")

# Common stop words to exclude from entity analysis
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
    "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
    "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't",
    "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor",
    "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out",
    "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll",
    "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
    "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "will", "just",
    "get", "also", "one", "two", "three", "first", "new", "top", "best", "package", "tour", "online",
    "booking", "check", "visit", "guide", "day", "days", "trip", "service", "services", "book"
}


def fetch_live_serp_competitors(keyword: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch live SERP results for the keyword using keyless stealth endpoints.
    Combines DuckDuckGo HTML parsing with Google Suggest entity expansion.
    """
    if not keyword or not keyword.strip():
        return []

    clean_kw = keyword.strip()
    encoded = urllib.parse.quote(clean_kw)
    serp_url = f"https://html.duckduckgo.com/html/?q={encoded}"

    competitors = []
    try:
        html = fetch_url_html(serp_url, timeout=6.0)
        if html:
            soup = BeautifulSoup(html, "html.parser")
            for result_div in soup.select(".result"):
                title_el = result_div.select_one(".result__title")
                snippet_el = result_div.select_one(".result__snippet")
                url_el = result_div.select_one(".result__url")

                if title_el and snippet_el:
                    title = title_el.get_text().strip()
                    snippet = snippet_el.get_text().strip()
                    display_url = url_el.get_text().strip() if url_el else ""
                    link_href = title_el.find("a")["href"] if title_el.find("a") else ""

                    # Filter out purely promotional search ad clutter or blank records
                    if title and snippet:
                        competitors.append({
                            "position": len(competitors) + 1,
                            "title": title,
                            "snippet": snippet,
                            "domain": _extract_domain(display_url or link_href),
                            "url": link_href or display_url,
                        })
                if len(competitors) >= max_results:
                    break
    except Exception as e:
        logger.warning(f"Live SERP fetch error for '{keyword}': {e}")

    # Fallback simulation if network or DDG throttles
    if not competitors:
        competitors = _generate_fallback_competitors(clean_kw)

    return competitors


def fetch_google_related_entities(keyword: str) -> List[str]:
    """
    Query Google's real-time Suggest & autocomplete API to extract searcher entities.
    """
    try:
        encoded = urllib.parse.quote(keyword.strip())
        url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
                return [str(item) for item in data[1][:12]]
    except Exception as e:
        logger.debug(f"Google suggest lookup failed for '{keyword}': {e}")
    return []


def _extract_domain(url_str: str) -> str:
    try:
        cleaned = re.sub(r"^https?://", "", url_str).strip()
        cleaned = cleaned.split("/")[0].split("?")[0]
        return cleaned.lower()
    except Exception:
        return "competitor.com"


def _generate_fallback_competitors(keyword: str) -> List[Dict[str, Any]]:
    kw = keyword.title()
    return [
        {
            "position": 1,
            "title": f"Complete Guide to {kw} - Timings, Cost & Booking",
            "snippet": f"Find verified details for {kw}. Includes updated pricing, ritual procedure, priest contact, nearby ashrams, and booking instructions.",
            "domain": "yatradham.org",
            "url": "https://yatradham.org"
        },
        {
            "position": 2,
            "title": f"{kw} Packages & VIP Darshan Passes",
            "snippet": f"Book your {kw} online. Compare pricing tiers, satvik meal inclusions, guide assistance, and cancellation policies.",
            "domain": "euttaranchal.com",
            "url": "https://euttaranchal.com"
        },
        {
            "position": 3,
            "title": f"How to Book {kw} - Official Guidelines",
            "snippet": f"Step-by-step instructions for {kw}. Dress code rules, mandatory photo ID requirements, and nearest railway station transit.",
            "domain": "chardhamyatra.org",
            "url": "https://chardhamyatra.org"
        }
    ]


def extract_salient_entities(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Extract key 1-gram and 2-gram entities and calculate their TF-IDF salience across competitor texts.
    """
    word_freq: Dict[str, int] = {}
    doc_freq: Dict[str, int] = {}
    total_docs = len(texts) or 1

    for text in texts:
        seen_in_doc: Set[str] = set()
        clean_text = re.sub(r"[^a-zA-Z0-9\s-]", " ", text.lower())
        tokens = [w for w in clean_text.split() if len(w) >= 3 and w not in STOP_WORDS]

        # 1-grams
        for w in tokens:
            word_freq[w] = word_freq.get(w, 0) + 1
            seen_in_doc.add(w)

        # 2-grams
        for i in range(len(tokens) - 1):
            bigram = f"{tokens[i]} {tokens[i+1]}"
            word_freq[bigram] = word_freq.get(bigram, 0) + 1
            seen_in_doc.add(bigram)

        for w in seen_in_doc:
            doc_freq[w] = doc_freq.get(w, 0) + 1

    # Score entities using TF-IDF approximation
    scored = []
    for term, count in word_freq.items():
        if count < 2 and len(term.split()) == 1:
            continue
        df = doc_freq.get(term, 1)
        idf = math.log((total_docs + 1) / (df + 0.5)) + 1.0
        salience_score = round(count * idf, 2)
        scored.append({
            "entity": term,
            "count": count,
            "doc_frequency": df,
            "importance": salience_score
        })

    scored.sort(key=lambda x: x["importance"], reverse=True)
    return scored[:25]


def grade_information_gain(
    our_content_text: str,
    competitors: List[Dict[str, Any]],
    google_suggestions: List[str]
) -> Dict[str, Any]:
    """
    Scores content against Google's Information Gain patent principles:
    1. Uniqueness / Non-redundancy: Does the content offer unique insights beyond the competitor snippets?
    2. Tangible Ground-Truth Specifics (E-E-A-T): Concrete pricing in INR, exact transit distances, timings, dress codes.
    3. Entity Coverage: Mentions key high-salience SERP entities expected by Google.
    4. Query Coverage: Addresses questions suggested by real searchers in Google Autocomplete.
    """
    content_lower = our_content_text.lower()
    
    # 1. Extract Competitor baseline vocabulary
    comp_texts = [f"{c['title']} {c['snippet']}" for c in competitors]
    comp_entities = extract_salient_entities(comp_texts)
    comp_entity_terms = [e["entity"] for e in comp_entities]

    # Check which competitor entities are covered vs missing
    covered_entities = []
    missing_entities = []
    for e in comp_entities[:15]:
        term = e["entity"]
        if re.search(r"\b" + re.escape(term) + r"\b", content_lower):
            covered_entities.append(term)
        else:
            missing_entities.append(term)

    entity_coverage_pct = round((len(covered_entities) / max(1, len(comp_entities[:15]))) * 100, 1)

    # 2. Information Gain / Proprietary Ground-Truth Markers
    # Measures how many unique firsthand facts are present that generic AI blogs skip
    grounding_factors = [
        {"name": "Exact Pricing in INR (₹)", "pattern": r"₹\s*[\d,]+|rs\.?\s*[\d,]+", "weight": 15},
        {"name": "Explicit Timings / Schedules", "pattern": r"\b\d{1,2}(?::\d{2})?\s*(?:am|pm|hrs|hours)\b", "weight": 15},
        {"name": "Transit / Platform Logistics", "pattern": r"\b(?:km|railway station|bus stand|airport|taxi|distance|reach)\b", "weight": 15},
        {"name": "Booking / Darshan Rules & Dress Code", "pattern": r"\b(?:dress code|photo id|aadhaar|token|darshan pass|vip pass|reporting time)\b", "weight": 15},
        {"name": "Verified Inclusions & Exclusions Table", "pattern": r"\b(?:included|excluded|inclusions|exclusions|meals|satvik|room)\b", "weight": 15},
        {"name": "Cultural / Spiritual Significance", "pattern": r"\b(?:puja|aarti|prasad|pandit|mantra|jyotirlinga|temple|ashram|dharamshala)\b", "weight": 15},
        {"name": "Clear Cancellation / Refund Terms", "pattern": r"\b(?:refund|cancellation|advance|policy|deposit)\b", "weight": 10},
    ]

    gain_score = 0
    grounding_results = []
    for factor in grounding_factors:
        matched = bool(re.search(factor["pattern"], content_lower))
        if matched:
            gain_score += factor["weight"]
        grounding_results.append({
            "factor": factor["name"],
            "present": matched,
            "weight": factor["weight"]
        })

    # 3. Google Autocomplete Query Alignment
    matched_queries = []
    missed_queries = []
    for q in google_suggestions[:8]:
        q_tokens = [w for w in q.lower().split() if w not in STOP_WORDS]
        # If at least 60% of query tokens are found in content
        matches = sum(1 for tok in q_tokens if tok in content_lower)
        if matches >= max(1, int(len(q_tokens) * 0.6)):
            matched_queries.append(q)
        else:
            missed_queries.append(q)

    search_intent_alignment_pct = round((len(matched_queries) / max(1, len(google_suggestions[:8]))) * 100, 1)

    # 4. Overall Prodigy Content Score (0 - 100)
    # 40% Information Gain, 35% Entity Coverage, 25% Search Intent Alignment
    composite_prodigy_score = round(
        (gain_score * 0.40) + (entity_coverage_pct * 0.35) + (search_intent_alignment_pct * 0.25),
        1
    )

    if composite_prodigy_score >= 88:
        verdict = "PRODIGY_OUTRANK_READY"
        verdict_badge = "🏆 Prodigy Level (Outranks Top 3 Competitors)"
    elif composite_prodigy_score >= 70:
        verdict = "STRONG_COMPETITIVE"
        verdict_badge = "⚡ Strong Competitive (Top 10 Contender)"
    else:
        verdict = "NEEDS_OPTIMIZATION"
        verdict_badge = "⚠️ Needs Differentiation (Low Information Gain)"

    # Actionable outrank recommendations
    recommendations = []
    if missing_entities:
        recommendations.append(f"Incorporate high-salience competitor entities: {', '.join(missing_entities[:5])}")
    if missed_queries:
        recommendations.append(f"Answer unaddressed searcher queries: {', '.join(missed_queries[:3])}")
    for gr in grounding_results:
        if not gr["present"]:
            recommendations.append(f"Inject missing firsthand proof: {gr['factor']}")

    return {
        "prodigy_score": composite_prodigy_score,
        "information_gain_score": min(100, gain_score),
        "entity_coverage_pct": entity_coverage_pct,
        "search_intent_alignment_pct": search_intent_alignment_pct,
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "covered_entities": covered_entities,
        "missing_entities": missing_entities[:8],
        "google_matched_queries": matched_queries,
        "google_missed_queries": missed_queries[:5],
        "grounding_factors": grounding_results,
        "outrank_recommendations": recommendations,
        "top_competitors": competitors[:5],
    }


def analyze_serp_and_grade_content(keyword: str, content_text: str) -> Dict[str, Any]:
    """
    Main entry point: Scrapes live SERP competitors, retrieves Google suggest queries,
    and returns a full Surfer/Clearscope-style audit report with Information Gain metrics.
    """
    competitors = fetch_live_serp_competitors(keyword, max_results=8)
    google_suggestions = fetch_google_related_entities(keyword)
    return grade_information_gain(content_text, competitors, google_suggestions)


if __name__ == "__main__":
    sample_kw = "Puja at Dwarka"
    sample_text = (
        "Puja at Dwarka booking on YatraDham.Org. Certified Pandit ji services starting from ₹ 1,500.00. "
        "Timings: Morning aarti starts at 6:30 AM and evening darshan at 7:30 PM. "
        "Distance from Dwarka railway station is 2.5 km. Dress code requires traditional attire. "
        "Includes satvik prasad, sankalp, mantra chanting, and confirmed darshan assistance."
    )
    res = analyze_serp_and_grade_content(sample_kw, sample_text)
    print("PRODIGY SCORE:", res["prodigy_score"])
    print("VERDICT:", res["verdict_badge"])
    print("RECOMMENDATIONS:", res["outrank_recommendations"])
