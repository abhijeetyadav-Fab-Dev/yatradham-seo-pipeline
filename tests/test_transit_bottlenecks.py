"""
Unit & Integration Tests for High-Intent Pilgrimage Transit Bottlenecks Engine & Guardrails
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transit_bottleneck_engine import (
    get_all_bottlenecks,
    find_bottleneck_by_id,
    calculate_bottleneck_intensity,
    generate_transit_champion_blueprint,
    validate_transit_bottleneck_guardrails
)
from main import app

client = TestClient(app)


def test_transit_bottleneck_catalog_integrity():
    catalog = get_all_bottlenecks()
    assert len(catalog) >= 8
    
    # Verify mandatory fields on each bottleneck
    for b in catalog:
        assert "id" in b
        assert "name" in b
        assert "transformation_math" in b
        assert "ticket_fares" in b
        assert len(b["ticket_fares"]["passenger"]) > 0
        assert "connecting_transit" in b
        assert len(b["onward_spokes"]) >= 3
        assert "scam_alert_warning" in b
        assert "operational_rules" in b


def test_calculate_bottleneck_intensity():
    # Test extreme bottleneck (Kedarnath helicopter)
    res_kedar = calculate_bottleneck_intensity("Kedarnath Helicopter booking from Phata and Sirsi", time_saved_hours=9.0, has_steep_climb=True)
    assert res_kedar["intensity_score"] >= 80.0
    assert res_kedar["serp_opportunity"] == "EXTREME_BOTTLENECK_SERP_GOLDMINE"
    assert "time_savings_impact" in res_kedar["friction_breakdown"]

    # Test standard moderate route
    res_std = calculate_bottleneck_intensity("Local auto rickshaw to temple", time_saved_hours=0.5)
    assert res_std["intensity_score"] < 70.0


def test_generate_transit_champion_blueprint():
    bp = generate_transit_champion_blueprint("girnar_ropeway")
    assert bp["success"] is True
    assert "Girnar Ropeway" in bp["title"]
    assert bp["structured_tables_count"] >= 3
    assert bp["onward_spokes_count"] >= 3
    
    md = bp["markdown_content"]
    assert "Official Timetable & Operating Slots" in md
    assert "Class-Wise Passenger Ticket Fares" in md
    assert "YatraDham.Org" in md
    assert "Frequently Asked Questions" in md
    assert "### Q1" in md


def test_validate_transit_bottleneck_guardrails():
    # Compliant content with all 6 guardrail rules
    compliant_md = """
    # Kedarnath Helicopter Booking
    Saves 16 km steep trek and cuts 9 hours walk down to 8 minutes flight.
    | Slot | Time |
    |---|---|
    | Morning | 06:00 AM |
    Fares are ₹5,500 per seat. 
    Beware of scam agents; IRCTC HeliYatra is the official authority.
    Buses run from Rishikesh to Guptkashi.
    Book your stay near Kedarnath at https://yatradham.org/.
    """
    g_pass = validate_transit_bottleneck_guardrails(compliant_md, title="Kedarnath Helicopter Booking")
    assert g_pass["compliant"] is True
    assert g_pass["passed_rules"] == 6

    # Incompliant content
    incompliant_md = "This is a helicopter ride. Very fast and nice. Book soon."
    g_fail = validate_transit_bottleneck_guardrails(incompliant_md, title="Heli Ride")
    assert g_fail["compliant"] is False
    assert g_fail["passed_rules"] < 4


def test_fastapi_transit_bottlenecks_endpoints():
    # 1. Catalog endpoint
    res_cat = client.get("/api/transit-bottlenecks/catalog")
    assert res_cat.status_code == 200
    assert res_cat.json()["total_bottlenecks"] >= 8

    # 2. Analyze endpoint
    res_ana = client.post("/api/transit-bottlenecks/analyze", json={
        "query_or_route": "Girnar Ropeway 9999 steps avoided",
        "has_steep_climb": True
    })
    assert res_ana.status_code == 200
    assert "intensity_score" in res_ana.json()

    # 3. Blueprint generator endpoint
    res_bp = client.post("/api/transit-bottlenecks/generate-blueprint", json={
        "bottleneck_id": "ghogha_hazira_ropax"
    })
    assert res_bp.status_code == 200
    assert "markdown_content" in res_bp.json()

    # 4. Guardrail check endpoint
    res_gr = client.post("/api/transit-bottlenecks/guardrail-check", json={
        "content": "Saves 370 km. | Route | Time |. Price ₹600. Official GMB portal. Buses connect station. Book dharamshala on YatraDham.Org."
    })
    assert res_gr.status_code == 200
    assert "compliance_score" in res_gr.json()
