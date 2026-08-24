"""Extract structured data from Yatradham HTML pages."""
import re
import warnings
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

GENERIC_TITLES = {"temple information", "home", "package", "yatradham", "yatradham.org", "yatradham temple", "tour package", "details", "best yoga retreats & wellness by yatradham.org", "page not found"}

# Known Indian Spiritual & Wellness Retreat Centers and Destinations
DESTINATIONS_MAP = {
    "abhayaranya": "Rishikesh, Uttarakhand",
    "earth roots": "Rishikesh, Uttarakhand",
    "kairali": "Palakkad, Kerala",
    "vaidyaratnam": "Baddi, Himachal Pradesh",
    "jahnavi": "Haridwar, Uttarakhand",
    "patanjali": "Rishikesh, Uttarakhand",
    "akhanda": "Rishikesh, Uttarakhand",
    "mrityunjay": "Rishikesh, Uttarakhand",
    "purnashakti": "Junagadh, Gujarat",
    "kriya yoga": "Gangasagar, West Bengal",
    "arogya": "Rishikesh, Uttarakhand",
    "the yoga institute": "Rishikesh, Uttarakhand",
    "modi yoga": "Rishikesh, Uttarakhand",
    "adhyatm": "New Delhi, Delhi",
    "corporate excellence": "New Delhi, Delhi",
    "gangasagar": "Gangasagar, West Bengal",
    "24 parganas": "Gangasagar, West Bengal",
    "bhubaneswar": "Bhubaneswar, Odisha",
    "nalsarovar": "Nalsarovar, Ahmedabad, Gujarat",
    "ahmedabad": "Ahmedabad, Gujarat",
    "kumarakom": "Kumarakom, Kerala",
    "palakkad": "Palakkad, Kerala",
    "kerala": "Palakkad, Kerala",
    "alibaug": "Alibaug, Maharashtra",
    "mumbai": "Mumbai, Maharashtra",
    "delhi": "New Delhi, Delhi",
    "new delhi": "New Delhi, Delhi",
    "junagadh": "Junagadh, Gujarat",
    "baddi": "Baddi, Himachal Pradesh",
    "kangra": "Kangra, Himachal Pradesh",
    "himachal": "Kangra, Himachal Pradesh",
    "manali": "Manali, Himachal Pradesh",
    "shimla": "Shimla, Himachal Pradesh",
    "dharamshala": "Dharamshala, Himachal Pradesh",
    "haridwar": "Haridwar, Uttarakhand",
    "rishikesh": "Rishikesh, Uttarakhand",
    "uttarakhand": "Rishikesh, Uttarakhand",
    "vrindavan": "Vrindavan, Uttar Pradesh",
    "barsana": "Barsana, Uttar Pradesh",
    "mathura": "Mathura, Uttar Pradesh",
    "varanasi": "Varanasi, Uttar Pradesh",
    "kashi": "Varanasi, Uttar Pradesh",
    "ayodhya": "Ayodhya, Uttar Pradesh",
    "puri": "Puri, Odisha",
    "shirdi": "Shirdi, Maharashtra",
    "tirupati": "Tirupati, Andhra Pradesh",
    "ujjain": "Ujjain, Madhya Pradesh",
    "dwarka": "Dwarka, Gujarat",
    "somnath": "Somnath, Gujarat",
    "kedarnath": "Kedarnath, Uttarakhand",
    "badrinath": "Badrinath, Uttarakhand",
    "gangotri": "Gangotri, Uttarakhand",
    "yamunotri": "Yamunotri, Uttarakhand",
    "rameshwaram": "Rameshwaram, Tamil Nadu",
    "madurai": "Madurai, Tamil Nadu",
    "goa": "Goa, India",
    "gokarna": "Gokarna, Karnataka"
}


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

    wellness_words = ["ayurved", "panchakarma", "massage", "rejuvenation", "retreat", "yoga vacation", "yoga institute", "wellness retreat", "detox", "naturopathy", "stress relief", "corporate excellence", "camp in delhi"]
    if any(w in text_lower or w in url_lower for w in wellness_words):
        return "wellness"

    stay_words = ["dharamshala", "ashram stay", "bhavan", "sanatorium", "room booking", "trh", "gmvn", "guest house"]
    if any(w in text_lower or w in url_lower for w in stay_words) and not any(w in text_lower or w in url_lower for w in ["tour package", "yatra package", "days tour"]):
        return "stay"

    if any(w in text_lower or w in url_lower for w in ["puja booking", "pandit ji", "rudrabhishek", "sankalp puja", "homa"]):
        return "puja"

    return "tour"


