# Graph Report - yatradham-seo-pipeline  (2026-08-24)

## Corpus Check
- 27 files · ~58,281 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 270 nodes · 583 edges · 16 communities (13 shown, 3 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6da1d06d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- main.py
- test_e2e_suite.py
- LLMClient
- models.py
- WordPressPublisher
- SitemapCrawler
- pipeline.py
- qa_agent.py
- .sanitize_meta_description
- content_creator_agent.py
- extract_package_data

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 34 edges
2. `run_suite()` - 19 edges
3. `SEOOutput` - 17 edges
4. `process_package()` - 17 edges
5. `PackageInput` - 14 edges
6. `SectionedContent` - 13 edges
7. `save_output()` - 12 edges
8. `worker_db_stress()` - 12 edges
9. `get_output()` - 11 edges
10. `run()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py
- `_sections_to_dict()` --uses--> `SectionedContent`  [INFERRED]
  database.py → models.py
- `_row_to_output()` --uses--> `PackageInput`  [INFERRED]
  database.py → models.py

## Import Cycles
- None detected.

## Communities (16 total, 3 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "main.py"
Cohesion: 0.06
Nodes (55): BackgroundTasks, clear_all_outputs(), delete, FastAPI, get, batch_urls(), BatchURLRequest, bulk_action() (+47 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.12
Nodes (39): bulk_update_status(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_conn(), get_output(), get_stats(), init_db() (+31 more)

### Community 3 - "LLMClient"
Cohesion: 0.07
Nodes (28): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any, Keyword agent: enforces 2-4 word primary keyword., run() (+20 more)

### Community 4 - "models.py"
Cohesion: 0.23
Nodes (13): batch_process(), Process multiple packages from JSON (manual input)., BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow (+5 more)

### Community 7 - "pipeline.py"
Cohesion: 0.11
Nodes (20): get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…, calculate_flesch_reading_ease(), Any, Real-Time SEO & GEO (Generative Engine Optimization) Linter for YatraDham., Audit content for SEO and AI Overview (GEO) citation compliance., Calculate Flesch Reading Ease score (0-100). (+12 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 14 - "content_creator_agent.py"
Cohesion: 0.22
Nodes (15): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+7 more)

### Community 15 - "extract_package_data"
Cohesion: 0.28
Nodes (8): clean_price_string(), detect_url_category(), extract_package_data(), Any, Extract structured data from Yatradham HTML pages., Extract package metadata, category, and raw text for LLM processing with robust…, Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'., Sanitize and format price strings cleanly. Never return hardcoded mock numbers.

## Knowledge Gaps
- **17 isolated node(s):** `📍 Package Overview`, `⚡ Quick Facts`, `🌟 Why Choose This Package?`, `Day 1`, `Day 2` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `test_e2e_suite.py`, `pipeline.py`, `qa_agent.py`, `content_creator_agent.py`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `process_package()` connect `pipeline.py` to `main.py`, `test_e2e_suite.py`, `LLMClient`, `models.py`, `qa_agent.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `run_seo_linter()` connect `pipeline.py` to `main.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._