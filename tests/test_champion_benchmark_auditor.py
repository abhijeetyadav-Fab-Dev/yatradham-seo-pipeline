"""
Unit & Integration Tests for Champion Blog Benchmark & Checkpoint Auditor
Validates that content is rigorously audited against the Ro-Pax Ghogha-Hazira gold standard.
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from champion_benchmark_auditor import audit_champion_blog_benchmarks, ROPAX_CHAMPION_PROFILE
from agents.content_creator_agent import _detect_blog_intent, _get_intent_structure
from ai_seo_audit import run_ai_seo_audit
from main import app

client = TestClient(app)

SAMPLE_CHAMPION_BLOG = """
# RoRo Ferry Service Ghogha to Hazira Timings and Ticket Price

The much-awaited Ro-Pax Ferry service connects Ghogha (near Bhavnagar) and Hazira (in Surat).
Traveling by road between Surat and Bhavnagar takes over 12 hours covering 394 km. 
The RoRo ferry saves 370 km and cuts travel time down to just 4 hours across a 90 km sea route.

## Everyday Two Trip Timetable
| Trip Route | Morning Departure | Evening Departure | Reporting Deadline |
|---|---|---|---|
| Ghogha to Hazira | 08:00 AM | 05:00 PM | 1 Hour Prior |
| Hazira to Ghogha | 09:00 AM | 04:00 PM | 1 Hour Prior |

## Passenger Class Ticket Price
| Travel Class | Ticket Fare (INR) | Luggage Limit |
|---|---|---|
| Executive Class | ₹600 per seat | Up to 15 kg |
| Business Class | ₹700 per seat | Up to 20 kg |
| Sleeper Class | ₹700 per seat | Up to 20 kg |
| Cambay Lounge | ₹1,700 per seat | Up to 25 kg |

## Vehicle Carriage Tariffs
| Vehicle Category | Tariff (INR) | Carriage Note |
|---|---|---|
| Two-Wheeler / Bike | ₹200 | Per bike (driver seat separate) |
| Four-Wheeler / Car | ₹1,300 | Per car (driver seat separate) |
| Tempo Traveller | ₹3,000 | Commercial permit required |
| Heavy Truck | ₹3,000 | Gross weight up to 3 tonnes |

## Connecting Bus Service
GSRTC operates direct connecting bus services between Bhavnagar Bus Station and Ghogha Ferry Terminal with a ticket fare of just ₹23. In Surat, buses run from Adajan Bus Station to Hazira Terminal.

## Onward Pilgrimage Destinations
| Destination | Distance from Ghogha | Sacred Highlights |
|---|---|---|
| Palitana Temples | 70 km away | Shatrunjaya Hill Jain Temples |
| Somnath Temple | 260 km away | First of the 12 Sacred Jyotirlingas |
| Sarangpur Hanuman Mandir | 98 km away | Kashtbhanjan Dev Temple |
| Dwarka Temple | 408 km away | Dwarkadhish Jagat Mandir |

