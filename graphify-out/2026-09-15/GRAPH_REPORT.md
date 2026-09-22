# Graph Report - yatradham-seo-pipeline  (2026-09-15)

## Corpus Check
- 43 files · ~92,428 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 666 nodes · 1367 edges · 56 communities (42 shown, 14 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 53 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cd4f793f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- RateLimitingMiddleware
- test_e2e_suite.py
- enrich_destination_data
- test_puja_pipeline_live.py
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- post
- qa_agent.py
- batch_process
- validation_layer.py
- scraper.py
- nlp_and_safety_toolkit.py
- localize_content
- content_creator_agent.py
- get
- semrush_suite.py
- models.py
- process_package
- SitemapCrawler
- main.py
- LLMClient
- semrush_backlinks_endpoint
- keyword_agent.py
- meta_agent.py
- title_agent.py
- llm_client.py
- analyze_serp_endpoint
- semrush_backlink_gap_endpoint
- BaseModel
- check_serp_rank
- crawl_sitemap
- scrape_stealth_endpoint
- seo_toolkit.py
- quality_audit_endpoint
- get_output_serp_audit
- publish_to_wordpress
- validate_category
- semrush_site_performance_endpoint
- get_robots_txt
- semrush_position_tracking_endpoint
- semrush_sensor_endpoint
- batch_urls
- get_outputs
- semrush_ai_search_endpoint
- deepseek_reasoning_endpoint
- semrush_compare_domains_endpoint
- semrush_keyword_overview_endpoint
- get_audit_trail_endpoint
- get_single_output
- semrush_dashboard_endpoint
- semrush_topic_research_endpoint
- semrush_traffic_insights_endpoint

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 43 edges
2. `process_package()` - 26 edges
3. `PackageInput` - 19 edges
4. `run_suite()` - 19 edges
5. `SEOOutput` - 17 edges
6. `clean_domain_name()` - 16 edges
7. `extract_package_data()` - 15 edges
8. `is_safe_url()` - 15 edges
9. `fetch_url_html()` - 14 edges
10. `get_domain_overview()` - 14 edges

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

## Communities (56 total, 14 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "RateLimitingMiddleware"
Cohesion: 0.29
Nodes (6): BaseHTTPMiddleware, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, SecurityHeadersMiddleware

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.07
Nodes (56): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output() (+48 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.09
Nodes (28): enrich_destination_endpoint(), get_forex_rates_endpoint(), get_serp_intelligence_endpoint(), get_transit_distance_endpoint(), Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, Calculate driving distance and duration via Open Source Routing Machine (OSRM)., Return live search intent, LSI keyword entities, and competitor heading… (+20 more)

### Community 4 - "test_puja_pipeline_live.py"
Cohesion: 0.24
Nodes (10): extract_package_data(), Any, Extract package metadata, category, and raw text for LLM processing with robust…, Verify live scraping of Puja at Dwarka accurately extracts destination, price,…, Verify end-to-end processing generates complete sections, >=85 QA score, and no…, Verify admin endpoints accept valid admin key and same-origin requests while…, test_admin_endpoints_authorization(), test_puja_at_dwarka_scraping() (+2 more)

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "post"
Cohesion: 0.15
Nodes (14): bulk_action(), clear_cache(), moderate_text_endpoint(), proofread_endpoint(), ProviderSettingsRequest, Bulk approve or reject outputs with admin authorization., Wipe all outputs from the database to start fresh (Protected Admin Action)., Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime… (+6 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 12 - "batch_process"
Cohesion: 0.40
Nodes (5): Exception, batch_process(), Process multiple packages from JSON (Admin Protected, Max 25 items)., Sanitizes raw python exception traces for public consumption., sanitize_error_detail()

### Community 13 - "validation_layer.py"
Cohesion: 0.15
Nodes (19): check_duplicate_content(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Extract the numeric ₹ amount from a string like 'Starting From ₹ 13,125.00 Per…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'. (+11 more)

### Community 14 - "scraper.py"
Cohesion: 0.15
Nodes (15): _extract_numeric_price(), Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string(), normalize_duration_string(), Extract structured data from Yatradham HTML pages. (+7 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.10
Nodes (21): analyze_keywords_endpoint(), get_dictionary_endpoint(), link_safety_preview_endpoint(), Any, field_validator, Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Extract top unigrams, bigrams, trigrams & Flesch reading score., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview. (+13 more)

### Community 16 - "localize_content"
Cohesion: 0.40
Nodes (4): localize_content(), Any, Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)., Translate and culturally localize SEOOutput sections into Hindi or Gujarati.

### Community 17 - "content_creator_agent.py"
Cohesion: 0.08
Nodes (24): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+16 more)

### Community 18 - "get"
Cohesion: 0.12
Nodes (16): get, export_csv_endpoint(), favicon(), get_providers_status(), Semrush Top Pages Traffic Share., Semrush Keyword Strategy Builder: Topic clusters & pillar architecture., Semrush Backlink Audit: Toxicity score and disavow candidates., Semrush Local SEO: 3-Pack rank potential & GBP audit. (+8 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.05
Nodes (74): fetch_url_html(), Scrapling-Powered Modern Scraping & DOM Parsing Engine for YatraDham SEO…, Fetch URL with SSRF protection, browser TLS fingerprint spoofing (curl_cffi…, clean_domain_name(), detect_domain_category(), extract_brand_tokens(), fetch_live_google_suggest(), get_ai_search_overview() (+66 more)

### Community 20 - "models.py"
Cohesion: 0.05
Nodes (44): HTTPAuthorizationCredentials, LogRecord, root(), BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation (+36 more)

### Community 21 - "process_package"
Cohesion: 0.15
Nodes (17): get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…, process_batch_background(), process_single(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, Process a single package through all 5 agents (manual JSON input)., scrape_and_process() (+9 more)

### Community 22 - "SitemapCrawler"
Cohesion: 0.10
Nodes (20): detect_url_category(), Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'., Any, Prioritizes bookable pilgrimage packages, destination stays, pujas, and…, Accurately classifies discovered links into stay, tour, wellness, or puja., Derives a clean human-readable title from URL segments when anchor text is…, Parses XML sitemaps with namespace stripping, index recursing, and regex…, Parses HTML category pages, capturing clean anchor titles and canonical URLs. (+12 more)

### Community 23 - "main.py"
Cohesion: 0.13
Nodes (20): FastAPI, check_ai_endpoint(), CheckAIRequest, humanize_endpoint(), humanize_markdown_content(), humanize_single_chunk(), HumanizeRequest, lifespan() (+12 more)

### Community 24 - "LLMClient"
Cohesion: 0.17
Nodes (9): LLMClient, Any, Execute DeepSeek two-stage reasoning protocol: 1. Stage 1 (<thinking>): Deep…, Allow setting runtime keys dynamically for a request without server restart., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., Strip internal thinking/reasoning tags leaked from thinking models., Return a rich, dynamic response when no LLM provider key is available.… (+1 more)

### Community 25 - "semrush_backlinks_endpoint"
Cohesion: 0.18
Nodes (12): api_route, Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,…, Semrush Backlink Analytics: Authority Score, Referring Domains, Dofollow Ratio,…, semrush_backlinks_endpoint(), semrush_domain_overview_endpoint(), semrush_keyword_magic_endpoint() (+4 more)

### Community 26 - "keyword_agent.py"
Cohesion: 0.50
Nodes (3): Any, Keyword agent: enforces 2-4 word primary keyword., run()

### Community 27 - "meta_agent.py"
Cohesion: 0.50
Nodes (3): Any, Meta description agent: 145-155 chars, natural language, no repetition., run()

### Community 28 - "title_agent.py"
Cohesion: 0.50
Nodes (3): Any, Title tag agent: 50-60 chars, optimized for click-through rate with accurate…, run()

### Community 29 - "llm_client.py"
Cohesion: 0.25
Nodes (9): _extract_json_from_response(), get_category_aware_fallback(), Any, Content agent: generates all 19 structured sections from scraped page data., Generates complete, enterprise-grade 19 sections strictly adhering to category…, Robustly extract JSON from LLM response, handling markdown blocks and…, run(), clean_price_string() (+1 more)

### Community 30 - "analyze_serp_endpoint"
Cohesion: 0.67
Nodes (3): analyze_serp_endpoint(), Native SERP Competitor & Information Gain Analyzer endpoint. Scrapes live SERP…, SERPAnalyzeRequest

### Community 31 - "semrush_backlink_gap_endpoint"
Cohesion: 0.40
Nodes (5): Semrush Keyword Gap: Identifies shared, missing, and untapped ranking…, Semrush Backlink Gap: Find link opportunities., semrush_backlink_gap_endpoint(), semrush_keyword_gap_endpoint(), SemrushGapRequest

### Community 32 - "BaseModel"
Cohesion: 0.20
Nodes (10): ContentGenerateRequest, generate_content(), localize(), LocalizeRequest, BaseModel, Generate net-new SEO content from scratch using AI., Translate and localize generated SEO content into Hindi or Gujarati., Verify WordPress credentials and REST API availability (Admin Protected). (+2 more)

### Community 33 - "check_serp_rank"
Cohesion: 0.17
Nodes (13): get_seo_audit_score_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., audit_onpage_seo_score(), check_serp_rank() (+5 more)

### Community 34 - "crawl_sitemap"
Cohesion: 0.67
Nodes (3): crawl_sitemap(), Crawl an XML Sitemap or Category Landing Page to extract package links with…, SitemapCrawlRequest

### Community 35 - "scrape_stealth_endpoint"
Cohesion: 0.67
Nodes (3): Scrapling + curl_cffi Chrome 124 stealth scrape with deep JSON-LD extraction., scrape_stealth_endpoint(), StealthScrapeRequest

### Community 36 - "seo_toolkit.py"
Cohesion: 0.20
Nodes (9): get_screenshot_preview_endpoint(), get_seo_tags_generator_endpoint(), Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), generate_seo_tags(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 37 - "quality_audit_endpoint"
Cohesion: 0.67
Nodes (3): quality_audit_endpoint(), QualityAuditRequest, Enterprise 100M-scale content quality, safety, readability, and AI-slop auditor.

### Community 39 - "publish_to_wordpress"
Cohesion: 0.67
Nodes (3): publish_to_wordpress(), Publish generated SEO content directly to WordPress (Admin Protected)., WpPublishRequest

### Community 40 - "validate_category"
Cohesion: 0.67
Nodes (3): Validate if the selected category matches the target URL., validate_category(), ValidateCategoryRequest

### Community 45 - "batch_urls"
Cohesion: 0.50
Nodes (4): BackgroundTasks, batch_urls(), BatchURLRequest, Scrape and process multiple URLs automatically in the background (Admin…

### Community 50 - "deepseek_reasoning_endpoint"
Cohesion: 0.67
Nodes (3): deepseek_reasoning_endpoint(), DeepSeekReasonRequest, DeepSeek two-stage reasoning protocol with chain-of-thought verification.

### Community 51 - "semrush_compare_domains_endpoint"
Cohesion: 0.67
Nodes (3): Semrush Compare Domains (Multi-domain benchmark)., semrush_compare_domains_endpoint(), SemrushCompareRequest

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `BaseModel`, `test_e2e_suite.py`, `test_puja_pipeline_live.py`, `qa_agent.py`, `localize_content`, `content_creator_agent.py`, `deepseek_reasoning_endpoint`, `process_package`, `main.py`, `keyword_agent.py`, `meta_agent.py`, `title_agent.py`, `llm_client.py`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `process_package`, `main.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `process_package()` connect `process_package` to `test_e2e_suite.py`, `test_puja_pipeline_live.py`, `qa_agent.py`, `batch_process`, `validation_layer.py`, `models.py`, `main.py`, `LLMClient`, `keyword_agent.py`, `llm_client.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._