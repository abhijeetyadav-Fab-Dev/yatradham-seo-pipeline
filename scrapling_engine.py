"""
Scrapling-Powered Modern Scraping & DOM Parsing Engine for YatraDham SEO Pipeline.
Leverages Scrapling (https://github.com/D4Vinci/Scrapling) + curl_cffi for ultra-fast,
stealthy HTML fetching (Chrome 124 TLS fingerprint impersonation) & deep JSON-LD / CSS / XPath extraction.
"""
import re
import json
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

try:
    from curl_cffi import requests as c_requests
    CURL_CFFI_AVAILABLE = True
except Exception as e:
    logger.warning(f"curl_cffi import fallback: {e}")
    CURL_CFFI_AVAILABLE = False


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 YatradhamBot/2.0"


def fetch_url_html(url: str, timeout: float = 6.0) -> str:
    """
    Fetch URL with SSRF protection, browser TLS fingerprint spoofing (curl_cffi Chrome 124)
    and stealth resilience to bypass Cloudflare / Akamai WAFs effortlessly.
    """
    if not url:
        return ""
    from ssrf_protection import is_safe_url
    safe, reason = is_safe_url(url)
    if not safe:
        logger.warning(f"SSRF block triggered for {url}: {reason}")
        return ""

    # Strategy 1: curl_cffi Chrome 124 impersonation (bypasses TLS fingerprinting & Cloudflare Turnstile)
    if CURL_CFFI_AVAILABLE:
        try:
            r = c_requests.get(
                url,
                impersonate="chrome124",
                timeout=timeout,
                allow_redirects=True,
                headers={"Accept-Language": "en-US,en;q=0.9,hi;q=0.8"}
            )
            if r.status_code == 200 and r.text:
                return r.text
            elif r.status_code in [403, 429]:
                logger.info(f"curl_cffi received HTTP {r.status_code} for {url}, trying fallback...")
        except Exception as e:
            logger.debug(f"curl_cffi fetch attempt for {url}: {e}")

    # Strategy 2: Standard requests with browser-grade headers
    import requests
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if r.status_code == 200 and r.text:
            return r.text
    except Exception as e:
        logger.warning(f"Standard requests failed for {url}: {e}")

    return ""