## Places to Stay & Dharamshala Bookings
Book your stay in Somnath and verified dharamshalas near Dwarka and Palitana via [YatraDham.Org](https://yatradham.org/). YatraDham offers verified family rooms, hot water facilities, and satvik food. Download the YatraDham App for instant booking.

## Cancellation, Refund & Weather Rules
- 30 days before date of journey: 90% refund
- Between 2 and 30 days before: 60% refund
- Same day / <24 hours: no refund
In case of weather disruptions or Gujarat Maritime Board (GMB) alerts, a 100% refund is issued.

## Frequently Asked Questions
### Q1: What is the distance saved by the Ro-Pax ferry?
The ferry saves 370 km by road and reduces a 12-hour journey to just 4 hours by sea.

### Q2: Can passengers sit inside the car during transit?
No, passengers must move to the designated AC passenger decks during the sea voyage.

### Q3: Are pets allowed on the ferry?
No, pets and domestic animals are strictly prohibited on the Ro-Pax vessel.

### Q4: Is overnight parking available at Hazira terminal?
Yes, overnight parking facility is available for private cars at both terminals.

### Q5: How can I book verified dharamshalas near Bhavnagar and Somnath?
You can book clean, verified rooms through YatraDham.Org with instant confirmation.

### Q6: Can a tempo traveller travel on the RoRo ferry?
Yes, tempo travellers can board at ₹3,000 vehicle fare.
"""


def test_champion_blog_benchmarks_high_score():
    """Verify that a comprehensive, structured blog achieves a high Champion score."""
    report = audit_champion_blog_benchmarks(
        content=SAMPLE_CHAMPION_BLOG,
        title="RoRo Ferry Service Ghogha to Hazira Timings and Ticket Price",
        meta_description="RoRo Ferry Service from Ghogha to Hazira timetable, passenger ticket price, vehicle fare and online booking guide.",
        target_keyword="RoRo Ferry Service Ghogha to Hazira"
    )
    assert report["champion_score"] >= 85.0
    assert report["passed_checkpoints"] >= 7
    assert report["total_checkpoints"] == 10


def test_champion_blog_benchmarks_superficial_content():
    """Verify that superficial content with no tables, math, or fares fails."""
    weak_content = "This is a short post about a ferry. It runs between two cities. It is very nice. Come visit."
    report = audit_champion_blog_benchmarks(
        content=weak_content,
        title="Ferry Service",
        meta_description="Ferry service info."
    )
    assert report["champion_score"] < 50.0
    assert report["verdict"] in ["SUPERFICIAL_AT_RISK", "AVERAGE_INFORMATIONAL_GUIDE"]
    assert len(report["recommendations"]) >= 3


def test_champion_benchmark_api_endpoints():
    """Verify FastAPI champion audit and champion profile endpoints."""
    # Test profile endpoint
    profile_res = client.get("/api/blog/champion-profile")
    assert profile_res.status_code == 200
    pdata = profile_res.json()
    assert pdata["success"] is True
    assert "champion_profile" in pdata
    assert pdata["champion_profile"]["tables_count"] == 14

    # Test audit endpoint
    audit_res = client.post("/api/blog/champion-audit", json={
        "content": SAMPLE_CHAMPION_BLOG,
        "title": "RoRo Ferry Service Ghogha to Hazira",
        "target_keyword": "RoRo Ferry"
    })
    assert audit_res.status_code == 200
    adata = audit_res.json()
    assert adata["success"] is True
    assert "champion_score" in adata
    assert "checkpoints" in adata
    assert len(adata["checkpoints"]) == 10


def test_ai_seo_audit_integration_champion_score():
    """Verify that run_ai_seo_audit includes champion_benchmark in its output."""
    audit_result = run_ai_seo_audit(
        title="RoRo Ferry Service Ghogha to Hazira",
        meta_description="RoRo Ferry Service from Ghogha to Hazira timetable, passenger ticket price, vehicle fare and online booking guide.",
        primary_keyword="RoRo Ferry",
        content_body=SAMPLE_CHAMPION_BLOG,
        pricing_str="₹600 - ₹3,000"
    )
    assert "champion_benchmark" in audit_result
    assert "champion_score" in audit_result["metrics"]
    assert audit_result["metrics"]["champion_score"] > 80.0


def test_transit_intent_detection():
    """Verify intent detector routes ferry and transit queries to transit_logistics_champion."""
    intent1 = _detect_blog_intent("Ro-Pax Ferry Service from Ghogha to Hazira Timetable and Fare")
    assert intent1 == "transit_logistics_champion"

    intent2 = _detect_blog_intent("Kedarnath Helicopter Service Booking and Ticket Price")
    assert intent2 == "transit_logistics_champion"

    struct = _get_intent_structure("transit_logistics_champion", "Ro-Pax Ferry", "Ro-Pax Ferry")
    assert "Service Overview & Traveler Transformation Math" in struct
    assert "Vehicle Transportation Tariffs" in struct
    assert "Connecting Public Transit" in struct
