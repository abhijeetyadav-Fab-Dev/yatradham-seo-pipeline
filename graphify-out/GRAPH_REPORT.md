# Graph Report - yatradham-seo-pipeline  (2026-09-12)

## Corpus Check
- 39 files · ~85,750 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 540 nodes · 1066 edges · 24 communities (23 shown, 1 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 48 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `94e685bf`
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
- main.py
- qa_agent.py
- fetch_semantic_lsi_keywords
- validation_layer.py
- extract_package_data
- nlp_and_safety_toolkit.py
- get_forex_rates_endpoint
- LLMClient
- get
- is_safe_url
- security_firewall.py
- content_creator_agent.py
- crawl_sitemap
- sanitize_xss

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 39 edges
2. `process_package()` - 21 edges
3. `run_suite()` - 19 edges
4. `SEOOutput` - 17 edges
5. `PackageInput` - 15 edges
6. `is_safe_url()` - 15 edges
7. `SectionedContent` - 13 edges
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
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py

## Import Cycles
- None detected.

## Communities (24 total, 1 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "check_serp_rank"
Cohesion: 0.17
Nodes (13): get_seo_audit_score_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., audit_onpage_seo_score(), check_serp_rank() (+5 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.06
Nodes (76): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output() (+68 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.19
Nodes (14): get_transit_distance_endpoint(), Calculate driving distance and duration via Open Source Routing Machine (OSRM)., enrich_destination_data(), fetch_climate_and_weather(), fetch_solar_timings(), fetch_transit_distance_osrm(), geocode_location(), Any (+6 more)

### Community 4 - "seo_toolkit.py"
Cohesion: 0.20
Nodes (9): get_screenshot_preview_endpoint(), get_seo_tags_generator_endpoint(), Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), generate_seo_tags(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "main.py"
Cohesion: 0.05
Nodes (65): BackgroundTasks, delete, FastAPI, batch_urls(), BatchURLRequest, bulk_action(), check_ai_endpoint(), CheckAIRequest (+57 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.13
Nodes (22): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), _check_banned(), _check_sections(), _check_sentences() (+14 more)

### Community 12 - "fetch_semantic_lsi_keywords"
Cohesion: 0.33
Nodes (6): get_serp_intelligence_endpoint(), Return live search intent, LSI keyword entities, and competitor heading…, fetch_semantic_lsi_keywords(), fetch_spiritual_heritage_facts(), Fetch verified cultural & spiritual heritage summary from Wikipedia REST API., Fetch semantic LSI synonyms & related terms using Datamuse API (free, keyless).

### Community 13 - "validation_layer.py"
Cohesion: 0.15
Nodes (20): check_duplicate_content(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'., Compare one section (e.g. 'why_choose_bullets') of the new row against the same… (+12 more)

### Community 14 - "extract_package_data"
Cohesion: 0.11
Nodes (22): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+14 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.15
Nodes (16): get_dictionary_endpoint(), link_safety_preview_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview., analyze_keywords_and_readability(), analyze_sentiment_and_moderation(), inspect_url_safety_and_preview(), lookup_word_dictionary() (+8 more)

### Community 16 - "get_forex_rates_endpoint"
Cohesion: 0.50
Nodes (4): get_forex_rates_endpoint(), Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, convert_inr_to_forex(), Convert INR package pricing to major international currencies using Frankfurter…

### Community 17 - "LLMClient"
Cohesion: 0.05
Nodes (33): Any, Keyword agent: enforces 2-4 word primary keyword., run(), Any, Meta description agent: 145-155 chars, natural language, no repetition., run(), Any, Title tag agent: 50-60 chars, optimized for click-through rate with accurate… (+25 more)

### Community 18 - "get"
Cohesion: 0.10
Nodes (20): get, enrich_destination_endpoint(), export_csv_endpoint(), favicon(), get_audit_trail_endpoint(), get_outputs(), get_providers_status(), get_robots_txt() (+12 more)

### Community 19 - "is_safe_url"
Cohesion: 0.08
Nodes (37): api_route, process_batch_background(), Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,…, Semrush Backlink Analytics: Authority Score, Referring Domains, Dofollow Ratio,…, Scrape a Yatradham URL and auto-process through all 5 agents with custom…, scrape_and_process() (+29 more)

### Community 20 - "security_firewall.py"
Cohesion: 0.06
Nodes (33): BaseHTTPMiddleware, Exception, HTTPAuthorizationCredentials, LogRecord, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP… (+25 more)

### Community 21 - "content_creator_agent.py"
Cohesion: 0.22
Nodes (15): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+7 more)

### Community 22 - "crawl_sitemap"
Cohesion: 0.36
Nodes (4): crawl_sitemap(), Crawl an XML Sitemap or Category Landing Page to extract package links with…, Any, SitemapCrawler

### Community 26 - "sanitize_xss"
Cohesion: 0.14
Nodes (12): analyze_keywords_endpoint(), Any, field_validator, Extract top unigrams, bigrams, trigrams & Flesch reading score., URLRequest, Any, field_validator, check_disallowed_xss_patterns() (+4 more)

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `test_e2e_suite.py`, `main.py`, `qa_agent.py`, `is_safe_url`, `content_creator_agent.py`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `test_e2e_suite.py`, `main.py`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
- **Should `test_e2e_suite.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05574229691876751 - nodes in this community are weakly interconnected._