def extract_with_scrapling(html: str, url: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract rich structured fields from HTML using Scrapling Selector (CSS & XPath)
    plus embedded JSON-LD schema parsing.
    Extracts:
    - title / h1 / package title
    - price_raw / price_amount / price_currency
    - location_raw / street_address / locality / region / postal_code
    - checkin_time / checkout_time
    - hero_image_url
    - star_rating
    - itinerary_items
    - inclusions & exclusions
    - amenities / room_types
    """
    data: Dict[str, Any] = {
        "title": "",
        "price_raw": "",
        "location_raw": "",
        "street_address": "",
        "locality": "",
        "region": "",
        "postal_code": "",
        "checkin_time": "",
        "checkout_time": "",
        "hero_image_url": "",
        "star_rating": "",
        "description_raw": "",
        "itinerary_items": [],
        "inclusions": [],
        "exclusions": [],
        "amenities": [],
        "json_ld_detected": False
    }

    if not html:
        return data

    # 1. Parse embedded JSON-LD schemas (Source of Truth for E-Commerce / Hotels / Tours)
    try:
        json_ld_blocks = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
        for block in json_ld_blocks:
            clean_block = block.strip()
            if not clean_block:
                continue
            try:
                parsed = json.loads(clean_block)
                items = [parsed] if isinstance(parsed, dict) else (parsed if isinstance(parsed, list) else [])
                if isinstance(parsed, dict) and "@graph" in parsed:
                    items = parsed["@graph"]

                for item in items:
                    if not isinstance(item, dict):
                        continue
                    itype = str(item.get("@type", ""))
                    if any(t in itype for t in ["Hotel", "Product", "LodgingBusiness", "TouristTrip", "Place"]):
                        data["json_ld_detected"] = True
                        if item.get("name") and not data["title"]:
                            data["title"] = str(item["name"]).strip()
                        if item.get("description") and not data["description_raw"]:
                            data["description_raw"] = str(item["description"]).strip()
                        if item.get("image") and not data["hero_image_url"]:
                            img = item["image"]
                            data["hero_image_url"] = img if isinstance(img, str) else (img[0] if isinstance(img, list) and img else "")
                        
                        # Address
                        addr = item.get("address")
                        if isinstance(addr, dict):
                            data["street_address"] = str(addr.get("streetAddress", "")).strip()
                            data["locality"] = str(addr.get("addressLocality", "")).strip()
                            data["region"] = str(addr.get("addressRegion", "")).strip()
                            data["postal_code"] = str(addr.get("postalCode", "")).strip()
                            full_loc = ", ".join(filter(None, [data["locality"], data["region"], data["postal_code"]]))
                            if full_loc and not data["location_raw"]:
                                data["location_raw"] = full_loc

                        # Offers / Price
                        offer = item.get("makesOffer") or item.get("offers")
                        if isinstance(offer, dict):
                            if offer.get("checkinTime"):
                                data["checkin_time"] = str(offer["checkinTime"]).strip()
                            if offer.get("checkoutTime"):
                                data["checkout_time"] = str(offer["checkoutTime"]).strip()
                            
                            price_spec = offer.get("priceSpecification")
                            if isinstance(price_spec, dict) and price_spec.get("price"):
                                p_val = price_spec.get("price")
                                p_curr = price_spec.get("priceCurrency", "INR")
                                data["price_raw"] = f"₹ {p_val}" if p_curr == "INR" else f"{p_curr} {p_val}"
                            elif offer.get("price"):
                                p_val = offer.get("price")
                                p_curr = offer.get("priceCurrency", "INR")
                                data["price_raw"] = f"₹ {p_val}" if p_curr == "INR" else f"{p_curr} {p_val}"

                        if item.get("priceRange") and not data["price_raw"]:
                            data["price_raw"] = str(item["priceRange"]).strip()

                        if item.get("starRating") and isinstance(item["starRating"], dict):
                            data["star_rating"] = str(item["starRating"].get("ratingValue", "")).strip()
            except Exception as ex:
                logger.debug(f"JSON-LD snippet parse error: {ex}")
    except Exception as e:
        logger.debug(f"JSON-LD scanning error: {e}")

    # 2. Extract with Scrapling Selector (or BeautifulSoup fallback)
    if SCRAPLING_PARSER_AVAILABLE:
        try:
            page = Selector(html)

            # Title Extraction
            if not data["title"]:
                h1_val = page.css("h1::text").get()
                if not h1_val:
                    h1_val = page.css(".package-title::text, .product-title::text, .entry-title::text").get()
                data["title"] = (h1_val or "").strip()

            # Price Extraction
            if not data["price_raw"]:
                price_val = page.css(".price::text, .package-price::text, .cost::text, .amount::text, [class*='price']::text").get()
                if not price_val:
                    # Search text for rupee or Rs
                    nodes = re.findall(r'(?:₹|Rs\.?)\s*[\d,]+', html)
                    if nodes:
                        price_val = nodes[0]
                data["price_raw"] = (price_val or "").strip()

            # Location / Center Extraction
            if not data["location_raw"]:
                loc_val = page.css(".location::text, .center-details::text, .destination::text, [class*='location']::text, .address::text").get()
                data["location_raw"] = (loc_val or "").strip()

            # Hero Image
            if not data["hero_image_url"]:
                og_img = page.css('meta[property="og:image"]::attr(content)').get()
                if og_img:
                    data["hero_image_url"] = og_img.strip()

            # Inclusions & Exclusions
            inclusions = page.css("ul.inclusions li::text, .inclusion-item::text, ul.package-inclusions li::text").getall()
            data["inclusions"] = [inc.strip() for inc in inclusions if inc.strip()]

            itinerary = page.css(".itinerary-day::text, .itinerary-item::text, ul.itinerary li::text").getall()
            data["itinerary_items"] = [it.strip() for it in itinerary if it.strip()]

            # Amenities
            amenities = page.css(".amenity::text, .facility::text, .facilities-list li::text").getall()
            data["amenities"] = [a.strip() for a in amenities if a.strip()]

        except Exception as e:
            logger.warning(f"Scrapling selector parse error: {e}")
    else:
        # Fallback regex & OpenGraph parser
        if not data["title"]:
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
            if title_match:
                data["title"] = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()

    return data
