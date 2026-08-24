"""
Scrapling-Powered Modern Scraping & DOM Parsing Engine for YatraDham SEO Pipeline.
Leverages https://github.com/D4Vinci/Scrapling for ultra-fast, stealthy HTML fetching & CSS/XPath extraction.
"""
import re
import logging
import urllib.request
from typing import Dict, Any, Optional, List

logger = logging.getLogger("scrapling_engine")

try:
    from scrapling.parser import Selector
    SCRAPLING_PARSER_AVAILABLE = True
except Exception as e:
    logger.warning(f"Scrapling parser import fallback: {e}")
    SCRAPLING_PARSER_AVAILABLE = False


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 YatradhamBot/2.0"


def fetch_url_html(url: str, timeout: int = 15) -> str:
    """Fetch URL with browser-grade headers and stealth resilience."""
    if not url:
        return ""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
            "Referer": "https://www.google.com/",
            "Upgrade-Insecure-Requests": "1"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return ""


def extract_with_scrapling(html: str, url: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract structured fields from HTML using Scrapling Selector (CSS & XPath).
    Extracts:
    - h1 / package title
    - price / starting cost
    - location / center details
    - itinerary bullets
    - inclusions & exclusions
    """
    data = {
        "title": "",
        "price_raw": "",
        "location_raw": "",
        "itinerary_items": [],
        "inclusions": [],
        "exclusions": []
    }
    
    if not html or not SCRAPLING_PARSER_AVAILABLE:
        return data

    try:
        page = Selector(html)
        
        # 1. Title Extraction
        h1_val = page.css("h1::text").get()
        if not h1_val:
            h1_val = page.css(".package-title::text, .product-title::text, .entry-title::text").get()
        data["title"] = (h1_val or "").strip()
        
        # 2. Price Extraction via CSS selectors
        price_val = page.css(".price::text, .package-price::text, .cost::text, .amount::text, [class*='price']::text").get()
        if not price_val:
            price_nodes = page.xpath("//*[contains(text(), '₹') or contains(text(), 'Rs.') or contains(text(), 'Starting From')]//text()").getall()
            if price_nodes:
                price_val = " ".join([p.strip() for p in price_nodes if p.strip()])
        data["price_raw"] = (price_val or "").strip()
        
        # 3. Location / Center Extraction
        loc_val = page.css(".location::text, .center-details::text, .destination::text, [class*='location']::text").get()
        if not loc_val:
            center_nodes = page.xpath("//*[contains(text(), 'Center Details')]//following::text()[1]").getall()
            if center_nodes:
                loc_val = " ".join([c.strip() for c in center_nodes if c.strip() and not re.search(r'\b\d\s*/\s*5\b', c)])
        data["location_raw"] = (loc_val or "").strip()


        # 4. Inclusions & Itinerary Lists
        inclusions = page.css("ul.inclusions li::text, .inclusion-item::text, ul.package-inclusions li::text").getall()
        data["inclusions"] = [inc.strip() for inc in inclusions if inc.strip()]

        itinerary = page.css(".itinerary-day::text, .itinerary-item::text, ul.itinerary li::text").getall()
        data["itinerary_items"] = [it.strip() for it in itinerary if it.strip()]

    except Exception as e:
        logger.warning(f"Scrapling selector parse error: {e}")

    return data
