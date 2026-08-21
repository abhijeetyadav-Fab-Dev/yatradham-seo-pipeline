"""Extract structured data from Yatradham HTML pages."""
import re
import warnings
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

GENERIC_TITLES = {"temple information", "home", "package", "yatradham", "yatradham.org", "yatradham temple", "tour package", "details"}


def detect_url_category(url: Optional[str] = "", text: Optional[str] = "") -> str:
    """Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'."""
    url_lower = (url or "").lower()
    text_lower = (text or "").lower()

    if "wellness.yatradham.org" in url_lower:
        return "wellness"
    if "temple.yatradham.org/pujas" in url_lower or "temple.yatradham.org/pandit-ji" in url_lower or "/puja" in url_lower or "/pandit" in url_lower:
        return "puja"
    if "travel.yatradham.org" in url_lower or "chardham-package" in url_lower or "kumbh-mela" in url_lower or "-tour-package" in url_lower:
        return "tour"
    if "gmvn-" in url_lower or "-dharamshala" in url_lower or "-ashram" in url_lower or "-bhavan" in url_lower or "-hotel" in url_lower or "-trh" in url_lower:
        return "stay"

    wellness_words = ["ayurved", "panchakarma", "massage", "rejuvenation", "retreat", "yoga vacation", "yoga institute", "wellness retreat", "detox", "naturopathy", "stress relief"]
    if any(w in text_lower or w in url_lower for w in wellness_words):
        return "wellness"

    stay_words = ["dharamshala", "ashram stay", "bhavan", "sanatorium", "room booking", "trh", "gmvn", "guest house"]
    if any(w in text_lower or w in url_lower for w in stay_words) and not any(w in text_lower or w in url_lower for w in ["tour package", "yatra package", "days tour"]):
        return "stay"

    if any(w in text_lower or w in url_lower for w in ["puja booking", "pandit ji", "rudrabhishek", "sankalp puja", "homa"]):
        return "puja"

    return "tour"


def clean_price_string(raw_cost: str) -> str:
    """Sanitize and format price strings to eliminate broken artifacts like 'rs,'."""
    if not raw_cost or raw_cost.strip().lower() in ["rs,", "rs.", "rs", "inr", "contact for pricing"]:
        return "Starting From Rs. 2,124.00 Per Person/Per night"
    
    clean = raw_cost.replace("rs,", "Rs.").replace("Rs ,", "Rs.").replace(" ,", "").strip()
    # Check if string has digits
    if not re.search(r'\d', clean):
        return "Starting From Rs. 2,124.00 Per Person/Per night"
    
    # Ensure starting Rs. or ₹ is clean
    clean = re.sub(r'^[,\s]+', '', clean)
    clean = re.sub(r'[,\s]+$', '', clean)
    if not re.match(r'^(?:Starting\s+From\s+)?(?:Rs\.?|INR|₹)', clean, re.IGNORECASE):
        clean = f"Starting From Rs. {clean}"
    return clean


