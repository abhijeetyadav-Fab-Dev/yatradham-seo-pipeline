"""Schema.org JSON-LD Structured Data Generator for YatraDham Packages."""
import json
import re
from typing import Dict, Any, List


def generate_json_ld(output_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive stacked Schema.org JSON-LD for Google Rich Results,
    SGE / AI Overviews, and Bing/Perplexity citation.
    """
    pkg_input = output_dict.get("package_input", {})
    sections = output_dict.get("sections", {})
    qf = sections.get("quick_facts", {})
    
    url = pkg_input.get("url") or "https://yatradham.org"
    pkg_name = output_dict.get("title_tag") or pkg_input.get("name") or "Spiritual Package"
    destination = qf.get("destination") or pkg_input.get("destination") or "India"
    category = pkg_input.get("category") or "tour"
    description = output_dict.get("meta_description") or sections.get("package_overview") or ""
    
    cost_str = qf.get("cost") or pkg_input.get("cost") or ""
    price_digits = re.findall(r'[\d,]+(?:\.\d{2})?', cost_str)
    price_val = price_digits[0].replace(",", "") if price_digits else ""
    
    graph: List[Dict[str, Any]] = []


    # 1. Primary Entity (TouristTrip vs HealthAndBeautyBusiness vs Hotel / Lodging)
    if category == "wellness":
        primary_entity = {
            "@type": ["HealthAndBeautyBusiness", "LodgingBusiness"],
            "@id": f"{url}#wellness-center",
            "name": qf.get("center_name") or f"Wellness Retreat in {destination}",
            "description": description,
            "url": url,
            "telephone": "+919484950060",
            "email": "info@wellness.yatradham.org",
            "priceRange": f"₹{price_val} per night",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": destination,
                "addressCountry": "IN"
            },
            "makesOffer": {
                "@type": "Offer",
                "name": pkg_name,
                "price": price_val,
                "priceCurrency": "INR",
                "availability": "https://schema.org/InStock",
                "url": url
            }
        }
    elif category == "stay":
        primary_entity = {
            "@type": "Hotel",
            "@id": f"{url}#lodging",
            "name": pkg_input.get("name") or f"Dharamshala in {destination}",
            "description": description,
            "url": url,
            "telephone": "+919484950060",
            "priceRange": f"₹{price_val} per room/night",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": destination,
                "addressCountry": "IN"
            },
            "checkinTime": "12:00:00",
            "checkoutTime": "12:00:00",
            "makesOffer": {
                "@type": "Offer",
                "name": pkg_name,
                "price": price_val,
                "priceCurrency": "INR",
                "availability": "https://schema.org/InStock",
                "url": url
            }
        }
    elif category == "puja":
        primary_entity = {
            "@type": "Service",
            "@id": f"{url}#puja-service",
            "name": pkg_input.get("name") or f"Online Puja & Pandit in {destination}",
            "description": description,
            "url": url,
            "provider": {
                "@type": "Organization",
                "name": "YatraDham.Org",
                "url": "https://temple.yatradham.org"
            },
            "offers": {
                "@type": "Offer",
                "price": price_val,
                "priceCurrency": "INR",
                "availability": "https://schema.org/InStock",
                "url": url
            }
        }
    else:  # Tour / Yatra Package
        itinerary_days = []
        for day in sections.get("itinerary", []):
            day_num = day.get("day_number", 1)
            desc_items = [s.get("activity", "") for s in day.get("sessions", []) if s.get("activity")]
            itinerary_days.append({
                "@type": "TouristAttraction",
                "name": f"Day {day_num} Itinerary",
                "description": " | ".join(desc_items) or f"Sightseeing and Darshan in {destination}"
            })

        primary_entity = {
            "@type": "TouristTrip",
            "@id": f"{url}#trip",
            "name": pkg_name,
            "description": description,
            "url": url,
            "touristType": ["Pilgrims", "Families", "Spiritual Seekers"],
            "offers": {
                "@type": "Offer",
                "price": price_val,
                "priceCurrency": "INR",
                "availability": "https://schema.org/InStock",
                "url": url
            },
            "itinerary": itinerary_days if itinerary_days else [{
                "@type": "TouristAttraction",
                "name": f"Full {qf.get('duration', 'Tour')} Itinerary",
                "description": f"Guided temple darshan, satvik meals, and verified stays in {destination}"
            }]
        }

    graph.append(primary_entity)

    # 2. FAQPage Schema
    faqs = sections.get("faq", [])
    if faqs:
        faq_entities = []
        for item in faqs:
            q = item.get("question") or item.get("q") or ""
            a = item.get("answer") or item.get("a") or ""
            if q and a:
                faq_entities.append({
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a
                    }
                })
        if faq_entities:
            graph.append({
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "mainEntity": faq_entities
            })

    # 3. BreadcrumbList Schema
    cat_title = category.title() if category != "wellness" else "Wellness & Yoga Retreats"
    graph.append({
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://yatradham.org"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": cat_title,
                "item": f"https://yatradham.org/{category}"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": destination,
                "item": url
            }
        ]
    })

    # 4. Organization Schema (YatraDham)
    graph.append({
        "@type": "Organization",
        "@id": "https://yatradham.org/#organization",
        "name": "YatraDham.Org",
        "url": "https://yatradham.org",
        "logo": "https://yatradham.org/media/logo.png",
        "sameAs": [
            "https://www.facebook.com/yatradhamorg",
            "https://www.instagram.com/yatradhamorg",
            "https://twitter.com/yatradhamorg"
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+919484950060",
            "contactType": "Customer Support",
            "areaServed": "IN",
            "availableLanguage": ["en", "hi", "gu"]
        }
    })

    return {
        "@context": "https://schema.org",
        "@graph": graph
    }
