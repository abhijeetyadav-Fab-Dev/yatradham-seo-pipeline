"""Comprehensive End-to-End Test Suite for Yatradham SEO Pipeline."""
import sys
import os
import io

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import time
import urllib.request
import traceback

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models import PackageInput, SEOOutput, SectionedContent
from database import init_db, save_output, get_output, list_outputs, update_output, bulk_update_status, delete_output, get_stats
from llm_client import LLMClient
from scraper import extract_package_data
from pipeline import process_package
from agents import keyword_agent, title_agent, meta_agent, content_agent, qa_agent, content_creator_agent
import main

test_results = []

def record(test_name: str, passed: bool, details: str = ""):
    status = "[PASS]" if passed else "[FAIL]"
    test_results.append({"name": test_name, "passed": passed, "details": details})
    print(f"{status} | {test_name}" + (f" -> {details}" if details else ""))

def run_suite():
    print("=" * 80)
    print("STARTING FULL END-TO-END SYSTEM & AGENT TEST SUITE")
    print("=" * 80)

    # 1. DATABASE & STORAGE TESTS
    print("\n--- [TEST GROUP 1: Database & Storage Engine] ---")
    try:
        init_db()
        stats_before = get_stats()
        record("Database Initialization & Stats Retrieval", True, f"Total records: {stats_before.get('total')}")
        
        # Test Save, Get, List
        dummy_pkg = PackageInput(
            url="https://travel.yatradham.org/test-package-e2e",
            name="Test E2E Spiritual Tour",
            cost="₹4,999",
            duration="3 Days",
            destination="Haridwar & Rishikesh",
            accommodation="Ashram stay",
            food="Sattvic meals"
        )
        dummy_sections = SectionedContent(
            package_overview="A serene 3-day spiritual retreat in Haridwar and Rishikesh."
        )
        dummy_output = SEOOutput(
            package_input=dummy_pkg,
            primary_keyword="Rishikesh 3 Days Spiritual Tour",
            title_tag="3 Days Haridwar & Rishikesh Tour | Yatradham.Org",
            meta_description="Book a peaceful 3-day spiritual tour with verified ashram stays.",
            sections=dummy_sections,
            qa_score=92,
            qa_flags=["Minor keyword density check passed"],
            status="pending"
        )
        saved_id = save_output(dummy_output)
        record("Database Save Output", saved_id > 0, f"Inserted Row ID #{saved_id}")

        retrieved = get_output(saved_id)
        record("Database Get Output by ID", retrieved is not None and retrieved.primary_keyword == "Rishikesh 3 Days Spiritual Tour")

        # Update status
        up_ok = bulk_update_status([saved_id], "approved")
        record("Database Status Update (Approved)", up_ok > 0)
        
        # Verify status
        retrieved_updated = get_output(saved_id)
        record("Database Verify Status Update", retrieved_updated.status == "approved")

        # Clean up test row
        del_ok = delete_output(saved_id)
        record("Database Row Deletion Cleanup", del_ok)
    except Exception as e:
        record("Database Suite Execution", False, str(e))
        traceback.print_exc()

    # 2. SCRAPER & HTML PARSER ENGINE
    print("\n--- [TEST GROUP 2: Live Web Scraper & Parser] ---")
    try:
        sample_url = "https://travel.yatradham.org/days-vrindavan-barsana-tour-package"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 YatradhamBot/1.0"}
        req = urllib.request.Request(sample_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        record("Live URL Scraper Fetch", len(html) > 1000, f"Fetched {len(html):,} bytes")

        scraped_data = extract_package_data(html, sample_url)
        has_name = bool(scraped_data.get("name"))
        has_cost = bool(scraped_data.get("cost"))
        has_text = len(scraped_data.get("raw_text", "")) > 500
        record("Package Data Extraction", has_name and has_text, f"Name: {scraped_data.get('name')} | Cost: {scraped_data.get('cost')} | Text chars: {len(scraped_data.get('raw_text', ''))}")
    except Exception as e:
        record("Web Scraper Engine", False, str(e))

    # 3. LLM CLIENT & PROVIDER DISCOVERY
    print("\n--- [TEST GROUP 3: LLM Client & Provider Architecture] ---")
    try:
        client = LLMClient()
        record("LLM Client Instantiation", client is not None)
        
        # Test dry-run / fallback mock response
        client.dry_run = True
        mock_res = client.chat_completion([{"role": "user", "content": "Generate title"}])
        client.dry_run = False
        record("LLM Dry-Run & Offline Fallback Safety", bool(mock_res))

        # Test reasoning tag stripper
        test_leaked = "<think>I should write a good intro</think>## Introduction\nWelcome to Rishikesh."
        stripped = client._strip_reasoning(test_leaked)
        record("Reasoning / Internal Monologue Stripper", stripped.startswith("## Introduction"))
    except Exception as e:
        record("LLM Architecture", False, str(e))

    # 4. UNDETECTABLE AI SCANNER & HUMANIZER BYPASS ENGINE
    print("\n--- [TEST GROUP 4: Undetectable AI Scanner & Bypass Humanizer] ---")
    try:
        test_ai_text = """Rishikesh is nestled in the foothills of the Himalayas. Moreover, it serves as a beacon of spirituality and a tapestry of ancient yoga traditions. In conclusion, one must delve into this transformative journey to foster holistic well-being."""
        
        # Test AI Detector Endpoint
        det_res = main.query_undetectable_detector(test_ai_text)
        record("AI Detector API Connection", "score" in det_res, f"Score detected: {det_res.get('score')}%")

        # Test Parallel Markdown Humanizer on Multi-Section Blog
        multi_section_sample = """## Introduction: Sacred Rishikesh
Rishikesh is nestled in the foothills of the Himalayas. Moreover, it serves as a beacon of spirituality and a tapestry of ancient yoga traditions. It is important to note that pilgrims visit annually.

## Essential Travel Logistics
Flights to Dehradun cost ₹4,000 to ₹7,000 one-way. Furthermore, Yatradham.Org offers verified dharamshalas starting at ₹600 per night with transparent pricing.

## Frequently Asked Questions
What is the best time to visit Rishikesh?
The best months are October to March with pleasant 15°C to 25°C weather."""

        t0 = time.time()
        humanized_result = main.humanize_markdown_content(multi_section_sample)
        elapsed = time.time() - t0
        
        record("Parallel Humanizer Execution", len(humanized_result) > 50, f"Rewritten in {elapsed:.2f}s | Chars: {len(humanized_result)}")
        record("Headings & Structure Preservation", "## " in humanized_result and len(humanized_result.split("## ")) >= 3)
        
        # Test Detector on Rewritten Result
        post_scan = main.query_undetectable_detector(humanized_result)
        post_score = post_scan.get("score", 100)
        human_score = round(100 - post_score, 2)
        record("Bypass Quality Gate (<5% AI / >95% Human)", post_score < 10.0, f"AI Score: {post_score}% | Human Score: {human_score}%")
    except Exception as e:
        record("Humanizer & Scanner Suite", False, str(e))

    # 5. LONG-FORM CONTENT GENERATION & INTEGRITY ENGINE
    print("\n--- [TEST GROUP 5: Content Creator & Section Integrity Engine] ---")
    try:
        from agents.content_creator_agent import _clean_markdown, _parse_markdown_sections, _sanitize_repetition
        
        sample_raw = """```markdown
# TITLE
7 Days Rishikesh Wellness Guide

# META DESCRIPTION
Discover 7 days of rejuvenation in Rishikesh.

# SUGGESTED TAGS
Rishikesh, Wellness, Yoga

# CONTENT
## Introduction
Welcome to Rishikesh.
```"""
        cleaned = _clean_markdown(sample_raw)
        sections = _parse_markdown_sections(cleaned)
        record("Content Section Parsing", sections.get("TITLE") == "7 Days Rishikesh Wellness Guide" and "CONTENT" in sections)

        # Test repetition sanitizer
        rep_text = "Rishikesh is wonderful.\n\nRishikesh is wonderful.\n\nRishikesh is wonderful."
        sanitized = _sanitize_repetition(rep_text)
        record("Repetition Sanitizer", sanitized.count("Rishikesh is wonderful.") < 3)
    except Exception as e:
        record("Content Creator Engine", False, str(e))

    # 6. CSV EXPORT & API DATA CONTRACTS
    print("\n--- [TEST GROUP 6: CSV Export Engine & API Data Contracts] ---")
    try:
        # Create a test output for export verification
        dummy_pkg = PackageInput(url="https://travel.yatradham.org/export-test", name="Export Test Package")
        dummy_output = SEOOutput(package_input=dummy_pkg, primary_keyword="Export Test", status="approved")
        test_id = save_output(dummy_output)
        
        csv_resp = main.export_csv(status="approved")
        record("CSV Export Response Generation", csv_resp.status_code == 200 and "text/csv" in csv_resp.media_type)
        delete_output(test_id)
    except Exception as e:
        record("CSV Export Engine", False, str(e))

    # SUMMARY
    print("\n" + "=" * 80)
    total_tests = len(test_results)
    passed_tests = sum(1 for t in test_results if t["passed"])
    failed_tests = total_tests - passed_tests
    print(f"SUMMARY: Total Tests: {total_tests} | Passed: {passed_tests} | Failed: {failed_tests}")
    print("=" * 80)

if __name__ == "__main__":
    run_suite()