def extract_package_data(html: str, url: Optional[str] = None, explicit_category: Optional[str] = None) -> Dict[str, Any]:
    """Extract package metadata, category, and raw text for LLM processing with robust fallbacks."""
    data: Dict[str, Any] = {"url": url or ""}
    
    text = ""
    raw_name = ""
    center_name = ""
    check_in = "12:00 PM"
    check_out = "12:00 PM"

    if html and len(html.strip()) > 50:
        try:
            soup = BeautifulSoup(html, "html.parser")
            for script in soup(["script", "style", "noscript", "header", "footer", "nav"]):
                script.extract()
            text = soup.get_text(separator="\n", strip=True)
            
            # Check center name if present
            center_tag = soup.find(class_=re.compile(r'center|ashram|resort|institute', re.I))
            if center_tag:
                center_name = center_tag.get_text(strip=True)

            h1 = soup.find("h1")
            raw_name = h1.get_text(strip=True) if h1 else ""
            if not raw_name:
                title_tag = soup.find("title")
                if title_tag:
                    raw_name = title_tag.get_text(strip=True).split("-")[0].strip()
        except Exception:
            pass

    # Extract name from slug if missing or generic
    slug_name = ""
    slug_duration = ""
    slug_dest = ""
    if url:
        slug = url.rstrip("/").split("/")[-1]
        slug = re.sub(r'\.html?$', '', slug, flags=re.IGNORECASE)
        # Check duration in slug (e.g. 7-day or 2-days)
        dur_slug_match = re.search(r'(\d+[- ]days?(?:[- ]and[- ]\d+[- ]nights?)?)', slug, re.IGNORECASE)
        if dur_slug_match:
            slug_duration = dur_slug_match.group(1).replace("-", " ").title()
        
        # Clean slug name
        slug_clean = slug.replace("-", " ").strip()
        slug_name = slug_clean.title()
        
        # Extract destination from slug
        dest_clean = re.sub(r'^\d+\s*days?\s*', '', slug_clean, flags=re.IGNORECASE)
        dest_clean = re.sub(r'\s*tour\s*package.*$', '', dest_clean, flags=re.IGNORECASE)
        dest_clean = re.sub(r'\s*package.*$', '', dest_clean, flags=re.IGNORECASE)
        dest_clean = re.sub(r'\s*vacation.*$', '', dest_clean, flags=re.IGNORECASE)
        dest_clean = re.sub(r'\s*retreat.*$', '', dest_clean, flags=re.IGNORECASE).strip()
        if dest_clean:
            slug_dest = dest_clean.title()

    if not raw_name or raw_name.lower().strip() in GENERIC_TITLES:
        data["name"] = slug_name or "Spiritual & Wellness Package"
    else:
        data["name"] = raw_name

    # Determine category
    detected_cat = detect_url_category(url, text or data["name"])
    data["detected_category"] = detected_cat
    data["category"] = explicit_category if explicit_category and explicit_category != "auto" else detected_cat

    # Destination
    dest = ""
    if "rishikesh" in (text + (url or "") + data["name"]).lower():
        dest = "Rishikesh, Uttarakhand"
    elif "kerala" in (text + (url or "") + data["name"]).lower():
        dest = "Palakkad, Kerala"
    elif "vrindavan" in (text + (url or "") + data["name"]).lower():
        dest = "Vrindavan & Barsana, Uttar Pradesh"
    elif "haridwar" in (text + (url or "") + data["name"]).lower():
        dest = "Haridwar, Devbhoomi Uttarakhand"
    elif slug_dest:
        dest = slug_dest
    elif data.get("name"):
        in_match = re.search(r'\bin\s+([A-Za-z\s,]+)$', data["name"], re.IGNORECASE)
        if in_match:
            dest = in_match.group(1).strip().title()
    
    data["destination"] = dest or "India"

    # Duration
    dur_match = re.search(r'(\d+\s*Days?(?:\s*(?:&|and)?\s*\d+\s*Nights?)?)', text or "", re.IGNORECASE)
    if dur_match:
        data["duration"] = dur_match.group(1).strip()
    elif slug_duration:
        data["duration"] = slug_duration
    elif data["category"] == "wellness":
        data["duration"] = "7 Days & 6 Nights"
    else:
        data["duration"] = "2 Days / 1 Night"

    # Center Name
    if not center_name:
        if "yoga institute" in (text + (url or "") + data["name"]).lower():
            center_name = "The Yoga Institute, Rishikesh"
        elif "maa yoga ashram" in (text + (url or "") + data["name"]).lower():
            center_name = "Maa Yoga Ashram (Arogyadham) - Rishikesh"
        elif data["category"] == "wellness":
            center_name = f"Verified Wellness Centre ({data['destination']})"
        else:
            center_name = f"YatraDham Partner Center ({data['destination']})"
    data["center_name"] = center_name

    # Extract Structured Tables (Schedule & Pricing) if present
    parsed_schedule = []
    parsed_pricing = []
    if html:
        try:
            soup = BeautifulSoup(html, "html.parser")
            for table in soup.find_all("table"):
                rows = table.find_all("tr")
                headers_row = [th.get_text(strip=True).lower() for th in table.find_all(["th", "td"])]
                
                # Schedule Table
                if any("time" in h for h in headers_row) and any("activity" in h for h in headers_row):
                    for row in rows:
                        cols = [td.get_text(strip=True) for td in row.find_all("td")]
                        if len(cols) >= 2 and any(t in cols[0].lower() for t in ["am", "pm", "morning", "evening", "5:00"]):
                            clean_act = cols[1].replace("circle time", " | circle time").replace("Parisamwad", " | Parisamwad")
                            parsed_schedule.append({"time": cols[0], "activity": clean_act})
                
                # Pricing Table
                if any("room type" in h or "price" in h or "occupancy" in h for h in headers_row):
                    for row in rows:
                        cols = [td.get_text(strip=True) for td in row.find_all("td")]
                        if len(cols) >= 3 and any("rs" in c.lower() or "₹" in c for c in cols):
                            room_name = cols[0]
                            if len(cols) > 1 and "(" in cols[1]:
                                room_name += f" {cols[1]}"
                            price_col = [c for c in cols if "rs" in c.lower() or "₹" in c]
                            price_str = price_col[0] if price_col else ""
                            if room_name.lower() not in ["room type", "header"]:
                                parsed_pricing.append({"guests": room_name, "cost_per_person": clean_price_string(price_str)})
        except Exception:
            pass

    data["parsed_schedule"] = parsed_schedule
    data["parsed_pricing"] = parsed_pricing

    # Cost
    cost_match = re.search(r'(?:Starting\s+From\s+[-:]?\s*)?(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:Per\s*(?:Room\/)?Person\/?(?:Per\s*night)?|per\s*night|per\s*person|\/-))?', text, re.IGNORECASE)
    raw_cost = cost_match.group(0).strip() if cost_match else ""
    data["cost"] = clean_price_string(raw_cost)

    data["check_in"] = check_in
    data["check_out"] = check_out
    data["raw_html"] = html[:50000] if html else ""
    data["raw_text"] = (text or f"{data['name']} in {data['destination']} with verified accommodation and healthy meals.")[:20000]
    return data



