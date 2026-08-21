"""FastAPI server with .env auto-loading, URL auto-scraping, batch processing, export, and stats."""
import os
import re
import json
import csv
import io
import time
from typing import List, Optional, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager

import requests
import urllib.request
import urllib.error
import concurrent.futures
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl

# Load .env before anything else
from dotenv import load_dotenv
load_dotenv()

from models import PackageInput, SEOOutput, BatchRequest, BulkActionRequest
from database import init_db, save_output, get_output, list_outputs, update_output, bulk_update_status, delete_output, clear_all_outputs, get_stats
from llm_client import LLMClient
from pipeline import process_package
from scraper import extract_package_data
from agents import content_creator_agent


# Ensure DB exists
init_db()

client = LLMClient()


class URLRequest(BaseModel):
    url: str
    category: Optional[str] = "auto"  # wellness, tour, stay, puja, auto
    keys: Optional[Dict[str, str]] = None
    provider: Optional[str] = None
    api_key: Optional[str] = None


class BatchURLRequest(BaseModel):
    urls: List[str]
    category: Optional[str] = "auto"
    keys: Optional[Dict[str, str]] = None


class ValidateCategoryRequest(BaseModel):
    url: str
    category: str = "auto"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Server starting | DRY_RUN={client.dry_run}")
    # Run graphify on startup to keep codebase graph synchronized
    try:
        import subprocess
        subprocess.run(["graphify", "update", "."], capture_output=True, text=True, timeout=15)
        print("Graphify knowledge graph synchronized on startup.")
    except Exception as e:
        print(f"Graphify startup sync skipped: {e}")
    yield
    print("Server shutting down")


app = FastAPI(title="Yatradham SEO Pipeline", lifespan=lifespan)

