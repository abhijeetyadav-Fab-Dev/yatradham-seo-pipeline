import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from ai_seo_audit import run_ai_seo_audit, auto_heal_content
from schema_generator import generate_blog_json_ld, generate_json_ld

client = TestClient(app)


def test_ai_seo_audit_15_signals():
    """Verify that run_ai_seo_audit executes all 15 audit dimensions cleanly."""
    title = "Dwarka Temple Darshan Booking & Aarti Timings | YatraDham"
    meta = "Book verified Dwarka Temple Darshan with YatraDham.Org. Complete Aarti timings, VIP passes, clean dharamshala rooms & satvik meals. Reserve your slot now!"
    keyword = "Dwarka Temple Darshan"
    
    content = """
    ## Sacred Sanctum Darshan & Aarti Overview
    Dwarka Temple Darshan offers devotees a direct spiritual encounter with Lord Krishna at the sacred Jagat Mandir. Morning Mangala Aarti starts at 6:30 AM every day.

    Devotees should plan their visits carefully. Queues can be long during festival seasons. Clean ashrams and dharamshalas are available near the temple gate. Distance from the railway station is 3 km.

    ## Verified Pricing and Booking Details
    | Service Category | Standard Price (INR) | VIP Fast-Track |
    | :--- | :--- | :--- |
    | General Sanctum Entry | Free / Nil | ₹100 – ₹250 |
    | Special Sankalp Puja | ₹501 – ₹1,100 | ₹2,100 |

    For verified room reservations, visit https://yatradham.org/.
    """

    audit = run_ai_seo_audit(
        title=title,
        meta_description=meta,
        primary_keyword=keyword,
        content_body=content,
        pricing_str="₹501"
    )

    assert audit["score"] >= 80, f"Expected audit score >= 80, got {audit['score']}"
    assert audit["status"] in ["EXCELLENT", "GOOD"]
    assert audit["audit_grade"] in ["A+", "A", "B+"]
    assert len(audit["checks"]) == 15, f"Expected 15 checks, got {len(audit['checks'])}"
    assert audit["geo_visibility"]["geo_ready"] is True
    assert audit["geo_visibility"]["has_inr_pricing"] is True
    assert audit["geo_visibility"]["has_answer_first"] is True


def test_ai_seo_audit_auto_heal():
    """Verify that auto_heal_content strips robotic clichés, replaces em-dashes, and heals formatting."""
    sloppy_content = "This sacred temple serves as a testament to faith — delving into rich tapestries — not only for peace, but also for joy."
    healed = auto_heal_content(sloppy_content, voice="warm")

    assert "—" not in healed, "Em-dashes should be eradicated"
    assert "testament to" not in healed, "'testament to' cliché should be removed"
    assert "delving into" not in healed, "'delving into' cliché should be removed"
    assert "serves as a" not in healed, "'serves as a' should be replaced"


def test_ai_audit_fastapi_endpoint():
    """Verify GET and POST /api/seo/ai-audit endpoints return valid audit reports."""
    payload = {
        "title": "Kedarnath Yatra Tour Package & Helicopter Booking | YatraDham",
        "meta_description": "Book verified Kedarnath Yatra Tour Package with YatraDham.Org. Helicopter transfers, clean camps, pure satvik food & guided darshan. Book now!",
        "primary_keyword": "Kedarnath Yatra",
        "content": """## Sacred Himalayan Kedarnath Yatra Overview
Kedarnath Yatra provides pilgrims with a sacred Himalayan trek. Daily helicopter transfers operate from Phata starting at 6:30 AM each morning.

## Package Inclusions and Pricing Details
| Package Option | Price (INR) | Helicopter Service |
| :--- | :--- | :--- |
| Standard Trek | ₹9,500 | Not Included |
| VIP Helicopter Package | ₹19,500 | Included |

Distance from Haridwar railway station is approximately 220 km. Reserve verified stays on https://travel.yatradham.org/.""",
        "pricing": "₹9,500"
    }

    res = client.post("/api/seo/ai-audit", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "audit" in data
    assert data["audit"]["score"] >= 65
    assert len(data["audit"]["checks"]) == 15


def test_blog_and_package_schema_validity():
    """Verify JSON-LD schema generation for both packages and blog articles."""
    # 1. Blog JSON-LD
    blog_schema = generate_blog_json_ld(
        title="Somnath Temple Aarti Timings 2026",
        meta_description="Complete guide to Somnath Temple Darshan and morning aarti.",
        canonical_url="https://yatradham.org/blog/somnath-temple-aarti-timings",
        primary_keyword="Somnath Temple Aarti",
        date_published="2026-03-15",
        word_count=1200
    )
    assert blog_schema["@context"] == "https://schema.org"
    assert blog_schema["@graph"][0]["@type"] == "BlogPosting"
    assert blog_schema["@graph"][0]["headline"] == "Somnath Temple Aarti Timings 2026"

    # 2. Package Tour JSON-LD
    tour_schema = generate_json_ld(
        product_type="tour",
        name="Chardham Yatra 10 Days Package",
        description="Comprehensive 10-day Chardham Yatra by road.",
        destination="Haridwar, Uttarakhand",
        price=18500,
        currency="INR"
    )
    assert tour_schema["@context"] == "https://schema.org"
    assert tour_schema["@graph"][0]["@type"] == "TouristTrip"
    assert tour_schema["@graph"][0]["offers"]["price"] == "18500"
