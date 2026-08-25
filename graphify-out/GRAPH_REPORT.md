# Graph Report - yatradham-seo-pipeline  (2026-08-24)

## Corpus Check
- 35 files · ~69,106 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 355 nodes · 736 edges · 19 communities (17 shown, 2 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7f18a548`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- main.py
- database.py
- LLMClient
- WordPressPublisher
- SitemapCrawler
- qa_agent.py
- validation_layer.py
- extract_package_data
- TestArchitecturalDecoupling
- enrich_destination_data
- models.py
- run_seo_linter
- generate_json_ld

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 37 edges
2. `process_package()` - 23 edges
3. `run_suite()` - 19 edges
4. `SEOOutput` - 17 edges
5. `PackageInput` - 14 edges
6. `SectionedContent` - 13 edges
7. `save_output()` - 12 edges
8. `extract_package_data()` - 12 edges
9. `worker_db_stress()` - 12 edges
10. `run_validation()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py
- `_row_to_output()` --uses--> `PackageInput`  [INFERRED]
  database.py → models.py
- `localize_content()` --uses--> `LLMClient`  [INFERRED]
  indic_engine.py → llm_client.py
- `localize()` --uses--> `LLMClient`  [INFERRED]
  main.py → llm_client.py

## Import Cycles
- None detected.

## Communities (19 total, 2 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "main.py"
Cohesion: 0.06
Nodes (61): BackgroundTasks, clear_all_outputs(), FastAPI, localize_content(), Any, Translate and culturally localize SEOOutput sections into Hindi or Gujarati., batch_process(), batch_urls() (+53 more)

### Community 2 - "database.py"
Cohesion: 0.09
Nodes (45): bulk_update_status(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output(), get_stats() (+37 more)

### Community 3 - "LLMClient"
Cohesion: 0.05
Nodes (50): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections() (+42 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 13 - "validation_layer.py"
Cohesion: 0.18
Nodes (16): check_duplicate_content(), extract_price_number(), find_duplicated_words(), Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'., Compare one section (e.g. 'why_choose_bullets') of the new row against the same…, Returns a report dict: { "status": "approved_candidate" | "flagged" |…, Returns (is_valid, error_message). Hard fail if destination is missing,… (+8 more)

### Community 14 - "extract_package_data"
Cohesion: 0.10
Nodes (23): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+15 more)

### Community 17 - "TestArchitecturalDecoupling"
Cohesion: 0.14
Nodes (8): Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio…, TestArchitecturalDecoupling

### Community 18 - "enrich_destination_data"
Cohesion: 0.09
Nodes (28): get, enrich_destination_endpoint(), get_audit_trail_endpoint(), get_outputs(), get_providers_status(), get_serp_intelligence_endpoint(), get_single_output(), List all SEO outputs with optional filter and pagination. (+20 more)

### Community 19 - "models.py"
Cohesion: 0.27
Nodes (12): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PackageInput, PricingRow, ProgramHighlights (+4 more)

### Community 22 - "run_seo_linter"
Cohesion: 0.50
Nodes (4): calculate_flesch_reading_ease(), Any, Real-Time Dynamic SEO & GEO Linter for YatraDham. Performs rigorous, non-…, run_seo_linter()

### Community 23 - "generate_json_ld"
Cohesion: 0.40
Nodes (4): generate_json_ld(), Any, Schema.org JSON-LD Structured Data Generator for YatraDham Packages., Generate comprehensive stacked Schema.org JSON-LD for Google Rich Results, SGE…

## Knowledge Gaps
- **17 isolated node(s):** `📍 Package Overview`, `⚡ Quick Facts`, `🌟 Why Choose This Package?`, `Day 1`, `Day 2` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `database.py`, `qa_agent.py`, `TestArchitecturalDecoupling`?**
  _High betweenness centrality (0.192) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `main.py`, `LLMClient`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `process_package()` connect `LLMClient` to `main.py`, `database.py`, `qa_agent.py`, `validation_layer.py`, `extract_package_data`, `models.py`, `run_seo_linter`, `generate_json_ld`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 8 INFERRED edges - model-reasoned connections that need verification._