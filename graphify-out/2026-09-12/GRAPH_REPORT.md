# Graph Report - yatradham-seo-pipeline  (2026-09-12)

## Corpus Check
- 40 files · ~77,949 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 511 nodes · 999 edges · 34 communities (32 shown, 2 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 48 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `89a8782a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- seo_toolkit.py
- test_e2e_suite.py
- pipeline.py
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- main.py
- qa_agent.py
- TestArchitecturalDecoupling
- validation_layer.py
- extract_package_data
- nlp_and_safety_toolkit.py
- LLMClient
- get
- process_package
- security_firewall.py
- content_creator_agent.py
- SitemapCrawler
- BaseModel
- post
- content_agent.py
- models.py
- analyze_keywords_endpoint
- localize_content
- ProviderSettingsRequest
- generate_content
- quality_audit_endpoint
- validate_category
- scrape_stealth_endpoint

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 39 edges
2. `process_package()` - 21 edges
3. `run_suite()` - 19 edges
4. `SEOOutput` - 17 edges
5. `PackageInput` - 15 edges
6. `SectionedContent` - 13 edges
7. `is_safe_url()` - 13 edges
8. `run_validation()` - 13 edges
9. `save_output()` - 12 edges
10. `extract_package_data()` - 12 edges

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

## Communities (34 total, 2 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "seo_toolkit.py"
Cohesion: 0.10
Nodes (22): get_screenshot_preview_endpoint(), get_seo_audit_score_endpoint(), get_seo_tags_generator_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword. (+14 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.10
Nodes (48): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output() (+40 more)

### Community 3 - "pipeline.py"
Cohesion: 0.14
Nodes (12): Any, Keyword agent: enforces 2-4 word primary keyword., run(), Any, Meta description agent: 145-155 chars, natural language, no repetition., run(), Any, Title tag agent: 50-60 chars, optimized for click-through rate with accurate… (+4 more)

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "main.py"
Cohesion: 0.15
Nodes (17): FastAPI, humanize_endpoint(), humanize_markdown_content(), humanize_single_chunk(), HumanizeRequest, lifespan(), localize(), LocalizeRequest (+9 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 12 - "TestArchitecturalDecoupling"
Cohesion: 0.12
Nodes (9): Architectural Decoupling & Zero-Leakage Verification Suite Ensures that all…, Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio… (+1 more)

### Community 13 - "validation_layer.py"
Cohesion: 0.13
Nodes (22): check_duplicate_content(), compute_objective_qa_score(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'. (+14 more)

### Community 14 - "extract_package_data"
Cohesion: 0.11
Nodes (22): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+14 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.15
Nodes (16): get_dictionary_endpoint(), link_safety_preview_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview., analyze_keywords_and_readability(), analyze_sentiment_and_moderation(), inspect_url_safety_and_preview(), lookup_word_dictionary() (+8 more)

### Community 17 - "LLMClient"
Cohesion: 0.17
Nodes (9): LLMClient, Any, Execute DeepSeek two-stage reasoning protocol: 1. Stage 1 (<thinking>): Deep…, Allow setting runtime keys dynamically for a request without server restart., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., Strip internal thinking/reasoning tags leaked from thinking models., Return a rich, dynamic response when no LLM provider key is available.… (+1 more)

### Community 18 - "get"
Cohesion: 0.06
Nodes (44): get, enrich_destination_endpoint(), export_csv_endpoint(), favicon(), get_audit_trail_endpoint(), get_forex_rates_endpoint(), get_outputs(), get_providers_status() (+36 more)

### Community 19 - "process_package"
Cohesion: 0.07
Nodes (29): Exception, get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…, calculate_flesch_reading_ease(), Any, Real-Time Dynamic SEO & GEO Linter for YatraDham. Performs rigorous, non-…, run_seo_linter() (+21 more)

### Community 20 - "security_firewall.py"
Cohesion: 0.06
Nodes (30): BaseHTTPMiddleware, HTTPAuthorizationCredentials, LogRecord, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, root() (+22 more)

### Community 21 - "content_creator_agent.py"
Cohesion: 0.22
Nodes (15): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+7 more)

### Community 23 - "BaseModel"
Cohesion: 0.15
Nodes (13): BackgroundTasks, batch_urls(), BatchURLRequest, check_ai_endpoint(), CheckAIRequest, crawl_sitemap(), deepseek_reasoning_endpoint(), DeepSeekReasonRequest (+5 more)

### Community 24 - "post"
Cohesion: 0.17
Nodes (12): bulk_action(), clear_cache(), moderate_text_endpoint(), proofread_endpoint(), publish_to_wordpress(), Bulk approve or reject outputs with admin authorization., Wipe all outputs from the database to start fresh (Protected Admin Action)., Publish generated SEO content directly to WordPress (Admin Protected). (+4 more)

### Community 25 - "content_agent.py"
Cohesion: 0.40
Nodes (5): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run()

### Community 26 - "models.py"
Cohesion: 0.13
Nodes (20): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights, ProgramSession (+12 more)

### Community 27 - "analyze_keywords_endpoint"
Cohesion: 0.33
Nodes (5): analyze_keywords_endpoint(), Any, field_validator, Extract top unigrams, bigrams, trigrams & Flesch reading score., URLRequest

### Community 28 - "localize_content"
Cohesion: 0.40
Nodes (4): localize_content(), Any, Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)., Translate and culturally localize SEOOutput sections into Hindi or Gujarati.

### Community 29 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime…, Test a provider API key live and return latency & status (Admin Protected)., test_provider_endpoint(), update_provider_settings()

### Community 30 - "generate_content"
Cohesion: 0.67
Nodes (3): ContentGenerateRequest, generate_content(), Generate net-new SEO content from scratch using AI.

### Community 31 - "quality_audit_endpoint"
Cohesion: 0.67
Nodes (3): quality_audit_endpoint(), QualityAuditRequest, Enterprise 100M-scale content quality, safety, readability, and AI-slop auditor.

### Community 32 - "validate_category"
Cohesion: 0.67
Nodes (3): Validate if the selected category matches the target URL., validate_category(), ValidateCategoryRequest

### Community 33 - "scrape_stealth_endpoint"
Cohesion: 0.67
Nodes (3): Scrapling + curl_cffi Chrome 124 stealth scrape with deep JSON-LD extraction., scrape_stealth_endpoint(), StealthScrapeRequest

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `test_e2e_suite.py`, `pipeline.py`, `main.py`, `qa_agent.py`, `TestArchitecturalDecoupling`, `process_package`, `content_creator_agent.py`, `BaseModel`, `content_agent.py`, `localize_content`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `process_package`, `pipeline.py`, `main.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `TestArchitecturalDecoupling` connect `TestArchitecturalDecoupling` to `LLMClient`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._