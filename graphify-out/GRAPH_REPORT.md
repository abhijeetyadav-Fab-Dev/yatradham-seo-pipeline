# Graph Report - yatradham-seo-pipeline  (2026-09-14)

## Corpus Check
- 42 files · ~89,422 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 646 nodes · 1326 edges · 60 communities (48 shown, 12 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 53 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2f09fa9d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- RateLimitingMiddleware
- test_e2e_suite.py
- enrich_destination_data
- ProviderSettingsRequest
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- post
- qa_agent.py
- batch_process
- validation_layer.py
- extract_package_data
- nlp_and_safety_toolkit.py
- audit_onpage_seo_score
- TestArchitecturalDecoupling
- get
- semrush_suite.py
- security_firewall.py
- process_package
- SitemapCrawler
- main.py
- .chat_completion
- semrush_backlinks_endpoint
- sanitize_user_prompt
- BaseModel
- models.py
- LLMClient
- .test_provider
- crawl_sitemap
- localize
- check_serp_rank
- enforce_rate_limit
- analyze_keywords_endpoint
- seo_toolkit.py
- quality_audit_endpoint
- get_providers_status
- test_all_products_integrity.py
- validate_category
- semrush_site_performance_endpoint
- verify_wordpress_connection
- semrush_top_pages_endpoint
- generate_json_ld
- batch_urls
- get_outputs
- semrush_local_seo_endpoint
- get_smart_internal_links
- SensitiveDataScrubberFilter
- deepseek_reasoning_endpoint
- semrush_compare_domains_endpoint
- scrape_stealth_endpoint
- OutputUpdateRequest
- favicon
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
9. `get_domain_overview()` - 14 edges
10. `run_validation()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py
- `_row_to_output()` --uses--> `PackageInput`  [INFERRED]
  database.py → models.py

## Import Cycles
- None detected.

## Communities (60 total, 12 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "RateLimitingMiddleware"
Cohesion: 0.25
Nodes (7): BaseHTTPMiddleware, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, root(), SecurityHeadersMiddleware

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.06
Nodes (68): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+60 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.09
Nodes (28): enrich_destination_endpoint(), get_forex_rates_endpoint(), get_serp_intelligence_endpoint(), get_transit_distance_endpoint(), Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, Calculate driving distance and duration via Open Source Routing Machine (OSRM)., Return live search intent, LSI keyword entities, and competitor heading… (+20 more)

### Community 4 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime…, Test a provider API key live and return latency & status (Admin Protected)., test_provider_endpoint(), update_provider_settings()

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "post"
Cohesion: 0.15
Nodes (15): bulk_action(), check_ai_endpoint(), humanize_endpoint(), moderate_text_endpoint(), proofread_endpoint(), query_undetectable_detector(), Semrush Keyword Gap: Identifies shared, missing, and untapped ranking…, Semrush Backlink Gap: Find link opportunities. (+7 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 12 - "batch_process"
Cohesion: 0.33
Nodes (6): Exception, batch_process(), Process multiple packages from JSON (Admin Protected, Max 25 items)., BatchRequest, Sanitizes raw python exception traces for public consumption., sanitize_error_detail()

### Community 13 - "validation_layer.py"
Cohesion: 0.13
Nodes (21): check_duplicate_content(), compute_objective_qa_score(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'. (+13 more)

### Community 14 - "extract_package_data"
Cohesion: 0.11
Nodes (22): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+14 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.15
Nodes (16): get_dictionary_endpoint(), link_safety_preview_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview., analyze_keywords_and_readability(), analyze_sentiment_and_moderation(), inspect_url_safety_and_preview(), lookup_word_dictionary() (+8 more)

### Community 16 - "audit_onpage_seo_score"
Cohesion: 0.22
Nodes (9): get_seo_audit_score_endpoint(), get_seo_tags_generator_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., audit_onpage_seo_score(), generate_seo_tags(), Any, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 17 - "TestArchitecturalDecoupling"
Cohesion: 0.12
Nodes (9): Architectural Decoupling & Zero-Leakage Verification Suite Ensures that all…, Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio… (+1 more)

### Community 18 - "get"
Cohesion: 0.12
Nodes (17): get, export_csv_endpoint(), get_robots_txt(), Semrush Position Tracking with Winners & Losers., Semrush Keyword Overview: Deep-dive search volume, global breakdown, KD%., Semrush Keyword Strategy Builder: Topic clusters & pillar architecture., Semrush Backlink Audit: Toxicity score and disavow candidates., Semrush Sensor: Google SERP Volatility gauge. (+9 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.08
Nodes (54): clean_domain_name(), detect_domain_category(), extract_brand_tokens(), fetch_live_google_suggest(), get_ai_search_overview(), get_backlink_audit(), get_backlink_gap(), get_backlink_overview() (+46 more)

### Community 20 - "security_firewall.py"
Cohesion: 0.16
Nodes (11): decrypt_secret(), _derive_key(), encrypt_secret(), InMemoryRateLimiter, mask_secret(), Enterprise Security Firewall & Hardening Layer for YatraDham SEO Pipeline.…, Token-bucket rate limiter enforcing max requests per window per IP., Return a masked representation of sensitive keys for logs and UI. (+3 more)

### Community 21 - "process_package"
Cohesion: 0.14
Nodes (20): process_batch_background(), process_single(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, Process a single package through all 5 agents (manual JSON input)., scrape_and_process(), PackageInput, process_package(), Run the full pipeline on a single package with parallel agent execution and… (+12 more)

### Community 22 - "SitemapCrawler"
Cohesion: 0.10
Nodes (18): Any, Prioritizes bookable pilgrimage packages, destination stays, pujas, and…, Accurately classifies discovered links into stay, tour, wellness, or puja., Derives a clean human-readable title from URL segments when anchor text is…, Parses XML sitemaps with namespace stripping, index recursing, and regex…, Parses HTML category pages, capturing clean anchor titles and canonical URLs., Crawls an XML Sitemap (single or index, including .gz) or an HTML Category Hub.…, SitemapCrawler (+10 more)

### Community 23 - "main.py"
Cohesion: 0.19
Nodes (12): clear_all_outputs(), FastAPI, clear_cache(), lifespan(), publish_to_wordpress(), FastAPI server with .env auto-loading, URL auto-scraping, batch processing,…, Wipe all outputs from the database to start fresh (Protected Admin Action)., Publish generated SEO content directly to WordPress (Admin Protected). (+4 more)

### Community 24 - ".chat_completion"
Cohesion: 0.20
Nodes (6): clean_price_string(), Any, Execute DeepSeek two-stage reasoning protocol: 1. Stage 1 (<thinking>): Deep…, Strip internal thinking/reasoning tags leaked from thinking models., Return a rich, dynamic response when no LLM provider key is available.…, Sanitize and format price strings cleanly. Never return hardcoded mock numbers…

### Community 25 - "semrush_backlinks_endpoint"
Cohesion: 0.18
Nodes (12): api_route, Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,…, Semrush Backlink Analytics: Authority Score, Referring Domains, Dofollow Ratio,…, semrush_backlinks_endpoint(), semrush_domain_overview_endpoint(), semrush_keyword_magic_endpoint() (+4 more)

### Community 26 - "sanitize_user_prompt"
Cohesion: 0.20
Nodes (9): Any, field_validator, check_disallowed_xss_patterns(), Any, Sanitizes user instructions and checks for active prompt injection attacks., Raises ValueError (resulting in 422 HTTP status) if dangerous XSS payloads are…, Enterprise HTML & Script Sanitizer: Strips all HTML tags, script elements,…, sanitize_user_prompt() (+1 more)

### Community 27 - "BaseModel"
Cohesion: 0.17
Nodes (12): CheckAIRequest, ContentGenerateRequest, generate_content(), HumanizeRequest, BaseModel, Semrush SEO Writing Assistant: Readability, SEO score, tone of voice., Semrush On-Page SEO Checker: Actionable strategy, backlink, UX recommendations., Generate net-new SEO content from scratch using AI. (+4 more)

### Community 28 - "models.py"
Cohesion: 0.31
Nodes (10): BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights, ProgramSession, BaseModel (+2 more)

### Community 29 - "LLMClient"
Cohesion: 0.14
Nodes (19): _extract_json_from_response(), get_category_aware_fallback(), Any, Content agent: generates all 19 structured sections from scraped page data., Generates complete, enterprise-grade 19 sections strictly adhering to category…, Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any (+11 more)

### Community 30 - ".test_provider"
Cohesion: 0.25
Nodes (4): Allow setting runtime keys dynamically for a request without server restart., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., OpenAI

### Community 31 - "crawl_sitemap"
Cohesion: 0.67
Nodes (3): crawl_sitemap(), Crawl an XML Sitemap or Category Landing Page to extract package links with…, SitemapCrawlRequest

### Community 32 - "localize"
Cohesion: 0.33
Nodes (6): localize_content(), Any, Translate and culturally localize SEOOutput sections into Hindi or Gujarati., localize(), LocalizeRequest, Translate and localize generated SEO content into Hindi or Gujarati.

### Community 33 - "check_serp_rank"
Cohesion: 0.25
Nodes (8): get_serp_rank_endpoint(), get_serp_search_endpoint(), Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., check_serp_rank(), fetch_serp_results(), Fetch live Google SERP organic rankings and People Also Ask questions.…, Check the current Google SERP ranking position of target_domain for a given…

### Community 34 - "enforce_rate_limit"
Cohesion: 0.33
Nodes (6): HTTPAuthorizationCredentials, enforce_rate_limit(), Request, FastAPI dependency to rate-limit requests by client IP., Verifies that the caller has valid administrative access. Allows request if: -…, verify_admin_access()

### Community 35 - "analyze_keywords_endpoint"
Cohesion: 0.33
Nodes (5): analyze_keywords_endpoint(), Any, field_validator, Extract top unigrams, bigrams, trigrams & Flesch reading score., URLRequest

### Community 36 - "seo_toolkit.py"
Cohesion: 0.33
Nodes (5): get_screenshot_preview_endpoint(), Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generate live website screenshot preview URLs. Uses ScreenshotOne API if key…

### Community 37 - "quality_audit_endpoint"
Cohesion: 0.67
Nodes (3): quality_audit_endpoint(), QualityAuditRequest, Enterprise 100M-scale content quality, safety, readability, and AI-slop auditor.

### Community 39 - "test_all_products_integrity.py"
Cohesion: 0.50
Nodes (4): parametrize, Verify that all 4 product categories generate 100% complete, verified,…, test_product_category_pipeline_integrity(), validate_no_duplicated_words()

### Community 40 - "validate_category"
Cohesion: 0.67
Nodes (3): Validate if the selected category matches the target URL., validate_category(), ValidateCategoryRequest

### Community 42 - "verify_wordpress_connection"
Cohesion: 0.67
Nodes (3): Verify WordPress credentials and REST API availability (Admin Protected)., verify_wordpress_connection(), WpVerifyRequest

### Community 44 - "generate_json_ld"
Cohesion: 0.40
Nodes (4): generate_json_ld(), Any, Schema.org JSON-LD Structured Data Generator for YatraDham Packages., Generate comprehensive stacked Schema.org JSON-LD for Google Rich Results, SGE…

### Community 45 - "batch_urls"
Cohesion: 0.50
Nodes (4): BackgroundTasks, batch_urls(), BatchURLRequest, Scrape and process multiple URLs automatically in the background (Admin…

### Community 48 - "get_smart_internal_links"
Cohesion: 0.50
Nodes (3): get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…

### Community 49 - "SensitiveDataScrubberFilter"
Cohesion: 0.50
Nodes (3): LogRecord, Logging filter that redacts API keys, passwords, and tokens before writing to…, SensitiveDataScrubberFilter

### Community 50 - "deepseek_reasoning_endpoint"
Cohesion: 0.67
Nodes (3): deepseek_reasoning_endpoint(), DeepSeekReasonRequest, DeepSeek two-stage reasoning protocol with chain-of-thought verification.

### Community 51 - "semrush_compare_domains_endpoint"
Cohesion: 0.67
Nodes (3): Semrush Compare Domains (Multi-domain benchmark)., semrush_compare_domains_endpoint(), SemrushCompareRequest

### Community 52 - "scrape_stealth_endpoint"
Cohesion: 0.67
Nodes (3): Scrapling + curl_cffi Chrome 124 stealth scrape with deep JSON-LD extraction., scrape_stealth_endpoint(), StealthScrapeRequest

### Community 53 - "OutputUpdateRequest"
Cohesion: 0.67
Nodes (3): Config, OutputUpdateRequest, BaseModel

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `localize`, `test_e2e_suite.py`, `test_all_products_integrity.py`, `qa_agent.py`, `TestArchitecturalDecoupling`, `deepseek_reasoning_endpoint`, `process_package`, `main.py`, `.chat_completion`, `.test_provider`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `process_package`, `test_all_products_integrity.py`, `LLMClient`, `main.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `process_package()` connect `process_package` to `test_e2e_suite.py`, `test_all_products_integrity.py`, `qa_agent.py`, `batch_process`, `generate_json_ld`, `extract_package_data`, `validation_layer.py`, `get_smart_internal_links`, `main.py`, `sanitize_user_prompt`, `LLMClient`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._