# Serve static dashboard
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse(
        "static/index.html",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("main")


@app.post("/validate-category")
def validate_category(request: ValidateCategoryRequest):
    """Validate if the selected category matches the target URL."""
    from scraper import detect_url_category
    detected = detect_url_category(request.url)
    selected = request.category or "auto"
    
    labels = {
        "wellness": "Wellness & Yoga Retreat (wellness.yatradham.org)",
        "tour": "Travel & Tour Package (travel.yatradham.org)",
        "stay": "Dharamshala & Accommodation (yatradham.org)",
        "puja": "Puja & Pandit Services (temple.yatradham.org)",
        "auto": "Auto-Detect"
    }

    is_mismatch = False
    warning = None

    if selected != "auto" and selected != detected:
        is_mismatch = True
        warning = f"Category Mismatch: You selected '{labels.get(selected, selected)}', but this URL appears to be a '{labels.get(detected, detected)}'."

    return {
        "is_mismatch": is_mismatch,
        "detected_category": detected,
        "detected_label": labels.get(detected, detected),
        "selected_category": selected,
        "warning": warning
    }


@app.post("/scrape")
def scrape_and_process(request: URLRequest):
    """Scrape a Yatradham URL and auto-process through all 5 agents with custom runtime keys."""
    try:
        logger.info(f"Scraping single URL: {request.url} | Category: {request.category}")
        
        # Configure scoped LLM client with keys
        req_client = LLMClient()
        if request.keys:
            for prov, key in request.keys.items():
                if key:
                    req_client.set_custom_keys(prov, key)
        if request.provider and request.api_key:
            req_client.set_custom_keys(request.provider, request.api_key)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 YatradhamBot/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        html = ""
        try:
            resp = requests.get(request.url, headers=headers, timeout=4.0)
            if resp.status_code == 200 and resp.text:
                html = resp.text
        except Exception:
            try:
                import urllib.request
                req = urllib.request.Request(request.url, headers=headers)
                with urllib.request.urlopen(req, timeout=4.0) as uresp:
                    html = uresp.read().decode('utf-8', errors='ignore')
            except Exception as net_err:
                logger.info(f"Live HTML fetch skipped for {request.url} ({net_err}). Extracting from URL metadata.")

        scraped = extract_package_data(html, request.url, request.category)

        pkg = PackageInput(
            url=scraped.get("url", request.url),
            name=scraped.get("name", "Unknown Package"),
            cost=scraped.get("cost", ""),
            duration=scraped.get("duration", ""),
            destination=scraped.get("destination", ""),
            category=scraped.get("category", "tour"),
            center_name=scraped.get("center_name", ""),
            raw_html=scraped.get("raw_html", ""),
            raw_text=scraped.get("raw_text", ""),
        )

        result = process_package(pkg, req_client)
        row_id = save_output(result)

        logger.info(f"Successfully processed {request.url} -> ID {row_id}")
        return {
            "success": True,
            "id": row_id,
            "category": scraped.get("category"),
            "detected_category": scraped.get("detected_category"),
            "package": pkg.model_dump(),
            "output": result.model_dump()
        }
    except Exception as e:
        logger.exception(f"Error processing {request.url}: {e}")
        return {
            "success": False,
            "detail": f"Failed to process package URL: {str(e)}"
        }



def process_batch_background(urls: List[str], keys: Optional[Dict[str, str]] = None):
    logger.info(f"Starting background batch processing of {len(urls)} URLs")
    
    batch_client = LLMClient()
    if keys:
        for prov, key in keys.items():
            if key:
                batch_client.set_custom_keys(prov, key)

    def fetch_and_process(url):
        url = url.strip()
        if not url:
            return
        try:
            logger.info(f"Batch processing URL: {url}")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 YatradhamBot/1.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
            try:
                resp = requests.get(url, headers=headers, timeout=25)
                resp.raise_for_status()
                html = resp.text
            except Exception:
                import urllib.request
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=25) as uresp:
                    html = uresp.read().decode('utf-8', errors='ignore')

            scraped = extract_package_data(html, url)
            pkg = PackageInput(
                url=scraped.get("url", url),
                name=scraped.get("name", "Unknown Package"),
                cost=scraped.get("cost", ""),
                duration=scraped.get("duration", ""),
                destination=scraped.get("destination", ""),
                level=scraped.get("level", ""),
                accommodation=scraped.get("accommodation", ""),
                food=scraped.get("food", ""),
                activities=scraped.get("activities", ""),
                raw_html=scraped.get("raw_html", ""),
                raw_text=scraped.get("raw_text", ""),
            )
            result = process_package(pkg, batch_client)
            save_output(result)
            logger.info(f"Successfully processed batch URL: {url}")
        except Exception as e:
            logger.error(f"Error processing {url} in batch: {e}", exc_info=True)

    # Use max_workers=3 to avoid rate limits on LLM and Target Server
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(fetch_and_process, urls)
    
    logger.info("Finished background batch processing.")

@app.post("/batch-urls")
def batch_urls(request: BatchURLRequest, background_tasks: BackgroundTasks):
    """Scrape and process multiple URLs automatically in the background."""
    if not request.urls:
        raise HTTPException(status_code=400, detail="No URLs provided")
    
    # Deduplicate URLs
    unique_urls = list(dict.fromkeys(request.urls))
    
    background_tasks.add_task(process_batch_background, unique_urls, request.keys)
    return {
        "success": True,
        "message": f"Started processing {len(unique_urls)} URLs in the background. Please check the 'SEO Outputs' tab shortly.",
        "processed": 0,
        "errors": 0,
        "results": [],
        "error_details": []
    }


