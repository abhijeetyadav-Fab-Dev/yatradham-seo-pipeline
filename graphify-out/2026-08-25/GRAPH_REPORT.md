# Graph Report - yatradham-seo-pipeline  (2026-08-25)

## Corpus Check
- 39 files · ~74,226 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 463 nodes · 920 edges · 29 communities (27 shown, 2 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 47 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `651bc042`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- main.py
- test_e2e_suite.py
- LLMClient
- WordPressPublisher
- post
- get
- qa_agent.py
- content_creator_agent.py
- validation_layer.py
- extract_package_data
- nlp_and_safety_toolkit.py
- batch_urls
- enrich_destination_data
- is_safe_url
- security_firewall.py
- process_package
- SitemapCrawler
- generate_content
- check_serp_rank
- models.py
- seo_toolkit.py
- get_forex_rates_endpoint
- BaseModel

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
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py
- `localize()` --uses--> `LLMClient`  [INFERRED]
  main.py → llm_client.py

## Import Cycles
- None detected.

## Communities (29 total, 2 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "main.py"
Cohesion: 0.12
Nodes (20): delete, FastAPI, crawl_sitemap(), delete_single_output(), humanize_endpoint(), humanize_markdown_content(), humanize_single_chunk(), HumanizeRequest (+12 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.11
Nodes (45): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output() (+37 more)

### Community 3 - "LLMClient"
Cohesion: 0.07
Nodes (29): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any, Keyword agent: enforces 2-4 word primary keyword., run() (+21 more)

### Community 6 - "post"
Cohesion: 0.12
Nodes (17): analyze_keywords_endpoint(), bulk_action(), clear_cache(), moderate_text_endpoint(), proofread_endpoint(), ProviderSettingsRequest, Any, Bulk approve or reject outputs with admin authorization. (+9 more)

### Community 7 - "get"
Cohesion: 0.12
Nodes (16): get, enrich_destination_endpoint(), get_audit_trail_endpoint(), get_outputs(), get_providers_status(), get_robots_txt(), get_single_output(), get_transit_distance_endpoint() (+8 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 12 - "content_creator_agent.py"
Cohesion: 0.08
Nodes (24): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+16 more)

### Community 13 - "validation_layer.py"
Cohesion: 0.15
Nodes (20): check_duplicate_content(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'., Compare one section (e.g. 'why_choose_bullets') of the new row against the same… (+12 more)

### Community 14 - "extract_package_data"
Cohesion: 0.11
Nodes (22): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+14 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.15
Nodes (16): get_dictionary_endpoint(), link_safety_preview_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview., analyze_keywords_and_readability(), analyze_sentiment_and_moderation(), inspect_url_safety_and_preview(), lookup_word_dictionary() (+8 more)

### Community 17 - "batch_urls"
Cohesion: 0.50
Nodes (4): BackgroundTasks, batch_urls(), BatchURLRequest, Scrape and process multiple URLs automatically in the background (Admin…

### Community 18 - "enrich_destination_data"
Cohesion: 0.16
Nodes (18): get_serp_intelligence_endpoint(), Return live search intent, LSI keyword entities, and competitor heading…, enrich_destination_data(), fetch_climate_and_weather(), fetch_semantic_lsi_keywords(), fetch_solar_timings(), fetch_spiritual_heritage_facts(), fetch_transit_distance_osrm() (+10 more)

### Community 19 - "is_safe_url"
Cohesion: 0.21
Nodes (10): process_batch_background(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, scrape_and_process(), URLRequest, fetch_url_html(), Scrapling-Powered Modern Scraping & DOM Parsing Engine for YatraDham SEO…, Fetch URL with SSRF protection, browser-grade headers and stealth resilience., is_safe_url() (+2 more)

### Community 20 - "security_firewall.py"
Cohesion: 0.07
Nodes (28): BaseHTTPMiddleware, HTTPAuthorizationCredentials, LogRecord, Request, Injects enterprise OWASP security headers on all HTTP responses., root(), SecurityHeadersMiddleware, Config (+20 more)

### Community 21 - "process_package"
Cohesion: 0.09
Nodes (22): Exception, get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…, calculate_flesch_reading_ease(), Any, Real-Time Dynamic SEO & GEO Linter for YatraDham. Performs rigorous, non-…, run_seo_linter() (+14 more)

### Community 23 - "generate_content"
Cohesion: 0.40
Nodes (5): ContentGenerateRequest, generate_content(), Generate net-new SEO content from scratch using AI., Sanitizes user instructions and checks for active prompt injection attacks., sanitize_user_prompt()

### Community 25 - "check_serp_rank"
Cohesion: 0.17
Nodes (13): get_seo_audit_score_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., audit_onpage_seo_score(), check_serp_rank() (+5 more)

### Community 26 - "models.py"
Cohesion: 0.15
Nodes (16): field_validator, BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights (+8 more)

### Community 27 - "seo_toolkit.py"
Cohesion: 0.20
Nodes (9): get_screenshot_preview_endpoint(), get_seo_tags_generator_endpoint(), Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), generate_seo_tags(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 30 - "get_forex_rates_endpoint"
Cohesion: 0.50
Nodes (4): get_forex_rates_endpoint(), Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, convert_inr_to_forex(), Convert INR package pricing to major international currencies using Frankfurter…

### Community 31 - "BaseModel"
Cohesion: 0.17
Nodes (12): check_ai_endpoint(), CheckAIRequest, publish_to_wordpress(), BaseModel, Validate if the selected category matches the target URL., Verify WordPress credentials and REST API availability (Admin Protected)., Publish generated SEO content directly to WordPress (Admin Protected)., validate_category() (+4 more)

## Knowledge Gaps
- **18 isolated node(s):** `Config`, `📍 Package Overview`, `⚡ Quick Facts`, `🌟 Why Choose This Package?`, `Day 1` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `test_e2e_suite.py`, `qa_agent.py`, `content_creator_agent.py`, `is_safe_url`, `process_package`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `main.py`, `LLMClient`, `process_package`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `TestArchitecturalDecoupling` connect `content_creator_agent.py` to `LLMClient`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `📍 Package Overview`, `⚡ Quick Facts` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._