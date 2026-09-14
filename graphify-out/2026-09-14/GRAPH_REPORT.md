# Graph Report - yatradham-seo-pipeline  (2026-09-14)

## Corpus Check
- 41 files · ~90,007 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 642 nodes · 1312 edges · 49 communities (40 shown, 9 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `db401ff6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- RateLimitingMiddleware
- database.py
- enrich_destination_data
- ProviderSettingsRequest
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- post
- qa_agent.py
- batch_process
- validation_layer.py
- PackageInput
- nlp_and_safety_toolkit.py
- seo_toolkit.py
- TestArchitecturalDecoupling
- get
- semrush_suite.py
- models.py
- test_e2e_suite.py
- SitemapCrawler
- main.py
- LLMClient
- semrush_backlinks_endpoint
- semrush_backlink_gap_endpoint
- BaseModel
- get_forex_rates_endpoint
- pipeline.py
- fetch_transit_distance_osrm
- crawl_sitemap
- localize
- semrush_on_page_checker_endpoint
- localize_content
- meta_agent.py
- title_agent.py
- quality_audit_endpoint
- get_providers_status
- semrush_writing_assistant_endpoint
- validate_category
- semrush_site_performance_endpoint
- verify_wordpress_connection
- semrush_top_pages_endpoint
- semrush_sensor_endpoint
- semrush_backlink_audit_endpoint
- get_outputs
- semrush_local_seo_endpoint
- temple_intel_endpoint

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 41 edges
2. `process_package()` - 24 edges
3. `run_suite()` - 19 edges
4. `PackageInput` - 17 edges
5. `SEOOutput` - 17 edges
6. `clean_domain_name()` - 16 edges
7. `extract_package_data()` - 15 edges
8. `is_safe_url()` - 15 edges
9. `get_domain_overview()` - 14 edges
10. `SectionedContent` - 13 edges

## Surprising Connections (you probably didn't know these)
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_agent.py → llm_client.py
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/keyword_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/meta_agent.py → llm_client.py

## Import Cycles
- None detected.

## Communities (49 total, 9 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "RateLimitingMiddleware"
Cohesion: 0.25
Nodes (7): BaseHTTPMiddleware, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, root(), SecurityHeadersMiddleware

### Community 2 - "database.py"
Cohesion: 0.07
Nodes (51): bulk_update_status(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output(), get_stats() (+43 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.18
Nodes (16): get_serp_intelligence_endpoint(), Return live search intent, LSI keyword entities, and competitor heading…, enrich_destination_data(), fetch_climate_and_weather(), fetch_semantic_lsi_keywords(), fetch_solar_timings(), fetch_spiritual_heritage_facts(), geocode_location() (+8 more)

### Community 4 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime…, Test a provider API key live and return latency & status (Admin Protected)., test_provider_endpoint(), update_provider_settings()

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "post"
Cohesion: 0.14
Nodes (14): BackgroundTasks, batch_urls(), BatchURLRequest, bulk_action(), moderate_text_endpoint(), proofread_endpoint(), Semrush Compare Domains (Multi-domain benchmark)., Scrape and process multiple URLs automatically in the background (Admin… (+6 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 12 - "batch_process"
Cohesion: 0.29
Nodes (7): Exception, batch_process(), process_single(), Process a single package through all 5 agents (manual JSON input)., Process multiple packages from JSON (Admin Protected, Max 25 items)., Sanitizes raw python exception traces for public consumption., sanitize_error_detail()

### Community 13 - "validation_layer.py"
Cohesion: 0.15
Nodes (19): check_duplicate_content(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'., Compare one section (e.g. 'why_choose_bullets') of the new row against the same… (+11 more)

### Community 14 - "PackageInput"
Cohesion: 0.07
Nodes (41): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), process_batch_background(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, Scrapling + curl_cffi Chrome 124 stealth scrape with deep JSON-LD extraction., scrape_and_process() (+33 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.10
Nodes (21): analyze_keywords_endpoint(), get_dictionary_endpoint(), link_safety_preview_endpoint(), Any, field_validator, Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Extract top unigrams, bigrams, trigrams & Flesch reading score., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview. (+13 more)

### Community 16 - "seo_toolkit.py"
Cohesion: 0.10
Nodes (22): get_screenshot_preview_endpoint(), get_seo_audit_score_endpoint(), get_seo_tags_generator_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword. (+14 more)

### Community 17 - "TestArchitecturalDecoupling"
Cohesion: 0.12
Nodes (9): Architectural Decoupling & Zero-Leakage Verification Suite Ensures that all…, Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio… (+1 more)

### Community 18 - "get"
Cohesion: 0.10
Nodes (21): get, enrich_destination_endpoint(), export_csv_endpoint(), favicon(), get_audit_trail_endpoint(), get_robots_txt(), get_single_output(), Semrush Consolidated Dashboard. (+13 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.07
Nodes (58): Semrush Keyword Overview: Deep-dive search volume, global breakdown, KD%., Semrush Keyword Strategy Builder: Topic clusters & pillar architecture., Semrush Topic Research: Mindmap cards, questions, and high-CTR headlines., semrush_keyword_overview_endpoint(), semrush_keyword_strategy_endpoint(), semrush_topic_research_endpoint(), clean_domain_name(), detect_domain_category() (+50 more)

### Community 20 - "models.py"
Cohesion: 0.05
Nodes (43): HTTPAuthorizationCredentials, LogRecord, BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow (+35 more)

### Community 21 - "test_e2e_suite.py"
Cohesion: 0.19
Nodes (18): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+10 more)

### Community 22 - "SitemapCrawler"
Cohesion: 0.10
Nodes (20): detect_url_category(), Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'., Any, Prioritizes bookable pilgrimage packages, destination stays, pujas, and…, Accurately classifies discovered links into stay, tour, wellness, or puja., Derives a clean human-readable title from URL segments when anchor text is…, Parses XML sitemaps with namespace stripping, index recursing, and regex…, Parses HTML category pages, capturing clean anchor titles and canonical URLs. (+12 more)

### Community 23 - "main.py"
Cohesion: 0.19
Nodes (14): clear_all_outputs(), FastAPI, check_ai_endpoint(), CheckAIRequest, clear_cache(), humanize_endpoint(), humanize_markdown_content(), humanize_single_chunk() (+6 more)

### Community 24 - "LLMClient"
Cohesion: 0.15
Nodes (11): clean_price_string(), LLMClient, Any, Execute DeepSeek two-stage reasoning protocol: 1. Stage 1 (<thinking>): Deep…, Allow setting runtime keys dynamically for a request without server restart., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., Strip internal thinking/reasoning tags leaked from thinking models. (+3 more)

### Community 25 - "semrush_backlinks_endpoint"
Cohesion: 0.18
Nodes (12): api_route, Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,…, Semrush Backlink Analytics: Authority Score, Referring Domains, Dofollow Ratio,…, semrush_backlinks_endpoint(), semrush_domain_overview_endpoint(), semrush_keyword_magic_endpoint() (+4 more)

### Community 26 - "semrush_backlink_gap_endpoint"
Cohesion: 0.40
Nodes (5): Semrush Keyword Gap: Identifies shared, missing, and untapped ranking…, Semrush Backlink Gap: Find link opportunities., semrush_backlink_gap_endpoint(), semrush_keyword_gap_endpoint(), SemrushGapRequest

### Community 27 - "BaseModel"
Cohesion: 0.14
Nodes (14): ContentGenerateRequest, deepseek_reasoning_endpoint(), DeepSeekReasonRequest, generate_content(), publish_to_wordpress(), BaseModel, Generate net-new SEO content from scratch using AI., Publish generated SEO content directly to WordPress (Admin Protected). (+6 more)

### Community 28 - "get_forex_rates_endpoint"
Cohesion: 0.50
Nodes (4): get_forex_rates_endpoint(), Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, convert_inr_to_forex(), Convert INR package pricing to major international currencies using Frankfurter…

### Community 29 - "pipeline.py"
Cohesion: 0.13
Nodes (18): _extract_json_from_response(), get_category_aware_fallback(), Any, Content agent: generates all 19 structured sections from scraped page data., Generates complete, enterprise-grade 19 sections strictly adhering to category…, Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any (+10 more)

### Community 30 - "fetch_transit_distance_osrm"
Cohesion: 0.50
Nodes (4): get_transit_distance_endpoint(), Calculate driving distance and duration via Open Source Routing Machine (OSRM)., fetch_transit_distance_osrm(), Compute driving distance and travel duration via Open Source Routing Machine…

### Community 31 - "crawl_sitemap"
Cohesion: 0.67
Nodes (3): crawl_sitemap(), Crawl an XML Sitemap or Category Landing Page to extract package links with…, SitemapCrawlRequest

### Community 32 - "localize"
Cohesion: 0.67
Nodes (3): localize(), LocalizeRequest, Translate and localize generated SEO content into Hindi or Gujarati.

### Community 33 - "semrush_on_page_checker_endpoint"
Cohesion: 0.67
Nodes (3): Semrush On-Page SEO Checker: Actionable strategy, backlink, UX recommendations., semrush_on_page_checker_endpoint(), SemrushOnPageRequest

### Community 34 - "localize_content"
Cohesion: 0.40
Nodes (4): localize_content(), Any, Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)., Translate and culturally localize SEOOutput sections into Hindi or Gujarati.

### Community 35 - "meta_agent.py"
Cohesion: 0.50
Nodes (3): Any, Meta description agent: 145-155 chars, natural language, no repetition., run()

### Community 36 - "title_agent.py"
Cohesion: 0.50
Nodes (3): Any, Title tag agent: 50-60 chars, optimized for click-through rate with accurate…, run()

### Community 37 - "quality_audit_endpoint"
Cohesion: 0.67
Nodes (3): quality_audit_endpoint(), QualityAuditRequest, Enterprise 100M-scale content quality, safety, readability, and AI-slop auditor.

### Community 39 - "semrush_writing_assistant_endpoint"
Cohesion: 0.67
Nodes (3): Semrush SEO Writing Assistant: Readability, SEO score, tone of voice., semrush_writing_assistant_endpoint(), SemrushWritingAssistantRequest

### Community 40 - "validate_category"
Cohesion: 0.67
Nodes (3): Validate if the selected category matches the target URL., validate_category(), ValidateCategoryRequest

### Community 42 - "verify_wordpress_connection"
Cohesion: 0.67
Nodes (3): Verify WordPress credentials and REST API availability (Admin Protected)., verify_wordpress_connection(), WpVerifyRequest

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `localize`, `localize_content`, `meta_agent.py`, `title_agent.py`, `database.py`, `qa_agent.py`, `PackageInput`, `TestArchitecturalDecoupling`, `test_e2e_suite.py`, `main.py`, `BaseModel`, `pipeline.py`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `BaseModel`, `pipeline.py`, `main.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `SitemapCrawler` connect `SitemapCrawler` to `crawl_sitemap`, `main.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._