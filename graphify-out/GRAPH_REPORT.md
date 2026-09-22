# Graph Report - yatradham-seo-pipeline  (2026-09-22)

## Corpus Check
- 44 files · ~98,141 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 740 nodes · 1482 edges · 57 communities (45 shown, 12 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `04ab624a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- models.py
- test_e2e_suite.py
- enrich_destination_data
- extract_package_data
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- ProviderSettingsRequest
- anti_ai_guardrails.py
- run_seo_linter
- validation_layer.py
- scraper.py
- nlp_and_safety_toolkit.py
- LLMClient
- content_creator_agent.py
- get
- semrush_suite.py
- security_firewall.py
- process_package
- SitemapCrawler
- main.py
- content_agent.py
- semrush_backlinks_endpoint
- de_slop_and_humanize
- TestArchitecturalDecoupling
- stress_test.py
- TestDeSlopAndHumanize
- analyze_serp_endpoint
- semrush_backlink_gap_endpoint
- post
- check_serp_rank
- TestVoiceProfiles
- TestFastAPIHumanizerEndpoints
- seo_toolkit.py
- quality_audit_endpoint
- serp_analyzer.py
- analyze_keywords_endpoint
- delete_single_output
- semrush_site_performance_endpoint
- get_robots_txt
- semrush_position_tracking_endpoint
- semrush_sensor_endpoint
- BaseModel
- semrush_on_page_checker_endpoint
- validate_row_endpoint
- export_csv_endpoint
- favicon
- semrush_top_pages_endpoint
- semrush_compare_domains_endpoint
- semrush_local_seo_endpoint
- get_audit_trail
- get_single_output
- semrush_dashboard_endpoint
- semrush_topic_research_endpoint

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 43 edges
2. `process_package()` - 26 edges
3. `de_slop_and_humanize()` - 24 edges
4. `PackageInput` - 19 edges
5. `run_suite()` - 19 edges
6. `SEOOutput` - 17 edges
7. `detect_55_patterns()` - 16 edges
8. `clean_domain_name()` - 16 edges
9. `extract_package_data()` - 15 edges
10. `is_safe_url()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_agent.py → llm_client.py
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py

## Import Cycles
- None detected.

## Communities (57 total, 12 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "models.py"
Cohesion: 0.13
Nodes (20): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights, ProgramSession (+12 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.16
Nodes (28): bulk_update_status(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_conn(), get_output(), get_stats(), init_db() (+20 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.09
Nodes (28): enrich_destination_endpoint(), get_forex_rates_endpoint(), get_serp_intelligence_endpoint(), get_transit_distance_endpoint(), Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, Calculate driving distance and duration via Open Source Routing Machine (OSRM)., Return live search intent, LSI keyword entities, and competitor heading… (+20 more)

### Community 4 - "extract_package_data"
Cohesion: 0.20
Nodes (13): process_batch_background(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, scrape_and_process(), extract_package_data(), Any, Extract package metadata, category, and raw text for LLM processing with robust…, fetch_url_html(), Scrapling-Powered Modern Scraping & DOM Parsing Engine for YatraDham SEO… (+5 more)

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime…, Test a provider API key live and return latency & status (Admin Protected)., test_provider_endpoint(), update_provider_settings()

### Community 11 - "anti_ai_guardrails.py"
Cohesion: 0.07
Nodes (36): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_burstiness_metrics() (+28 more)

### Community 12 - "run_seo_linter"
Cohesion: 0.12
Nodes (15): fixture, calculate_flesch_reading_ease(), Any, Real-Time Dynamic SEO & GEO Linter for YatraDham. Performs rigorous, non-…, run_seo_linter(), batch_process(), localize(), process_single() (+7 more)

### Community 13 - "validation_layer.py"
Cohesion: 0.15
Nodes (19): check_duplicate_content(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Extract the numeric ₹ amount from a string like 'Starting From ₹ 13,125.00 Per…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'. (+11 more)

### Community 14 - "scraper.py"
Cohesion: 0.15
Nodes (15): _extract_numeric_price(), Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string(), normalize_duration_string(), Extract structured data from Yatradham HTML pages. (+7 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.11
Nodes (20): get_dictionary_endpoint(), link_safety_preview_endpoint(), moderate_text_endpoint(), proofread_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Grammar, spellcheck & stylistic review via LanguageTool API., Evaluate tone sentiment, spiritual reverence, and toxicity., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview. (+12 more)

### Community 16 - "LLMClient"
Cohesion: 0.15
Nodes (14): Any, Keyword agent: enforces 2-4 word primary keyword., run(), Any, Meta description agent: 145-155 chars, natural language, no repetition., run(), Any, Title tag agent: 50-60 chars, optimized for click-through rate with accurate… (+6 more)

### Community 17 - "content_creator_agent.py"
Cohesion: 0.20
Nodes (14): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+6 more)

### Community 18 - "get"
Cohesion: 0.11
Nodes (18): get, get_humanizer_patterns(), get_outputs(), get_providers_status(), Semrush Keyword Overview: Deep-dive search volume, global breakdown, KD%., Semrush Keyword Strategy Builder: Topic clusters & pillar architecture., Semrush Backlink Audit: Toxicity score and disavow candidates., Semrush Organic Traffic Insights: Landing pages & queries. (+10 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.08
Nodes (54): clean_domain_name(), detect_domain_category(), extract_brand_tokens(), fetch_live_google_suggest(), get_ai_search_overview(), get_backlink_audit(), get_backlink_gap(), get_backlink_overview() (+46 more)

### Community 20 - "security_firewall.py"
Cohesion: 0.06
Nodes (33): BaseHTTPMiddleware, Exception, HTTPAuthorizationCredentials, LogRecord, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP… (+25 more)

### Community 21 - "process_package"
Cohesion: 0.15
Nodes (19): Any, verify_ground_truth(), get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…, PackageInput, parametrize, process_package() (+11 more)

### Community 22 - "SitemapCrawler"
Cohesion: 0.10
Nodes (20): detect_url_category(), Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'., Any, Prioritizes bookable pilgrimage packages, destination stays, pujas, and…, Accurately classifies discovered links into stay, tour, wellness, or puja., Derives a clean human-readable title from URL segments when anchor text is…, Parses XML sitemaps with namespace stripping, index recursing, and regex…, Parses HTML category pages, capturing clean anchor titles and canonical URLs. (+12 more)

### Community 23 - "main.py"
Cohesion: 0.14
Nodes (16): clear_all_outputs(), FastAPI, check_ai_endpoint(), CheckAIRequest, clear_cache(), lifespan(), query_undetectable_detector(), FastAPI server with .env auto-loading, URL auto-scraping, batch processing,… (+8 more)

### Community 24 - "content_agent.py"
Cohesion: 0.08
Nodes (17): _extract_json_from_response(), get_category_aware_fallback(), Any, Content agent: generates all 19 structured sections from scraped page data., Generates complete, enterprise-grade 19 sections strictly adhering to category…, Robustly extract JSON from LLM response, handling markdown blocks and…, run(), clean_price_string() (+9 more)

### Community 25 - "semrush_backlinks_endpoint"
Cohesion: 0.25
Nodes (9): api_route, Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Backlink Analytics: Authority Score, Referring Domains, Dofollow Ratio,…, semrush_backlinks_endpoint(), semrush_domain_overview_endpoint(), semrush_keyword_magic_endpoint(), SemrushDomainRequest (+1 more)

### Community 26 - "de_slop_and_humanize"
Cohesion: 0.13
Nodes (15): apply_voice_transformations(), de_slop_and_humanize(), eradicate_em_dashes(), mask_protected_structures(), Masks markdown code blocks, tables, URLs, HTML tags, and template variables so…, Restores all protected structures exactly as they were., Aboudjem Humanizer Rule: Zero-tolerance on em dashes ('—') and conversational…, blader & Aboudjem Humanizer Rule: Transforms formulaic 'not only X, but also Y'… (+7 more)

### Community 27 - "TestArchitecturalDecoupling"
Cohesion: 0.14
Nodes (8): Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio…, TestArchitecturalDecoupling

### Community 28 - "stress_test.py"
Cohesion: 0.26
Nodes (11): export_csv(), Export outputs to CSV with authorized access., High-Concurrency Multi-Threaded Stress Test Suite for Yatradham SEO Pipeline., Stress test AI Detector endpoint concurrently., Stress test multi-threaded parallel markdown humanizer., Stress test CSV export streaming and stats aggregation., record_metric(), run_stress_test() (+3 more)

### Community 29 - "TestDeSlopAndHumanize"
Cohesion: 0.17
Nodes (7): Key AI buzzwords must be replaced with clean plain English., Markdown tables, URLs, and code blocks must not be corrupted., Smart curly quotes must be normalized to straight ASCII quotes., Verify deterministic de-slopping, em-dash removal, and replacements., Em dashes must be replaced with commas, colons, or clean punctuation., not only X, but also Y' should be transformed to natural 'X and Y'., TestDeSlopAndHumanize

### Community 30 - "analyze_serp_endpoint"
Cohesion: 0.67
Nodes (3): analyze_serp_endpoint(), Native SERP Competitor & Information Gain Analyzer endpoint. Scrapes live SERP…, SERPAnalyzeRequest

### Community 31 - "semrush_backlink_gap_endpoint"
Cohesion: 0.40
Nodes (5): Semrush Keyword Gap: Identifies shared, missing, and untapped ranking…, Semrush Backlink Gap: Find link opportunities., semrush_backlink_gap_endpoint(), semrush_keyword_gap_endpoint(), SemrushGapRequest

### Community 32 - "post"
Cohesion: 0.13
Nodes (15): bulk_action(), ContentGenerateRequest, crawl_sitemap(), generate_content(), publish_to_wordpress(), Validate if the selected category matches the target URL., Bulk approve or reject outputs with admin authorization., Generate net-new SEO content from scratch using AI. (+7 more)

### Community 33 - "check_serp_rank"
Cohesion: 0.17
Nodes (13): get_seo_audit_score_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., audit_onpage_seo_score(), check_serp_rank() (+5 more)

### Community 34 - "TestVoiceProfiles"
Cohesion: 0.17
Nodes (7): Verify that the 5 distinct voice profiles apply their characteristics., Casual voice introduces natural contractions and conversational tone., Blunt voice strips hedging and fluff., Technical voice preserves facts and strips flowery praise., Warm voice maintains compassionate, pilgrim-friendly atmosphere., Professional voice ensures clear, authoritative prose without corporate jargon., TestVoiceProfiles

### Community 35 - "TestFastAPIHumanizerEndpoints"
Cohesion: 0.25
Nodes (5): Verify the FastAPI HTTP endpoints for check-ai, humanize, and patterns., GET /api/humanizer/patterns returns 55 patterns and voice profiles., POST /api/check-ai returns 55-pattern detection and burstiness., POST /api/humanize transforms text using selected voice profile and strips em-…, TestFastAPIHumanizerEndpoints

### Community 36 - "seo_toolkit.py"
Cohesion: 0.20
Nodes (9): get_screenshot_preview_endpoint(), get_seo_tags_generator_endpoint(), Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), generate_seo_tags(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 37 - "quality_audit_endpoint"
Cohesion: 0.67
Nodes (3): quality_audit_endpoint(), QualityAuditRequest, Enterprise 100M-scale content quality, safety, readability, and AI-slop auditor.

### Community 38 - "serp_analyzer.py"
Cohesion: 0.19
Nodes (16): get_output_serp_audit(), Run real-time SERP competitor and Information Gain audit on a saved SEO output., analyze_serp_and_grade_content(), _extract_domain(), extract_salient_entities(), fetch_google_related_entities(), fetch_live_serp_competitors(), _generate_fallback_competitors() (+8 more)

### Community 39 - "analyze_keywords_endpoint"
Cohesion: 0.33
Nodes (5): analyze_keywords_endpoint(), Any, field_validator, Extract top unigrams, bigrams, trigrams & Flesch reading score., URLRequest

### Community 40 - "delete_single_output"
Cohesion: 0.67
Nodes (3): delete, delete_single_output(), Delete a single output with admin authorization.

### Community 45 - "BaseModel"
Cohesion: 0.12
Nodes (16): BackgroundTasks, batch_urls(), BatchURLRequest, deepseek_reasoning_endpoint(), DeepSeekReasonRequest, HumanizeRequest, LocalizeRequest, BaseModel (+8 more)

### Community 46 - "semrush_on_page_checker_endpoint"
Cohesion: 0.67
Nodes (3): Semrush On-Page SEO Checker: Actionable strategy, backlink, UX recommendations., semrush_on_page_checker_endpoint(), SemrushOnPageRequest

### Community 47 - "validate_row_endpoint"
Cohesion: 0.67
Nodes (3): Enterprise code-based validation endpoint., validate_row_endpoint(), ValidateRowRequest

### Community 51 - "semrush_compare_domains_endpoint"
Cohesion: 0.67
Nodes (3): Semrush Compare Domains (Multi-domain benchmark)., semrush_compare_domains_endpoint(), SemrushCompareRequest

### Community 55 - "get_audit_trail"
Cohesion: 0.40
Nodes (5): get_audit_trail(), Any, Retrieve audit history for a package or global pipeline activity., get_audit_trail_endpoint(), Return enterprise audit trail log for compliance and change tracking.

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `test_e2e_suite.py`, `extract_package_data`, `anti_ai_guardrails.py`, `run_seo_linter`, `BaseModel`, `content_creator_agent.py`, `process_package`, `main.py`, `content_agent.py`, `TestArchitecturalDecoupling`, `stress_test.py`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `de_slop_and_humanize()` connect `de_slop_and_humanize` to `TestVoiceProfiles`, `anti_ai_guardrails.py`, `content_creator_agent.py`, `main.py`, `content_agent.py`, `TestDeSlopAndHumanize`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `detect_55_patterns()` connect `anti_ai_guardrails.py` to `main.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._