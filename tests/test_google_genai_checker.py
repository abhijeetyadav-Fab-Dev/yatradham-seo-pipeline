"""
Tests for Google Generative AI Content Compliance Checker
=========================================================
Verifies implementation of Google Search Central guidance:
https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from google_genai_checker import (
    audit_google_genai_compliance,
    inject_google_compliance_disclosure,
    check_scaled_content_abuse,
    check_factual_accuracy_and_hallucinations,
    check_transparency_who_how_why
)

client = TestClient(app)


def test_google_genai_compliant_content():
    """Verify that a high-quality, transparent, fact-checked pilgrimage guide receives top compliance score."""
    title = "3 Days Somnath Temple Darshan & Tour Package | YatraDham.Org"
    meta = "Explore the verified 3 Days Somnath Temple Tour Package with YatraDham.Org. Daily Aarti timings, clean ashram rooms, satvik meals & verified cab transfers."
    content = """# 3 Days Somnath Temple Pilgrimage Guide & Darshan Package
By YatraDham Editorial Team

Editorial Disclosure: This guide was researched and drafted with AI assistance for structural clarity and comprehensively fact-checked, reviewed, and verified by the YatraDham.Org Editorial Team to ensure 100% accuracy, authentic local timings, and verified pilgrim hospitality standards.

## Sacred Sanctum Darshan & Aarti Schedule
Somnath Temple is the first among the twelve sacred Jyotirlinga shrines of Lord Shiva. Morning Mangala Aarti begins promptly at 7:00 AM, followed by Afternoon Bhog Aarti at 12:00 PM and the grand Sandhya Aarti at 7:00 PM. The famous Sound and Light Show takes place between 8:00 PM and 9:00 PM against the Arabian Sea backdrop.

## Day-by-Day Route Itinerary
Day 1: Arrive at Veraval Railway Station (6 km from temple). Transfer to verified YatraDham Dharamshala near the temple gate. Attend evening Sandhya Aarti.
Day 2: Early morning temple darshan, Bhalka Tirth visit, and Triveni Sangam holy snan.
Day 3: Check out by 11:00 AM after morning prayers and depart comfortably.

## Real Logistics & Tariffs (in INR)
| Room Category | Tariff per Night | Inclusions |
| :--- | :--- | :--- |
| Standard AC Room | ₹1,200 – ₹1,800 | Hot water, 24/7 check-in, parking |
| Family Suite (4 Bed) | ₹2,200 – ₹3,200 | Attached bath, elevator, Satvik bhojanalaya |

## Temple Protocols & Devotee Guidelines
Devotees should deposit mobile phones and footwear at the official cloakroom counters at Gate 2. Men must wear traditional dhotis or formal trousers, while women are requested to wear sarees or salwar suits.
    """

    res = audit_google_genai_compliance(
        content=content,
        title=title,
        meta_description=meta,
        author="YatraDham Editorial Team",
        methodology_disclosure="Drafted with AI assistance and fact-checked by YatraDham editors.",
        json_ld_schema={"@type": "TouristTrip", "name": "Somnath Tour"},
        pricing_str="₹1,200"
    )

    assert res["score"] >= 85, f"Expected score >= 85, got {res['score']}"
    assert res["grade"] in ["A+", "A"]
    assert res["verdict"] == "COMPLIANT_HIGH_QUALITY"
    assert res["status"] == "PASSED"
    assert len(res["checks"]) == 6
    assert res["transparency"]["who_verified"] is True
    assert res["transparency"]["how_verified"] is True
    assert res["transparency"]["why_people_first"] is True
    assert not res["hallucination_indicators"]["has_hallucinations"]


def test_google_genai_hallucination_and_placeholder_detection():
    """Verify that unresolved AI placeholder tokens trigger hallucination alerts."""
    content = "Welcome to [city]. The price for staying at [hotel] is [price]. Contact [phone number] for booking details."
    score, status, findings, hallucinations = check_factual_accuracy_and_hallucinations(
        content, title="Trip Guide", meta_description="Trip description"
    )

    assert len(hallucinations) >= 3
    assert status in ["WARNING", "FAILED"]
    assert any("[city]" in h for h in hallucinations)
    assert any("[hotel]" in h for h in hallucinations)


def test_google_genai_missing_context_transparency():
    """Verify that lack of 'Who' and 'How' context transparency triggers appropriate recommendations."""
    raw_content = "This is a generic travel article about temples. You can visit and enjoy the place. Keep walking and taking photos."
    score, status, findings, summary = check_transparency_who_how_why(raw_content)

    assert summary["who_verified"] is False
    assert summary["how_verified"] is False
    assert score < 16
    assert any("Who" in f for f in findings)
    assert any("How" in f for f in findings)


def test_google_genai_inject_disclosure():
    """Verify that inject_google_compliance_disclosure adds the compliant editorial disclosure."""
    content = "## Kedarnath Yatra Guide\n\nKedarnath temple is located in Rudraprayag district."
    healed = inject_google_compliance_disclosure(content, author_name="YatraDham Editorial Team")

    assert "Editorial Integrity & Transparency Note" in healed
    assert "Google Search Essentials Compliance" in healed
    assert "YatraDham Editorial Team" in healed
    
    # Running audit on the healed content should now detect 'How' methodology
    res = audit_google_genai_compliance(content=healed, title="Kedarnath Guide")
    assert res["transparency"]["how_verified"] is True


def test_google_genai_fastapi_endpoints():
    """Verify FastAPI routes /api/check-google-genai and /api/google-genai/inject-disclosure."""
    # 1. Check compliance endpoint
    payload = {
        "title": "2 Days Haridwar Yatra Package | YatraDham.Org",
        "meta_description": "Verified 2 days Haridwar tour package with Ganga aarti darshan, clean dharamshala rooms, and private transfers on YatraDham.Org.",
        "content": """# 2 Days Haridwar Yatra
By YatraDham Editorial Team
Editorial Disclosure: Researched with AI assistance and fact-checked by local pilgrim guides.
Morning Aarti is at 6:00 AM. Distance from station is 2 km. Room tariff is ₹800 per night.
Devotees can book verified stays on YatraDham.Org.""",
        "author": "YatraDham Editorial Team"
    }
    resp = client.post("/api/check-google-genai", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "score" in data
    assert "verdict" in data
    assert "policy_citation" in data

    # 2. Inject disclosure endpoint
    resp_inj = client.post("/api/google-genai/inject-disclosure", json={"content": "Brief temple summary."})
    assert resp_inj.status_code == 200
    inj_data = resp_inj.json()
    assert inj_data["success"] is True
    assert "Editorial Integrity" in inj_data["content"]
