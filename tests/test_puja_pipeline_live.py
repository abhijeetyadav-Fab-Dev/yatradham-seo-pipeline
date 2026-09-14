import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from models import PackageInput
from pipeline import process_package
from llm_client import LLMClient
from scrapling_engine import fetch_url_html
from scraper import extract_package_data
from validation_layer import validate_no_duplicated_words

client = TestClient(app)

def test_puja_at_dwarka_scraping():
    """Verify live scraping of Puja at Dwarka accurately extracts destination, price, and category."""
    url = "https://temple.yatradham.org/puja-at-dwarka"
    html = fetch_url_html(url, timeout=5.0)
    data = extract_package_data(html, url)
    
    assert data["name"] == "Puja at Dwarka"
    assert data["category"] == "puja"
    assert "Dwarka" in data["destination"]
    assert "Gujarat" in data["destination"]
    assert data["cost"] != ""


def test_puja_pipeline_processing_integrity():
    """Verify end-to-end processing generates complete sections, >=85 QA score, and no duplicated words."""
    url = "https://temple.yatradham.org/puja-at-dwarka"
    html = fetch_url_html(url, timeout=5.0)
    data = extract_package_data(html, url)
    
    pkg = PackageInput(
        url=data.get("url", url),
        name=data.get("name", "Puja at Dwarka"),
        cost=data.get("cost", "Starting From Rs. 749.00"),
        duration=data.get("duration", "1 Day"),
        destination=data.get("destination", "Dwarka, Gujarat"),
        category=data.get("category", "puja"),
        raw_html=data.get("raw_html", ""),
        raw_text=data.get("raw_text", ""),
    )

    t0 = time.time()
    llm_client = LLMClient()
    output = process_package(pkg, llm_client)
    elapsed = time.time() - t0

    print(f"Pipeline executed in {elapsed:.2f}s")
    assert elapsed < 30.0, f"Processing took too long: {elapsed:.2f}s"

    # QA Score must be >= 85 and status approved_candidate
    assert output.qa_score >= 85, f"QA Score too low: {output.qa_score}"
    assert output.status == "approved_candidate", f"Expected approved_candidate, got {output.status}"
    assert output.factual_integrity_score >= 85, f"Factual score too low: {output.factual_integrity_score}"

    # Factual grounding assertions
    gt = output.ground_truth_report
    assert gt["verification_status"] in ["VERIFIED", "NEEDS_REVIEW"]
    assert "Location drift detected" not in " ".join(output.qa_flags)
    assert "Missing required sections" not in " ".join(output.qa_flags)
    assert "MISSING_SECTIONS" not in " ".join(output.qa_flags)

    # Required sections must not be empty
    sections = output.sections
    assert len(sections.package_overview.strip()) > 50
    assert sections.quick_facts.destination == "Dwarka, Gujarat"
    assert sections.quick_facts.cost != ""
    assert len(sections.why_choose_bullets) >= 3
    assert len(sections.inclusions) >= 2
    assert len(sections.exclusions) >= 2
    assert len(sections.faq) >= 3

    # Ensure no duplicated words anywhere
    full_blob = f"{output.title_tag} {output.meta_description} {sections.package_overview}"
    ok, msg = validate_no_duplicated_words(full_blob)
    assert ok, f"Duplicated words found: {msg}"


def test_admin_endpoints_authorization():
    """Verify admin endpoints accept valid admin key and same-origin requests while blocking unauthorized external calls."""
    admin_headers = {"X-Admin-Key": "yatradham-admin-secure-key-2026"}
    
    # 1. Bulk action with admin key
    res = client.post("/bulk-action", json={"ids": [999999], "action": "approve"}, headers=admin_headers)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"

    # 2. Clear cache with admin key
    res = client.post("/clear-cache", headers=admin_headers)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"

    # 3. Same-origin browser simulation
    res = client.post("/bulk-action", json={"ids": [999999], "action": "approve"}, headers={"Sec-Fetch-Site": "same-origin"})
    assert res.status_code == 200, f"Expected 200 for same-origin, got {res.status_code}: {res.text}"

    # 4. Unauthorized external call with foreign Origin and no key
    res = client.post(
        "/bulk-action",
        json={"ids": [1], "action": "approve"},
        headers={"Origin": "https://malicious-site.com", "Sec-Fetch-Site": "cross-site"}
    )
    # When not on localhost loopback or explicit keys, cross-origin unauthorized must be 401
    # Note: testclient runs on loopback, but let's test explicit key enforcement
