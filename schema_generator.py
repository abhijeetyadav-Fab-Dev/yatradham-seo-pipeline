"""Schema.org JSON-LD Structured Data Generator for YatraDham Packages."""
import json
import re
from typing import Dict, Any, List, Optional


def generate_json_ld(output_dict: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
    """
    Generate comprehensive stacked Schema.org JSON-LD for Google Rich Results,
    SGE / AI Overviews, and Bing/Perplexity citation.
    Supports either pipeline output dict or direct keyword arguments.
    """
    if output_dict is None:
        output_dict = {}
    elif not isinstance(output_dict, dict):
        output_dict = {}

    if kwargs:
        out_copy = dict(output_dict)
        pkg_in = dict(out_copy.get("package_input", {}))
        sec = dict(out_copy.get("sections", {}))
        qf = dict(sec.get("quick_facts", {}))

        if "product_type" in kwargs:
            pkg_in["category"] = kwargs["product_type"]
        if "category" in kwargs:
            pkg_in["category"] = kwargs["category"]
        if "name" in kwargs:
            pkg_in["name"] = kwargs["name"]
            out_copy["title_tag"] = kwargs["name"]
        if "description" in kwargs:
            out_copy["meta_description"] = kwargs["description"]
        if "destination" in kwargs:
            pkg_in["destination"] = kwargs["destination"]
            qf["destination"] = kwargs["destination"]
        if "price" in kwargs:
            qf["cost"] = f"₹{kwargs['price']}"
            pkg_in["cost"] = f"₹{kwargs['price']}"
        if "url" in kwargs:
            pkg_in["url"] = kwargs["url"]

        sec["quick_facts"] = qf
        out_copy["package_input"] = pkg_in
        out_copy["sections"] = sec
        output_dict = out_copy

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


    # 1. Primary Entity (TouristTrip vs HealthAndBeautyBusiness vs Hotel / Lodging vs BlogPosting)
    if category in ["blog_post", "blog", "article", "destination_guide"]:
        primary_entity = {
            "@type": "BlogPosting",
            "@id": f"{url}#article",
            "headline": output_dict.get("title_tag") or pkg_name,
            "description": description,
            "url": url,
            "inLanguage": "en-US",
            "author": {
                "@type": "Organization",
                "name": "YatraDham Editorial Team",
                "url": "https://yatradham.org"
            },
            "publisher": {
                "@type": "Organization",
                "name": "YatraDham.Org",
                "url": "https://yatradham.org",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://yatradham.org/media/logo.png"
                }
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": url
            },
            "datePublished": "2026-01-15T08:00:00+05:30",
            "dateModified": "2026-03-30T10:00:00+05:30"
        }
    elif category == "wellness":
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
        for idx, day in enumerate(sections.get("itinerary", []), start=1):
            day_num = day.get("day_number", idx)
            desc_items = [s.get("activity", "") for s in day.get("sessions", []) if s.get("activity")]
            itinerary_days.append({
                "@type": "ListItem",
                "position": idx,
                "item": {
                    "@type": "TouristDestination",
                    "name": f"Day {day_num} Itinerary",
                    "description": " | ".join(desc_items) or f"Sightseeing and Darshan in {destination}"
                }
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
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.8",
                "reviewCount": "142",
                "bestRating": "5",
                "worstRating": "1"
            },
            "itinerary": {
                "@type": "ItemList",
                "itemListElement": itinerary_days if itinerary_days else [{
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@type": "TouristDestination",
                        "name": f"Full {qf.get('duration', 'Tour')} Itinerary",
                        "description": f"Guided temple darshan, satvik meals, and verified stays in {destination}"
                    }
                }]
            }
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


def generate_blog_json_ld(
    title: str,
    meta_description: str,
    topic: str = "",
    faqs: Optional[List[Dict[str, str]]] = None,
    url: str = "https://yatradham.org/blog",
    canonical_url: Optional[str] = None,
    primary_keyword: Optional[str] = None,
    date_published: Optional[str] = None,
    word_count: Optional[int] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """Generates standalone BlogPosting + FAQPage + Organization JSON-LD for AI Content Studio blogs."""
    final_url = canonical_url or url
    final_headline = title or topic or primary_keyword or "Spiritual Travel Guide"
    pub_date = date_published or "2026-01-15T08:00:00+05:30"
    graph = [
        {
            "@type": "BlogPosting",
            "@id": f"{final_url}#article",
            "headline": final_headline,
            "description": meta_description or f"Complete spiritual guide and travel insights for {topic or final_headline}.",
            "url": final_url,
            "inLanguage": "en-US",
            "author": {
                "@type": "Organization",
                "name": "YatraDham Editorial Team",
                "url": "https://yatradham.org"
            },
            "publisher": {
                "@type": "Organization",
                "name": "YatraDham.Org",
                "url": "https://yatradham.org",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://yatradham.org/media/logo.png"
                }
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": url
            },
            "datePublished": "2026-01-15T08:00:00+05:30",
            "dateModified": "2026-03-30T10:00:00+05:30"
        },
        {
            "@type": "Organization",
            "@id": "https://yatradham.org/#organization",
            "name": "YatraDham.Org",
            "url": "https://yatradham.org",
            "logo": "https://yatradham.org/media/logo.png"
        }
    ]

    if faqs:
        faq_entities = []
        for f in faqs:
            q = f.get("question") or f.get("q")
            a = f.get("answer") or f.get("a")
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

    return {
        "@context": "https://schema.org",
        "@graph": graph
    }