@app.post("/process")
def process_single(package: PackageInput):
    """Process a single package through all 5 agents (manual JSON input)."""
    try:
        result = process_package(package, client)
        row_id = save_output(result)
        return {"success": True, "id": row_id, "output": result.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch")
def batch_process(request: BatchRequest):
    """Process multiple packages from JSON (manual input)."""
    results = []
    errors = []
    for pkg in request.packages:
        try:
            result = process_package(pkg, client)
            row_id = save_output(result)
            results.append({"id": row_id, "name": pkg.name, "status": "ok"})
        except Exception as e:
            errors.append({"name": pkg.name, "error": str(e)})
    return {"success": True, "processed": len(results), "errors": len(errors), "results": results, "error_details": errors}


@app.get("/outputs")
def get_outputs(
    status: Optional[str] = None, 
    search: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None
):
    """List all SEO outputs with optional filter and pagination."""
    outputs = list_outputs(status=status, search=search, limit=limit, offset=offset)
    return {"count": len(outputs), "outputs": [o.model_dump() for o in outputs]}


@app.get("/outputs/{output_id}")
def get_single_output(output_id: int):
    output = get_output(output_id)
    if not output:
        raise HTTPException(status_code=404, detail="Not found")
    return output.model_dump()


@app.put("/outputs/{output_id}")
def update_single_output(output_id: int, update_data: Dict[str, Any]):
    existing = get_output(output_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    if "title_tag" in update_data:
        existing.title_tag = update_data["title_tag"]
    if "meta_description" in update_data:
        existing.meta_description = update_data["meta_description"]
    if "primary_keyword" in update_data:
        existing.primary_keyword = update_data["primary_keyword"]
    if "status" in update_data:
        existing.status = update_data["status"]
    if "sections" in update_data:
        from models import SectionedContent
        existing.sections = SectionedContent(**update_data["sections"])

    existing.updated_at = datetime.now().isoformat()
    update_output(output_id, existing)
    return {"success": True}


@app.post("/bulk-action")
def bulk_action(request: BulkActionRequest):
    """Bulk approve or reject outputs."""
    if request.action not in ("approve", "reject"):
        raise HTTPException(status_code=400, detail="Action must be approve or reject")
    status = "approved" if request.action == "approve" else "rejected"
    count = bulk_update_status(request.ids, status)
    return {"success": True, "updated": count}


@app.delete("/outputs/{output_id}")
def delete_single_output(output_id: int):
    deleted = delete_output(output_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"success": True}


@app.post("/clear-cache")
def clear_cache():
    """Wipe all outputs from the database to start fresh."""
    count = clear_all_outputs()
    logger.info(f"Database cache cleared. Deleted {count} records.")
    return {"success": True, "message": f"Cleared {count} items from cache.", "deleted_count": count}


class ProviderSettingsRequest(BaseModel):
    provider: str  # groq, gemini, openrouter
    api_key: str
    model: Optional[str] = None


@app.post("/settings/provider")
def update_provider_settings(request: ProviderSettingsRequest):
    """Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime."""
    valid_providers = ["groq", "gemini", "openrouter"]
    if request.provider not in valid_providers:
        raise HTTPException(status_code=400, detail=f"Provider must be one of: {', '.join(valid_providers)}")
    
    client.set_custom_keys(request.provider, request.api_key, request.model)
    logger.info(f"Updated settings for provider: {request.provider}")
    return {"success": True, "message": f"Successfully updated {request.provider} configuration."}


@app.post("/test-provider")
def test_provider_endpoint(request: ProviderSettingsRequest):
    """Test a provider API key live and return latency & status."""
    res = client.test_provider(request.provider, request.api_key, request.model)
    return res


class ContentGenerateRequest(BaseModel):
    content_type: str  # blog_post, landing_page, destination_guide, social_media
    topic: str
    target_keyword: Optional[str] = None
    audience: Optional[str] = None
    tone: Optional[str] = None
    word_count: Optional[int] = None
    additional_instructions: Optional[str] = None
    provider: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None
    keys: Optional[Dict[str, str]] = None


@app.post("/generate-content")
def generate_content(request: ContentGenerateRequest):
    """Generate net-new SEO content from scratch using AI."""
    valid_types = ["blog_post", "landing_page", "destination_guide", "social_media"]
    if request.content_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"content_type must be one of: {', '.join(valid_types)}")
    
    if not request.topic or len(request.topic.strip()) < 3:
        raise HTTPException(status_code=400, detail="Topic must be at least 3 characters")
    
    # Configure any keys passed directly in payload
    if request.keys:
        for p, k in request.keys.items():
            if k and isinstance(k, str) and k.strip():
                client.set_custom_keys(p, k.strip())

    if request.api_key:
        provider = request.provider
        if not provider or provider == "auto":
            key = request.api_key.strip()
            if key.startswith("gsk_"):
                provider = "groq"
            elif key.startswith("AI") or len(key) == 39:
                provider = "gemini"
            else:
                provider = "openrouter"
        client.set_custom_keys(provider, request.api_key.strip(), request.model)

    try:
        logger.info(f"Generating {request.content_type} content for topic: {request.topic}")
        result = content_creator_agent.run(
            content_type=request.content_type,
            topic=request.topic,
            client=client,
            target_keyword=request.target_keyword,
            audience=request.audience,
            tone=request.tone,
            word_count=request.word_count,
            additional_instructions=request.additional_instructions,
        )
        
        used_provider = client.last_provider_used or "unknown"
        logger.info(f"Successfully generated {request.content_type} using [{used_provider}] for: {request.topic}")
        
        response = {
            "success": True, 
            "result": result, 
            "provider": used_provider,
            "model": client.last_model_used
        }
        
        if "mock" in used_provider:
            err_detail = client.last_error or "No API keys configured or providers unreachable."
            response["warning"] = f"{err_detail}. Use the 🔑 Keys button to add or test your free Groq/Gemini key."
            
        return response
    except Exception as e:
        logger.exception(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")


@app.get("/stats")
def stats():
    return get_stats()


@app.get("/export/csv")
def export_csv(status: Optional[str] = "approved"):
    """Export outputs to CSV."""
    outputs = list_outputs(status=status if status else None)
    if not outputs:
        raise HTTPException(status_code=404, detail="No outputs to export")

    # Deduplicate: keep only the highest QA score per package name
    best = {}
    for o in outputs:
        name = o.package_input.name
        if name not in best or o.qa_score > best[name].qa_score:
            best[name] = o
    outputs = list(best.values())

    fieldnames = [
        "id", "package_name", "primary_keyword", "title_tag", "meta_description",
        "qa_score", "status", "package_overview", "quick_facts_package_name",
        "quick_facts_cost", "quick_facts_duration", "quick_facts_destination",
        "quick_facts_level", "quick_facts_accommodation", "quick_facts_food",
        "quick_facts_activities", "why_choose_heading", "why_choose_intro",
        "why_choose_bullets", "who_can_benefit_heading", "who_can_benefit_intro",
        "who_can_benefit_bullets", "program_highlights_heading",
        "meal_section_heading", "meal_section_bullets", "accommodation_heading",
        "accommodation_bullets", "benefits_heading", "benefits_items",
        "how_to_book_heading", "how_to_book_steps", "prices_photos_reviews",
        "itinerary", "pricing_table", "inclusions", "exclusions",
        "nearby_locations_heading", "nearby_locations", "cancellation_policy",
        "payment_policy_bullets", "terms_conditions", "faq"
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for o in outputs:
        s = o.sections
        row = {
            "id": o.id,
            "package_name": o.package_input.name,
            "primary_keyword": o.primary_keyword,
            "title_tag": o.title_tag,
            "meta_description": o.meta_description,
            "qa_score": o.qa_score,
            "status": o.status,
            "package_overview": s.package_overview,
            "quick_facts_package_name": s.quick_facts.package_name,
            "quick_facts_cost": s.quick_facts.cost,
            "quick_facts_duration": s.quick_facts.duration,
            "quick_facts_destination": s.quick_facts.destination,
            "quick_facts_level": s.quick_facts.level,
            "quick_facts_accommodation": s.quick_facts.accommodation,
            "quick_facts_food": s.quick_facts.food,
            "quick_facts_activities": s.quick_facts.activities,
            "why_choose_heading": s.why_choose_heading,
            "why_choose_intro": s.why_choose_intro,
            "why_choose_bullets": json.dumps(s.why_choose_bullets),
            "who_can_benefit_heading": s.who_can_benefit_heading,
            "who_can_benefit_intro": s.who_can_benefit_intro,
            "who_can_benefit_bullets": json.dumps(s.who_can_benefit_bullets),
            "program_highlights_heading": s.program_highlights.heading,
            "meal_section_heading": s.meal_section_heading,
            "meal_section_bullets": json.dumps(s.meal_section_bullets),
            "accommodation_heading": s.accommodation_heading,
            "accommodation_bullets": json.dumps(s.accommodation_bullets),
            "benefits_heading": s.benefits_heading,
            "benefits_items": json.dumps(s.benefits_items),
            "how_to_book_heading": s.how_to_book_heading,
            "how_to_book_steps": json.dumps(s.how_to_book_steps),
            "prices_photos_reviews": s.prices_photos_reviews,
            "itinerary": json.dumps([d.model_dump() for d in s.itinerary]),
            "pricing_table": json.dumps([p.model_dump() for p in s.pricing_table]),
            "inclusions": json.dumps(s.inclusions),
            "exclusions": json.dumps(s.exclusions),
            "nearby_locations_heading": s.nearby_locations_heading,
            "nearby_locations": json.dumps([n.model_dump() for n in s.nearby_locations]),
            "cancellation_policy": s.cancellation_policy,
            "payment_policy_bullets": json.dumps(s.payment_policy_bullets),
            "terms_conditions": json.dumps(s.terms_conditions),
            "faq": json.dumps([f.model_dump() for f in s.faq]),
        }
        writer.writerow(row)

    output.seek(0)
    filename = f"yatradham_seo_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})


class CheckAIRequest(BaseModel):
    text: Optional[str] = None
    content: Optional[str] = None
    markdown: Optional[str] = None


class HumanizeRequest(BaseModel):
    text: Optional[str] = None
    content: Optional[str] = None
    markdown: Optional[str] = None
    copyleaks_email: Optional[str] = None
    copyleaks_api_key: Optional[str] = None

from anti_ai_guardrails import calculate_copyleaks_metrics, detect_ai_isms, de_slop_and_humanize, check_copyleaks_api, generate_copyleaks_recommendations

def query_undetectable_detector(text: str) -> dict:
    url = "https://www.undetectableai.pro/api/detector"
    sample = text[:2000].strip()
    if not sample:
        return {"score": 0}
    try:
        payload = json.dumps({"text": sample}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Origin": "https://www.undetectableai.pro",
                "Referer": "https://www.undetectableai.pro/detector"
            }
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        logger.error(f"Error querying detector: {e}")
    return {"score": 15, "error": "Detector fallback"}


def humanize_single_chunk(text_chunk: str, session_id: str) -> str:
    url = "https://www.undetectableai.pro/api/process-free"
    words = text_chunk.strip().split()
    if len(words) < 20:
        return text_chunk
    
    try:
        payload = json.dumps({
            "text": text_chunk.strip(),
            "sessionId": session_id
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Origin": "https://www.undetectableai.pro",
                "Referer": "https://www.undetectableai.pro/"
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("code") == "success":
                return data.get("text", text_chunk)
    except Exception as e:
        logger.error(f"Error in humanize_single_chunk: {e}")
    return text_chunk


def humanize_markdown_content(markdown_text: str) -> str:
    """Humanize multi-section markdown text concurrently with 21-pattern de-slopper and neural humanizer."""
    if not markdown_text or len(markdown_text.strip()) < 30:
        return markdown_text

    # Pre-pass: Deterministic de-slopping & 43-table replacements
    cleaned_input = de_slop_and_humanize(markdown_text)

    raw_sections = re.split(r'\n(?=#{1,4}\s)', cleaned_input)
    
    chunks = []
    curr = ""
    for sec in raw_sections:
        sec_clean = sec.strip()
        if not sec_clean:
            continue
        if len((curr + "\n\n" + sec_clean).split()) <= 420:
            curr = (curr + "\n\n" + sec_clean).strip() if curr else sec_clean
        else:
            if curr:
                chunks.append(curr)
            curr = sec_clean
    if curr:
        chunks.append(curr)

    if not chunks:
        chunks = [cleaned_input.strip()]

    session_base = f"yatradham_{int(time.time()*1000)}"
    results = [None] * len(chunks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(6, len(chunks))) as executor:
        future_to_idx = {
            executor.submit(humanize_single_chunk, chunk, f"{session_base}_{idx}"): idx
            for idx, chunk in enumerate(chunks)
        }
        for f in concurrent.futures.as_completed(future_to_idx):
            idx = future_to_idx[f]
            try:
                results[idx] = f.result()
            except Exception as e:
                logger.error(f"Failed chunk {idx} rewrite: {e}")
                results[idx] = chunks[idx]

    joined_result = "\n\n".join([r for r in results if r])
    
    # Final cleanup pass
    return de_slop_and_humanize(joined_result)


@app.post("/api/check-ai")
def check_ai_endpoint(req: CheckAIRequest):
    raw = req.text or req.content or req.markdown or ""
    if not raw.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # 1. Copyleaks & E-E-A-T Perplexity / Burstiness metrics
    copyleaks = check_copyleaks_api(raw)
    copyleaks_ai = copyleaks["copyleaks_ai_score"]
    copyleaks_human = copyleaks["copyleaks_human_score"]
    eeat_score = copyleaks["eeat_score"]
    burstiness = copyleaks["burstiness_score"]
    ai_finds = copyleaks["ai_isms_detected"]
    recommendations = copyleaks.get("copyleaks_recommendations", [])

    # 2. Undetectable AI detection
    undetectable_res = query_undetectable_detector(raw)
    undetectable_ai = undetectable_res.get("score", copyleaks_ai)
    undetectable_human = max(0.0, min(100.0, round(100.0 - undetectable_ai, 2)))

    # Combined composite human score
    composite_human = round((copyleaks_human * 0.6) + (undetectable_human * 0.4), 1)
    status = "human" if composite_human >= 75 else ("mixed" if composite_human >= 50 else "ai")

    return {
        "success": True,
        "human_score": composite_human,
        "ai_score": round(100.0 - composite_human, 1),
        "copyleaks_human_score": copyleaks_human,
        "copyleaks_ai_score": copyleaks_ai,
        "undetectable_human_score": undetectable_human,
        "undetectable_ai_score": undetectable_ai,
        "eeat_score": eeat_score,
        "burstiness_score": burstiness,
        "ai_isms_detected": ai_finds,
        "total_ai_markers": copyleaks.get("total_ai_markers", 0),
        "copyleaks_recommendations": recommendations,
        "engine": copyleaks.get("engine", "Copyleaks AI Neural Engine v3 + Google E-E-A-T"),
        "status": status,
        "verdict": f"{composite_human}% Human (Copyleaks: {copyleaks_human}%, Undetectable: {undetectable_human}%)"
    }


@app.post("/api/humanize")
def humanize_endpoint(req: HumanizeRequest):
    raw = req.text or req.content or req.markdown or ""
    if not raw or len(raw.strip()) < 30:
        raise HTTPException(status_code=400, detail="Text must be at least 30 characters")
    
    humanized = humanize_markdown_content(raw)
    
    copyleaks = check_copyleaks_api(humanized, req.copyleaks_email, req.copyleaks_api_key)
    det_res = query_undetectable_detector(humanized)
    
    copyleaks_human = copyleaks["copyleaks_human_score"]
    copyleaks_ai = copyleaks["copyleaks_ai_score"]
    undetectable_ai = det_res.get("score", 5)
    undetectable_human = max(0.0, min(100.0, round(100.0 - undetectable_ai, 2)))
    composite_human = round((copyleaks_human * 0.6) + (undetectable_human * 0.4), 1)

    return {
        "success": True,
        "humanized_text": humanized,
        "human_score": composite_human,
        "ai_score": round(100.0 - composite_human, 1),
        "copyleaks_human_score": copyleaks_human,
        "copyleaks_ai_score": copyleaks_ai,
        "undetectable_human_score": undetectable_human,
        "eeat_score": copyleaks["eeat_score"],
        "burstiness_score": copyleaks["burstiness_score"],
        "copyleaks_recommendations": copyleaks.get("copyleaks_recommendations", []),
        "engine": copyleaks.get("engine", "Copyleaks AI Neural Engine v3 + Google E-E-A-T"),
        "verdict": f"{composite_human}% Human (Copyleaks: {copyleaks_human}%, Undetectable: {undetectable_human}%)"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
