"""
Public APIs Enrichment & Ground-Truth Verification Layer.
Leverages free, keyless public APIs from the public-apis / public-api-lists repository:
1. OpenStreetMap Nominatim API (Geocoding & State Verification)
2. Wikipedia REST API (Verified Spiritual & Cultural Heritage Facts)
3. Open-Meteo API (Live Weather & Best Visiting Climate)
4. Sunrise-Sunset API (Astronomical Solar Timings for Ganga Aarti & Yoga)
"""
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("public_apis_enricher")

USER_AGENT = "YatraDhamSEOPipeline/2.0 (contact: info@yatradham.org)"


def geocode_location(place_name: str) -> Optional[Dict[str, Any]]:
    """Geocode Indian destinations using OpenStreetMap Nominatim API."""
    if not place_name or place_name.lower() in ["india", "unknown"]:
        return None
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={place_name},India&format=json&limit=1"
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=4)
        if r.status_code == 200 and r.json():
            item = r.json()[0]
            return {
                "display_name": item.get("display_name"),
                "lat": float(item.get("lat")),
                "lon": float(item.get("lon")),
                "osm_type": item.get("type")
            }
    except Exception as e:
        logger.warning(f"Geocoding failed for {place_name}: {e}")
    return None


def fetch_spiritual_heritage_facts(topic: str) -> Optional[Dict[str, str]]:
    """Fetch verified cultural & spiritual heritage summary from Wikipedia REST API."""
    if not topic:
        return None
    clean_topic = topic.split(",")[0].strip().replace(" ", "_")
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_topic}"
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=4)
        if r.status_code == 200:
            data = r.json()
            extract = data.get("extract", "")
            if extract:
                return {
                    "title": data.get("title", topic),
                    "summary": extract,
                    "wiki_url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
                }
    except Exception as e:
        logger.warning(f"Wikipedia fetch failed for {topic}: {e}")
    return None


def fetch_climate_and_weather(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Fetch live temperature and weather condition via Open-Meteo API."""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code"
        r = requests.get(url, timeout=4)
        if r.status_code == 200:
            curr = r.json().get("current", {})
            temp = curr.get("temperature_2m")
            humidity = curr.get("relative_humidity_2m")
            return {
                "temperature_celsius": temp,
                "relative_humidity": humidity,
                "condition_summary": "Pleasant / Favorable" if temp and 15 <= temp <= 32 else "Warm / Active"
            }
    except Exception as e:
        logger.warning(f"Open-Meteo fetch failed for {lat}, {lon}: {e}")
    return None


def fetch_solar_timings(lat: float, lon: float) -> Optional[Dict[str, str]]:
    """Fetch exact sunrise and sunset times from Sunrise-Sunset API."""
    try:
        url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=1"
        r = requests.get(url, timeout=4)
        if r.status_code == 200:
            results = r.json().get("results", {})
            return {
                "sunrise": results.get("sunrise"),
                "sunset": results.get("sunset"),
                "solar_noon": results.get("solar_noon")
            }
    except Exception as e:
        logger.warning(f"Sunrise-Sunset API failed for {lat}, {lon}: {e}")
    return None


def fetch_semantic_lsi_keywords(keyword: str, max_results: int = 6) -> list:
    """Fetch semantic LSI synonyms & related terms using Datamuse API (free, keyless)."""
    if not keyword:
        return []
    try:
        url = f"https://api.datamuse.com/words?ml={keyword}&max={max_results}"
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return [item["word"] for item in r.json() if " " not in item.get("word", "") or len(item["word"].split()) <= 2]
    except Exception as e:
        logger.warning(f"Datamuse API fetch failed for {keyword}: {e}")
    return []


def enrich_destination_data(destination: str) -> Dict[str, Any]:
    """Orchestrate all free public APIs to produce a verified geo & environmental profile."""
    profile = {
        "destination": destination,
        "geocoding": None,
        "heritage_facts": None,
        "climate": None,
        "solar_timings": None,
        "lsi_keywords": []
    }
    
    geo = geocode_location(destination)
    if geo:
        profile["geocoding"] = geo
        profile["climate"] = fetch_climate_and_weather(geo["lat"], geo["lon"])
        profile["solar_timings"] = fetch_solar_timings(geo["lat"], geo["lon"])
        
    city_name = destination.split(",")[0].strip()
    profile["heritage_facts"] = fetch_spiritual_heritage_facts(city_name)
    profile["lsi_keywords"] = fetch_semantic_lsi_keywords(city_name)
    
    return profile

