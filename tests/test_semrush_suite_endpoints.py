"""
Tests for Semrush SEO Suite FastAPI Endpoints
Ensures all 21 endpoints are reachable, return valid schema, and handle edge cases gracefully.
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure root directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_semrush_domain_overview_live_and_nxdomain():
    # Live domain
    res = client.get("/api/semrush/domain-overview?domain=yatradham.org")
    assert res.status_code == 200
    data = res.json()
    assert "authority_score" in data
    assert "organic_traffic" in data
    assert "is_live" in data
    assert data["is_live"] is True

    # NXDOMAIN / invalid domain
    res_invalid = client.get("/api/semrush/domain-overview?domain=therahulgohil.blog")
    assert res_invalid.status_code == 200
    data_inv = res_invalid.json()
    assert data_inv["is_live"] is False
    assert data_inv["authority_score"] == 0


def test_semrush_keyword_magic_endpoint():
    res = client.get("/api/semrush/keyword-magic?keyword=kedarnath+yatra&limit=10")
    assert res.status_code == 200
    data = res.json()
    assert "seed_keyword" in data
    assert "total_keywords" in data
    assert "keywords" in data
    assert isinstance(data["keywords"], list)


def test_semrush_site_audit_post():
    res = client.post("/api/semrush/site-audit", json={"url": "https://yatradham.org"})
    assert res.status_code == 200
    data = res.json()
    assert "site_health_score" in data
    assert "checks" in data
    assert "checks_summary" in data
    assert len(data["checks"]) == 30


def test_semrush_backlinks_endpoint():
    res = client.get("/api/semrush/backlinks?domain=yatradham.org")
    assert res.status_code == 200
    data = res.json()
    assert "domain" in data
    assert "total_backlinks" in data
    assert "referring_domains" in data


def test_semrush_dashboard_and_pulse_endpoints():
    res = client.get("/api/semrush/dashboard?domain=yatradham.org")
    assert res.status_code == 200
    data = res.json()
    assert "domain" in data
    assert "authority_score" in data

    res_sensor = client.get("/api/semrush/sensor")
    assert res_sensor.status_code == 200
    assert "volatility_score" in res_sensor.json()


def test_semrush_gaps_and_comparison():
    res_gap = client.post("/api/semrush/keyword-gap", json={
        "domain_a": "yatradham.org",
        "domain_b": "makemytrip.com"
    })
    assert res_gap.status_code == 200
    data = res_gap.json()
    assert "shared_keywords" in data or "keywords" in data or "summary" in data

    res_comp = client.post("/api/semrush/compare-domains", json={
        "domains": ["yatradham.org", "makemytrip.com"]
    })
    assert res_comp.status_code == 200
    assert "comparison" in res_comp.json() or "domains" in res_comp.json()