def clean_price_string(raw_cost: str) -> str:
    """Sanitize and format price strings cleanly. Never return hardcoded mock numbers or bogus small amounts."""
    if not raw_cost or str(raw_cost).strip().lower() in ["rs,", "rs.", "rs", "inr", "contact for pricing", "null", "none", ""]:
        return "Starting From ₹ Contact for Pricing"
    
    clean = str(raw_cost).replace("rs,", "").replace("Rs ,", "").replace(" ,", "").strip()
    
    # Reject negative prices, 0, or free
    if "-" in clean or re.search(r'\b(?:free|0)\b', clean, re.I):
        return "Starting From ₹ Contact for Pricing"

    digits_match = re.search(r'[\d,]+(?:\.\d{2})?', clean)
    if not digits_match:
        return "Starting From ₹ Contact for Pricing"
    
    amount_str = digits_match.group(0)
    try:
        numeric_val = float(amount_str.replace(",", ""))
        if numeric_val < 100:
            return "Starting From ₹ Contact for Pricing"
    except ValueError:
        return "Starting From ₹ Contact for Pricing"
    
    if "." in amount_str:
        parts = amount_str.split(".")
        main_num = int(parts[0].replace(",", ""))
        formatted_amount = f"{main_num:,}.{parts[1]}"
    else:
        formatted_amount = f"{int(numeric_val):,}"

    suffix = ""
    if re.search(r'per\s*night', clean, re.I):
        suffix = " Per Person/Per night"
    elif re.search(r'per\s*person', clean, re.I):
        suffix = " Per Person"
        
    return f"Starting From ₹ {formatted_amount}{suffix}".strip()



def normalize_duration_string(raw_dur: str) -> str:
    """Normalize duration string to ensure correct singular/plural English grammar."""
    if not raw_dur:
        return "Flexible Duration"
    
    d = raw_dur.strip().replace("-", " ")
    d = re.sub(r'\b1\s+Days\b', '1 Day', d, flags=re.IGNORECASE)
    
    match_dn = re.search(r'(\d+)\s*Days?(?:\s*(?:&|and)\s*(\d+)\s*Nights?)?', d, re.IGNORECASE)
    if match_dn:
        days = int(match_dn.group(1))
        nights = match_dn.group(2)
        day_str = f"{days} Day" if days == 1 else f"{days} Days"
        if nights:
            n_count = int(nights)
            night_str = f"{n_count} Night" if n_count == 1 else f"{n_count} Nights"
            return f"{day_str} & {night_str}"
        return day_str
    
    return d.title()




