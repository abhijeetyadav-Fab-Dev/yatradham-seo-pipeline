# Graph Report - yatradham-seo-pipeline  (2026-08-22)

## Corpus Check
- 24 files · ~53,807 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 245 nodes · 541 edges · 13 communities (12 shown, 1 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 42 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `be88c4cf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- main.py
- stress_test.py
- LLMClient
- models.py
- extract_package_data
- run_suite
- run_seo_linter
- qa_agent.py
- .sanitize_meta_description

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

## Communities (13 total, 1 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "main.py"
Cohesion: 0.07
Nodes (50): BackgroundTasks, clear_all_outputs(), delete, FastAPI, get, batch_process(), batch_urls(), BatchURLRequest (+42 more)

### Community 2 - "stress_test.py"
Cohesion: 0.14
Nodes (33): bulk_update_status(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_conn(), get_output(), get_stats(), init_db() (+25 more)

### Community 3 - "LLMClient"
Cohesion: 0.07
Nodes (35): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Any, Keyword agent: enforces 2-4 word primary keyword., run() (+27 more)

### Community 4 - "models.py"
Cohesion: 0.29
Nodes (11): BatchRequest, BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights, ProgramSession (+3 more)

### Community 5 - "extract_package_data"
Cohesion: 0.28
Nodes (8): clean_price_string(), detect_url_category(), extract_package_data(), Any, Extract structured data from Yatradham HTML pages., Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'., Sanitize and format price strings to eliminate broken artifacts like 'rs,'., Extract package metadata, category, and raw text for LLM processing with robust…

### Community 6 - "run_suite"
Cohesion: 0.20
Nodes (17): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+9 more)

### Community 7 - "run_seo_linter"
Cohesion: 0.12
Nodes (15): localize_content(), Any, Translate and culturally localize SEOOutput sections into Hindi or Gujarati., calculate_flesch_reading_ease(), Any, Real-Time SEO & GEO (Generative Engine Optimization) Linter for YatraDham., Audit content for SEO and AI Overview (GEO) citation compliance., Calculate Flesch Reading Ease score (0-100). (+7 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

## Knowledge Gaps
- **17 isolated node(s):** `📍 Package Overview`, `⚡ Quick Facts`, `🌟 Why Choose This Package?`, `Day 1`, `Day 2` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `main.py`, `stress_test.py`, `run_suite`, `run_seo_linter`, `qa_agent.py`?**
  _High betweenness centrality (0.195) - this node is a cross-community bridge._
- **Why does `process_package()` connect `LLMClient` to `main.py`, `stress_test.py`, `qa_agent.py`, `run_seo_linter`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `run_seo_linter()` connect `run_seo_linter` to `main.py`, `LLMClient`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `run_suite()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`run_suite()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SEOOutput` (e.g. with `get_output()` and `list_outputs()`) actually correct?**
  _`SEOOutput` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._