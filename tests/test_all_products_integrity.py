import sys
import os
import time
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import PackageInput
from pipeline import process_package
from llm_client import LLMClient
from validation_layer import validate_no_duplicated_words, run_validation


TEST_PRODUCTS = [
    {
        "category": "puja",
        "name": "Puja at Dwarka",
        "destination": "Dwarka, Gujarat",
        "cost": "Starting From ₹ 1,500.00",
        "duration": "1 Day",
        "url": "https://temple.yatradham.org/puja-at-dwarka",
    },
    {
        "category": "stay",
        "name": "Swargashram Trust Dharamshala",
        "destination": "Rishikesh, Uttarakhand",
        "cost": "Starting From ₹ 800.00",
        "duration": "1 Night",
        "url": "https://yatradham.org/swargashram-trust-rishikesh.html",
    },
    {
        "category": "tour",
        "name": "Char Dham Yatra Haridwar",
        "destination": "Haridwar, Uttarakhand",
        "cost": "Starting From ₹ 18,500.00",
        "duration": "10 Days & 9 Nights",
        "url": "https://yatradham.org/chardham-yatra-from-haridwar.html",
    },
    {
        "category": "wellness",
        "name": "Ayurvedic Stress Relief Retreat",
        "destination": "Palakkad, Kerala",
        "cost": "Starting From ₹ 12,000.00",
        "duration": "7 Days",
        "url": "https://wellness.yatradham.org/ayurvedic-stress-relief-retreat",
    }
]


@pytest.mark.parametrize("product", TEST_PRODUCTS, ids=lambda p: p["category"])
def test_product_category_pipeline_integrity(product):
    """Verify that all 4 product categories generate 100% complete, verified, uncorrupted content."""
    pkg = PackageInput(
        url=product["url"],
        name=product["name"],
        cost=product["cost"],
        duration=product["duration"],
        destination=product["destination"],
        category=product["category"],
        raw_html="<html><body><h1>" + product["name"] + "</h1><p>Price: " + product["cost"] + "</p></body></html>",
        raw_text=f"{product['name']} in {product['destination']}. Price: {product['cost']}. Duration: {product['duration']}.",
    )

    t0 = time.time()
    llm_client = LLMClient()
    output = process_package(pkg, llm_client)
    elapsed = time.time() - t0

    print(f"\n[{product['category'].upper()}] Pipeline finished in {elapsed:.2f}s, QA Score: {output.qa_score}")

    # 1. Performance & Latency: Fast execution
    assert elapsed < 15.0, f"Processing took too long: {elapsed:.2f}s"

    # 2. Objective Quality Gate
    assert output.qa_score >= 85, f"QA Score too low for {product['category']}: {output.qa_score}"
    assert output.status == "approved_candidate", f"Expected approved_candidate for {product['category']}, got {output.status}"
    assert output.factual_integrity_score >= 85, f"Factual score too low for {product['category']}: {output.factual_integrity_score}"

    # 3. Ground Truth & Anti-Hallucination
    gt = output.ground_truth_report or {}
    assert gt.get("verification_status") in ["VERIFIED", "NEEDS_REVIEW"]
    flags_joined = " ".join(output.qa_flags)
    assert "Location drift detected" not in flags_joined, f"Location drift in {product['category']}: {flags_joined}"
    assert "Missing required sections" not in flags_joined, f"Missing sections in {product['category']}: {flags_joined}"
    assert "MISSING_SECTIONS" not in flags_joined, f"MISSING_SECTIONS flag in {product['category']}: {flags_joined}"
    assert "Duplicated word(s) found" not in flags_joined, f"Duplicated words in {product['category']}: {flags_joined}"

    # 4. Snippet Constraints
    assert 50 <= len(output.title_tag) <= 65, f"Title tag length out of bounds ({len(output.title_tag)} chars): '{output.title_tag}'"
    assert len(output.meta_description) <= 160, f"Meta description exceeds 160 chars ({len(output.meta_description)} chars): '{output.meta_description}'"
    assert len(output.meta_description) >= 60, f"Meta description too short ({len(output.meta_description)} chars): '{output.meta_description}'"

    # 5. Full 19 Structured Sections Verification
    sec = output.sections
    assert len(sec.package_overview.strip()) >= 50, f"Overview too short in {product['category']}"
    assert sec.quick_facts.destination == product["destination"]
    assert sec.quick_facts.cost != ""
    assert len(sec.why_choose_bullets) >= 3
    assert len(sec.who_can_benefit_bullets) >= 3
    assert len(sec.inclusions) >= 2
    assert len(sec.exclusions) >= 2
    assert len(sec.faq) >= 3
    assert len(sec.itinerary) >= 1
    assert len(sec.pricing_table) >= 1
    assert len(sec.terms_conditions) >= 2
    assert sec.cancellation_policy != ""

    # 6. GEO Quick Answer presence
    assert sec.geo_quick_answer != "", f"GEO Quick Answer missing in {product['category']}"
    assert product["destination"] in sec.geo_quick_answer or product["destination"].split(",")[0] in sec.geo_quick_answer

    # 7. No Duplicated Words Anywhere
    full_blob = f"{output.title_tag} {output.meta_description} {sec.package_overview} {' '.join(sec.why_choose_bullets)}"
    ok, msg = validate_no_duplicated_words(full_blob)
    assert ok, f"Duplicated words detected in {product['category']}: {msg}"
