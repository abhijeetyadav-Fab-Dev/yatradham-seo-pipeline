# Graph Report - yatradham-seo-pipeline  (2026-09-30)

## Corpus Check
- 47 files · ~104,691 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 786 nodes · 1598 edges · 47 communities (41 shown, 6 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 59 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `36c40365`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- models.py
- test_e2e_suite.py
- enrich_destination_data
- RateLimitingMiddleware
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- post
- anti_ai_guardrails.py
- .chat_completion
- validation_layer.py
- verify_ground_truth
- nlp_and_safety_toolkit.py
- LLMClient
- content_creator_agent.py
- get
- semrush_suite.py
- ProviderSettingsRequest
- get_smart_internal_links
- SitemapCrawler
- BaseModel
- .test_provider
- api_route
- run_ai_seo_audit
- TestArchitecturalDecoupling
- seo_toolkit.py
- de_slop_and_humanize
- generate_content
- get_forex_rates_endpoint
- publish_to_wordpress
- semrush_compare_domains_endpoint
- verify_wordpress_connection
- batch_process
- get_screenshot_preview_endpoint
- semrush_keyword_strategy_endpoint
- serp_analyzer.py
- analyze_keywords_endpoint
- semrush_backlink_audit_endpoint
- generate_blog_json_ld
- batch_urls
- main.py
- semrush_top_pages_endpoint
- semrush_ai_search_endpoint
- get_single_output

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 46 edges
2. `process_package()` - 28 edges
3. `de_slop_and_humanize()` - 25 edges
4. `PackageInput` - 19 edges
5. `run_suite()` - 19 edges
6. `detect_55_patterns()` - 18 edges
7. `run_ai_seo_audit()` - 17 edges
8. `SEOOutput` - 17 edges
9. `clean_domain_name()` - 16 edges
10. `extract_package_data()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py
- `deepseek_reasoning_endpoint()` --uses--> `LLMClient`  [INFERRED]
  main.py → llm_client.py

## Import Cycles
- None detected.

## Communities (47 total, 6 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "models.py"
Cohesion: 0.05
Nodes (44): HTTPAuthorizationCredentials, LogRecord, root(), BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation (+36 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.05
Nodes (80): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output() (+72 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.11
Nodes (24): enrich_destination_endpoint(), get_serp_intelligence_endpoint(), get_transit_distance_endpoint(), Destination intelligence fusing OSM Nominatim, Wikipedia, Open-Meteo, Sunrise-…, Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Calculate driving distance and duration via Open Source Routing Machine (OSRM)., Return live search intent, LSI keyword entities, and competitor heading…, temple_intel_endpoint() (+16 more)

### Community 4 - "RateLimitingMiddleware"
Cohesion: 0.29
Nodes (6): BaseHTTPMiddleware, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, SecurityHeadersMiddleware

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "post"
Cohesion: 0.11
Nodes (19): bulk_action(), clear_cache(), crawl_sitemap(), deepseek_reasoning_endpoint(), DeepSeekReasonRequest, DeepSeek two-stage reasoning protocol with chain-of-thought verification., Semrush Keyword Gap: Identifies shared, missing, and untapped ranking…, Semrush Backlink Gap: Find link opportunities. (+11 more)

### Community 11 - "anti_ai_guardrails.py"
Cohesion: 0.05
Nodes (51): _check_banned(), _check_sections(), _check_sentences(), _extract_prose_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., Extract natural sentences from sections dictionary, skipping JSON syntax. (+43 more)

### Community 12 - ".chat_completion"
Cohesion: 0.33
Nodes (3): Any, Execute DeepSeek two-stage reasoning protocol: 1. Stage 1 (<thinking>): Deep…, Strip internal thinking/reasoning tags leaked from thinking models.

### Community 13 - "validation_layer.py"
Cohesion: 0.11
Nodes (25): parametrize, Verify that all 4 product categories generate 100% complete, verified,…, test_product_category_pipeline_integrity(), check_duplicate_content(), compute_objective_qa_score(), extract_price_number(), find_duplicated_words(), _is_empty_val() (+17 more)

### Community 14 - "verify_ground_truth"
Cohesion: 0.17
Nodes (13): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+5 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.11
Nodes (20): get_dictionary_endpoint(), link_safety_preview_endpoint(), moderate_text_endpoint(), proofread_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Grammar, spellcheck & stylistic review via LanguageTool API., Evaluate tone sentiment, spiritual reverence, and toxicity., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview. (+12 more)

### Community 16 - "LLMClient"
Cohesion: 0.10
Nodes (27): _extract_json_from_response(), get_category_aware_fallback(), Any, Content agent: generates all 19 structured sections from scraped page data., Generates complete, enterprise-grade 19 sections strictly adhering to category…, Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any (+19 more)

### Community 17 - "content_creator_agent.py"
Cohesion: 0.12
Nodes (26): _clean_markdown(), _detect_blog_intent(), _generate_long_form_blog(), _get_intent_structure(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2… (+18 more)

### Community 18 - "get"
Cohesion: 0.06
Nodes (32): get, export_csv_endpoint(), favicon(), get_audit_trail_endpoint(), get_humanizer_patterns(), get_outputs(), get_providers_status(), get_robots_txt() (+24 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.08
Nodes (54): clean_domain_name(), detect_domain_category(), extract_brand_tokens(), fetch_live_google_suggest(), get_ai_search_overview(), get_backlink_audit(), get_backlink_gap(), get_backlink_overview() (+46 more)

### Community 20 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime…, Test a provider API key live and return latency & status (Admin Protected)., test_provider_endpoint(), update_provider_settings()

### Community 21 - "get_smart_internal_links"
Cohesion: 0.50
Nodes (3): get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…

### Community 22 - "SitemapCrawler"
Cohesion: 0.10
Nodes (19): Any, Prioritizes bookable pilgrimage packages, destination stays, pujas, and…, Accurately classifies discovered links into stay, tour, wellness, or puja., Derives a clean human-readable title from URL segments when anchor text is…, Parses XML sitemaps with namespace stripping, index recursing, and regex…, Parses HTML category pages, capturing clean anchor titles and canonical URLs., Returns cached XML sitemap for wellness.yatradham.org when remote Cloudflare…, Crawls an XML Sitemap (single or index, including .gz) or an HTML Category Hub.… (+11 more)

### Community 23 - "BaseModel"
Cohesion: 0.17
Nodes (12): analyze_serp_endpoint(), CheckAIRequest, HumanizeRequest, BaseModel, Semrush On-Page SEO Checker: Actionable strategy, backlink, UX recommendations., Native SERP Competitor & Information Gain Analyzer endpoint. Scrapes live SERP…, Scrapling + curl_cffi Chrome 124 stealth scrape with deep JSON-LD extraction., scrape_stealth_endpoint() (+4 more)

### Community 24 - ".test_provider"
Cohesion: 0.25
Nodes (4): Allow setting runtime keys dynamically for a request without server restart., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., OpenAI

### Community 25 - "api_route"
Cohesion: 0.14
Nodes (15): api_route, AIAuditRequest, get_ai_seo_audit_endpoint(), Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,…, Semrush Backlink Analytics: Authority Score, Referring Domains, Dofollow Ratio,…, 15-Point Automated AI-SEO-Audit Gate (marketplace/actions/ai-seo-audit +… (+7 more)

### Community 26 - "run_ai_seo_audit"
Cohesion: 0.15
Nodes (20): auto_heal_content(), calculate_burstiness_variance(), calculate_readability_metrics(), extract_clean_prose(), Any, AI SEO Audit & Autonomous Quality Gate Engine…, Executes the comprehensive 15-Point AI-SEO-Audit Gate. Returns: - score (0 -…, Extract readable prose from nested dicts, lists, or markdown strings, skipping… (+12 more)

### Community 27 - "TestArchitecturalDecoupling"
Cohesion: 0.14
Nodes (8): Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio…, TestArchitecturalDecoupling

### Community 28 - "seo_toolkit.py"
Cohesion: 0.13
Nodes (18): get_seo_audit_score_endpoint(), get_seo_tags_generator_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., Generate HTML Meta tags, OpenGraph tags, and Twitter Cards. (+10 more)

### Community 29 - "de_slop_and_humanize"
Cohesion: 0.10
Nodes (16): de_slop_and_humanize(), Deterministic Anti-AI De-Slopper & Humanizer Pipeline: 1. Masks code blocks,…, Key AI buzzwords must be replaced with clean plain English., Markdown tables, URLs, and code blocks must not be corrupted., Smart curly quotes must be normalized to straight ASCII quotes., Verify that the 5 distinct voice profiles apply their characteristics., Casual voice introduces natural contractions and conversational tone., Blunt voice strips hedging and fluff. (+8 more)

### Community 30 - "generate_content"
Cohesion: 0.67
Nodes (3): ContentGenerateRequest, generate_content(), Generate net-new SEO content from scratch using AI.

### Community 31 - "get_forex_rates_endpoint"
Cohesion: 0.50
Nodes (4): get_forex_rates_endpoint(), Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, convert_inr_to_forex(), Convert INR package pricing to major international currencies using Frankfurter…

### Community 32 - "publish_to_wordpress"
Cohesion: 0.67
Nodes (3): publish_to_wordpress(), Publish generated SEO content directly to WordPress (Admin Protected)., WpPublishRequest

### Community 33 - "semrush_compare_domains_endpoint"
Cohesion: 0.67
Nodes (3): Semrush Compare Domains (Multi-domain benchmark)., semrush_compare_domains_endpoint(), SemrushCompareRequest

### Community 34 - "verify_wordpress_connection"
Cohesion: 0.67
Nodes (3): Verify WordPress credentials and REST API availability (Admin Protected)., verify_wordpress_connection(), WpVerifyRequest

### Community 35 - "batch_process"
Cohesion: 0.13
Nodes (11): Exception, fixture, batch_process(), Process multiple packages from JSON (Admin Protected, Max 25 items)., Sanitizes raw python exception traces for public consumption., sanitize_error_detail(), Verify the FastAPI HTTP endpoints for check-ai, humanize, and patterns., GET /api/humanizer/patterns returns 55 patterns and voice profiles. (+3 more)

### Community 36 - "get_screenshot_preview_endpoint"
Cohesion: 0.50
Nodes (4): get_screenshot_preview_endpoint(), Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), Generate live website screenshot preview URLs. Uses ScreenshotOne API if key…

### Community 38 - "serp_analyzer.py"
Cohesion: 0.19
Nodes (16): get_output_serp_audit(), Run real-time SERP competitor and Information Gain audit on a saved SEO output., analyze_serp_and_grade_content(), _extract_domain(), extract_salient_entities(), fetch_google_related_entities(), fetch_live_serp_competitors(), _generate_fallback_competitors() (+8 more)

### Community 39 - "analyze_keywords_endpoint"
Cohesion: 0.33
Nodes (5): analyze_keywords_endpoint(), Any, field_validator, Extract top unigrams, bigrams, trigrams & Flesch reading score., URLRequest

### Community 42 - "generate_blog_json_ld"
Cohesion: 0.29
Nodes (6): generate_blog_json_ld(), Any, Schema.org JSON-LD Structured Data Generator for YatraDham Packages., Generates standalone BlogPosting + FAQPage + Organization JSON-LD for AI…, Verify JSON-LD schema generation for both packages and blog articles., test_blog_and_package_schema_validity()

### Community 44 - "batch_urls"
Cohesion: 0.50
Nodes (4): BackgroundTasks, batch_urls(), BatchURLRequest, Scrape and process multiple URLs automatically in the background (Admin…

### Community 45 - "main.py"
Cohesion: 0.13
Nodes (16): FastAPI, lifespan(), localize(), LocalizeRequest, quality_audit_endpoint(), QualityAuditRequest, FastAPI server with .env auto-loading, URL auto-scraping, batch processing,…, Enterprise 100M-scale content quality, safety, readability, and AI-slop auditor. (+8 more)

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `test_e2e_suite.py`, `post`, `anti_ai_guardrails.py`, `.chat_completion`, `main.py`, `validation_layer.py`, `content_creator_agent.py`, `.test_provider`, `TestArchitecturalDecoupling`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `de_slop_and_humanize()` connect `de_slop_and_humanize` to `anti_ai_guardrails.py`, `main.py`, `LLMClient`, `content_creator_agent.py`, `run_ai_seo_audit`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `detect_55_patterns()` connect `anti_ai_guardrails.py` to `run_ai_seo_audit`, `main.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._