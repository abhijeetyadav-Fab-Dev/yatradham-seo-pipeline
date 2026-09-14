import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from sitemap_crawler import SitemapCrawler

client = TestClient(app)

def test_sitemap_crawl_xml_endpoint():
    """Test XML sitemap crawling via FastAPI endpoint."""
    res = client.post("/api/sitemap/crawl", json={
        "source_url": "wellness.yatradham.org/sitemap.xml",
        "max_urls": 10
    })
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert data["success"] is True
    assert data["total_found"] > 0
    assert len(data["items"]) <= 10
    for item in data["items"]:
        assert "url" in item
        assert "suggested_name" in item
        assert item["category"] in ["wellness", "tour", "stay", "puja"]


def test_category_hub_crawl_endpoint():
    """Test category hub crawling via FastAPI endpoint."""
    res = client.post("/api/sitemap/crawl", json={
        "source_url": "https://yatradham.org/chardham-package",
        "max_urls": 50
    })
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert data["success"] is True
    assert data["total_found"] > 0
    for item in data["items"]:
        u = item["url"].lower()
        assert not u.endswith(".jpg")
        assert not u.endswith(".png")
        assert "why-choose-us" not in u
        assert "customers_otp" not in u
        assert "customer-reviews" not in u
        assert "privacy-policy" not in u


def test_max_urls_over_100_support():
    """Verify max_urls=200 does not trigger 422 validation error."""
    res = client.post("/api/sitemap/crawl", json={
        "source_url": "https://wellness.yatradham.org/sitemap.xml",
        "max_urls": 200
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["total_found"] > 50


def test_ssrf_blocking_on_sitemap_endpoint():
    """Ensure SSRF attacks on localhost / internal subnets are blocked with HTTP 400."""
    res = client.post("/api/sitemap/crawl", json={
        "source_url": "http://127.0.0.1:8000/secret.xml",
        "max_urls": 10
    })
    assert res.status_code == 400
    assert "SSRF" in res.json().get("detail", "")

    res2 = client.post("/api/sitemap/crawl", json={
        "source_url": "http://169.254.169.254/latest/meta-data/",
        "max_urls": 10
    })
    assert res2.status_code == 400
    assert "SSRF" in res2.json().get("detail", "")


def test_unit_crawler_title_generation():
    """Verify URL path slug cleaning and destination title generation."""
    title1 = SitemapCrawler._generate_title_from_url("https://yatradham.org/yatradham-destinations/uttarakhand/kedarnath.html")
    assert title1 == "Kedarnath, Uttarakhand"

    title2 = SitemapCrawler._generate_title_from_url("https://travel.yatradham.org/package/chardham-yatra-packages")
    assert title2 == "Chardham Yatra Packages"

    title3 = SitemapCrawler._generate_title_from_url("https://wellness.yatradham.org/7-day-yoga-vacation")
    assert title3 == "7 Day Yoga Vacation"


if __name__ == "__main__":
    test_sitemap_crawl_xml_endpoint()
    print("[PASS] test_sitemap_crawl_xml_endpoint")
    test_category_hub_crawl_endpoint()
    print("[PASS] test_category_hub_crawl_endpoint")
    test_max_urls_over_100_support()
    print("[PASS] test_max_urls_over_100_support")
    test_ssrf_blocking_on_sitemap_endpoint()
    print("[PASS] test_ssrf_blocking_on_sitemap_endpoint")
    test_unit_crawler_title_generation()
    print("[PASS] test_unit_crawler_title_generation")
    print("\nAll 5 sitemap ingestion pre-production tests passed successfully!")
