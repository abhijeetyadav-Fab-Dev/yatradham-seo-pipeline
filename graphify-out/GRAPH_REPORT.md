# Graph Report - yatradham-seo-pipeline  (2026-10-03)

## Corpus Check
- 55 files · ~131,314 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 910 nodes · 1839 edges · 63 communities (48 shown, 15 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 63 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `df1462ef`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- security_firewall.py
- test_e2e_suite.py
- enrich_destination_data
- de_slop_and_humanize
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- post
- anti_ai_guardrails.py
- audit_google_genai_compliance
- validation_layer.py
- scraper.py
- nlp_and_safety_toolkit.py
- TestHumanizer55Patterns
- content_creator_agent.py
- get
- semrush_suite.py
- test_transit_bottlenecks.py
- process_package
- SitemapCrawler
- ProviderSettingsRequest
- LLMClient
- api_route
- test_champion_benchmark_auditor.py
- TestArchitecturalDecoupling
- check_serp_rank
- humanize_endpoint
- generate_content
- pipeline.py
- is_safe_url
- qa_agent.py
- semrush_backlink_gap_endpoint
- run_seo_linter
- seo_toolkit.py
- check_google_genai_endpoint
- generate_transit_blueprint_endpoint
- get_outputs
- semrush_backlink_audit_endpoint
- BaseModel
- run_ai_seo_audit
- test_semrush_suite_endpoints.py
- semrush_site_performance_endpoint
- main.py
- get_audit_trail_endpoint
- semrush_keyword_magic_endpoint
- get_humanizer_patterns
- semrush_dashboard_endpoint
- semrush_sensor_endpoint
- semrush_ai_search_endpoint
- analyze_serp_endpoint
- get_smart_internal_links
- crawl_sitemap
- semrush_compare_domains_endpoint
- validate_category
- verify_wordpress_connection
- semrush_keyword_strategy_endpoint
- get_providers_status
- get_robots_txt
- semrush_position_tracking_endpoint
- semrush_topic_research_endpoint

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 50 edges
2. `process_package()` - 28 edges
3. `de_slop_and_humanize()` - 25 edges
4. `run_ai_seo_audit()` - 22 edges
5. `PackageInput` - 19 edges
6. `run_suite()` - 19 edges
7. `detect_55_patterns()` - 18 edges
8. `audit_google_genai_compliance()` - 17 edges
9. `SEOOutput` - 17 edges
10. `clean_domain_name()` - 16 edges

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
  agents/qa_agent.py → llm_client.py

## Import Cycles
- None detected.

## Communities (63 total, 15 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "security_firewall.py"
Cohesion: 0.06
Nodes (30): BaseHTTPMiddleware, HTTPAuthorizationCredentials, LogRecord, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, root() (+22 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.07
Nodes (61): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output() (+53 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.09
Nodes (28): enrich_destination_endpoint(), get_forex_rates_endpoint(), get_serp_intelligence_endpoint(), get_transit_distance_endpoint(), Return live search intent, LSI keyword entities, and competitor heading…, Destination intelligence fusing OSM Nominatim, Wikipedia, Open-Meteo, Sunrise-…, Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,… (+20 more)

### Community 4 - "de_slop_and_humanize"
Cohesion: 0.07
Nodes (24): apply_voice_transformations(), de_slop_and_humanize(), mask_protected_structures(), Masks markdown code blocks, tables, URLs, HTML tags, and template variables so…, Restores all protected structures exactly as they were., blader & Aboudjem Humanizer Rule: Transforms formulaic 'not only X, but also Y'…, Applies style-specific linguistic adjustments for the selected voice profile:…, Deterministic Anti-AI De-Slopper & Humanizer Pipeline: 1. Masks code blocks,… (+16 more)

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "post"
Cohesion: 0.12
Nodes (17): BackgroundTasks, batch_urls(), BatchURLRequest, check_transit_guardrails_endpoint(), clear_cache(), moderate_text_endpoint(), proofread_endpoint(), quality_audit_endpoint() (+9 more)

### Community 11 - "anti_ai_guardrails.py"
Cohesion: 0.15
Nodes (20): calculate_burstiness_metrics(), calculate_copyleaks_metrics(), check_copyleaks_api(), detect_55_patterns(), detect_ai_isms(), generate_copyleaks_recommendations(), Any, Anti-AI Guardrails Engine & Advanced Humanizer Suite Integrates: 1.… (+12 more)

### Community 12 - "audit_google_genai_compliance"
Cohesion: 0.10
Nodes (31): audit_google_genai_compliance(), check_eeat_firsthand_experience(), check_factual_accuracy_and_hallucinations(), check_humanizer_and_anti_slop(), check_metadata_and_structured_data(), check_scaled_content_abuse(), check_transparency_who_how_why(), extract_plain_text() (+23 more)

### Community 13 - "validation_layer.py"
Cohesion: 0.13
Nodes (21): check_duplicate_content(), compute_objective_qa_score(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Extract the numeric ₹ amount from a string like 'Starting From ₹ 13,125.00 Per… (+13 more)

### Community 14 - "scraper.py"
Cohesion: 0.13
Nodes (17): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+9 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.07
Nodes (28): analyze_keywords_endpoint(), get_dictionary_endpoint(), link_safety_preview_endpoint(), Any, field_validator, Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Extract top unigrams, bigrams, trigrams & Flesch reading score., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview. (+20 more)

### Community 16 - "TestHumanizer55Patterns"
Cohesion: 0.12
Nodes (9): Verify that all 55 patterns are defined, detectable, and actionable., Ensure all 55 patterns (P01 through P55) are correctly registered., P01: Detects 'stands as a testament to' and 'pivotal role'., P13: Detects em-dash overuse., P09: Detects 'not only X, but also Y'., P03: Detects trailing -ing phrases., P18: Detects chatbot residue like 'Certainly! Here is a guide'., P20: Detects 'In today's fast-paced world' and 'When it comes to'. (+1 more)

### Community 17 - "content_creator_agent.py"
Cohesion: 0.06
Nodes (52): _clean_markdown(), _detect_blog_intent(), _generate_long_form_blog(), _get_intent_structure(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2… (+44 more)

### Community 18 - "get"
Cohesion: 0.11
Nodes (18): get, export_csv_endpoint(), favicon(), get_champion_benchmark_profile_endpoint(), get_single_output(), Returns the gold-standard benchmark profile extracted from the #1 Ro-Pax…, Semrush Top Pages Traffic Share., Serve favicon directly for root browser icon requests. (+10 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.08
Nodes (54): clean_domain_name(), detect_domain_category(), extract_brand_tokens(), fetch_live_google_suggest(), get_ai_search_overview(), get_backlink_audit(), get_backlink_gap(), get_backlink_overview() (+46 more)

### Community 20 - "test_transit_bottlenecks.py"
Cohesion: 0.15
Nodes (19): get_transit_bottlenecks_catalog_endpoint(), Returns the catalog of all pre-indexed high-intent pilgrimage transit…, Unit & Integration Tests for High-Intent Pilgrimage Transit Bottlenecks Engine…, test_calculate_bottleneck_intensity(), test_generate_transit_champion_blueprint(), test_transit_bottleneck_catalog_integrity(), test_validate_transit_bottleneck_guardrails(), calculate_bottleneck_intensity() (+11 more)

### Community 21 - "process_package"
Cohesion: 0.22
Nodes (13): Any, run(), PackageInput, parametrize, process_package(), Run the full pipeline on a single package with parallel agent execution and…, Verify that all 4 product categories generate 100% complete, verified,…, test_product_category_pipeline_integrity() (+5 more)

### Community 22 - "SitemapCrawler"
Cohesion: 0.09
Nodes (21): detect_url_category(), Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'., Any, Prioritizes bookable pilgrimage packages, destination stays, pujas, and…, Accurately classifies discovered links into stay, tour, wellness, or puja., Derives a clean human-readable title from URL segments when anchor text is…, Parses XML sitemaps with namespace stripping, index recursing, and regex…, Parses HTML category pages, capturing clean anchor titles and canonical URLs. (+13 more)

### Community 23 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime…, Test a provider API key live and return latency & status (Admin Protected)., test_provider_endpoint(), update_provider_settings()

### Community 24 - "LLMClient"
Cohesion: 0.12
Nodes (14): Any, run(), Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)., clean_price_string(), LLMClient, Any, Execute DeepSeek two-stage reasoning protocol: 1. Stage 1 (<thinking>): Deep…, Allow setting runtime keys dynamically for a request without server restart. (+6 more)

### Community 25 - "api_route"
Cohesion: 0.12
Nodes (18): api_route, AIVisibilityRequest, ChampionBenchmarkRequest, check_champion_benchmark_endpoint(), get_ai_visibility_audit_endpoint(), Dedicated AI-Visibility & Generative Engine Optimization (GEO) Audit Endpoint.…, Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,… (+10 more)

### Community 26 - "test_champion_benchmark_auditor.py"
Cohesion: 0.16
Nodes (13): audit_champion_blog_benchmarks(), Any, Champion Blog Benchmark & Checkpoint Auditor…, Evaluates blog content against the 10 Golden Checkpoints of YatraDham's #1…, Unit & Integration Tests for Champion Blog Benchmark & Checkpoint Auditor…, Verify that superficial content with no tables, math, or fares fails., Verify FastAPI champion audit and champion profile endpoints., Verify that run_ai_seo_audit includes champion_benchmark in its output. (+5 more)

### Community 27 - "TestArchitecturalDecoupling"
Cohesion: 0.12
Nodes (9): Architectural Decoupling & Zero-Leakage Verification Suite Ensures that all…, Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio… (+1 more)

### Community 28 - "check_serp_rank"
Cohesion: 0.17
Nodes (13): get_seo_audit_score_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., audit_onpage_seo_score(), check_serp_rank() (+5 more)

### Community 29 - "humanize_endpoint"
Cohesion: 0.40
Nodes (5): humanize_endpoint(), humanize_markdown_content(), humanize_single_chunk(), query_undetectable_detector(), Humanize multi-section markdown text concurrently with 55-pattern de-slopper,…

### Community 30 - "generate_content"
Cohesion: 0.25
Nodes (8): ContentGenerateRequest, deepseek_reasoning_endpoint(), DeepSeekReasonRequest, generate_content(), DeepSeek two-stage reasoning protocol with chain-of-thought verification., Generate net-new SEO content from scratch using AI., Sanitizes user instructions and checks for active prompt injection attacks., sanitize_user_prompt()

### Community 31 - "pipeline.py"
Cohesion: 0.15
Nodes (15): _extract_json_from_response(), get_category_aware_fallback(), Any, Content agent: generates all 19 structured sections from scraped page data., Generates complete, enterprise-grade 19 sections strictly adhering to category…, Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Keyword agent: enforces 2-4 word primary keyword. (+7 more)

### Community 32 - "is_safe_url"
Cohesion: 0.17
Nodes (14): process_batch_background(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, scrape_and_process(), extract_package_data(), Any, Extract package metadata, category, and raw text for LLM processing with robust…, fetch_url_html(), Scrapling-Powered Modern Scraping & DOM Parsing Engine for YatraDham SEO… (+6 more)

### Community 33 - "qa_agent.py"
Cohesion: 0.36
Nodes (9): _check_banned(), _check_sections(), _check_sentences(), _extract_prose_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., Extract natural sentences from sections dictionary, skipping JSON syntax. (+1 more)

### Community 34 - "semrush_backlink_gap_endpoint"
Cohesion: 0.40
Nodes (5): Semrush Keyword Gap: Identifies shared, missing, and untapped ranking…, Semrush Backlink Gap: Find link opportunities., semrush_backlink_gap_endpoint(), semrush_keyword_gap_endpoint(), SemrushGapRequest

### Community 35 - "run_seo_linter"
Cohesion: 0.06
Nodes (29): Any, AI Visibility & Generative Engine Optimization (GEO / AEO) Module. Inspired by…, Simulates how an AI search engine (Perplexity / ChatGPT Search / SGE)…, simulate_ai_search_response(), Exception, fixture, localize_content(), Any (+21 more)

### Community 36 - "seo_toolkit.py"
Cohesion: 0.20
Nodes (9): get_screenshot_preview_endpoint(), get_seo_tags_generator_endpoint(), Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), generate_seo_tags(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 37 - "check_google_genai_endpoint"
Cohesion: 0.67
Nodes (3): check_google_genai_endpoint(), GoogleGenAIRequest, Google Search Guidance on Generative AI Content Compliance Checker.…

### Community 38 - "generate_transit_blueprint_endpoint"
Cohesion: 0.67
Nodes (3): generate_transit_blueprint_endpoint(), Generates a complete, 10-checkpoint publication-ready pillar guide for a…, TransitBlueprintRequest

### Community 41 - "BaseModel"
Cohesion: 0.17
Nodes (12): AIAuditRequest, CheckAIRequest, get_ai_seo_audit_endpoint(), HumanizeRequest, BaseModel, Scrapling + curl_cffi Chrome 124 stealth scrape with deep JSON-LD extraction., Semrush On-Page SEO Checker: Actionable strategy, backlink, UX recommendations., 15-Point Automated AI-SEO-Audit Gate (marketplace/actions/ai-seo-audit +… (+4 more)

### Community 42 - "run_ai_seo_audit"
Cohesion: 0.10
Nodes (27): auto_heal_content(), calculate_burstiness_variance(), calculate_readability_metrics(), extract_clean_prose(), Any, AI SEO Audit & Autonomous Quality Gate Engine…, Executes the comprehensive 15-Point AI-SEO-Audit Gate. Returns: - score (0 -…, Extract readable prose from nested dicts, lists, or markdown strings, skipping… (+19 more)

### Community 45 - "main.py"
Cohesion: 0.13
Nodes (18): FastAPI, analyze_transit_bottleneck_endpoint(), inject_google_disclosure_endpoint(), InjectDisclosureRequest, lifespan(), publish_to_wordpress(), FastAPI server with .env auto-loading, URL auto-scraping, batch processing,…, Analyzes a pilgrimage transit route, computing bottleneck intensity and SERP… (+10 more)

### Community 47 - "semrush_keyword_magic_endpoint"
Cohesion: 0.50
Nodes (4): Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Keyword Magic Tool: Fan-out suggest mining with intent classification., semrush_keyword_magic_endpoint(), SemrushKeywordRequest

### Community 52 - "analyze_serp_endpoint"
Cohesion: 0.67
Nodes (3): analyze_serp_endpoint(), Native SERP Competitor & Information Gain Analyzer endpoint. Scrapes live SERP…, SERPAnalyzeRequest

### Community 53 - "get_smart_internal_links"
Cohesion: 0.50
Nodes (3): get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…

### Community 54 - "crawl_sitemap"
Cohesion: 0.67
Nodes (3): crawl_sitemap(), Crawl an XML Sitemap or Category Landing Page to extract package links with…, SitemapCrawlRequest

### Community 55 - "semrush_compare_domains_endpoint"
Cohesion: 0.67
Nodes (3): Semrush Compare Domains (Multi-domain benchmark)., semrush_compare_domains_endpoint(), SemrushCompareRequest

### Community 56 - "validate_category"
Cohesion: 0.67
Nodes (3): Validate if the selected category matches the target URL., validate_category(), ValidateCategoryRequest

### Community 57 - "verify_wordpress_connection"
Cohesion: 0.67
Nodes (3): Verify WordPress credentials and REST API availability (Admin Protected)., verify_wordpress_connection(), WpVerifyRequest

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `is_safe_url`, `qa_agent.py`, `test_e2e_suite.py`, `run_seo_linter`, `main.py`, `content_creator_agent.py`, `process_package`, `TestArchitecturalDecoupling`, `generate_content`, `pipeline.py`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Why does `de_slop_and_humanize()` connect `de_slop_and_humanize` to `run_ai_seo_audit`, `anti_ai_guardrails.py`, `main.py`, `content_creator_agent.py`, `humanize_endpoint`, `pipeline.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `detect_55_patterns()` connect `anti_ai_guardrails.py` to `TestHumanizer55Patterns`, `run_ai_seo_audit`, `humanize_endpoint`, `main.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._