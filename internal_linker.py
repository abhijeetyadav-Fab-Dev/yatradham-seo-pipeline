"""Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem."""
import re
from typing import Dict, Any, List


# Knowledge base of high-authority YatraDham subdomains and hubs
DESTINATION_LINK_MATRIX = {
    "rishikesh": [
        {
            "anchor_text": "Verified Dharamshalas & Ashram Stays in Rishikesh",
            "target_url": "https://yatradham.org/rishikesh",
            "subdomain": "yatradham.org",
            "context_description": "Clean, affordable pilgrim rooms with satvik food near Triveni Ghat & Ram Jhula."
        },
        {
            "anchor_text": "Ganga Aarti & Special Puja Booking in Rishikesh",
            "target_url": "https://temple.yatradham.org/pujas",
            "subdomain": "temple.yatradham.org",
            "context_description": "Book authorized Vedic pandits for Triveni Ghat Ganga Aarti and sacred rituals."
        },
        {
            "anchor_text": "Haridwar & Rishikesh 3-Day Sightseeing Tour Packages",
            "target_url": "https://travel.yatradham.org/haridwar-rishikesh-tour-package",
            "subdomain": "travel.yatradham.org",
            "context_description": "Complete guided yatra covering Mansa Devi, Chandi Devi, and Parmarth Niketan."
        }
    ],
    "haridwar": [
        {
            "anchor_text": "Dharamshala Booking near Har Ki Pauri, Haridwar",
            "target_url": "https://yatradham.org/haridwar",
            "subdomain": "yatradham.org",
            "context_description": "Verified ashram accommodation within walking distance of holy Ganga ghats."
        },
        {
            "anchor_text": "Har Ki Pauri Special Ganga Aarti & Pind Daan Booking",
            "target_url": "https://temple.yatradham.org/pujas",
            "subdomain": "temple.yatradham.org",
            "context_description": "Authorized Pandit Ji services for ancestral rituals and evening Ganga Aarti."
        },
        {
            "anchor_text": "Chardham Yatra Departure Packages from Haridwar",
            "target_url": "https://yatradham.org/chardham-package",
            "subdomain": "travel.yatradham.org",
            "context_description": "Comfortable 10-day luxury tempo traveller and helicopter yatra packages."
        }
    ],
    "chardham": [
        {
            "anchor_text": "GMVN TRH Guest House & Dharamshala Booking on Chardham Route",
            "target_url": "https://yatradham.org/chardham-stay",
            "subdomain": "yatradham.org",
            "context_description": "Official government and verified private stays in Barkot, Guptkashi, and Badrinath."
        },
        {
            "anchor_text": "Kedarnath & Badrinath Special Online Puja Booking",
            "target_url": "https://temple.yatradham.org/pujas",
            "subdomain": "temple.yatradham.org",
            "context_description": "Perform Rudrabhishek at Kedarnath and Maha Abhishek at Badrinath temple."
        },
        {
            "anchor_text": "Chardham Yatra Helicopter & Tempo Packages",
            "target_url": "https://yatradham.org/chardham-package",
            "subdomain": "travel.yatradham.org",
            "context_description": "All-inclusive packages with VIP darshan passes and Satvik food."
        }
    ],
    "vrindavan": [
        {
            "anchor_text": "Verified Dharamshalas & Bhavans in Vrindavan & Barsana",
            "target_url": "https://yatradham.org/mathura-vrindavan",
            "subdomain": "yatradham.org",
            "context_description": "Clean AC/Non-AC rooms near Banke Bihari Temple and Prem Mandir."
        },
        {
            "anchor_text": "Banke Bihari Special Puja & Braj Darshan Services",
            "target_url": "https://temple.yatradham.org/pujas",
            "subdomain": "temple.yatradham.org",
            "context_description": "Guided Chappan Bhog and Mangala Aarti darshan support."
        },
        {
            "anchor_text": "2-Day Vrindavan, Mathura & Barsana Tour Package",
            "target_url": "https://travel.yatradham.org/2-days-vrindavan-barsana-tour-package",
            "subdomain": "travel.yatradham.org",
            "context_description": "Complete Braj 84 Kos sightseeing with private dedicated cab."
        }
    ],
    "kerala": [
        {
            "anchor_text": "Authentic Ayurvedic Rejuvenation & Panchakarma in Kerala",
            "target_url": "https://wellness.yatradham.org/ayurvedic-rejuvenation-massage-wellness-retreat-kerala",
            "subdomain": "wellness.yatradham.org",
            "context_description": "Doctor-guided detox therapies, Shirodhara, and herbal nutrition."
        },
        {
            "anchor_text": "Guruvayur & Padmanabhaswamy Temple Darshan Stays",
            "target_url": "https://yatradham.org/kerala",
            "subdomain": "yatradham.org",
            "context_description": "Verified pilgrim accommodation with traditional South Indian Satvik meals."
        }
    ],
    "default": [
        {
            "anchor_text": "Search 1000+ Verified Dharamshalas Across India",
            "target_url": "https://yatradham.org",
            "subdomain": "yatradham.org",
            "context_description": "India's trusted religious accommodation booking platform."
        },
        {
            "anchor_text": "Book Authorized Pandit Ji & Temple Pujas Online",
            "target_url": "https://temple.yatradham.org/pujas",
            "subdomain": "temple.yatradham.org",
            "context_description": "Perform Vedic rituals with live streaming and doorstep prasadam."
        },
        {
            "anchor_text": "Explore All-Inclusive Yatra & Tour Packages",
            "target_url": "https://travel.yatradham.org",
            "subdomain": "travel.yatradham.org",
            "context_description": "Pilgrimage and wellness vacation packages with verified amenities."
        }
    ]
}


def get_smart_internal_links(destination: str, category: str, current_url: str = "") -> List[Dict[str, str]]:
    """Return contextual internal links filtered to avoid linking to the current page itself."""
    dest_lower = (destination or "").lower()
    matched_key = "default"
    for k in DESTINATION_LINK_MATRIX:
        if k in dest_lower:
            matched_key = k
            break

    links = DESTINATION_LINK_MATRIX.get(matched_key, DESTINATION_LINK_MATRIX["default"])
    
    # Filter out current URL if already matches
    result = []
    for link in links:
        if current_url and current_url.rstrip("/") in link["target_url"]:
            continue
        result.append(link)
    
    if len(result) < 2 and matched_key != "default":
        for def_link in DESTINATION_LINK_MATRIX["default"]:
            if def_link not in result:
                result.append(def_link)
                if len(result) >= 3:
                    break

    return result[:4]
