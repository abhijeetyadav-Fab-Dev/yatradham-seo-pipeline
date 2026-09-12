# Graph Report - yatradham-seo-pipeline  (2026-08-26)

## Corpus Check
- 40 files · ~75,734 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 491 nodes · 953 edges · 32 communities (31 shown, 1 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 47 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6e0dab19`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- main.py
- database.py
- LLMClient
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- seo_toolkit.py
- qa_agent.py
- TestArchitecturalDecoupling
- validation_layer.py
- extract_package_data
- nlp_and_safety_toolkit.py
- get
- enrich_destination_data
- is_safe_url
- security_firewall.py
- post
- SitemapCrawler
- localize
- BaseModel
- audit_onpage_seo_score
- models.py
- batch_process
- batch_urls
- get_forex_rates_endpoint
- run_seo_linter
- generate_json_ld

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 37 edges
2. `process_package()` - 21 edges
3. `run_suite()` - 19 edges
4. `SEOOutput` - 17 edges
5. `PackageInput` - 15 edges
6. `SectionedContent` - 13 edges
7. `run_validation()` - 13 edges
8. `save_output()` - 12 edges
9. `extract_package_data()` - 12 edges
10. `is_safe_url()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py
- `localize_content()` --uses--> `LLMClient`  [INFERRED]
  indic_engine.py → llm_client.py
- `localize()` --uses--> `LLMClient`  [INFERRED]
  main.py → llm_client.py
- `process_batch_background()` --uses--> `LLMClient`  [INFERRED]
  main.py → llm_client.py

## Import Cycles
- None detected.

## Communities (32 total, 1 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "main.py"
Cohesion: 0.15
Nodes (17): FastAPI, ContentGenerateRequest, crawl_sitemap(), generate_content(), humanize_endpoint(), humanize_markdown_content(), humanize_single_chunk(), HumanizeRequest (+9 more)

### Community 2 - "database.py"
Cohesion: 0.10
Nodes (46): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output() (+38 more)

### Community 3 - "LLMClient"
Cohesion: 0.05
Nodes (51): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections() (+43 more)

### Community 5 - "WordPressPublisher"
Cohesion: 0.27
Nodes (5): Verify WordPress credentials and REST API availability (Admin Protected)., verify_wordpress_connection(), WpVerifyRequest, Any, WordPressPublisher

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.09
Nodes (22): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting, 1. Security & OWASP Hardening Layer (+14 more)

### Community 7 - "seo_toolkit.py"
Cohesion: 0.15
Nodes (13): get_screenshot_preview_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., Generate screenshot preview card URL for any landing page or competitor site., check_serp_rank(), fetch_serp_results() (+5 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 12 - "TestArchitecturalDecoupling"
Cohesion: 0.14
Nodes (8): Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio…, TestArchitecturalDecoupling

### Community 13 - "validation_layer.py"
Cohesion: 0.15
Nodes (20): check_duplicate_content(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'., Compare one section (e.g. 'why_choose_bullets') of the new row against the same… (+12 more)

### Community 14 - "extract_package_data"
Cohesion: 0.11
Nodes (22): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+14 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.12
Nodes (19): analyze_keywords_endpoint(), get_dictionary_endpoint(), link_safety_preview_endpoint(), Any, Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Extract top unigrams, bigrams, trigrams & Flesch reading score., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview., analyze_keywords_and_readability() (+11 more)

### Community 17 - "get"
Cohesion: 0.11
Nodes (18): get, enrich_destination_endpoint(), export_csv_endpoint(), get_audit_trail_endpoint(), get_outputs(), get_providers_status(), get_robots_txt(), get_single_output() (+10 more)

### Community 18 - "enrich_destination_data"
Cohesion: 0.16
Nodes (18): get_serp_intelligence_endpoint(), Return live search intent, LSI keyword entities, and competitor heading…, enrich_destination_data(), fetch_climate_and_weather(), fetch_semantic_lsi_keywords(), fetch_solar_timings(), fetch_spiritual_heritage_facts(), fetch_transit_distance_osrm() (+10 more)

### Community 19 - "is_safe_url"
Cohesion: 0.21
Nodes (10): process_batch_background(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, scrape_and_process(), URLRequest, fetch_url_html(), Scrapling-Powered Modern Scraping & DOM Parsing Engine for YatraDham SEO…, Fetch URL with SSRF protection, browser-grade headers and stealth resilience., is_safe_url() (+2 more)

### Community 20 - "security_firewall.py"
Cohesion: 0.06
Nodes (30): BaseHTTPMiddleware, HTTPAuthorizationCredentials, LogRecord, Request, RateLimitingMiddleware, Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, Injects enterprise OWASP security headers on all HTTP responses., root() (+22 more)

### Community 21 - "post"
Cohesion: 0.15
Nodes (14): bulk_action(), clear_cache(), moderate_text_endpoint(), proofread_endpoint(), ProviderSettingsRequest, Bulk approve or reject outputs with admin authorization., Wipe all outputs from the database to start fresh (Protected Admin Action)., Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime… (+6 more)

### Community 23 - "localize"
Cohesion: 0.33
Nodes (6): localize_content(), Any, Translate and culturally localize SEOOutput sections into Hindi or Gujarati., localize(), LocalizeRequest, Translate and localize generated SEO content into Hindi or Gujarati.

### Community 24 - "BaseModel"
Cohesion: 0.22
Nodes (9): check_ai_endpoint(), CheckAIRequest, publish_to_wordpress(), BaseModel, Validate if the selected category matches the target URL., Publish generated SEO content directly to WordPress (Admin Protected)., validate_category(), ValidateCategoryRequest (+1 more)

### Community 25 - "audit_onpage_seo_score"
Cohesion: 0.22
Nodes (9): get_seo_audit_score_endpoint(), get_seo_tags_generator_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., audit_onpage_seo_score(), generate_seo_tags(), Any, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 26 - "models.py"
Cohesion: 0.14
Nodes (18): field_validator, BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights (+10 more)

### Community 27 - "batch_process"
Cohesion: 0.29
Nodes (7): Exception, batch_process(), process_single(), Process a single package through all 5 agents (manual JSON input)., Process multiple packages from JSON (Admin Protected, Max 25 items)., Sanitizes raw python exception traces for public consumption., sanitize_error_detail()

### Community 28 - "batch_urls"
Cohesion: 0.50
Nodes (4): BackgroundTasks, batch_urls(), BatchURLRequest, Scrape and process multiple URLs automatically in the background (Admin…

### Community 29 - "get_forex_rates_endpoint"
Cohesion: 0.50
Nodes (4): get_forex_rates_endpoint(), Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, convert_inr_to_forex(), Convert INR package pricing to major international currencies using Frankfurter…

### Community 30 - "run_seo_linter"
Cohesion: 0.50
Nodes (4): calculate_flesch_reading_ease(), Any, Real-Time Dynamic SEO & GEO Linter for YatraDham. Performs rigorous, non-…, run_seo_linter()

### Community 31 - "generate_json_ld"
Cohesion: 0.40
Nodes (4): generate_json_ld(), Any, Schema.org JSON-LD Structured Data Generator for YatraDham Packages., Generate comprehensive stacked Schema.org JSON-LD for Google Rich Results, SGE…

## Knowledge Gaps
- **36 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+31 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `database.py`, `qa_agent.py`, `TestArchitecturalDecoupling`, `is_safe_url`, `localize`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `main.py`, `LLMClient`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `TestArchitecturalDecoupling` connect `TestArchitecturalDecoupling` to `LLMClient`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _36 weakly-connected nodes found - possible documentation gaps or missing edges._