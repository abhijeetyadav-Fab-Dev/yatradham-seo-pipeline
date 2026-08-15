"""Extract structured data from Yatradham HTML pages."""
import re
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup


def extract_package_data(html: str, url: Optional[str] = None) -> Dict[str, Any]:
    """Extract basic package metadata and raw text for LLM processing."""
    soup = BeautifulSoup(html, "html.parser")
    data: Dict[str, Any] = {"url": url or ""}
    
    # Strip unnecessary scripts and styles to keep raw text clean
    for script in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        script.extract()
        
    text = soup.get_text(separator="\n", strip=True)

    # --- BASIC FIELDS (For initial prompt context) ---
    # Title / Package Name
    h1 = soup.find("h1")
    data["name"] = h1.get_text(strip=True) if h1 else ""
    if not data["name"]:
        title_tag = soup.find("title")
        data["name"] = title_tag.get_text(strip=True).split("-")[0].strip() if title_tag else "Yatradham Package"

    # Destination - from URL or text
    if url:
        url_parts = url.rstrip("/").split("/")
        last_part = url_parts[-1] if url_parts else ""
        slug_dest = last_part.replace("-", " ").replace("tour package", "").replace("package", "").strip()
        data["destination"] = slug_dest.title() if slug_dest else ""
    else:
        data["destination"] = ""

    # Duration - look for "X Days"
    dur_match = re.search(r'(\d+)\s*Days?', text, re.IGNORECASE)
    data["duration"] = dur_match.group(0) if dur_match else ""

    # Merge everything for the LLM
    data["raw_html"] = html[:50000]  # truncate for storage
    data["raw_text"] = text[:20000]  # truncate text for prompt
    return data
