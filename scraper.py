"""Extract structured data from Yatradham HTML pages."""
import re
import warnings
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

GENERIC_TITLES = {"temple information", "home", "package", "yatradham", "yatradham.org", "yatradham temple", "tour package"}


def extract_package_data(html: str, url: Optional[str] = None) -> Dict[str, Any]:
    """Extract basic package metadata and raw text for LLM processing with robust fallbacks."""
    data: Dict[str, Any] = {"url": url or ""}
    
    text = ""
    raw_name = ""
    if html and len(html.strip()) > 50:
        try:
            soup = BeautifulSoup(html, "html.parser")
            for script in soup(["script", "style", "noscript", "header", "footer", "nav"]):
                script.extract()
            text = soup.get_text(separator="\n", strip=True)
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
        # Check duration in slug (e.g. 2-days or 3-days)
        dur_slug_match = re.search(r'(\d+[- ]days?(?:[- ]and[- ]\d+[- ]nights?)?)', slug, re.IGNORECASE)
        if dur_slug_match:
            slug_duration = dur_slug_match.group(1).replace("-", " ").title()
        
        # Clean slug name
        slug_clean = slug.replace("-", " ").strip()
        slug_name = slug_clean.title()
        
        # Extract destination from slug
        dest_clean = re.sub(r'^\d+\s*days?\s*', '', slug_clean, flags=re.IGNORECASE)
        dest_clean = re.sub(r'\s*tour\s*package.*$', '', dest_clean, flags=re.IGNORECASE)
        dest_clean = re.sub(r'\s*package.*$', '', dest_clean, flags=re.IGNORECASE).strip()
        if dest_clean:
            slug_dest = dest_clean.title()

    if not raw_name or raw_name.lower().strip() in GENERIC_TITLES:
        data["name"] = slug_name or "Spiritual Tour Package"
    else:
        data["name"] = raw_name

    # Destination
    dest = ""
    if slug_dest:
        dest = slug_dest
    elif data.get("name"):
        in_match = re.search(r'\bin\s+([A-Za-z\s,]+)$', data["name"], re.IGNORECASE)
        if in_match:
            dest = in_match.group(1).strip().title()
    
    data["destination"] = dest or "Vrindavan Barsana" if "vrindavan" in (text + (url or "")).lower() else (dest or "India")

    # Duration
    dur_match = re.search(r'(\d+\s*Days?(?:\s*(?:&|and)?\s*\d+\s*Nights?)?)', text or "", re.IGNORECASE)
    if dur_match:
        data["duration"] = dur_match.group(1).strip()
    elif slug_duration:
        data["duration"] = slug_duration
    else:
        data["duration"] = "2 Days"

    # Cost
    cost_match = re.search(r'(?:Rs\.?|INR|₹)\s*[\d,]+(?:\s*(?:per\s*person|per\s*night|\/-))?', text, re.IGNORECASE)
    data["cost"] = cost_match.group(0).strip() if cost_match else "Contact for pricing"

    data["raw_html"] = html[:50000] if html else ""
    data["raw_text"] = (text or f"{data['name']} in {data['destination']} with verified accommodation, darshan assistance, and vegetarian meals.")[:20000]
    return data

