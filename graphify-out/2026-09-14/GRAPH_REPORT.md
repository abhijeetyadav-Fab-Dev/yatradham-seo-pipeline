# Graph Report - yatradham-seo-pipeline  (2026-09-14)

## Corpus Check
- 39 files · ~84,520 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 613 nodes · 1248 edges · 46 communities (34 shown, 12 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 48 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `210add52`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- check_serp_rank
- test_e2e_suite.py
- enrich_destination_data
- seo_toolkit.py
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- ProviderSettingsRequest
- qa_agent.py
- process_package
- validation_layer.py
- scraper.py
- nlp_and_safety_toolkit.py
- audit_onpage_seo_score
- LLMClient
- get
- semrush_suite.py
- security_firewall.py
- content_creator_agent.py
- SitemapCrawler
- post
- main.py
- semrush_backlinks_endpoint
- sanitize_xss
- sanitize_user_prompt
- batch_urls
- RateLimitingMiddleware
- enforce_rate_limit
- check_disallowed_xss_patterns
- is_safe_url
- get_on_page_seo_checker
- validate_category
- SensitiveDataScrubberFilter
- InMemoryRateLimiter
- favicon
- get_providers_status
- get_robots_txt
- get_single_output
- semrush_site_performance_endpoint
- semrush_position_tracking_endpoint
- semrush_top_pages_endpoint
- semrush_sensor_endpoint
- semrush_traffic_insights_endpoint

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 39 edges
2. `process_package()` - 21 edges
3. `run_suite()` - 19 edges
4. `SEOOutput` - 17 edges
5. `clean_domain_name()` - 16 edges
6. `PackageInput` - 15 edges
7. `is_safe_url()` - 15 edges
8. `get_domain_overview()` - 14 edges
9. `SectionedContent` - 13 edges
10. `run_validation()` - 13 edges

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

## Communities (46 total, 12 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "check_serp_rank"
Cohesion: 0.25
Nodes (8): get_serp_rank_endpoint(), get_serp_search_endpoint(), Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., check_serp_rank(), fetch_serp_results(), Fetch live Google SERP organic rankings and People Also Ask questions.…, Check the current Google SERP ranking position of target_domain for a given…

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.05
Nodes (73): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Keyword agent: enforces 2-4 word primary keyword., Meta description agent: 145-155 chars, natural language, no repetition., Title tag agent: 50-60 chars, optimized for click-through rate with accurate… (+65 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.09
Nodes (28): enrich_destination_endpoint(), get_forex_rates_endpoint(), get_serp_intelligence_endpoint(), get_transit_distance_endpoint(), Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, Calculate driving distance and duration via Open Source Routing Machine (OSRM)., Return live search intent, LSI keyword entities, and competitor heading… (+20 more)

### Community 4 - "seo_toolkit.py"
Cohesion: 0.33
Nodes (5): get_screenshot_preview_endpoint(), Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generate live website screenshot preview URLs. Uses ScreenshotOne API if key…

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime…, Test a provider API key live and return latency & status (Admin Protected)., test_provider_endpoint(), update_provider_settings()

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 12 - "process_package"
Cohesion: 0.10
Nodes (20): Any, run(), Exception, get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…, calculate_flesch_reading_ease(), Any (+12 more)

### Community 13 - "validation_layer.py"
Cohesion: 0.15
Nodes (20): check_duplicate_content(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'., Compare one section (e.g. 'why_choose_bullets') of the new row against the same… (+12 more)

### Community 14 - "scraper.py"
Cohesion: 0.16
Nodes (14): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+6 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.10
Nodes (22): analyze_keywords_endpoint(), get_dictionary_endpoint(), link_safety_preview_endpoint(), moderate_text_endpoint(), proofread_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Grammar, spellcheck & stylistic review via LanguageTool API., Extract top unigrams, bigrams, trigrams & Flesch reading score. (+14 more)

### Community 16 - "audit_onpage_seo_score"
Cohesion: 0.22
Nodes (9): get_seo_audit_score_endpoint(), get_seo_tags_generator_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., audit_onpage_seo_score(), generate_seo_tags(), Any, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 17 - "LLMClient"
Cohesion: 0.06
Nodes (28): Any, run(), Any, run(), localize_content(), Any, Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)., Translate and culturally localize SEOOutput sections into Hindi or Gujarati. (+20 more)

### Community 18 - "get"
Cohesion: 0.12
Nodes (16): get, export_csv_endpoint(), get_audit_trail_endpoint(), get_outputs(), Semrush Consolidated Dashboard., Semrush Backlink Audit: Toxicity score and disavow candidates., Semrush AI Search & SGE Optimizer., Semrush Local SEO: 3-Pack rank potential & GBP audit. (+8 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.07
Nodes (56): Semrush Keyword Overview: Deep-dive search volume, global breakdown, KD%., Semrush Keyword Strategy Builder: Topic clusters & pillar architecture., Semrush Topic Research: Mindmap cards, questions, and high-CTR headlines., semrush_keyword_overview_endpoint(), semrush_keyword_strategy_endpoint(), semrush_topic_research_endpoint(), clean_domain_name(), detect_domain_category() (+48 more)

### Community 20 - "security_firewall.py"
Cohesion: 0.15
Nodes (14): FastAPI, lifespan(), Config, decrypt_secret(), _derive_key(), encrypt_secret(), mask_secret(), OutputUpdateRequest (+6 more)

### Community 21 - "content_creator_agent.py"
Cohesion: 0.17
Nodes (18): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+10 more)

### Community 23 - "post"
Cohesion: 0.10
Nodes (26): check_ai_endpoint(), CheckAIRequest, clear_cache(), humanize_endpoint(), HumanizeRequest, localize(), LocalizeRequest, publish_to_wordpress() (+18 more)

### Community 24 - "main.py"
Cohesion: 0.17
Nodes (13): crawl_sitemap(), quality_audit_endpoint(), QualityAuditRequest, FastAPI server with .env auto-loading, URL auto-scraping, batch processing,…, Verify WordPress credentials and REST API availability (Admin Protected)., Crawl an XML Sitemap or Category Landing Page to extract package links with…, Enterprise code-based validation endpoint., Enterprise 100M-scale content quality, safety, readability, and AI-slop auditor. (+5 more)

### Community 25 - "semrush_backlinks_endpoint"
Cohesion: 0.18
Nodes (12): api_route, Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,…, Semrush Backlink Analytics: Authority Score, Referring Domains, Dofollow Ratio,…, semrush_backlinks_endpoint(), semrush_domain_overview_endpoint(), semrush_keyword_magic_endpoint() (+4 more)

### Community 26 - "sanitize_xss"
Cohesion: 0.32
Nodes (5): Any, field_validator, Any, Enterprise HTML & Script Sanitizer: Strips all HTML tags, script elements,…, sanitize_xss()

### Community 27 - "sanitize_user_prompt"
Cohesion: 0.25
Nodes (8): ContentGenerateRequest, deepseek_reasoning_endpoint(), DeepSeekReasonRequest, generate_content(), Generate net-new SEO content from scratch using AI., DeepSeek two-stage reasoning protocol with chain-of-thought verification., Sanitizes user instructions and checks for active prompt injection attacks., sanitize_user_prompt()

### Community 28 - "batch_urls"
Cohesion: 0.50
Nodes (4): BackgroundTasks, batch_urls(), BatchURLRequest, Scrape and process multiple URLs automatically in the background (Admin…

### Community 29 - "RateLimitingMiddleware"
Cohesion: 0.29
Nodes (6): BaseHTTPMiddleware, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, SecurityHeadersMiddleware

### Community 30 - "enforce_rate_limit"
Cohesion: 0.29
Nodes (7): HTTPAuthorizationCredentials, root(), enforce_rate_limit(), Request, FastAPI dependency to rate-limit requests by client IP., Verifies that the caller has valid administrative access. Allows request if: -…, verify_admin_access()

### Community 31 - "check_disallowed_xss_patterns"
Cohesion: 0.40
Nodes (4): Any, field_validator, check_disallowed_xss_patterns(), Raises ValueError (resulting in 422 HTTP status) if dangerous XSS payloads are…

### Community 32 - "is_safe_url"
Cohesion: 0.12
Nodes (21): process_batch_background(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, Scrapling + curl_cffi Chrome 124 stealth scrape with deep JSON-LD extraction., scrape_and_process(), scrape_stealth_endpoint(), StealthScrapeRequest, URLRequest, extract_package_data() (+13 more)

### Community 33 - "get_on_page_seo_checker"
Cohesion: 0.40
Nodes (5): Semrush On-Page SEO Checker: Actionable strategy, backlink, UX recommendations., semrush_on_page_checker_endpoint(), SemrushOnPageRequest, get_on_page_seo_checker(), Semrush On-Page SEO Checker. Provides targeted recommendations across Strategy,…

### Community 34 - "validate_category"
Cohesion: 0.40
Nodes (5): Validate if the selected category matches the target URL., validate_category(), ValidateCategoryRequest, detect_url_category(), Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'.

### Community 35 - "SensitiveDataScrubberFilter"
Cohesion: 0.50
Nodes (3): LogRecord, Logging filter that redacts API keys, passwords, and tokens before writing to…, SensitiveDataScrubberFilter

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `is_safe_url`, `test_e2e_suite.py`, `qa_agent.py`, `process_package`, `content_creator_agent.py`, `post`, `main.py`, `sanitize_user_prompt`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `main.py`, `test_e2e_suite.py`, `process_package`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
- **Should `test_e2e_suite.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0546218487394958 - nodes in this community are weakly interconnected._