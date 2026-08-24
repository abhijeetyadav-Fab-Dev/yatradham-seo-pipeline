# Graph Report - yatradham-seo-pipeline  (2026-08-24)

## Corpus Check
- 34 files · ~67,472 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 327 nodes · 688 edges · 26 communities (24 shown, 2 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `31a4147f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- main.py
- test_e2e_suite.py
- LLMClient
- WordPressPublisher
- crawl_sitemap
- pipeline.py
- anti_ai_guardrails.py
- .sanitize_meta_description
- run_validation
- extract_package_data
- content_creator_agent.py
- models.py
- enrich_destination_data
- post
- BaseModel
- get
- publish_to_wordpress
- scrape_and_process
- validate_row_endpoint
- validate_category

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 34 edges
2. `process_package()` - 22 edges
3. `run_suite()` - 19 edges
4. `SEOOutput` - 17 edges
5. `PackageInput` - 14 edges
6. `SectionedContent` - 13 edges
7. `save_output()` - 12 edges
8. `extract_package_data()` - 12 edges
9. `worker_db_stress()` - 12 edges
10. `run_validation()` - 12 edges

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

## Communities (26 total, 2 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "main.py"
Cohesion: 0.20
Nodes (13): delete, FastAPI, check_ai_endpoint(), CheckAIRequest, delete_single_output(), humanize_endpoint(), humanize_markdown_content(), humanize_single_chunk() (+5 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.12
Nodes (40): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_conn(), get_output(), get_stats() (+32 more)

### Community 3 - "LLMClient"
Cohesion: 0.07
Nodes (28): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any, Keyword agent: enforces 2-4 word primary keyword., run() (+20 more)

### Community 6 - "crawl_sitemap"
Cohesion: 0.31
Nodes (5): crawl_sitemap(), Crawl an XML Sitemap or Category Landing Page to extract package links., SitemapCrawlRequest, Any, SitemapCrawler

### Community 7 - "pipeline.py"
Cohesion: 0.10
Nodes (24): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), get_smart_internal_links() (+16 more)

### Community 11 - "anti_ai_guardrails.py"
Cohesion: 0.29
Nodes (10): calculate_copyleaks_metrics(), check_copyleaks_api(), detect_ai_isms(), generate_copyleaks_recommendations(), Any, Anti-AI Guardrails Engine & Copyleaks AI Detection Optimizer Implements: 1.…, Detect all AI-isms and robotic patterns across the 21 pattern categories., Model the Copyleaks AI Detection algorithm: 1. Perplexity variance… (+2 more)

### Community 13 - "run_validation"
Cohesion: 0.18
Nodes (16): check_duplicate_content(), extract_price_number(), find_duplicated_words(), Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'., Compare one section (e.g. 'why_choose_bullets') of the new row against the same…, Returns a report dict: { "status": "approved_candidate" | "flagged" |…, Returns (is_valid, error_message). Hard fail if destination is missing,… (+8 more)

### Community 14 - "extract_package_data"
Cohesion: 0.09
Nodes (25): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+17 more)

### Community 15 - "content_creator_agent.py"
Cohesion: 0.22
Nodes (15): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+7 more)

### Community 17 - "models.py"
Cohesion: 0.29
Nodes (11): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights, ProgramSession (+3 more)

### Community 18 - "enrich_destination_data"
Cohesion: 0.20
Nodes (14): enrich_destination_data(), fetch_climate_and_weather(), fetch_semantic_lsi_keywords(), fetch_solar_timings(), fetch_spiritual_heritage_facts(), geocode_location(), Any, Public APIs Enrichment & Ground-Truth Verification Layer. Leverages free,… (+6 more)

### Community 19 - "post"
Cohesion: 0.15
Nodes (14): batch_process(), bulk_action(), clear_cache(), process_single(), ProviderSettingsRequest, Process a single package through all 5 agents (manual JSON input)., Process multiple packages from JSON (manual input)., Bulk approve or reject outputs. (+6 more)

### Community 20 - "BaseModel"
Cohesion: 0.17
Nodes (12): BackgroundTasks, batch_urls(), BatchURLRequest, ContentGenerateRequest, generate_content(), process_batch_background(), BaseModel, Scrape and process multiple URLs automatically in the background. (+4 more)

### Community 21 - "get"
Cohesion: 0.25
Nodes (8): get, enrich_destination_endpoint(), get_outputs(), get_single_output(), List all SEO outputs with optional filter and pagination., Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, root(), stats()

### Community 22 - "publish_to_wordpress"
Cohesion: 0.67
Nodes (3): publish_to_wordpress(), Publish generated SEO content directly to WordPress., WpPublishRequest

### Community 23 - "scrape_and_process"
Cohesion: 0.67
Nodes (3): Scrape a Yatradham URL and auto-process through all 5 agents with custom…, scrape_and_process(), URLRequest

### Community 24 - "validate_row_endpoint"
Cohesion: 0.67
Nodes (3): Enterprise code-based validation endpoint., validate_row_endpoint(), ValidateRowRequest

### Community 25 - "validate_category"
Cohesion: 0.67
Nodes (3): Validate if the selected category matches the target URL., validate_category(), ValidateCategoryRequest

## Knowledge Gaps
- **17 isolated node(s):** `📍 Package Overview`, `⚡ Quick Facts`, `🌟 Why Choose This Package?`, `Day 1`, `Day 2` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `test_e2e_suite.py`, `pipeline.py`, `content_creator_agent.py`, `BaseModel`, `scrape_and_process`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `run_validation` to `validate_row_endpoint`, `main.py`, `pipeline.py`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `enrich_destination_data()` connect `enrich_destination_data` to `main.py`, `get`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 8 INFERRED edges - model-reasoned connections that need verification._