def extract_package_data(html: str, url: Optional[str] = None, explicit_category: Optional[str] = None) -> Dict[str, Any]:
    """Extract package metadata, category, and raw text for LLM processing with robust extraction."""
    data: Dict[str, Any] = {"url": url or ""}
    
    text = ""
    raw_name = ""
    center_name = ""
    center_loc = ""
    is_not_found = False

    # Extract name and duration from slug as primary fallback
    slug_name = ""
    slug_duration = ""
    slug_dest = ""
    if url:
        slug = url.rstrip("/").split("/")[-1]
        slug = re.sub(r'\.html?$', '', slug, flags=re.IGNORECASE)
        # Check duration in slug (e.g. 7-day, 14-day, 2-days, weekend)
        if "weekend" in slug.lower():
            slug_duration = "2 Days & 1 Night"
        else:
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

    if html and len(html.strip()) > 50:
        try:
            # 1. Scrapling Structured Parser for fast DOM querying
            try:
                from scrapling_engine import extract_with_scrapling
                scrapling_data = extract_with_scrapling(html, url)
                if scrapling_data.get("title"):
                    raw_name = scrapling_data["title"]
                if scrapling_data.get("location_raw"):
                    center_loc = scrapling_data["location_raw"]
            except Exception:
                pass

            # 2. BeautifulSoup Parser fallback & text extraction
            soup = BeautifulSoup(html, "html.parser")
            
            # Check 404 / Not Found
            title_tag = soup.find("title")
            title_text = title_tag.get_text(strip=True) if title_tag else ""
            if "page not found" in title_text.lower() or "404" in title_text:
                is_not_found = True

            # Extract Center Details & Inquiry block before removing tags
            full_text_raw = soup.get_text(separator="\n", strip=True)
            center_match = re.search(r'Center Details & Inquiry\s*\n+([^\n]+)\s*\n+([^\n]+)', full_text_raw, re.I)
            if center_match:
                center_name = center_match.group(1).strip()
                if not center_loc:
                    center_loc = center_match.group(2).strip()

            for script in soup(["script", "style", "noscript", "header", "footer", "nav"]):
                script.extract()
            text = soup.get_text(separator="\n", strip=True)

            if not raw_name:
                h1 = soup.find("h1")
                raw_name = h1.get_text(strip=True) if h1 else ""
            if not raw_name and title_text and not is_not_found:
                raw_name = title_text.split("-")[0].split("|")[0].strip()
        except Exception:
            pass


    if is_not_found or not raw_name or raw_name.lower().strip() in GENERIC_TITLES:
        data["name"] = slug_name or "Spiritual & Wellness Package"
    else:
        data["name"] = raw_name

    # Determine category
    detected_cat = detect_url_category(url, text or data["name"])
    data["detected_category"] = detected_cat
    data["category"] = explicit_category if explicit_category and explicit_category != "auto" else detected_cat

    # Determine Destination with strict priority:
    # 1. Center Location from 'Center Details & Inquiry' (e.g. "West Bengal, 24 Parganas (s)", "Gujarat, Ahmedabad")
    # 2. Package Name / Title ("in Rishikesh", "at Gangasagar", "in Delhi", "in Bhubaneswar", "in Kerala")
    # 3. Known Destinations lookup in package title and slug
    # 4. Slug destination
    dest = ""
    name_and_slug = f"{data['name']} {slug_name} {url}".lower()

    if center_loc and not any(g in center_loc.lower() for g in ["yatradham", "inquiry", "+91"]):
        # Clean up location (e.g. "West Bengal, 24 Parganas (s)" or "Uttarakhand, Rishikesh")
        loc_parts = [p.strip() for p in center_loc.split(",") if p.strip()]
        if len(loc_parts) >= 2:
            dest = f"{loc_parts[1]}, {loc_parts[0]}"  # City, State
        else:
            dest = center_loc

    if not dest:
        # 1. Direct search across known spiritual destinations in name and URL slug
        for key, val in DESTINATIONS_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', name_and_slug, re.IGNORECASE):
                dest = val
                break

    if not dest:
        # 2. Check specific destination patterns in title (e.g. "at Gangasagar", "in Rishikesh", "in Delhi")
        in_match = re.search(r'\b(?:in|at)\s+([A-Za-z\s]+?)(?:\s*[-–|,]|\s*Package|\s*Retreat|\s*Camp|\s*Tour|$)', data["name"], re.IGNORECASE)
        if in_match:
            candidate = in_match.group(1).strip().lower()
            for key, val in DESTINATIONS_MAP.items():
                if key in candidate:
                    dest = val
                    break
            if not dest and len(candidate) > 2 and candidate not in ["the", "this", "our", "three", "seven", "ayurveda", "wellness", "yatradham", "days", "day"]:
                dest = f"{candidate.title()}, India"

    if not dest and slug_dest:
        dest = f"{slug_dest}, India"

    data["destination"] = dest or "India"


    # Duration Extraction
    dur = ""
    name_and_text = f"{data['name']} {text}"
    if "weekend" in name_and_slug:
        dur = "2 Days & 1 Night"
    else:
        dur_match = re.search(r'(\d+\s*Days?(?:\s*(?:&|and)?\s*\d+\s*Nights?)?)', name_and_text, re.IGNORECASE)
        if dur_match:
            dur = normalize_duration_string(dur_match.group(1).strip())
        elif slug_duration:
            dur = slug_duration
        elif data["category"] == "wellness":
            dur = "7 Days & 6 Nights"
        else:
            dur = "3 Days & 2 Nights"
    data["duration"] = dur


    # Center Name Extraction
    if not center_name:
        if "arogya yoga school" in name_and_slug:
            center_name = "Arogya Yoga School - Rishikesh"
        elif "yoga institute" in name_and_slug:
            center_name = "The Yoga Institute, Rishikesh"
        elif "kriya yoga" in name_and_slug:
            center_name = f"Kriya Yoga Wellness Center - {data['destination']}"
        elif "modi" in name_and_slug:
            center_name = f"Modi Yoga & Wellness Retreats - {data['destination']}"
        elif "adhyatm" in name_and_slug:
            center_name = f"Adhyatm Sadhna Kendra - {data['destination']}"
        elif "kumarakom" in name_and_slug:
            center_name = "Kumarakom Lake Resort, Kerala"
        elif "ayuskama" in name_and_slug:
            center_name = f"Ayuskama Ayurveda Wellness Center - {data['destination']}"
        elif data["category"] == "wellness":
            center_name = f"Verified Wellness Center ({data['destination']})"
        else:
            center_name = f"YatraDham Partner Center ({data['destination']})"
    data["center_name"] = center_name

    # Extract Structured Tables (Schedule & Pricing) if present
    parsed_schedule = []
    parsed_pricing = []
    if html and not is_not_found:
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
                        if len(cols) >= 2 and any("rs" in c.lower() or "₹" in c for c in cols):
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

    # Cost Extraction from Page Text
    cost_val = ""
    if text and not is_not_found:
        # Find all price mentions
        all_prices = re.findall(r'(?:Starting\s+From\s+[-:]?\s*)?(?:₹|Rs\.?|INR)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:Per\s*(?:Room\/)?Person\/?(?:Per\s*night)?|per\s*night|per\s*person|\/-))?', text, re.IGNORECASE)
        valid_prices = [p.strip() for p in all_prices if re.search(r'\d', p) and "0000" not in p]
        if valid_prices:
            # Pick first valid price
            cost_val = clean_price_string(valid_prices[0])
    
    if not cost_val:
        cost_val = "Starting From ₹ Contact for Pricing"
    data["cost"] = cost_val

    data["check_in"] = "12:00 PM"
    data["check_out"] = "12:00 PM"
    data["raw_html"] = html[:50000] if html else ""
    data["raw_text"] = (text or f"{data['name']} in {data['destination']} with verified accommodation and healthy meals.")[:20000]
    return data




